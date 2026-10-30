
import json
import re
from functools import lru_cache

from app.config import DATA_DIR


@lru_cache(maxsize=1)
def load_recipes():
    """Load recipes from the project's JSON dataset."""
    recipes_path = DATA_DIR / "recipes.json"

    if not recipes_path.exists():
        raise FileNotFoundError(
            f"Recipe dataset not found: {recipes_path}"
        )

    with open(recipes_path, "r", encoding="utf-8") as file:
        return json.load(file)


def tokenize(text: str) -> set[str]:
    """Convert text into lowercase searchable words."""
    return set(re.findall(r"\b[a-z0-9]+\b", text.lower()))


def search_recipes(
    query: str,
    dietary: str | None = None,
    limit: int = 5
) -> list[dict]:
    """
    Search recipes by name, cuisine, ingredients, and cooking steps.
    Optionally filter by an exact dietary tag.
    """
    recipes = load_recipes()
    query = query.strip().lower()

    if not query:
        return []

    query_words = tokenize(query)
    results = []

    for recipe in recipes:
        tags = [tag.lower() for tag in recipe.get("dietary", [])]

        # Apply an optional dietary filter.
        if dietary and dietary.lower() not in tags:
            continue

        name = recipe.get("name", "").lower()
        cuisine = recipe.get("cuisine", "").lower()

        ingredients = " ".join(
            ingredient.get("item", "")
            for ingredient in recipe.get("ingredients", [])
        ).lower()

        steps = " ".join(recipe.get("steps", [])).lower()

        searchable_text = f"{name} {cuisine} {ingredients} {steps}"
        matched_words = query_words.intersection(
            tokenize(searchable_text)
        )

        score = len(matched_words)

        # Give stronger preference to recipe-name matches.
        if query in name:
            score += 5

        # Give additional preference to cuisine matches.
        if query in cuisine:
            score += 3

        if score > 0:
            results.append({
                "recipe": recipe,
                "score": score
            })

    results.sort(
        key=lambda item: item["score"],
        reverse=True
    )

    return [
        item["recipe"]
        for item in results[:limit]
    ]
