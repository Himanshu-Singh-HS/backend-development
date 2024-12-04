# import re
# def extract_bracketed_terms(query):
#     i=1
#     pattern = r"\((.*?)\)"

#     matches = re.findall(pattern, query)


#     for match in matches:
#         print(f"{i}({match})")
#         i+=1

# query = """
# (((ACOUSTIC OR ULTRASONIC OR SONOGRAPHIC OR SOUND OR ECHO OR ULTRASOUND OR SONAR OR (SOUND 1D WAVE)) 1D (IMAG+ OR MAP+ OR VISUALIZ+))
# OR (ACOUSTIC 1D SCANNING) OR (ECHOGRAPHY) OR (SONOGRAPHIC 1D VISUAL+) OR (SUPERSONIC 1D IMAGING))/TI/AB/ICLM

# """
# extract_bracketed_terms(query)


import re
def extract_all_bracketed(query):
    results = []
    # query = re.sub(r"\s1D\s", " ", query)
    # Recursive function to extract bracketed content

    def find_brackets(s):
        

        pattern = r"\(([^()]*?)\)"
        matches = re.findall(pattern, s)

        for match in matches:
            results.append(f"({match})")
         
        # If matches are found, replace them with placeholders and continue
        while matches:
            s = re.sub(pattern, "", s, count=1)  # Remove the processed match
            matches = re.findall(pattern, s)  # Search for remaining brackets

    # Initial call to recursive function
    find_brackets(query)

 
    pattern = r"\(([^()]+(?:\([^()]*\))*)\)"
    matches = re.findall(pattern, query)
    results.append(f"({matches[0]})")
    results.append(query.strip())
    
    return results


query = """

(((ACOUSTIC OR ULTRASONIC OR SONOGRAPHIC OR SOUND OR ECHO OR ULTRASOUND OR SONAR OR (SOUND 1D WAVE)) 1D (IMAG+ OR MAP+ OR VISUALIZ+)) 
OR (ACOUSTIC 1D SCANNING) OR (ECHOGRAPHY) OR (SONOGRAPHIC 1D VISUAL+) OR (SUPERSONIC 1D IMAGING))

"""

all_brackets = extract_all_bracketed(query)

for i,item in enumerate(all_brackets,1):
    print(i, item)

'''   

(SOUND 1D WAVE)
(IMAG+ OR MAP+ OR VISUALIZ+)
(ACOUSTIC 1D SCANNING)

(ECHOGRAPHY)
(SONOGRAPHIC 1D VISUAL+)
(SUPERSONIC 1D IMAGING)

(ACOUSTIC OR ULTRASONIC OR SONOGRAPHIC OR SOUND OR ECHO OR ULTRASOUND OR SONAR OR (SOUND 1D WAVE))
((ACOUSTIC OR ULTRASONIC OR SONOGRAPHIC OR SOUND OR ECHO OR ULTRASOUND OR SONAR OR (SOUND 1D WAVE))  1D (IMAG+ OR MAP+ OR VISUALIZ+)) 
(((ACOUSTIC OR ULTRASONIC OR SONOGRAPHIC OR SOUND OR ECHO OR ULTRASOUND OR SONAR OR (SOUND 1D WAVE))  1D (IMAG+ OR MAP+ OR VISUALIZ+)) OR (ACOUSTIC 1D SCANNING) OR (ECHOGRAPHY) OR (SONOGRAPHIC 1D VISUAL+) OR (SUPERSONIC 1D IMAGING))/TI/AB/ICLM

'''

# total output = 9


#  query_without_suffix = query.split("/TI/AB/ICLM")[0].strip()  # Remove the /TI/AB/ICLM part
#     if query_without_suffix:
#         results.append(f"({query_without_suffix})")
