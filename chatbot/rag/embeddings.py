"""Embeddings for the chatbot application."""

from langchain_community.embeddings import HuggingFaceEmbeddings

# Load once
embeddings = HuggingFaceEmbeddings(
    model_name="all-MiniLM-L6-v2"
)
