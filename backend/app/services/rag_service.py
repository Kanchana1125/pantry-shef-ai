
from app.services.llm_service import get_chat_model
from app.services.semantic_search import semantic_search


# Initial relevance threshold.
# Lower cosine distance means better semantic similarity.
MAX_DISTANCE = 0.60


def answer_recipe_question(
    question: str,
    dietary: str | None = None
) -> dict:

    question = question.strip()

    if not question:
        return {
            "answer": "Please enter a recipe-related question.",
            "sources": []
        }

    # Step 1: Retrieve semantically similar recipes.
    matches = semantic_search(
        query=question,
        limit=5,
        dietary=dietary
    )

    # Step 2: Keep only sufficiently relevant recipes.
    relevant_matches = [
        match
        for match in matches
        if match["distance"] <= MAX_DISTANCE
    ]

    # Step 3: Refuse if no relevant recipes are found.
    if not relevant_matches:
        return {
            "answer": (
                "I'm sorry, but I couldn't find a sufficiently "
                "relevant recipe in my collection for your question. "
                "Please try asking about another recipe or ingredient."
            ),
            "sources": []
        }

    # Step 4: Prepare context from relevant recipes only.
    recipes = [
        match["recipe"]
        for match in relevant_matches
    ]

    context = ""

    for recipe in recipes:
        context += f"""
Recipe: {recipe['name']}
Cuisine: {recipe.get('cuisine', 'Not specified')}
Dietary tags: {', '.join(recipe.get('dietary', []))}
Servings: {recipe.get('servings', 'Not specified')}
Cooking time: {recipe.get('time_minutes', 'Not specified')} minutes

Ingredients:
"""

        for ingredient in recipe.get("ingredients", []):
            context += (
                f"- {ingredient['quantity']} "
                f"{ingredient['unit']} "
                f"{ingredient['item']}\n"
            )

        context += "\nCooking steps:\n"

        for index, step in enumerate(recipe.get("steps", []), 1):
            context += f"{index}. {step}\n"

    # Step 5: Generate an answer using Groq.
    prompt = f"""
You are Pantry Shef, an AI-powered recipe assistant.

Answer the user's question using ONLY the recipe information
provided below.

Rules:
1. Never invent recipes or ingredients.
2. Never invent quantities or cooking instructions.
3. Use only the supplied recipe context.
4. If the context does not answer the question,
   politely explain that the information is unavailable.
5. Keep the response friendly and easy to understand.
6. Mention the recipe names when relevant.

RECIPE CONTEXT:
{context}

USER QUESTION:
{question}

Answer:
"""

    model = get_chat_model()
    response = model.invoke(prompt)

    return {
        "answer": response.content,
        "sources": [
            recipe["name"]
            for recipe in recipes
        ]
    }
