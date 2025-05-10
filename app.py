import streamlit as st
from src.data_ingestion import load_and_chunk_documents
from src.vector_store import create_faiss_index, retrieve_context
from src.agent import Orchestrator

def main():
    st.title("Knowledge Assistant")
    
    # Initialize components once
    if 'agent' not in st.session_state:
        with st.spinner('Initializing system...'):
            chunks = load_and_chunk_documents()
            vector_store = create_faiss_index(chunks)
            st.session_state.agent = Orchestrator(vector_store)

    query = st.text_input("Enter your question:")
    
    if query:
        result = st.session_state.agent.process_query(query)
        
        st.subheader("Execution Path:")
        st.write(f"Tool Used: {result[1]}")
        
        # if result[1] == "RAG Pipeline":
        #     st.subheader("Retrieved Context:")
        #     for ctx in result[2]:
        #         st.write(f"- {ctx}")
        
        st.subheader("Answer:")
        st.write(result[0])

if __name__ == "__main__":
    main()  # Remove manual event loop handling