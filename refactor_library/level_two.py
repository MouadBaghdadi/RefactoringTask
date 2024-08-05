import ast
from refactor_library.refactor_base import Refactor
class LevelTwo(ast.NodeTransformer,Refactor):
    
    def __init__(self):
        self.assigned_vars = {}
        self.used_vars = set()
    
    def visit_Assign(self, node):
        # Track variable assignments
        if isinstance(node.targets[0], ast.Name):
            var_name = node.targets[0].id
            self.assigned_vars[var_name] = node
        
        # Continue processing the assignment
        self.generic_visit(node)
        return node
    
    def visit_Name(self, node):
        # Track used variables
        if isinstance(node.ctx, ast.Load):
            self.used_vars.add(node.id)
        return node

    def visit_Print(self, node):
        # Ensure all variables in print statements are marked as used
        for value in node.values:
            if isinstance(value, ast.Name):
                self.used_vars.add(value.id)
        return self.generic_visit(node)

    def visit_If(self, node):
        # Track variables used in the if condition
        self.generic_visit(node.test)
        
        # Check if the if condition is a 'not' condition
        if isinstance(node.test, ast.UnaryOp) and isinstance(node.test.op, ast.Not):
            inner_test = node.test.operand
            if isinstance(inner_test, ast.Compare):
                left = inner_test.left
                right = inner_test.comparators[0]
                op = inner_test.ops[0]

                if isinstance(left, ast.Name) and isinstance(right, ast.Name) and left.id == right.id:
                    # Handle 'not' conditions that are always false
                    if isinstance(op, (ast.Eq, ast.LtE, ast.GtE)):
                        if node.orelse:
                            return self.process_orelse(node.orelse)
                        else:
                            return None  # Ignore the if statement completely
                    
                    # Handle 'not' conditions that are always true
                    elif isinstance(op, (ast.NotEq, ast.Gt, ast.Lt)):
                        return node.body  # Remove the if and return its body directly

        # Check if the condition is between the same variable
        if isinstance(node.test, ast.Compare):
            left = node.test.left
            right = node.test.comparators[0]
            op = node.test.ops[0]

            if isinstance(left, ast.Name) and isinstance(right, ast.Name) and left.id == right.id:
                # Handle conditions that are always true
                if isinstance(op, (ast.Eq, ast.LtE, ast.GtE)):
                    return node.body  # Remove the if and return its body directly

                # Handle conditions that are always false
                elif isinstance(op, (ast.NotEq, ast.Gt, ast.Lt)):
                    if node.orelse:
                        return self.process_orelse(node.orelse)
                    else:
                        return None  # Ignore the if statement completely

        # Visit child nodes (if any)
        self.generic_visit(node)
        return node

    def process_orelse(self, orelse):
        """
        Process the elif/else branches as we did with the original if statement.
        """
        new_body = []
        for stmt in orelse:
            if isinstance(stmt, ast.If):
                # Apply the same refactoring to the elif condition
                refactored_stmt = self.visit_If(stmt)
                if refactored_stmt:
                    if isinstance(refactored_stmt, list):
                        new_body.extend(refactored_stmt)
                    else:
                        new_body.append(refactored_stmt)
            else:
                new_body.append(stmt)
        return new_body
    
    def remove_unused_assignments(self, node):
        # Check for each assigned variable if it is used
        new_body = []
        for stmt in node.body:
            if isinstance(stmt, ast.Assign):
                var_name = stmt.targets[0].id
                if var_name in self.used_vars:
                    new_body.append(stmt)
            else:
                new_body.append(stmt)
        
        node.body = new_body
        return node
    
    def visit_Module(self, node):
        # Handle the module (top-level) body
        self.generic_visit(node)
        return self.remove_unused_assignments(node)

    def refactor(self,source_code):
        # Parse the source code into an AST
        tree = ast.parse(source_code)

        # Refactor the AST
        refactorer = LevelTwo()
        refactorer.visit(tree)

        # Unparse the AST back into source code
        return f"{ast.unparse(tree)}\n"

# Examples of code snippets to refactor
code_snippets = [
    """g = 3
v = 8
if not v < v :
	print(v)
elif g != 3 :
	print(v)
else :
	print(v)
"""
]

# Refactor each code snippet
#for code in code_snippets:
#    refactored_code =LevelTwo().refactor(code)
#    print("Original Code:\n", code)
#    print("Refactored Code:\n", refactored_code)
#    print("-" * 40)
