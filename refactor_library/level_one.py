from refactor_library.refactor_base import Refactor
import re


class LevelOne(Refactor):
    """THis class is responsible for simplifying code at level 1 both 1.1 and 1.2"""
    
    
    
    def refactor(self, text: str) -> str:
        """Tthis method will simplify the code"""
        return self.__simplify_code(text)
        
    def __simplify_code(self, code: str)->str:
        local_vars = {}
        simplified_code = ""
        
        # Split the code into individual statements
        statements = re.split(r'\n', code)
        
        for statement in statements:
            statement = statement.strip()
            if not statement or statement.startswith('#'):
                continue
            
            if statement.startswith('print'):
                # Extract the expression within the print statement
                expr = re.search(r'print\((.*)\)', statement).group(1)
                simplified_expr = self.__format_expression(expr, local_vars)
                simplified_code += f"print({simplified_expr})\n"
            else:
                # Execute the assignment in the local_vars dictionary
                exec(statement, {}, local_vars)
        
        return simplified_code
    
    def __format_expression(self, expr, local_vars):
        def replace_var(match):
            var = match.group(0)
            return str(local_vars.get(var, var))
        
        # Replace variables with their values using regex
        expr = re.sub(r'\b[a-zA-Z_]\w*\b', replace_var, expr)
        return expr
    
        