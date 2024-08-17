import random
import io
import os
import contextlib
import json
from tqdm import tqdm
from printed_variables_detector import get_printed_and_condition_variables
from level_2.comparison_check import has_diff_var_comparison

simplifications = []

file_path = os.path.join('level_2', 'dataset2.txt')

level_2 = True
result = False


with open(file_path, 'r') as file:
    lines = file.read()

simplification = lines.split('# Simplification')[1:]

for i in range(len(simplification)):
    simplifications.append(simplification[i].split('\n\n\n#')[0])

printed_vars = {}
for i,snippet in enumerate(simplifications):
    printed_vars[i] = get_printed_and_condition_variables(snippet)


random.seed(42)
random_initializations_var1 = []
random_initializations_var2 = []
random_initializations_var3 = []
random_initializations_var4 = []
random_initializations_var5 = []
for _ in range(50):
    random_initializations_var1.append(random.randint(0, 15))
    random_initializations_var2.append(random.randint(0, 15))
    random_initializations_var3.append(random.randint(0, 15))
    random_initializations_var4.append(random.randint(0, 15))
    random_initializations_var5.append(random.randint(0, 15))

def execute_code_with_random_initialization(snippet, variables, num):
    # Prepare a dictionary of random values to initialize variables

    if level_2:
        result = has_diff_var_comparison(snippet)
    
    if (result and level_2) or not(result and level_2): #when we have a comparison between two diff variables
        if len(variables) == 0:
           code = f"""{snippet}
    """
        elif len(variables) == 1:
            code = f"""{variables[0]} = {random_initializations_var1[num]}
{snippet}
    """
        elif len(variables) == 2:
            code = f"""{variables[0]} = {random_initializations_var1[num]}
{variables[1]} = {random_initializations_var2[num]}        
{snippet}
    """
        elif len(variables) == 3:
            code = f"""{variables[0]} = {random_initializations_var1[num]}
{variables[1]} = {random_initializations_var2[num]} 
{variables[2]} = {random_initializations_var3[num]}       
{snippet}"""
        elif len(variables) == 4:
            code = f"""{variables[0]} = {random_initializations_var1[num]}
{variables[1]} = {random_initializations_var2[num]} 
{variables[2]} = {random_initializations_var3[num]}    
{variables[3]} = {random_initializations_var4[num]}   
{snippet}"""
        else:
            code = f"""{variables[0]} = {random_initializations_var1[num]}
{variables[1]} = {random_initializations_var2[num]} 
{variables[2]} = {random_initializations_var3[num]}    
{variables[3]} = {random_initializations_var4[num]}
{variables[4]} = {random_initializations_var5[num]}    
{snippet}"""
    else: # when we don't have a comparison between two diff variables
        if len(variables) == 0:
            code = f"""{snippet}
    """
        elif len(variables) == 1:
            code = f"""{variables[0]} = {random_initializations_var1[num]}
{snippet}
    """
        elif len(variables) == 2:
            code = f"""{variables[0]} = {random_initializations_var1[num]}
{variables[1]} = {random_initializations_var1[num]}        
{snippet}
    """
        elif len(variables) == 3:
            code = f"""{variables[0]} = {random_initializations_var1[num]}
{variables[1]} = {random_initializations_var1[num]} 
{variables[2]} = {random_initializations_var1[num]}       
{snippet}"""
        elif len(variables) == 4:
            code = f"""{variables[0]} = {random_initializations_var1[num]}
{variables[1]} = {random_initializations_var1[num]} 
{variables[2]} = {random_initializations_var1[num]}    
{variables[3]} = {random_initializations_var1[num]}   
{snippet}"""
        else: 
            code = f"""{variables[0]} = {random_initializations_var1[num]}
{variables[1]} = {random_initializations_var1[num]} 
{variables[2]} = {random_initializations_var1[num]}    
{variables[3]} = {random_initializations_var1[num]}
{variables[4]} = {random_initializations_var1[num]}    
{snippet}"""
    # Capture the output of the code
    output = io.StringIO()
    try:
        # Capture the stdout and execute the code
        with contextlib.redirect_stdout(output):
            exec(code)
    except Exception as e:
        # Capture exceptions such as division by zero, etc.
        return str(e)

    # Return the captured output or the error message
    return output.getvalue().strip()
outputs = {}
for i in tqdm(range(1000)):
    output = []
    for num in range(50):
        output.append(execute_code_with_random_initialization(simplifications[i], list(printed_vars[i]), num))
    outputs[i] = output

file_path = 'level_2\outputs_level2.json'
with open(file_path, "w") as write_file:
    json.dump(outputs, write_file)

print(f'the outputs of the simplified programs are stored in {file_path}')

 
