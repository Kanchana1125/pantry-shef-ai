from app.schemas import ChatRequest, ChatResponse
from app.services.rag_service import answer_recipe_question
from fastapi import APIRouter, Query, HTTPException
from app.services.semantic_search import semantic_search

from app.services.recipe_search import search_recipes

router = APIRouter()


@router.get("/recipes/search")
def recipe_search(
    q: str = Query(..., min_length=1, description="Search for a recipe"),
    dietary: str | None = Query(
        default=None,
        description="Optional dietary filter, e.g. vegetarian or vegan"
    ),
    limit: int = Query(default=5, ge=1, le=15)
):
    try:
        results = search_recipes(
            query=q,
            dietary=dietary,
            limit=limit
        )

        return {
            "query": q,
            "count": len(results),
            "results": results
        }

    except FileNotFoundError as error:
        raise HTTPException(status_code=500, detail=str(error))

@router.get("/recipes/semantic-search")
def recipe_semantic_search(
    q: str = Query(
        ...,
        min_length=1,
        description="Describe the food you are looking for"
    ),
    dietary: str | None = Query(default=None),
    limit: int = Query(default=5, ge=1, le=15)
):
    try:
        results = semantic_search(
            query=q,
            limit=limit,
            dietary=dietary
        )

        return {
            "query": q,
            "count": len(results),
            "results": results
        }

    except FileNotFoundError as error:
        raise HTTPException(status_code=500, detail=str(error))
      
      

@router.post("/recipes/ask", response_model=ChatResponse)
def ask_recipe_question(request: ChatRequest):
    try:
        result = answer_recipe_question(
            question=request.message
        )

        return result

    except Exception as error:
        raise HTTPException(
            status_code=500,
            detail=f"Could not process your question: {str(error)}"
        )


