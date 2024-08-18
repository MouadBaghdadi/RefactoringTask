import random
import re
import ast
import astor
import traceback
from transformations.add_operations import add_operations
from transformations.remove_unused_variables import remove_unused_vars
from transformations.reorder_statment import reorder_statements
from transformations.remove_useless_operations import remove_useless_operations
from transformations.modfy_direction_assignments import apply_simplify_expression
from transformations.simplify_obvious_operations import simplify_obvious_operations
from transformations.simplify_if_statements import apply_randomized_if_simplification
from transformations.simplify_complex_if_statements import simplify_conditions

transformations = {
    0: remove_useless_operations,
    0.11: remove_unused_vars,
    0.001: apply_simplify_expression,
    0.2: add_operations,
    0.0001: reorder_statements,
    0.00001: simplify_obvious_operations,
    0.0002: apply_randomized_if_simplification,
    0.21: simplify_conditions
}

class CodeTransformer(ast.NodeTransformer):
    def __init__(self):
        super().__init__()
        self.variable_map = {}
        self.constant_map = {}
        self.in_simple_assignment = False  # To track if we're inside a simple assignment
    
    def visit_Assign(self, node):
        if isinstance(node.value, ast.Constant):
            self.in_simple_assignment = True
            for target in node.targets:
                if isinstance(target, ast.Name):
                    old_name = target.id
                    new_name = self.get_new_variable_name()
                    self.variable_map[old_name] = new_name
                    target.id = new_name

            old_value = node.value.value
            new_value = self.get_new_constant_value()
            self.constant_map[old_value] = new_value
            node.value.value = new_value
            self.in_simple_assignment = False
        
        return node

    def visit_Name(self, node):
        if node.id in self.variable_map:
            node.id = self.variable_map[node.id]
        return node

    def visit_Constant(self, node):
        if self.in_simple_assignment and node.value in self.constant_map:
            node.value = self.constant_map[node.value]
        return node

    def apply_self_transformations(self, source_code):
        tree = ast.parse(source_code)
        transformed_tree = self.visit(tree)
        transformed_code = astor.to_source(transformed_tree)

        # Ensure all variable occurrences are replaced consistently
        transformed_code = self.replace_all_variable_occurrences(transformed_code)
        return transformed_code

    def replace_all_variable_occurrences(self, code):
        for old_name, new_name in self.variable_map.items():
            pattern = rf'\b{re.escape(old_name)}\b'
            code = re.sub(pattern, new_name, code)
        return code

    def get_new_variable_name(self):
        return f"var_{random.randint(1000, 9999)}"
    
    def get_new_constant_value(self):
        return random.randint(0, 100)

    def enforce_print_statement(self, code):
        last_line_pattern = r'print\(([^)]+)\)'
        match = re.search(last_line_pattern, code)
        if match:
            variable_name = match.group(1).split('/')[0].strip()
            new_print_statement = f'print({variable_name} / {variable_name})'
            code = re.sub(last_line_pattern, new_print_statement, code)
        return code

    def apply_transformations(self, code_snippet):
        code = code_snippet

        # Apply self transformations first
        code = self.apply_self_transformations(code)

        # Prepare to log failed transformations
        log_file_path = 'failed_transformations.txt'
        with open(log_file_path, 'a') as log_file:
            # Shuffle and apply each transformation based on probability
            transformation_items = list(transformations.items())
            for threshold, transformation in transformation_items:
                random_uniform = random.uniform(0, 1)  # Use uniform distribution for probability
                if random_uniform > threshold:
                    try:
                        code = transformation(code)
                    except Exception as e:
                        # Write the failed code snippet and error message to the log file
                        stack_trace = traceback.format_exc()
                        log_file.write(f"Error in transformation:\n{code}\nException: {str(e)}\nStack Trace:\n{stack_trace}\n\n")
                     
        return code