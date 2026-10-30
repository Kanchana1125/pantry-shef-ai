
from functools import lru_cache

import chromadb
from sentence_transformers import SentenceTransformer

from app.config import DATA_DIR, VECTORSTORE_DIR
from app.services.recipe_search import load_recipes


MODEL_NAME = "all-MiniLM-L6-v2"
COLLECTION_NAME = "pantry_shef_recipes"


@lru_cache(maxsize=1)
def get_embedding_model():
    """Load the embedding model once."""
    return SentenceTransformer(MODEL_NAME)


@lru_cache(maxsize=1)
def get_collection():
    """Create or connect to the persistent ChromaDB collection."""
    VECTORSTORE_DIR.mkdir(parents=True, exist_ok=True)

    client = chromadb.PersistentClient(
        path=str(VECTORSTORE_DIR)
    )

    return client.get_or_create_collection(
        name=COLLECTION_NAME,
        metadata={"hnsw:space": "cosine"}
    )


def create_recipe_document(recipe: dict) -> str:
    """Combine recipe information into searchable text."""
    ingredients = ", ".join(
        item["item"]
        for item in recipe.get("ingredients", [])
    )

    steps = " ".join(recipe.get("steps", []))

    dietary = ", ".join(recipe.get("dietary", []))

    return (
        f"Recipe: {recipe['name']}. "
        f"Cuisine: {recipe.get('cuisine', '')}. "
        f"Ingredients: {ingredients}. "
        f"Dietary tags: {dietary}. "
        f"Cooking instructions: {steps}"
    )


def index_recipes() -> int:
    """Generate embeddings and store all recipes in ChromaDB."""
    recipes = load_recipes()

    if not recipes:
        return 0

    collection = get_collection()
    model = get_embedding_model()

    ids = [recipe["id"] for recipe in recipes]

    documents = [
        create_recipe_document(recipe)
        for recipe in recipes
    ]

    embeddings = model.encode(
        documents,
        normalize_embeddings=True
    ).tolist()

    metadatas = [
        {
            "recipe_id": recipe["id"],
            "name": recipe["name"]
        }
        for recipe in recipes
    ]

    collection.upsert(
        ids=ids,
        documents=documents,
        embeddings=embeddings,
        metadatas=metadatas
    )

    return len(recipes)


def semantic_search(
    query: str,
    limit: int = 5,
    dietary: str | None = None
) -> list[dict]:
    """Find recipes based on the meaning of a user's query."""
    query = query.strip()

    if not query:
        return []

    recipes = load_recipes()
    recipe_lookup = {
        recipe["id"]: recipe
        for recipe in recipes
    }

    collection = get_collection()

    # Index recipes when the collection is empty.
    if collection.count() == 0:
        index_recipes()

    model = get_embedding_model()

    query_embedding = model.encode(
        [query],
        normalize_embeddings=True
    )[0].tolist()

    total = collection.count()

    if total == 0:
        return []

    results = collection.query(
        query_embeddings=[query_embedding],
        n_results=total,
        include=["metadatas", "distances"]
    )

    matches = []

    ids = results["ids"][0]
    distances = results["distances"][0]

    for recipe_id, distance in zip(ids, distances):
        recipe = recipe_lookup.get(recipe_id)

        if recipe is None:
            continue

        tags = [
            tag.lower()
            for tag in recipe.get("dietary", [])
        ]

        if dietary and dietary.lower() not in tags:
            continue

        matches.append({
            "recipe": recipe,
            "distance": round(float(distance), 4)
        })

    return matches[:limit]
