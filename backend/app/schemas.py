
from pydantic import BaseModel, Field
from typing import Optional


# Chat request from the frontend
class ChatRequest(BaseModel):
    message: str
    session_id: str = "default"


# Chat response from the AI
class ChatResponse(BaseModel):
    answer: str
    sources: list[str] = Field(default_factory=list)


# Individual pantry ingredient
class PantryItem(BaseModel):
    name: str
    quantity: Optional[str] = None


# Structured receipt extraction response
class ReceiptExtract(BaseModel):
    store: Optional[str] = None
    items: list[PantryItem] = Field(default_factory=list)


# Individual recipe ingredient
class RecipeIngredient(BaseModel):
    item: str
    quantity: float
    unit: str


# Structured recipe response
class RecipeResponse(BaseModel):
    recipe_name: str
    ingredients: list[RecipeIngredient]
    dietary_tags: list[str] = Field(default_factory=list)
