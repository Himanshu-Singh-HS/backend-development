# # # import re

# # # def simplify_expression(expression: str) -> str:
# # #     # Remove redundant outer parentheses around the entire expression
# # #     def remove_outer_parentheses(expr: str) -> str:
# # #         while expr.startswith("(") and expr.endswith(")"):
# # #             inner = expr[1:-1]
# # #             # Check if inner content has balanced parentheses
# # #             if inner.count("(") == inner.count(")"):
# # #                 expr = inner
# # #             else:
# # #                 break
# # #         return expr

# # #     # Ensure all parentheses are balanced
# # #     def validate_parentheses(expr: str):
# # #         stack = []
# # #         for char in expr:
# # #             if char == "(":
# # #                 stack.append(char)
# # #             elif char == ")":
# # #                 if not stack:
# # #                     raise ValueError("Unbalanced parentheses in the expression.")
# # #                 stack.pop()
# # #         if stack:
# # #             raise ValueError("Unbalanced parentheses in the expression.")

# # #     # Simplify redundant parentheses inside the expression
# # #     def simplify_redundant(expr: str) -> str:
# # #         # Simplify (single item) -> single item
# # #         expr = re.sub(r"\((\w+)\)", r"\1", expr)
# # #         # Simplify ((...)) -> (...)
# # #         expr = re.sub(r"\(\((.*?)\)\)", r"(\1)", expr)
# # #         return expr

# # #     # Step 1: Validate parentheses before processing
# # #     validate_parentheses(expression)

# # #     # Step 2: Remove redundant outer parentheses
# # #     expression = remove_outer_parentheses(expression)

# # #     # Step 3: Simplify redundant parentheses
# # #     expression = simplify_redundant(expression)

# # #     # Step 4: Final parentheses validation
# # #     validate_parentheses(expression)

# # #     return expression

# # # # Example Usage
# # # expr = "((a OR b OR (c 1D d)) AND ((f) OR g))"
# # # try:
# # #     simplified_expr = simplify_expression(expr)
# # #     print("Simplified Expression:", simplified_expr)
# # # except ValueError as e:
# # #     print("Error:", e)



# # import re

# # def simplify_expression(expression: str) -> str:
# #     # Remove redundant outer parentheses around the entire expression
# #     def remove_outer_parentheses(expr: str) -> str:
# #         while expr.startswith("(") and expr.endswith(")"):
# #             inner = expr[1:-1]
# #             # Check if inner content has balanced parentheses
# #             if inner.count("(") == inner.count(")"):
# #                 expr = inner
# #             else:
# #                 break
# #         return expr

# #     # Ensure all parentheses are balanced
# #     def validate_parentheses(expr: str):
# #         stack = []
# #         for index, char in enumerate(expr):
# #             if char == "(":
# #                 stack.append(index)
# #             elif char == ")":
# #                 if not stack:
# #                     raise ValueError(f"Unbalanced parentheses: Extra ')' at position {index}")
# #                 stack.pop()
# #         if stack:
# #             raise ValueError(f"Unbalanced parentheses: Extra '(' at positions {stack}")

# #     # Simplify redundant parentheses inside the expression
# #     def simplify_redundant(expr: str) -> str:
# #         # Simplify (single item) -> single item
# #         expr = re.sub(r"\((\w+)\)", r"\1", expr)
# #         # Simplify ((...)) -> (...)
# #         expr = re.sub(r"\(\((.*?)\)\)", r"(\1)", expr)
# #         return expr

# #     # Step 1: Validate parentheses before processing
# #     try:
# #         validate_parentheses(expression)
# #     except ValueError as e:
# #         print("Validation Error:", e)
# #         raise

# #     # Step 2: Remove redundant outer parentheses
# #     expression = remove_outer_parentheses(expression)

# #     # Step 3: Simplify redundant parentheses
# #     expression = simplify_redundant(expression)

# #     # Step 4: Final parentheses validation
# #     try:
# #         validate_parentheses(expression)
# #     except ValueError as e:
# #         print("Validation Error after simplification:", e)
# #         raise

# #     return expression

# # # Example Usage
# # expr = "((a OR b OR (c 1D d)) AND ((f) OR g))"  # Adjust if necessary to trigger errors
# # try:
# #     simplified_expr = simplify_expression(expr)
# #     print("Simplified Expression:", simplified_expr)
# # except ValueError as e:
# #     print("Error:", e)


# import re

