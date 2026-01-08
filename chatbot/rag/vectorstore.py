from langchain_community.vectorstores import FAISS
from .embeddings import embeddings

# Structure:
# vector_stores[conversation_id][doc_id] = FAISS store
vector_stores = {}

def add_texts(conversation_id: str, doc_id: str, texts: list[str]):
    if conversation_id not in vector_stores:
        vector_stores[conversation_id] = {}

    if doc_id in vector_stores[conversation_id]:
        vector_stores[conversation_id][doc_id].add_texts(texts)
    else:
        vector_stores[conversation_id][doc_id] = FAISS.from_texts(texts, embeddings)

def similarity_search(conversation_id: str, doc_id: str, query: str, k=4):
    store = vector_stores.get(conversation_id, {}).get(doc_id)
    if not store:
        return []
    return store.similarity_search(query, k=k)

def has_documents(conversation_id: str):
    return conversation_id in vector_stores and bool(vector_stores[conversation_id])

def list_documents(conversation_id: str):
    return list(vector_stores.get(conversation_id, {}).keys())
