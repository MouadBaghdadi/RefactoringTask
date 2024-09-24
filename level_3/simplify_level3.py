import ast
import astor

class CodeSimplification(ast.NodeTransformer):
    def __init__(self):
        super().__init__()
        self.assignments = {}
        self.for_loop_variable = None
        self.is_variable_used_in_print = False

    def visit_Assign(self, node):
        if isinstance(node.targets[0], ast.Name):
            if isinstance(node.value, ast.BinOp):
                if not (isinstance(node.value.left, ast.Constant) and isinstance(node.value.right, ast.Constant)):
                    self.assignments[node.targets[0].id] = node.value
            elif isinstance(node.value, ast.Name):
                self.assignments[node.targets[0].id] = node.value
        return None
        
    def visit_For(self, node):
        if isinstance(node.target, ast.Name):
            self.for_loop_variable = node.target.id

        for stmt in node.body:
            self.generic_visit(stmt)

        if not self.is_variable_used_in_print:
            node.target.id = '_'

        return node

    def visit_Print(self, node):

        # Visit all child nodes (which will include Name nodes)
        self.generic_visit(node)

        return node

    def visit_Name(self, node):
        # Check if the loop variable is used in a print statement
        if node.id == self.for_loop_variable:
            self.is_variable_used_in_print = True

        # Replace variables with their initialization values recursively
        if isinstance(node.ctx, ast.Load) and node.id in self.assignments:
            return ast.copy_location(self._replace_with_value(self.assignments[node.id]), node)
        return node

    def _replace_with_value(self, value):
        
        if isinstance(value, ast.Name) and value.id in self.assignments:
            return self._replace_with_value(self.assignments[value.id])
        elif isinstance(value, ast.BinOp):
            value.left = self._replace_with_value(value.left)
            value.right = self._replace_with_value(value.right)
        return value

    
def simplify_code_level3(code):
    # Parse the code into an AST
    tree = ast.parse(code)
    
    # Transform the AST
    transformer = CodeSimplification()
    transformed_tree = transformer.visit(tree)
    
    # Convert the AST back to code
    return astor.to_source(transformed_tree)

# # Example
# code = """
# p = 60
# c = p + 20
# while p >= 59 :
# 	print(c)
# 	p = p - 1
# """

# transformed_code = simplify_code_level3(code)
# print(f'original code: \n{code}')
# print(f'transformed_code: \n{transformed_code}')