# def simplify_expression(expression: str) -> str:
#     # Remove redundant outer parentheses around the entire expression
#     def remove_outer_parentheses(expr: str) -> str:
#         while expr.startswith("(") and expr.endswith(")"):
#             inner = expr[1:-1]
#             if inner.count("(") == inner.count(")"):  # Balanced check
#                 expr = inner
#             else:
#                 break
#         return expr

#     # Ensure all parentheses are balanced
#     def validate_parentheses(expr: str):
#         stack = []
#         for index, char in enumerate(expr):
#             if char == "(":
#                 stack.append(index)
#             elif char == ")":
#                 if not stack:
#                     raise ValueError(f"Unbalanced parentheses: Extra ')' at position {index}")
#                 stack.pop()
#         if stack:
#             raise ValueError(f"Unbalanced parentheses: Extra '(' at positions {stack}")

#     # Simplify redundant parentheses inside the expression
#     def simplify_redundant(expr: str) -> str:
#         print(f"Before redundant simplification: {expr}")
#         expr = re.sub(r"\((\w+)\)", r"\1", expr)  # Simplify (single item)
#         expr = re.sub(r"\(\((.*?)\)\)", r"(\1)", expr)  # Simplify nested parentheses
#         print(f"After redundant simplification: {expr}")
#         return expr

#     print(f"Original Expression: {expression}")

#     # Step 1: Validate parentheses before processing
#     try:
#         validate_parentheses(expression)
#     except ValueError as e:
#         print("Validation Error:", e)
#         raise

#     # Step 2: Remove redundant outer parentheses
#     expression = remove_outer_parentheses(expression)
#     print(f"After removing outer parentheses: {expression}")

#     # Step 3: Simplify redundant parentheses
#     expression = simplify_redundant(expression)

#     # Step 4: Final parentheses validation
#     try:
#         validate_parentheses(expression)
#     except ValueError as e:
#         print("Validation Error after simplification:", e)
#         raise

#     return expression

# # Example Usage
# expr = "((a OR b OR (c 1D d)) AND ((f) OR g))"  # Adjust input if necessary
# try:
#     simplified_expr = simplify_expression(expr)
#     print("Simplified Expression:", simplified_expr)
# except ValueError as e:
#     print("Error:", e)


import re

def simplify_expression(expression: str) -> str:
    # Remove redundant outer parentheses around the entire expression
    def remove_outer_parentheses(expr: str) -> str:
        while expr.startswith("(") and expr.endswith(")"):
            inner = expr[1:-1]
            # Check if the inner expression is balanced
            if inner.count("(") == inner.count(")"):
                expr = inner  # Remove the outer parentheses if balanced
            else:
                break
        return expr

    # Ensure all parentheses are balanced
    def validate_parentheses(expr: str):
        stack = []
        for index, char in enumerate(expr):
            if char == "(":
                stack.append(index)
            elif char == ")":
                if not stack:
                    raise ValueError(f"Unbalanced parentheses: Extra ')' at position {index}")
                stack.pop()
        if stack:
            raise ValueError(f"Unbalanced parentheses: Extra '(' at positions {stack}")

    # Simplify redundant parentheses inside the expression
    def simplify_redundant(expr: str) -> str:
        print(f"Before redundant simplification: {expr}")
        # Simplify redundant parentheses
        expr = re.sub(r"\(\s*(\w+)\s*\)", r"\1", expr)  # Simplify (single item) with optional spaces
        expr = re.sub(r"\(\((.*?)\)\)", r"(\1)", expr)  # Simplify nested parentheses
        print(f"After redundant simplification: {expr}")
        return expr

    print(f"Original Expression: {expression}")

    # Step 1: Validate parentheses before processing
    try:
        validate_parentheses(expression)
    except ValueError as e:
        print("Validation Error:", e)
        raise

    # Step 2: Remove redundant outer parentheses
    expression = remove_outer_parentheses(expression)
    print(f"After removing outer parentheses: {expression}")

    # Step 3: Simplify redundant parentheses
    expression = simplify_redundant(expression)

    # Step 4: Final parentheses validation
    try:
        validate_parentheses(expression)
    except ValueError as e:
        print("Validation Error after simplification:", e)
        raise

    return expression

# Example Usage
expr = "((a OR b OR (c 1D d)) AND ((f) OR g))"  # Adjust input if necessary
try:
    simplified_expr = simplify_expression(expr)
    print("Simplified Expression:", simplified_expr)
except ValueError as e:
    print("Error:", e)
