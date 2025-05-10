
import asyncio
import torch
import os 

try:
    loop = asyncio.get_running_loop()
except RuntimeError: 
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)


if hasattr(torch, 'classes') and hasattr(torch.classes, '__path__'):
    torch.classes.__path__ = []


import streamlit as st
from src.data_ingestion import load_and_chunk_documents
from src.vector_store import create_faiss_index
from src.agent import Orchestrator

def main():
    """
    Main function to run the Streamlit application.
    Initializes the knowledge assistant and handles user queries.
    """
    st.title("Knowledge Assistant")
    
    # Initialize components once using Streamlit's session state
    if 'agent' not in st.session_state:
        with st.spinner('Initializing system... This may take a moment.'):
            # Step 1: Load and chunk documents
            chunks = load_and_chunk_documents()
            
            # Step 2: Create FAISS vector index from chunks
            vector_store = create_faiss_index(chunks)
            
            # Step 3: Initialize the Orchestrator agent with the vector store
            st.session_state.agent = Orchestrator(vector_store)
            st.success("System initialized successfully!")

    # Get user input
    query = st.text_input("Enter your question:")
    
    if query:
        # Process the query using the initialized agent
        with st.spinner("Processing your query..."):
            try:
               
                answer, tool_used, context_docs = st.session_state.agent.process_query(query)
                
                st.subheader("Execution Path:")
                st.write(f"Tool Used: {tool_used}")
                
                
                if tool_used == "RAG Pipeline" and context_docs:
                    st.subheader("Retrieved Context:")
                    for i, ctx in enumerate(context_docs):
                        st.text_area(f"Context Snippet {i+1}", ctx, height=100, key=f"ctx_{i}")
                
                st.subheader("Answer:")
                st.markdown(answer) # Using markdown for potentially richer text formatting

            except Exception as e:
                st.error(f"An error occurred while processing your query: {e}")
                st.exception(e) # Provides a more detailed traceback in the Streamlit app for debugging

if __name__ == "__main__":
    
    main()
