# src/agent.py

from langchain.agents import initialize_agent, AgentType, Tool
from langchain_google_genai import ChatGoogleGenerativeAI
from .tools import calculate, define_term # Assuming these are your custom tools
from .vector_store import retrieve_context
from .llm_integration import generate_answer # Assuming this is your LLM call for RAG

class Orchestrator:
    """
    Orchestrator class to manage different processing paths:
    - Using tools (Calculator, Dictionary)
    - Using a RAG (Retrieval Augmented Generation) pipeline
    """
    def __init__(self, vector_store):
        """
        Initializes the Orchestrator with an LLM, tools, and a retriever.

        Args:
            vector_store: The FAISS vector store instance.
        """
        self.llm = ChatGoogleGenerativeAI(model='gemini-pro', temperature=0)
        
        self.tools = [
            Tool(
                name="Calculator",
                func=calculate.run, # Make sure your tool 'calculate' has a .run method or is directly callable
                description="Use for math calculations. Input should be a mathematical expression."
            ),
            Tool(
                name="Dictionary",
                func=define_term.run, # Make sure your tool 'define_term' has a .run method or is directly callable
                description="Use for word definitions. Input should be the term to define."
            )
        ]
        
        self.retriever = vector_store.as_retriever(search_kwargs={'k': 3}) 
        
        
        self.agent = initialize_agent(
            tools=self.tools,
            llm=self.llm,
            agent=AgentType.STRUCTURED_CHAT_ZERO_SHOT_REACT_DESCRIPTION, # Or another agent type if preferred
            verbose=True, # Set to False in production if too noisy
            handle_parsing_errors=True # Recommended for more robust agent behavior
        )

    def process_query(self, query: str):
        """
        Processes the user query by deciding whether to use a tool or the RAG pipeline.

        Args:
            query (str): The user's query.

        Returns:
            tuple: (answer, tool_name_or_pipeline_type, context_list_or_empty)
        """
        query_lower = query.lower()

        # Simple routing logic (can be improved with more sophisticated decision making)
        if "calculate" in query_lower:
            # It's generally better to let the agent decide to use the tool.
            # However, if you want explicit routing:
            try:
                calculation_expression = query.lower().replace("calculate", "").strip()
                if not calculation_expression: # Handle cases like just "calculate"
                    return "Please provide a mathematical expression to calculate.", "Calculator Tool", []
                result = calculate.run(calculation_expression)
                return result, "Calculator Tool", []
            except Exception as e:
                return f"Error using calculator: {e}", "Calculator Tool", []

        elif "define" in query_lower:
            # Similar to calculate, parse the term if needed.
            try:
                term_to_define = query.lower().replace("define", "").strip()
                if not term_to_define: # Handle cases like just "define"
                    return "Please provide a term to define.", "Dictionary Tool", []
                result = define_term.run(term_to_define)
                return result, "Dictionary Tool", []
            except Exception as e:
                return f"Error using dictionary: {e}", "Dictionary Tool", []
        
        else:
            return self._fallback_to_rag(query)

    def _fallback_to_rag(self, query: str):
        """
        Helper method to perform RAG.
        """
        try:
            # Retrieve context using the updated retrieve_context function
            context = retrieve_context(query, self.retriever)
            
            # Generate an answer based on the query and retrieved context
            answer = generate_answer(query, context)
            return answer, "RAG Pipeline", context
        except Exception as e:
            # Log the error or handle it as needed
            print(f"Error in RAG pipeline: {e}") # Print to console for debugging
            return "I encountered an issue trying to answer your question with my knowledge base.", "RAG Pipeline Error", []

