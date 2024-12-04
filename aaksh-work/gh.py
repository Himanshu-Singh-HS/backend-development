import re

def simplify_query(query: str) -> str:
    
    def is_valid_parentheses(query):
        # Stack-based validation for balanced parentheses
        stack = []
        for char in query:
            if char == '(':
                stack.append(char)
            elif char == ')':
                if stack:
                    stack.pop()
                else:
                    return False
        return len(stack) == 0
    
    query_valid = is_valid_parentheses(query)
    
    if not query_valid:
        print("Given query is invalid. Please enter a valid query.")
        return None

    # Step 1: Remove empty parentheses
    query = re.sub(r'\(\s*\)', '', query)

    # Step 2: Remove redundant nested parentheses: ((f)) -> f
    query = re.sub(r'\(\s*([^\(\)]+?)\s*\)', r'\1', query)

    # Step 3: Simplify logical expressions like ((a OR b)) -> (a OR b)
    query = re.sub(r'\(\s*([^\(\)]+?)\s*\)', r'(\1)', query)

    # Step 4: Remove unnecessary parentheses at the outermost level
    if query.startswith('(') and query.endswith(')'):
        inner_expr = query[1:-1]
        if is_valid_parentheses(inner_expr):
            query = inner_expr
    
    # Step 5: Final cleanup: ensure parentheses are kept only around logical groups where necessary
    # For example, keep parentheses around (a OR b) but not around single variables.
    query = re.sub(r'\(\s*([a-zA-Z0-9\s\+\-\*\/\^\&\|<>=]+)\s*\)', r'(\1)', query)

    return query

# Test the function with your queries
queries = [
    "((((ACOUSTIC OR ULTRASONIC OR SONOGRAPHIC OR SOUND OR ECHO OR ULTRASOUND OR SONAR OR (((SOUND 1D WAVE)))) 1D (((IMAG+ OR MAP+ OR VISUALIZ+)))) AND (ACOUSTIC AND SCANNING)))",
    "((((a AND b))) OR (((c OR d))))",
    "(((((x OR y)))))",
    "(((a OR b) AND ((c AND d)))) OR ((((e))))",
    "((a OR b OR (c 1D d)) AND (((f) OR g) ))",  # important test cases
    "((a OR b OR (c 1D d)) AND ((f)) OR g))",  # important test cases
    " ((a OR b OR (c 1D d)) AND ((f) OR g))",
    "((a OR b OR (c 1D d)) AND()()() ((f) OR g))()())",
    " ((a OR b OR (c 1D d)) AND ((f)OR g)))))"
]

for query in queries:
    simplified_query = simplify_query(query)
    print("Original Query:", query)
    print("Simplified Query:", simplified_query)
    print()
