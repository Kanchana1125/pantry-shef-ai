
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.api.routes import router

app = FastAPI(
    title="Pantry Shef API",
    description="AI-powered Recipe and Pantry Helper",
    version="1.0.0"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(router)


@app.get("/")
def home():
    return {
        "message": "Welcome to Pantry Shef API!",
        "status": "running"
    }


@app.get("/health")
def health_check():
    return {"status": "healthy"}
