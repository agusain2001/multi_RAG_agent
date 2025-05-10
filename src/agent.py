from langchain.agents import initialize_agent, AgentType, Tool
from langchain_google_genai import ChatGoogleGenerativeAI
from .tools import calculate, define_term
from .vector_store import retrieve_context
from .llm_integration import generate_answer

class Orchestrator:
    def __init__(self, vector_store):
        self.llm = ChatGoogleGenerativeAI(model='gemini-pro', temperature=0)
        self.tools = [
            Tool(
                name="Calculator",
                func=calculate.run,
                description="Use for math calculations"
            ),
            Tool(
                name="Dictionary",
                func=define_term.run,
                description="Use for word definitions"
            )
        ]
        self.retriever = vector_store.as_retriever()  # Use built-in retriever
        
        self.agent = initialize_agent(
            tools=self.tools,
            llm=self.llm,
            agent=AgentType.STRUCTURED_CHAT_ZERO_SHOT_REACT_DESCRIPTION,
            verbose=True
        )

    def process_query(self, query):
        query_lower = query.lower()
        if "calculate" in query_lower:
            return calculate.run(query), "Calculator Tool", []
        elif "define" in query_lower:
            return define_term.run(query.split()[-1]), "Dictionary Tool", []
        else:
            context = retrieve_context(query, self.retriever)
            answer = generate_answer(query, context)
            return answer, "RAG Pipeline", context