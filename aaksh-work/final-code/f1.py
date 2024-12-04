# import re


# def simplify_query(query: str) -> str:
#     """
#     Simplifies a logical query by removing only truly redundant brackets.
#     """
#     # Remove all empty parentheses "()"    
#     query = re.sub(r'\(\s*\)', '', query)
    
#     # Iteratively reduce multiple nested parentheses, but only if they do not alter logical grouping
#     while re.search(r'\(\(([^()]*?)\)\)', query):  # Matches nested brackets containing no operators
#         query = re.sub(r'\(\(([^()]*?)\)\)', r'(\1)', query)
    
#     # Balance parentheses
#     def balance_parentheses(query):
#         stack = []
#         result = []
#         for char in query:
#             if char == '(':
#                 stack.append(char)
#                 result.append(char)
#             elif char == ')':
#                 if stack:
#                     stack.pop()
#                     result.append(char)
#             else:
#                 result.append(char)
#         # Add missing closing parentheses
#         while stack:
#             result.append(')')
#             stack.pop()
#         return ''.join(result)
    
#     query = balance_parentheses(query)
    
#     return query

# def check_redundant(query: str) -> str:
#     """
#     Analyzes whether a query contains redundant brackets.
    
#     Args:
#         query (str): The input logical query.
        
#     Returns:
#         str: A message indicating whether the query has redundant brackets.
#     """
#     simplified_query = simplify_query(query)
#     if simplified_query == query:
#         return "The query is correct and does not contain redundant brackets."
#     else:
#         return "The query contains redundant brackets."

# # Example usage 
# query = "((a OR b OR (c 1D d)) AND ((f) OR g))" 
# # query="((a OR b OR (c 1D d)) AND ((f))OR g))"
# query="(((((x OR y)))))"
# query= "((a OR b OR (c 1D d)) AND ((f) OR g))" 
# query="((a OR b OR (c 1D d)) AND (((f) OR g) ))"  
# print("Original Query:", query)
# print("Simplified Query:", simplify_query(query))
# print(check_redundant(query))


import re

def simplify_query(query: str) -> str:
    # Step 1: Remove empty parentheses
    query = re.sub(r'\(\s*\)', '', query)

    # Step 2: Remove redundant nested parentheses like ((...)) to (...)
    while re.search(r'\(\(([^()]+)\)\)', query):
        query = re.sub(r'\(\(([^()]+)\)\)', r'(\1)', query)

    # Step 3: Balance parentheses properly
    def balance_parentheses(query):
        stack = []
        result = []
        for char in query:
            if char == '(':
                stack.append(char)
                result.append(char)
            elif char == ')':
                if stack:
                    stack.pop()
                    result.append(char)
            else:
                result.append(char)

        # Add any closing parentheses that were missed
        while stack:
            result.append(')')
            stack.pop()
        return ''.join(result)

    # Step 4: Call balance_parentheses to ensure the parentheses are properly balanced
    query = balance_parentheses(query)
    return query


# Example usage
queries = [
    "(((((x OR y)))))",
    "(((a OR b) AND ((c AND d)))) OR ((((e))))",
    "(((a AND b))) OR (((c OR d)))",
    "((a OR b OR (c 1D d)) AND ((f) OR g))" ,
    "((a OR b OR (c 1D d)) AND (((f) OR g)))"  ,
    "((((ACOUSTIC OR ULTRASONIC OR SONOGRAPHIC OR SOUND OR ECHO OR ULTRASOUND OR SONAR OR (((SOUND 1D WAVE)))) 1D (((IMAG+ OR MAP+ OR VISUALIZ+)))) AND (ACOUSTIC AND SCANNING)))"
]

for query in queries:
    simplified_query = simplify_query(query)
    print("Original Query:", query)
    print("Simplified Query:", simplified_query)
    print()

