


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

query = '''
(((ACOUSTIC + OR ULTRASON+ OR SONOGRAPH+ OR SOUND OR ECHO OR ULTRASOUND OR SONAR OR (SOUND 1D WAVE) OR SUPERSON+) 1D
(   ((PHOTO+ OR IMAG+) 2D (CAPTUR+ OR ACQU+)) OR (IMAGING+ OR PHOTOGRAPHY+)  )) OR (ACOUSTIC+ 1D MAPPING+) OR (ACOUSTIC+ 1D SCANNING) OR (ECHOGRAPH+)
OR (SONOGRAPHIC 1D VISUAL+))
'''

query = """

(((ACOUSTIC OR ULTRASONIC OR SONOGRAPHIC OR SOUND OR ECHO OR ULTRASOUND OR SONAR OR (SOUND 1D WAVE)) 1D (IMAG+ OR MAP+ OR VISUALIZ+)) 
OR (ACOUSTIC 1D SCANNING) OR (ECHOGRAPHY) OR (SONOGRAPHIC 1D VISUAL+) OR (SUPERSONIC 1D IMAGING))

"""
query='''
((((ACOUSTIC OR ULTRASONIC OR SONOGRAPHIC OR SOUND OR ECHO OR ULTRASOUND OR SONAR OR (SOUND 1D WAVE)) 1D (IMAG+ OR MAP+ OR VISUALIZ+)) OR (ACOUSTIC 1D SCANNING) OR (ECHOGRAPHY) OR (SONOGRAPHIC 1D VISUAL+) OR (SUPERSONIC 1D IMAGING))/TI/AB/CLMS/DESC/ODES AND ((SORAMA)/PA/OPA/NPAN OR (EINDHOVEN 1D TECH+)/PA/OPA/NPAN OR (FLUKE 1D RECORD+)/PA/OPA/NPAN OR (SMI)/PA/OPA/NPAN OR (NL 1D ACOUSTIC+)/PA/OPA/NPAN OR (DISTRAN)/PA/OPA/NPAN OR (UE 1D SYSTEM+)/PA/OPA/NPAN OR (CAE 1D SYSTEM+)/PA/OPA/NPAN OR (FLIR)/PA/OPA/NPAN OR (OFIL)/PA/OPA/NPAN)) AND (EPRD >= 2004-01-01) AND (STATE/ACT=ALIVE)


'''

extract_text_within_brackets(query)
