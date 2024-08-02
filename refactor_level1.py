import ast
import astor

class RemoveUnusedVariablesAndSimplifyPrint(ast.NodeTransformer):
    def __init__(self):
        self.used_vars = set()
        self.assigned_vars = {}
    
    def visit_Name(self, node):
        if isinstance(node.ctx, ast.Load):
            self.used_vars.add(node.id)
            # print(self.used_vars)
        elif isinstance(node.ctx, ast.Store):
            self.assigned_vars[node.id] = None
            # print(self.assigned_vars)
        return node
    
    def visit_Assign(self, node):
        self.generic_visit(node.value)
        for target in node.targets:
            if isinstance(target, ast.Name):
                self.visit_Name(target)
                self.assigned_vars[target.id] = node.value
        return node
    
    # def visit_Expr(self, node):
    #     if isinstance(node.value, ast.Call) and isinstance(node.value.func, ast.Name) and node.value.func.id == 'print':
    #         for i, arg in enumerate(node.value.args):
    #             if isinstance(arg, ast.Name):
    #                 var_name = arg.id
    #                 # replacing the variable within the print statement with its value
    #                 if var_name in self.assigned_vars and self.assigned_vars[var_name] is not None:
    #                     node.value.args[i] = self.assigned_vars[var_name]
    #     return node
    def visit_Expr(self, node):
        if isinstance(node.value, ast.Call) and isinstance(node.value.func, ast.Name) and node.value.func.id == 'print':
            new_args = []
            for arg in node.value.args:
                if isinstance(arg, ast.Name):
                    var_name = arg.id
                    if var_name in self.assigned_vars and self.assigned_vars[var_name] is not None:
                        new_args.append(self.assigned_vars[var_name])
                    else:
                        new_args.append(arg)
                else:
                    new_args.append(arg)
            node.value.args = new_args

        return node
    
    # def visit_Module(self, node):
    #     # visit all nodes to gather information about used and assigned variables
    #     self.generic_visit(node)
        
    #     # filter out assignments where the assigned variable is not used
    #     new_body = []
    #     for n in node.body:
    #         if isinstance(n, ast.Assign):
    #             c = [t.id for t in n.targets if isinstance(t, ast.Name)]
    #             target_names = [t.id for t in n.targets if isinstance(t, ast.Name)]
    #             if any(tn in self.used_vars for tn in target_names):
    #                 new_body.append(n)
    #         else:
    #             new_body.append(n)
    #     node.body = new_body
    #     return node

    def visit_Module(self, node):
        self.generic_visit(node)
        
        new_body = []
        for n in node.body:
            if isinstance(n, ast.Assign):
                target_names = [t.id for t in n.targets if isinstance(t, ast.Name)]
                if any(tn in self.used_vars for tn in target_names):
                    new_body.append(n)
            elif isinstance(n, ast.Expr) and isinstance(n.value, ast.Call) and n.value.func.id == 'print':
                # replace variable names with their values in print statements
                new_args = []
                for i, arg in enumerate(n.value.args):
                    if isinstance(arg, ast.BinOp):
                        left = arg.left.id
                        op = arg.op
                        right = arg.right.id
                        print(op)
                        if left in self.assigned_vars and isinstance(self.assigned_vars[left], ast.Constant) and right in self.assigned_vars and isinstance(self.assigned_vars[right], ast.Constant):

                            n.value.args[i] = ast.BinOp(self.assigned_vars[left],arg.op,self.assigned_vars[right])
                new_body.append(n)
            else:
                new_body.append(n)
        
        node.body = new_body
        return node

def remove_unused_variables_and_simplify_print(code):
    tree = ast.parse(code)
    transformer = RemoveUnusedVariablesAndSimplifyPrint()
    tree = transformer.visit(tree)
    return astor.to_source(tree)

# exemples to try
snippets = [
    """a = 2
c = a + 1
u = 4
print(a + u)
"""
]

for i, snippet in enumerate(snippets):
    refactored_code = remove_unused_variables_and_simplify_print(snippet)
    print(f"original code {i+1}:\n{snippet}")
    print(f"refactored code {i+1}:\n{refactored_code}\n")
