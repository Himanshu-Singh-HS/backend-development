

#output

''' 

1 (SOUND 1D WAVE)
2 (IMAG+ OR MAP+ OR VISUALIZ+)
3 (ACOUSTIC 1D SCANNING)
4 (ECHOGRAPHY)
5 (SONOGRAPHIC 1D VISUAL+)
6 (SUPERSONIC 1D IMAGING)
7 (ACOUSTIC OR ULTRASONIC OR SONOGRAPHIC OR SOUND OR ECHO OR ULTRASOUND OR SONAR OR (SOUND 1D WAVE))
8 ((ACOUSTIC OR ULTRASONIC OR SONOGRAPHIC OR SOUND OR ECHO OR ULTRASOUND OR SONAR OR (SOUND 1D WAVE))  1D (IMAG+ OR MAP+ OR VISUALIZ+)) 
9 (((ACOUSTIC OR ULTRASONIC OR SONOGRAPHIC OR SOUND OR ECHO OR ULTRASOUND OR SONAR OR (SOUND 1D WAVE))  1D (IMAG+ OR MAP+ OR VISUALIZ+)) OR (ACOUSTIC 1D SCANNING) OR (ECHOGRAPHY) OR (SONOGRAPHIC 1D VISUAL+) OR (SUPERSONIC 1D IMAGING))


'''


def extract_nested_brackets_with_numbers(query):
    stack = []
    result = []
    start_indices = {}

    for i, char in enumerate(query):
        if char == '(':
            stack.append(char)
            if len(stack) not in start_indices:  # Record the start index for the first time this level appears
                start_indices[len(stack)] = i
        elif char == ')':
            if stack:
                start_index = start_indices[len(stack)]  # Get the corresponding start index
                segment = query[start_index:i + 1]  # Extract the segment for this level
                if len(result) < len(stack):  # Ensure no duplicates for the same level
                    result.append(segment.strip())
                stack.pop()

    result.append(segment.strip())
    for idx, segment in enumerate(result, 1):
        print(f"{idx} {segment}")

query = """
(((ACOUSTIC OR ULTRASONIC OR SONOGRAPHIC OR SOUND OR ECHO OR ULTRASOUND OR SONAR OR (SOUND 1D WAVE)) 1D (IMAG+ OR MAP+ OR VISUALIZ+)) 
OR (ACOUSTIC 1D SCANNING) OR (ECHOGRAPHY) OR (SONOGRAPHIC 1D VISUAL+) OR (SUPERSONIC 1D IMAGING))
"""
extract_nested_brackets_with_numbers(query)






# import re

# def extract_all_bracketed(query):
#     results = []
    
#     # Recursive function to extract brackets
#     def find_brackets(s):
#         pattern = r"\(([^()]+(?:\([^()]*\))*)\)"  # Matches inner brackets first
#         matches = re.findall(pattern, s)
#         for match in matches:
#             if match.strip() not in results:  # Avoid duplicates
#                 results.append(f"({match.strip()})")
#             # Recursively search within this match
#             find_brackets(match)
    
#     find_brackets(query)
#     results.append(query.strip()) 
#     return results

# query = """
# (((ACOUSTIC OR ULTRASONIC OR SONOGRAPHIC OR SOUND OR ECHO OR ULTRASOUND OR SONAR OR (SOUND 1D WAVE)) 1D (IMAG+ OR MAP+ OR VISUALIZ+)) 
# OR (ACOUSTIC 1D SCANNING) OR (ECHOGRAPHY) OR (SONOGRAPHIC 1D VISUAL+) OR (SUPERSONIC 1D IMAGING))
# """

# all_brackets = extract_all_bracketed(query)

# # Print results in the desired format
# for i, item in enumerate(all_brackets, 1):
#     print(i, item)