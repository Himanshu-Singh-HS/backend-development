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

    def find_brackets(s):
        
        pattern = r"\(([^()]*?)\)"
        matches = re.findall(pattern, s)

        for match in matches:
            results.append(f"({match})")
        
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

query = '''

(((ACOUSTIC + OR ULTRASON+ OR SONOGRAPH+ OR SOUND OR ECHO OR ULTRASOUND OR SONAR OR (SOUND 1D WAVE) OR SUPERSON+) 1D
( ((PHOTO+ OR IMAG+) 2D (CAPTUR+ OR ACQU+)) OR (IMAGING+ OR PHOTOGRAPHY+) )) OR (ACOUSTIC+ 1D MAPPING+) OR (ACOUSTIC+ 1D SCANNING) OR (ECHOGRAPH+)
OR (SONOGRAPHIC 1D VISUAL+))

'''

all_brackets = extract_all_bracketed(query)
for i,item in enumerate(all_brackets,1):
    print(i, item)
#output 2nd query  
''' 

(SOUND 1D WAVE)
(PHOTO+ OR IMAG+)
(CAPTUR+ OR ACQU+)

(IMAGING+ OR PHOTOGRAPHY+)
(ACOUSTIC+ 1D MAPPING+)
(ACOUSTIC+ 1D SCANNING)

(ECHOGRAPH+)
(SONOGRAPHIC 1D VISUAL+)
1 (ACOUSTIC+ OR ULTRASON+ OR SONOGRAPH+ OR SOUND OR ECHO OR ULTRASOUND OR SONAR OR (SOUND 1D WAVE) OR SUPERSON+)  #findout 

2 ((PHOTO+ OR IMAG+) 2D (CAPTUR+ OR ACQU+))  #findout 
3 (((PHOTO+ OR IMAG+) 2D (CAPTUR+ OR ACQU+)) OR (IMAGING+ OR PHOTOGRAPHY+))
4 ((ACOUSTIC + OR ULTRASON+ OR SONOGRAPH+ OR SOUND OR ECHO OR ULTRASOUND OR SONAR OR (SOUND 1D WAVE) OR SUPERSON+) 1D(((PHOTO+ OR IMAG+) 2D (CAPTUR+ OR ACQU+)) OR (IMAGING+ OR PHOTOGRAPHY+)))


5 (((ACOUSTIC+ OR ULTRASON+ OR SONOGRAPH+ OR SOUND OR ECHO OR ULTRASOUND OR SONAR OR (SOUND 1D WAVE) OR SUPERSON+) 1D
(((PHOTO+ OR IMAG+) 2D (CAPTUR+ OR ACQU+))
OR (IMAGING+ OR PHOTOGRAPHY+))) OR (ACOUSTIC+ 1D MAPPING+) OR (ACOUSTIC+ 1D SCANNING) OR (ECHOGRAPH+)
OR (SONOGRAPHIC 1D VISUAL+)) #findout 

'''


#output want like this  for 1st query 
'''   

(SOUND 1D WAVE)
(IMAG+ OR MAP+ OR VISUALIZ+)
(ACOUSTIC 1D SCANNING)

(ECHOGRAPHY)
(SONOGRAPHIC 1D VISUAL+)
(SUPERSONIC 1D IMAGING)

(ACOUSTIC OR ULTRASONIC OR SONOGRAPHIC OR SOUND OR ECHO OR ULTRASOUND OR SONAR OR (SOUND 1D WAVE))
((ACOUSTIC OR ULTRASONIC OR SONOGRAPHIC OR SOUND OR ECHO OR ULTRASOUND OR SONAR OR (SOUND 1D WAVE))  1D (IMAG+ OR MAP+ OR VISUALIZ+)) 
(((ACOUSTIC OR ULTRASONIC OR SONOGRAPHIC OR SOUND OR ECHO OR ULTRASOUND OR SONAR OR (SOUND 1D WAVE))  1D (IMAG+ OR MAP+ OR VISUALIZ+)) OR (ACOUSTIC 1D SCANNING) OR (ECHOGRAPHY) OR (SONOGRAPHIC 1D VISUAL+) OR (SUPERSONIC 1D IMAGING))

'''

# total output = 9


#  query_without_suffix = query.split("/TI/AB/ICLM")[0].strip()  # Remove the /TI/AB/ICLM part
#     if query_without_suffix:
#         results.append(f"({query_without_suffix})")
