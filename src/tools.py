# tools.py
from langchain.agents import tool
import requests

@tool
def calculate(query: str) -> str:
    """Use for calculations involving math operations. Example: 'Calculate 15*25'."""
    try:
        return str(eval(query))
    except:
        return "Error in calculation"

@tool
def define_term(query: str) -> str:
    """Use to define words or concepts. Example: 'Define quantum computing'."""
    api_url = f"https://api.dictionaryapi.dev/api/v2/entries/en/{query}"
    response = requests.get(api_url)
    return response.json()[0]['meanings'][0]['definitions'][0]['definition']