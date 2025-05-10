

from langchain_huggingface import HuggingFaceEmbeddings
from langchain_community.vectorstores import FAISS


def create_faiss_index(chunks):
    """
    Create a FAISS vector index from a list of document chunks.
    """
    embeddings = HuggingFaceEmbeddings(model_name="sentence-transformers/all-MiniLM-L6-v2")
    vector_store = FAISS.from_documents(chunks, embeddings)
    vector_store.save_local("faiss_index")
    return vector_store


def retrieve_context(query, retriever, k=3):
    """
    Retrieve top-k relevant documents from the retriever object based on a query.
    """
    results = retriever.get_relevant_documents(query, k=k)
    return [doc.page_content for doc in results]
