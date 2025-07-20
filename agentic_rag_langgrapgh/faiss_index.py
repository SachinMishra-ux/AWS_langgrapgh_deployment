
from langchain_community.vectorstores import FAISS
from agentic_rag_langgrapgh.embedding import get_azure_embedding_model

# === Load FAISS index ===
def load_faiss_index(index_path, embedding_model):
    return FAISS.load_local(index_path, embedding_model, allow_dangerous_deserialization=True)


# === Load retriever from FAISS index ===
def get_retriever():
    embedding_model = get_azure_embedding_model()
    db = FAISS.load_local(
        "faiss_index_zoology_book",
        embedding_model,
        allow_dangerous_deserialization=True
    )
    return db.as_retriever(search_kwargs={"k": 7})