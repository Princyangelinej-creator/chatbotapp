"""Loader for the chatbot application."""

import PyPDF2

def extract_text(uploaded_file) -> str:
    """Extract text from uploaded file."""
    if uploaded_file.name.endswith(".pdf"):
        reader = PyPDF2.PdfReader(uploaded_file)
        return "\n".join(page.extract_text() or "" for page in reader.pages)

    return uploaded_file.read().decode("utf-8", errors="ignore")
    