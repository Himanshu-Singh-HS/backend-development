#input-->>>>  ((a OR b OR (c 1D d)) AND ((f) OR g))
#output ->>>>      (a OR b OR (c 1D d)) AND (f OR g)
              #  (a OR b OR (c 1D d)) AND ((f) OR g)

#input ->>>>>   ((a OR b OR (c 1D d)) AND (((f) OR g) ))   

#output  ->>   (a OR b OR (c 1D d)) AND (f OR g)
#output ->>>    (a OR b OR (c 1D d)) AND (f OR g)


# raw_query = "((((ACOUSTIC OR ULTRASONIC OR SONOGRAPHIC OR SOUND OR ECHO OR ULTRASOUND OR SONAR OR ((SOUND 1D WAVE))) 1D (IMAG+ OR MAP+ OR VISUALIZ+)) AND (ACOUSTIC AND SCANNING)))"

#  ((ACOUSTIC OR ULTRASONIC OR SONOGRAPHIC OR SOUND OR ECHO OR ULTRASONIC OR SONAR OR (SOUND 1D WAVE)) 1D (IMAG+ OR MAP+ OR VISUALIZ+)) AND (ACOUSTIC AND SCANNING)

import re

def simplify_expression(expression: str) -> str:
    # Remove redundant outer parentheses around the entire expression
    while expression.startswith("(") and expression.endswith(")"):
        inner = expression[1:-1]
        # Ensure the inner part has balanced parentheses
        if inner.count("(") == inner.count(")"):
            expression = inner
        else:
            break

    # Simplify redundant single-element parentheses
    expression = re.sub(r"\((\w+)\)", r"\1", expression)

    # Simplify logical structures like ((X) OR Y) or (X AND (Y))
    expression = re.sub(r"\(\((.*?)\)\)", r"(\1)", expression)

    return expression

 
expr = "((a OR b OR (c 1D d)) AND ((f) OR g))"
excr= "((a OR b OR (c 1D d)) AND (((f) OR g)))"
# excr = "((((ACOUSTIC OR ULTRASONIC OR SONOGRAPHIC OR SOUND OR ECHO OR ULTRASOUND OR SONAR OR ((SOUND 1D WAVE))) 1D (IMAG+ OR MAP+ OR VISUALIZ+)) AND (ACOUSTIC AND SCANNING)))"
simplified_expr = simplify_expression(excr)
print("Simplified Expression:", simplified_expr)


def simplify_expression(expression: str) -> str:
    # Remove redundant outer parentheses around the entire expression
    while expression.startswith("(") and expression.endswith(")"):
        inner = expression[1:-1]
        if inner.count("(") == inner.count(")"):  # Check if parentheses are balanced
            expression = inner
        else:
            break

    # Simplify redundant parentheses around single elements
    expression = re.sub(r"\((\w+)\)", r"\1", expression)

    # Simplify nested parentheses like ((X) OR Y)
    expression = re.sub(r"\(\((.*?)\)\)", r"(\1)", expression)

    # Ensure no unmatched parentheses are left
    open_paren_count = expression.count("(")
    close_paren_count = expression.count(")")
    if open_paren_count != close_paren_count:
        raise ValueError("Unbalanced parentheses in the expression.")

    return expression

# Example Usage
expr = "((a OR b OR (c 1D d)) AND ((f) OR g))"
expr= "((a OR b OR (c 1D d)) AND (((f) OR g)))"
simplified_expr = simplify_expression(expr)
print("Simplified Expression:", simplified_expr)


 


#(ACOUSTIC OR ULTRASONIC OR SONOGRAPHIC OR SOUND OR ECHO OR ULTRASOUND OR SONAR OR (SOUND 1D WAVE)) 1D (IMAG+ OR MAP+ OR VISUALIZ+) AND (ACOUSTIC AND SCANNING)
