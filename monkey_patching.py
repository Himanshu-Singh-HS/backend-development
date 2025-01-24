class student:
    def __init__(self,name):
        self.name=name
    def printname(self):
        print(f"hello {self.name}!")
s=student("singh")
s.printname()


def new_function_name(g):
    print("yes  this is monkey patching ",g.name)
student.printname=new_function_name

s.printname()  


def is_valid_parentheses(expression):
    stack = []
    for char in expression:
        if char == '(':
            stack.append(char)
        elif char == ')':
            if stack and stack[-1] == '(':
                stack.pop()
            else:
                return False  
    return len(stack) == 0   

expression = "-((a OR b OR (c 1D d)) AND ((f)OR g)))))"
if is_valid_parentheses(expression):
    print("The parentheses are valid.")
else:
    print("The parentheses are invalid.")

def is_valid_parentheses(expression):
    stack = []
    for char in expression:
        if char == '(':
            stack.append(char)
        elif char == ')':
            if stack and stack[-1] == '(':
                stack.pop()
            else:
                return False  # Unmatched closing parenthesis
    return len(stack) == 0  # True if stack is empty, False otherwise

# Test queries
queries = [
    "(a AND b) OR (c AND d)",              # Valid
    "((a OR b) AND (c OR d))",             # Valid
    "-((a OR b) AND ((c AND d) OR e))",    # Valid
    "(a AND (b OR (c AND d)))",            # Valid
    "((a AND b) OR c) AND (d OR e)",       # Valid
    "(a AND b) OR c)",                     # Invalid
    "((a OR b) AND (c OR d))(",            # Invalid
    "(a AND (b OR c)",                     # Invalid
    "((a AND b) OR (c AND d)))))",         # Invalid
    "((a AND b) OR ((c AND d)",            # Invalid
]

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
for i, query in enumerate(queries, 1):
    result = is_valid_parentheses(query)
    print(f"Query {i}: {'Valid' if result else 'Invalid'}")

