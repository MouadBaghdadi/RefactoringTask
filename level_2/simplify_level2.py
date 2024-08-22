import ast
import astor

class CodeSimplification(ast.NodeTransformer):
    def __init__(self):
        super().__init__()
        self.assignments = {}
        self.for_loop_variable = None

    def visit_Assign(self, node):
        # Only store assignments involving variables or a binary operation with at least one variable
        if isinstance(node.targets[0], ast.Name):
            if isinstance(node.value, ast.BinOp):
                # Check if the binary operation has at least one variable
                if not (isinstance(node.value.left, ast.Constant) and isinstance(node.value.right, ast.Constant)):
                    self.assignments[node.targets[0].id] = node.value
            elif isinstance(node.value, ast.Name):
                self.assignments[node.targets[0].id] = node.value
        # Remove the assignment statement
        return None

    def visit_Name(self, node):
        # Replace variables with their initialization values recursively
        if isinstance(node.ctx, ast.Load) and node.id in self.assignments:
            return ast.copy_location(self._replace_with_value(self.assignments[node.id]), node)
        return node

    def _replace_with_value(self, value):
        # Recursively replace any names in the expression with their assigned values
        if isinstance(value, ast.Name) and value.id in self.assignments:
            return self._replace_with_value(self.assignments[value.id])
        # Apply the transformation recursively to any other complex expressions
        elif isinstance(value, ast.BinOp):
            value.left = self._replace_with_value(value.left)
            value.right = self._replace_with_value(value.right)
        return value
    
def simplify_code_level2(code):
    # Parse the code into an AST
    tree = ast.parse(code)
    
    # Transform the AST
    transformer = CodeSimplification()
    transformed_tree = transformer.visit(tree)
    
    # Convert the AST back to code
    return astor.to_source(transformed_tree)

# Example
# code = """q = 8
# if  q > 2 :
# 	print(q)
# elif  q < q :
# 	print(q)
# else :
# 	print(q)
# """

# transformed_code = simplify_code_level3(code)
# print(f'original code: \n{code}')
# print(f'transformed_code: \n{transformed_code}')