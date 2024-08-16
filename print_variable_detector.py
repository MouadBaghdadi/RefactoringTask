import ast

class PrintVariablesDetector(ast.NodeVisitor):
    def __init__(self):
        self.printed_vars = set()

    def visit_Call(self, node):
        # Check if the function being called is 'print'
        if isinstance(node.func, ast.Name) and node.func.id == 'print':
            for arg in node.args:
                self._extract_variables(arg)
        self.generic_visit(node)

    def _extract_variables(self, node):
        # Recursively extract variable names from the expression
        if isinstance(node, ast.Name):
            self.printed_vars.add(node.id)
        elif isinstance(node, ast.BinOp):
            self._extract_variables(node.left)
            self._extract_variables(node.right)
        elif isinstance(node, ast.UnaryOp):
            self._extract_variables(node.operand)
        elif isinstance(node, ast.Call):
            for arg in node.args:
                self._extract_variables(arg)
        elif isinstance(node, ast.Attribute):
            self.printed_vars.add(node.attr)
        elif isinstance(node, ast.Subscript):
            self._extract_variables(node.value)

def get_printed_variables(code):

    detector = PrintVariablesDetector()
    tree = ast.parse(code)

    detector.visit(tree)

    return detector.printed_vars

# snippet = """print((t + 0) / (8 / 5))"""

# detector = PrintVariablesDetector()

# printed_vars = get_printed_variables(snippet)
# print(f"In snippet '{snippet}': printed variables are {printed_vars}")

