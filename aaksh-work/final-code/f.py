import re

def simplify_query(query: str) -> str: 
    
    
    def is_valid_parentheses(query):
        stack = []
        for char in query:
            if char == '(':
                stack.append(char)
            elif char == ')':
                if stack and stack[-1] == '(':
                    stack.pop()
                else:
                    return False  
        return len(stack) == 0   
    
    query_valid=is_valid_parentheses(query)
    
    if query_valid:  # want to remove reduntant brackets or or unwanted brackets 
        
        # first we r removing  empty parentheses
        query = re.sub(r'\(\s*\)', '', query)

        while re.search(r'\(\(([^()]+)\)\)', query):
            query = re.sub(r'\(\(([^()]+)\)\)', r'(\1)', query)
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
                    #  if we do not get any paranthesis so easily append it .
                else:
                    result.append(char)
            # we r adding here  closing parentheses
            while stack:
                result.append(')')
                stack.pop()
            return ''.join(result)
        query = balance_parentheses(query)
      
        return query
    else:
        # raise ValueError("given query is invalid plz enter the correct query ")
        print("given query is invalid plz enter the correct query ")

queries = [
    "((((ACOUSTIC OR ULTRASONIC OR SONOGRAPHIC OR SOUND OR ECHO OR ULTRASOUND OR SONAR OR (((SOUND 1D WAVE)))) 1D (((IMAG+ OR MAP+ OR VISUALIZ+)))) AND (ACOUSTIC AND SCANNING)))",
    "((((a AND b))) OR (((c OR d))))",
    "(((((x OR y)))))",
    "(((a OR b) AND ((c AND d)))) OR ((((e))))",
    "((a OR b OR (c 1D d)) AND (((f) OR g) ))",  # important test cases
    "((a OR b OR (c 1D d)) AND ((f)) OR g))",  # importatnt test cases
    " ((a OR b OR (c 1D d)) AND ((f) OR g))",
    "((a OR b OR (c 1D d)) AND()()() ((f) OR g))()())",
    " ((a OR b OR (c 1D d)) AND ((f)OR g)))))"
]
for query in queries:
    simplified_query = simplify_query(query)
    print("Original Query:", query)
    print("Simplified Query:", simplified_query)
    print()

 














# Example usage
query = "((((ACOUSTIC OR ULTRASONIC OR SONOGRAPHIC OR SOUND OR ECHO OR ULTRASOUND OR SONAR OR (((SOUND 1D WAVE)))) 1D (((IMAG+ OR MAP+ OR VISUALIZ+)))) AND (ACOUSTIC AND SCANNING)))"
query = "(((a AND b))) OR (((c OR d)))"
query = "(((((x OR y)))))"
query = "(((a OR b) AND ((c AND d)))) OR ((((e))))"
# query="))))((((ACOUSTIC OR (((SONAR))) OR (((((ULTRASOUND))))) OR SOUND)))))))) AND ((((IMAG+ OR MAP+)))))))))(((((())))))"
# query="((((ACOUSTIC OR (((SONAR))) OR (((((ULTRASOUND))))) OR SOUND))) AND ((((IMAG+ OR MAP+)))))))))(((((())))))"
#
# query="((a OR b OR (c 1D d)) AND (((f) OR g) ))"    #important test cases
# query="((a OR b OR (c 1D d)) AND ((f)) OR g))"   #importatnt test cases
# query=" ((a OR b OR (c 1D d)) AND ((f) OR g))"
# query = "((a OR b OR (c 1D d)) AND()()() ((f) OR g))()())"
# simplified_query = simplify_query(query)
# print("Original Query:", query)
# print("Simplified Query:", simplified_query)



# input-->>>>  ((a OR b OR (c 1D d)) AND ((f) OR g))
# output ->>>>      (a OR b OR (c 1D d)) AND (f OR g)
    #  ((a OR b OR (c 1D d)) AND ((f) OR g))
