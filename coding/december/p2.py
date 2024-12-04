# import re

# def extract_all_bracketed(query):
#     results = []

#     # Recursive function to extract bracketed content, including nested ones
#     def find_brackets(s):
#         # Pattern to match innermost parentheses
#         pattern = r"\(([^()]+(?:\([^()]*\))*)\)"
#         matches = re.findall(pattern, s)

#         # Loop to process each match
#         for match in matches:
#             results.append(f"({match})")
        
#         # If there are still parentheses in the string, continue recursively
#         if matches:
#             s = re.sub(pattern, "", s)  # Remove the processed match
#             find_brackets(s)

#     # Initial recursive call
#     find_brackets(query)
    
#     # Add the entire query (without the suffix) as the last item
#     query_without_suffix = query.split("/TI/AB/ICLM")[0].strip()
#     if query_without_suffix and query_without_suffix != query:
#         results.append(f"({query_without_suffix})")

#     return results


# # Example query
# query = """
# (((ACOUSTIC OR ULTRASONIC OR SONOGRAPHIC OR SOUND OR ECHO OR ULTRASOUND OR SONAR OR (SOUND 1D WAVE)) 1D (IMAG+ OR MAP+ OR VISUALIZ+)) 
# OR (ACOUSTIC 1D SCANNING) OR (ECHOGRAPHY) OR (SONOGRAPHIC 1D VISUAL+) OR (SUPERSONIC 1D IMAGING)/TI/AB/ICLM
# """

# # Extract all bracketed content
# all_brackets = extract_all_bracketed(query)
# i=1
# # Print the extracted results
# for item in all_brackets:
#     print(i,item)
#     i+=1


import re

def extract_all_bracketed(query):
    results = []

    # Pattern to match full parentheses expressions, including nested ones
    pattern = r"\(([^()]+(?:\([^()]*\))*)\)"

    # Remove isolated fragments like '1D' that are not enclosed in parentheses
    query = re.sub(r"\s1D\s", " ", query)

    # Function to extract and process the bracketed expressions
    def find_brackets(s):
        matches = re.findall(pattern, s)

        for match in matches:
            # Avoid appending empty parentheses
            if match.strip():
                results.append(f"({match.strip()})")
        
        # If matches were found, process the remaining part
        if matches:
            s = re.sub(pattern, "", s)  # Remove the processed match
            find_brackets(s)

    # Start the extraction
    find_brackets(query)
    
    # Add the part outside of the brackets (without suffix) if necessary
    query_without_suffix = query.split("/TI/AB/ICLM")[0].strip() 
    if query_without_suffix and query_without_suffix != query:
        results.append(f"({query_without_suffix})")

    return results


# Example query
query = """
(((ACOUSTIC OR ULTRASONIC OR SONOGRAPHIC OR SOUND OR ECHO OR ULTRASOUND OR SONAR OR (SOUND 1D WAVE)) 1D (IMAG+ OR MAP+ OR VISUALIZ+)) 
OR (ACOUSTIC 1D SCANNING) OR (ECHOGRAPHY) OR (SONOGRAPHIC 1D VISUAL+) OR (SUPERSONIC 1D IMAGING)/TI/AB/ICLM
"""

# Extract all bracketed content
all_brackets = extract_all_bracketed(query)

# Print the extracted results
for item in all_brackets:
    print(item)
