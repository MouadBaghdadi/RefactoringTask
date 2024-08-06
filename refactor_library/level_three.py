import ast
from refactor_library.refactor_base import Refactor

class LevelThree(ast.NodeTransformer, Refactor):
    """THis class is responsible for simplifying code at level 3.1 and 3.2"""
    def __init__(self):
        self.assigned_vars = {}
        self.used_vars = set()
        self.for_loop_removed = False
        self.for_loop_var = None
        self.print_var = None
        self.map = {}
        self.zero_init_vars = set()
        self.division_by_zero_found = False
    
    def visit_Assign(self, node):
        # Track variable assignments with their values
        if isinstance(node.targets[0], ast.Name):
            var_name = node.targets[0].id
            if isinstance(node.value, ast.Constant):
                self.assigned_vars[var_name] = node.value.value
                if node.value.value == 0:
                    self.zero_init_vars.add(var_name)
            else:
                self.assigned_vars[var_name] = node.value
            
            if isinstance(node.value, ast.BinOp):  
                self.map = self.is_variable_used(node.value, var_name)

        # Continue processing the assignment
        self.generic_visit(node)
        self.check_division_by_zero(node.value)
        return node
    
    def check_division_by_zero(self, node):
        """Check if there is a division by zero or by a variable initialized to zero"""
        if isinstance(node, ast.BinOp) and isinstance(node.op, ast.Div):
            if isinstance(node.right, ast.Constant) and node.right.value == 0:
                self.division_by_zero_found = True
            elif isinstance(node.right, ast.Name) and node.right.id in self.zero_init_vars:
                self.division_by_zero_found = True
        
        for child in ast.iter_child_nodes(node):
            self.check_division_by_zero(child)


    def is_variable_used(self, node, var_name):
        """
        Check if a variable is used within a given AST node
        """
        if isinstance(node, ast.Name) and node.id == var_name:
            if var_name not in self.map:
                    self.map[var_name] = []
            self.map[var_name].append(var_name)
            return self.map
        for child in ast.iter_child_nodes(node):
            if isinstance(child, ast.BinOp):  
                self.map = self.is_variable_used(child, var_name)
            if isinstance(child,ast.Name):
                if var_name not in self.map:
                    self.map[var_name] = []
                self.map[var_name].append(child.id)
        return self.map
    
    def visit_Name(self, node):
        # Track used variables
        if isinstance(node.ctx, ast.Load):
            self.used_vars.add(node.id)
        return node
    
    def visit_For(self, node):
        self.for_loop_var = node.target.id
        
        # Track variables used in the for loop
        if isinstance(node.target, ast.Name):
            self.used_vars.add(node.target.id)
        
        # Track variables used in the loop body
        for stmt in node.body:
            self.generic_visit(stmt)
        
        # check the range values
        if (isinstance(node.iter, ast.Call) and 
            isinstance(node.iter.func, ast.Name) and 
            node.iter.func.id == 'range'):
            range_args = node.iter.args
            if (isinstance(range_args[0], ast.Constant) and 
                isinstance(range_args[1], ast.Constant)):
                start_value = range_args[0].value
                end_value = range_args[1].value
                if start_value >= end_value:
                    self.for_loop_removed = True
                    return None  # ignore the for loop completely
        self.generic_visit(node)
        return node

    def visit_Expr(self, node):

        self.print_var =  node.value.args[0].id

        if self.print_var != self.for_loop_var and self.for_loop_var not in self.map[self.print_var] and self.print_var not in self.map[self.print_var]:
            if isinstance(node.value, ast.Call) and isinstance(node.value.func, ast.Name) and node.value.func.id ==     'print':
                new_args = []
                for arg in node.value.args:
                    if isinstance(arg, ast.Name):
                        var_name = arg.id
                
                        if var_name in self.assigned_vars and self.assigned_vars[var_name] is not None:
                            new_args.append(self.assigned_vars[var_name])
                            self.used_vars.remove(var_name)
                        else:
                            new_args.append(arg)
                    else:
                        new_args.append(arg)
                if isinstance(new_args[0], int):
                    new_args = [ast.Constant(value=new_args[0], kind=None)]
                node.value.args = new_args
        return node

    def remove_unused_assignments(self, node):
        #check for each assigned variable if it is used
        if self.for_loop_removed or self.print_var == self.for_loop_var:
            node.body = [stmt for stmt in node.body if not isinstance(stmt, ast.Assign)]
        else:
            # check for each assigned variable if it is used
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
        #handle the module (top-level) body
        self.generic_visit(node)
        if self.division_by_zero_found:
            node.body = []
        return self.remove_unused_assignments(node)

    def refactor(self,source_code):
    
        tree = ast.parse(source_code)
        
        refactorer = LevelThree()
        refactorer.visit(tree)
        
        return f"{ast.unparse(tree)}\n"

code_snippets = [
"""c = 0
d = 7
b = (b * 3)/(b * b)/(b + 8)-(b * 5)/(b)-(3)
for b in range(4, 8) :
	print(b)
"""
]

# Refactor each code snippet
# for code in code_snippets:
#     refactored_code = refactor(code)
#     print("Original Code:\n", code)
#     print("Refactored Code:\n", refactored_code)
#     print("-" * 40)
