import ast
import astor

class RemoveUnusedVariablesAndSimplifyPrint(ast.NodeTransformer):
    def __init__(self):
        self.used_vars = set()
        self.assigned_vars = {}
        self.dependencies = {}
    
    def visit_Name(self, node):
        
        if isinstance(node.ctx, ast.Load):
            # check if the current variable (node.id) is used by any other variable already in used_vars probably it solves the problem
            for var, deps in self.dependencies.items():
                if var in self.used_vars and node.id in deps:
                    self.used_vars.add(node.id)
                    break
        elif isinstance(node.ctx, ast.Store):
            self.assigned_vars[node.id] = None
        return node
    
    def visit_Assign(self, node):
        self.generic_visit(node.value)
        for target in node.targets:
            if isinstance(target, ast.Name):
                self.visit_Name(target)
                self.assigned_vars[target.id] = node.value
                dependencies = self.find_dependencies(node.value)
                self.dependencies[target.id] = dependencies

        return node

    def find_dependencies(self, node):
        dependencies = set()
        for child in ast.walk(node):
            if isinstance(child, ast.Name) and isinstance(child.ctx, ast.Load):
                dependencies.add(child.id)
        return dependencies
    
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

    def visit_Module(self, node):
        self.generic_visit(node)

        all_used_vars = set(self.used_vars)
        additional_vars = set(self.used_vars)
        while additional_vars:
            current_var = additional_vars.pop()
            if current_var in self.dependencies:
                additional_dependencies = self.dependencies[current_var]
                new_vars = additional_dependencies - all_used_vars
                all_used_vars.update(additional_dependencies)
                additional_vars.update(new_vars)

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
    """y = 9
o = 1
c = 6
x = o * 2
print(y * o)
"""
]

for i, snippet in enumerate(snippets):
    refactored_code = remove_unused_variables_and_simplify_print(snippet)
    print(f"original code {i+1}:\n{snippet}")
    print(f"refactored code {i+1}:\n{refactored_code}\n")
