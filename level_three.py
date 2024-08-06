import ast

class ForStatementRefactorer(ast.NodeTransformer):
    def __init__(self):
        self.assigned_vars = {}
        self.used_vars = set()
        self.for_loop_removed = False
        self.for_loop_var = None
        self.print_var = None
    
    def visit_Assign(self, node):
        # Track variable assignments with their values
        if isinstance(node.targets[0], ast.Name):
            var_name = node.targets[0].id
            if isinstance(node.value, ast.Constant):
                self.assigned_vars[var_name] = node.value.value
            else:
                self.assigned_vars[var_name] = node.value
        
        # Continue processing the assignment
        self.generic_visit(node)
        return node
    
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
        ####################################### for tomorrow ####################################################
        self.print_var =  node.value.args[0].id
        if self.print_var != self.for_loop_var:
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
        if self.for_loop_removed:
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
        return self.remove_unused_assignments(node)

def refactor_code(source_code):

    tree = ast.parse(source_code)
    
    refactorer = ForStatementRefactorer()
    refactorer.visit(tree)
    
    return ast.unparse(tree)

code_snippets = [
"""p = 2
g = 8
v = 0
for g in range(6, 10, 1) :
	print(v)
"""
]

# Refactor each code snippet
for code in code_snippets:
    refactored_code = refactor_code(code)
    print("Original Code:\n", code)
    print("Refactored Code:\n", refactored_code)
    print("-" * 40)
