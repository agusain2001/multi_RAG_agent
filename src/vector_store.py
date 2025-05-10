# src/vector_store.py

from langchain_huggingface import HuggingFaceEmbeddings
from langchain_community.vectorstores import FAISS


def create_faiss_index(chunks):
    """
    Create a FAISS vector index from a list of document chunks.
    The index is saved locally to "faiss_index".
    """
    # Initialize HuggingFace embeddings model
    embeddings = HuggingFaceEmbeddings(model_name="sentence-transformers/all-MiniLM-L6-v2")
    
    # Create FAISS vector store from document chunks and embeddings
    vector_store = FAISS.from_documents(chunks, embeddings)
    
    # Save the vector store locally
    vector_store.save_local("faiss_index")
    return vector_store


def retrieve_context(query: str, retriever):
    """
    Retrieve relevant document contexts from the retriever object based on a query.
    Uses the new .invoke() method as per LangChain deprecation guidelines.
    The number of documents to retrieve (k) should be configured on the retriever itself.

    Args:
        query (str): The user's query string.
        retriever: The LangChain retriever object (e.g., from FAISS.as_retriever()).

    Returns:
        list[str]: A list of page content from the relevant documents.
    """
    # Use the .invoke() method on the retriever
    # The 'k' (number of documents) should be configured when the retriever is created,
    # e.g., vector_store.as_retriever(search_kwargs={'k': 3})
    results = retriever.invoke(query)
    
    # Extract the page content from the retrieved documents
    return [doc.page_content for doc in results]

