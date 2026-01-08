"""Embeddings for the chatbot application."""

from langchain_huggingface import HuggingFaceEmbeddings

# Load once
embeddings = HuggingFaceEmbeddings(
    model_name="all-MiniLM-L6-v2"
)
