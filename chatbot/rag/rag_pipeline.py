"""RAG pipeline for the chatbot application."""

from langchain_text_splitters import RecursiveCharacterTextSplitter

from .vectorstore import add_texts, similarity_search


splitter = RecursiveCharacterTextSplitter(
    chunk_size=500,
    chunk_overlap=100
)

def process_document(conversation_id: str, text: str) -> None:
    """Process and store a document for a given conversation."""
    chunks = splitter.split_text(text)
    add_texts(conversation_id, chunks)


def get_relevant_context(conversation_id: str, query: str) -> str | None:
    """Retrieve relevant context for a query from stored documents."""
    docs = similarity_search(conversation_id, query)
    if not docs:
        return None
    return "\n".join(doc.page_content for doc in docs)
