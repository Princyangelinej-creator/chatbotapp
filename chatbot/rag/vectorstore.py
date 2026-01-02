"""vector store for the chatbot application."""

from langchain_community.vectorstores import FAISS
from .embeddings import embeddings

# One vector store per conversation
vector_stores = {}

def add_texts(conversation_id: str, texts: list[str]):
    """Add texts to the vector store for a given conversation."""
    if conversation_id in vector_stores:
        vector_stores[conversation_id].add_texts(texts)
    else:
        vector_stores[conversation_id] = FAISS.from_texts(texts, embeddings)

def similarity_search(conversation_id: str, query: str, k=4):
    """Search for similar documents in the vector store."""
    store = vector_stores.get(conversation_id)
    if not store:
        return []
    return store.similarity_search(query, k=k)

def has_documents(conversation_id: str) -> bool:
    """check if there are documents for a given conversation."""
    return conversation_id in vector_stores
