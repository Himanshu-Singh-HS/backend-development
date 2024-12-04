def extract_text_within_brackets(query):
    stack = []
    result = []
    start_indices = {}
    for i, char in enumerate(query):
        if char == '(':
            stack.append(char)
            start_indices[len(stack)] = i
        elif char == ')':
            if stack:
                stack.pop()
                start_index = start_indices[len(stack) + 1]  # Correct the start index for the current level
                segment = query[start_index:i + 1].strip()  # Extract the segment inside the parentheses
                
                if segment:  
                    result.append(segment)

    for idx, segment in enumerate(result,1):
        print(idx,segment)
        
raw_query = "((((ACOUSTIC OR ULTRASONIC OR SONOGRAPHIC OR SOUND OR ECHO OR ULTRASOUND OR SONAR OR ((SOUND 1D WAVE))  ))) 1D (IMAG+ OR MAP+ OR VISUALIZ+)) AND (ACOUSTIC AND SCANNING)))"
raw_query=" ((((ACOUSTIC OR ULTRASONIC OR SONOGRAPHIC OR SOUND OR ECHO OR ULTRASOUND OR SONAR OR ((SOUND 1D WAVE))) 1D (IMAG+ OR MAP+ OR VISUALIZ+)) AND (ACOUSTIC AND SCANNING)))"
raw_query=" (((ACOUSTIC OR ULTRASONIC OR SONOGRAPHIC OR SOUND OR ECHO OR ULTRASOUND OR SONAR OR (SOUND 1D WAVE))))) 1D (IMAG+ OR MAP+ OR VISUALIZ+)) OR (ACOUSTIC 1D SCANNING) OR (ECHOGRAPHY) OR (SONOGRAPHIC 1D VISUAL+) OR (SUPERSONIC 1D IMAGING))"

extract_text_within_brackets(raw_query)

#input-->>>>  ((a OR b OR (c 1D d)) AND ((f) OR g))
#output ->>>>      (a OR b OR (c 1D d)) AND (f OR g)


#input ->>>>>   ((a OR b OR (c 1D d)) AND (((f) OR g) ))

#output  ->>   (a OR b OR (c 1D d)) AND (f OR g)
#output ->>>    ((a OR b OR (c 1D d)) AND (f OR g))


# raw_query = "((((ACOUSTIC OR ULTRASONIC OR SONOGRAPHIC OR SOUND OR ECHO OR ULTRASOUND OR SONAR OR ((SOUND 1D WAVE))) 1D (IMAG+ OR MAP+ OR VISUALIZ+)) AND (ACOUSTIC AND SCANNING)))"
#  ((ACOUSTIC OR ULTRASONIC OR SONOGRAPHIC OR SOUND OR ECHO OR ULTRASONIC OR SONAR OR (SOUND 1D WAVE)) 1D (IMAG+ OR MAP+ OR VISUALIZ+)) AND (ACOUSTIC AND SCANNING)



import re
def simplify_query(query: str) -> str:
     # first we r removing  empty parentheses 
    query = re.sub(r'\(\s*\)', '', query)
    while re.search(r'\(\((.*?)\)\)', query):
        query = re.sub(r'\(\((.*?)\)\)', r'(\1)', query)
        
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

# Example usage
query= "((a OR b OR (c 1D d)) AND ((f) OR g))"   #importatnt test cases 
# query = "((((ACOUSTIC OR ULTRASONIC OR SONOGRAPHIC OR SOUND OR ECHO OR ULTRASOUND OR SONAR OR (((SOUND 1D WAVE)))) 1D (((IMAG+ OR MAP+ OR VISUALIZ+)))) AND (ACOUSTIC AND SCANNING)))"
# query="(((a AND b))) OR (((c OR d)))"
# query="(((((x OR y)))))"
query="(((a OR b) AND ((c AND d)))) OR ((((e))))"
# query="))))((((ACOUSTIC OR (((SONAR))) OR (((((ULTRASOUND))))) OR SOUND)))))))) AND ((((IMAG+ OR MAP+)))))))))(((((())))))"
# query = "((a OR b OR (c 1D d)) AND()()() ((f) OR g))()())"
# query="((((ACOUSTIC OR (((SONAR))) OR (((((ULTRASOUND))))) OR SOUND))) AND ((((IMAG+ OR MAP+)))))))))(((((())))))"

# query="((a OR b OR (c 1D d)) AND (((f) OR g) ))"    important test cases

simplified_query = simplify_query(query)
print("Original Query:", query)
print("Simplified Query:", simplified_query)

















#corrected code 

# import re

# def simplify_query(query: str) -> str:
    
    
#      # Remove empty parentheses 
#     query = re.sub(r'\(\s*\)', '', query)
    
    
#     while re.search(r'\(\((.*?)\)\)', query):
#         query = re.sub(r'\(\((.*?)\)\)', r'(\1)', query)
        
#       # Remove excessive unmatched closing parentheses
#     open_count = query.count('(')
#     close_count = query.count(')')
#     if close_count > open_count:
#         query = query[:-(close_count - open_count)]
    
#      # Step 3: Balance parentheses by trimming excess
#     # open_count = query.count('(')
#     # close_count = query.count(')')
#     # if close_count > open_count:
#     #     query = query[:-(close_count - open_count)]
#     # elif open_count > close_count:
#     #     query += ')' * (open_count - close_count)
        
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
#                 #  if we do not get any paranthesis so easily append it .
#             else:
#                 result.append(char)
#         # we r adding here  closing parentheses
#         while stack:
#             result.append(')')
#             stack.pop()
#         return ''.join(result)
#     query = balance_parentheses(query)
#     return query

# # Example usage
# # query= "((a OR b OR (c 1D d)) AND (((f) OR g)))"
# # query = "((((ACOUSTIC OR ULTRASONIC OR SONOGRAPHIC OR SOUND OR ECHO OR ULTRASOUND OR SONAR OR (((SOUND 1D WAVE)))) 1D (((IMAG+ OR MAP+ OR VISUALIZ+)))) AND (ACOUSTIC AND SCANNING)))"
# # query="(((a AND b))) OR (((c OR d)))"
# # query="(((((x OR y)))))"
# # query="(((a OR b) AND ((c AND d)))) OR ((((e))))"
# # query="))))((((ACOUSTIC OR (((SONAR))) OR (((((ULTRASOUND))))) OR SOUND)))))))) AND ((((IMAG+ OR MAP+)))))))))(((((())))))"
# query = "((a OR b OR (c 1D d)) AND()()() ((f) OR g))()())"
# # query="((((ACOUSTIC OR (((SONAR))) OR (((((ULTRASOUND))))) OR SOUND))) AND ((((IMAG+ OR MAP+)))))))))(((((())))))"
# simplified_query = simplify_query(query)
# print("Original Query:", query)
# print("Simplified Query:", simplified_query)
