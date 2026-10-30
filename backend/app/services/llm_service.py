
from langchain_groq import ChatGroq

from app.config import GROQ_API_KEY, GROQ_CHAT_MODEL


def get_chat_model():
    """Create the Groq chat model."""
    return ChatGroq(
        model=GROQ_CHAT_MODEL,
        api_key=GROQ_API_KEY,
        temperature=0
    )
