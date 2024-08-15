import ast
import astor
import random
import string

class VariableRenamer(ast.NodeTransformer):
    def __init__(self):
        super().__init__()
        self.variable_map = {}

    def generate_new_name(self, length=1):
        # Generate a random variable name
        return ''.join(random.choices(string.ascii_lowercase, k=length))

    def visit_Name(self, node):
        # Skip changing the name if it's part of the 'print' function
        if isinstance(node.ctx, ast.Load) or isinstance(node.ctx, ast.Store):
            if node.id not in self.variable_map:
                # Generate a new name for the variable if it doesn't already have one
                self.variable_map[node.id] = self.generate_new_name()
            # Replace the variable name with the new name
            node.id = self.variable_map[node.id]
        return node

    def visit_Call(self, node):
        # Ensure that the 'print' function name stays intact
        if isinstance(node.func, ast.Name) and node.func.id == 'print':
            # Visit the arguments to rename variables inside them
            new_args = []
            for arg in node.args:
                new_args.append(self.visit(arg))
            node.args = new_args
            return node
        return self.generic_visit(node)

def generate_clone_code(source_code):
    tree = ast.parse(source_code)
    renamer = VariableRenamer()
    transformed_tree = renamer.visit(tree)
    return astor.to_source(transformed_tree)

# Example usage
code = """
q = 6
d = 6
w = 3
i = 8
e = (5 * q) + (3 * 6) / (3 + q)
print(e)
"""

clone_code = generate_clone_code(code)
print("Original Code:\n", code)
print("Clone Code:\n", clone_code)
