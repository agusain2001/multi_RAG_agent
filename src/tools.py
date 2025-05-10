# src/tools.py
from langchain.agents import tool
import requests # For define_term
import re
import ast
import operator

# --- Helper function for safer evaluation of math expressions ---
_ALLOWED_OPS = {
    ast.Add: operator.add,
    ast.Sub: operator.sub,
    ast.Mult: operator.mul,
    ast.Div: operator.truediv,
    # ast.Pow: operator.pow, # You can enable power if needed
    ast.USub: operator.neg,
}

def safe_eval_math_expr(expr: str):
    """
    Safely evaluates a string containing a basic mathematical expression.
    Supports addition, subtraction, multiplication, division, and negation.
    """
    try:
        # Remove any potentially harmful characters not part of a valid basic math expression.
        # This is a simple sanitization; more robust parsing might be needed for complex scenarios.
        sanitized_expr = "".join(c for c in expr if c in "0123456789.+-*/() ")
        if not sanitized_expr:
            raise ValueError("Expression is empty after sanitization.")
            
        node = ast.parse(sanitized_expr, mode='eval')
    except (SyntaxError, ValueError) as e:
        # print(f"Syntax error or invalid character in expression '{expr}': {e}") # For debugging
        raise ValueError(f"Invalid mathematical expression syntax: {expr}")

    def _eval(node):
        if isinstance(node, ast.Constant): # Handles numbers (Python 3.8+)
            return node.value
        elif isinstance(node, ast.Num): # Handles numbers (Python < 3.8)
            return node.n
        elif isinstance(node, ast.BinOp):
            if type(node.op) not in _ALLOWED_OPS:
                raise ValueError(f"Unsupported binary operator: {type(node.op).__name__}")
            left_val = _eval(node.left)
            right_val = _eval(node.right)
            return _ALLOWED_OPS[type(node.op)](left_val, right_val)
        elif isinstance(node, ast.UnaryOp):
            if type(node.op) not in _ALLOWED_OPS:
                raise ValueError(f"Unsupported unary operator: {type(node.op).__name__}")
            operand_val = _eval(node.operand)
            return _ALLOWED_OPS[type(node.op)](operand_val)
        else:
            raise TypeError(f"Unsupported node type in expression: {type(node).__name__}")
    
    return _eval(node.body)
# --- End of helper function ---

@tool
def calculate(expression: str) -> str:
    """
    Use for calculations involving math operations.
    Handles basic arithmetic (e.g., '15*25', '100/4') and percentage expressions like 'X% of Y' (e.g., '15% of 80').
    The input 'expression' should be the part of the query that contains the actual calculation,
    e.g., if user says 'calculate 20% of 100', the input here should be '20% of 100'.
    """
    # The expression received here is after "calculate" is stripped by the agent.py
    # e.g., "15% of 80" or "10 + 5"
    processed_expression = expression.strip().lower()

    try:
        # Regex to match "X% of Y"
        # Using re.fullmatch to ensure the entire string matches this pattern.
        percentage_match = re.fullmatch(r"(\d+\.?\d*)\s*%\s*of\s*(\d+\.?\d*)", processed_expression)
        
        if percentage_match:
            percentage_val = float(percentage_match.group(1))
            of_number = float(percentage_match.group(2))
            
            result = (percentage_val / 100.0) * of_number
            return str(result)
        else:
            # If it's not a percentage calculation, try to evaluate as a standard math expression
            # The 'expression' variable still holds the original case version from the agent if needed,
            # but safe_eval_math_expr should handle the already stripped 'processed_expression' or original 'expression'.
            # Let's pass the original `expression` to `safe_eval_math_expr` as it might rely on exact input.
            result = safe_eval_math_expr(expression)
            return str(result)

    except Exception as e:
        # print(f"Error in calculation tool for expression '{expression}': {e}") # Uncomment for server-side debugging
        return "Error in calculation"

@tool
def define_term(query: str) -> str:
    """Use to define words or concepts. Example: 'Define quantum computing'.
       Input should be the term to define.
    """
    api_url = f"https://api.dictionaryapi.dev/api/v2/entries/en/{query.strip()}"
    try:
        response = requests.get(api_url)
        response.raise_for_status() # Raise an exception for HTTP errors
        definition_data = response.json()
        if definition_data and isinstance(definition_data, list):
            # Take the first definition found
            first_entry = definition_data[0]
            if 'meanings' in first_entry and first_entry['meanings']:
                first_meaning = first_entry['meanings'][0]
                if 'definitions' in first_meaning and first_meaning['definitions']:
                    return first_meaning['definitions'][0]['definition']
        return f"Could not find a definition for '{query}'."
    except requests.exceptions.HTTPError as http_err:
        if response.status_code == 404:
            return f"Could not find a definition for '{query}' (404 Error)."
        else:
            # print(f"HTTP error occurred while defining '{query}': {http_err}") # Server-side debug
            return f"Error fetching definition for '{query}' (HTTP {response.status_code})."
    except Exception as e:
        # print(f"An error occurred while defining '{query}': {e}") # Server-side debug
        return f"An error occurred while trying to define '{query}'."

