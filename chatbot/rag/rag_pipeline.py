"""RAG pipeline for the chatbot application."""

from langchain_text_splitters import RecursiveCharacterTextSplitter

from .vectorstore import add_texts, similarity_search


splitter = RecursiveCharacterTextSplitter(
    chunk_size=800,
    chunk_overlap=120
)

def process_document(conversation_id: str,doc_id: str, text: str):
    """Process and store a document for a given conversation."""
    chunks = splitter.split_text(text)
    add_texts(conversation_id,doc_id,chunks)


def get_relevant_context(conversation_id: str,doc_id:str, query: str):
    """Retrieve relevant context for a query from stored documents."""
    docs = similarity_search(conversation_id,doc_id, query)
    if not docs:
        return None
    return "\n".join(doc.page_content for doc in docs)
    