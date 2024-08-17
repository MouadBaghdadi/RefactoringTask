import ast

class ComparisonDetector(ast.NodeVisitor):
    def __init__(self):
        self.has_comparison_between_diff_vars = False

    def visit_Compare(self, node):
        # Check if the left side of the comparison is a variable
        if isinstance(node.left, ast.Name):
            left_var = node.left.id

            # Check all comparators (right-hand side of the comparison)
            for comparator in node.comparators:
                if isinstance(comparator, ast.Name) and comparator.id != left_var:
                    # If there is a comparison between two different variables
                    self.has_comparison_between_diff_vars = True
                    return  # No need to continue if we already found a match

        self.generic_visit(node)

def has_diff_var_comparison(code):
    tree = ast.parse(code)
    detector = ComparisonDetector()
    detector.visit(tree)
    return detector.has_comparison_between_diff_vars

# code_snippet = """
# if not r != r and r == r:
#     print(h)
# elif not r == w:
#     print(h)
# else:
#     print(h)
# """

# result = has_diff_var_comparison(code_snippet)
# print(result) 
