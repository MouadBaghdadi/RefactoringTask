import random
import io
import contextlib
import json
from tqdm import tqdm
from print_variable_detector import get_printed_variables

simplifications = []

with open('dataset1.txt', 'r') as file:
    lines = file.readlines()

for i, line in enumerate(lines):
    if "# Simplification" in line:
        simplifications.append(lines[i + 1].strip())

printed_vars = {}
for i,snippet in enumerate(simplifications):
    printed_vars[i] = get_printed_variables(snippet)

random.seed(42)
random_initializations_var1 = []
random_initializations_var2 = []
for _ in range(100):
    random_initializations_var1.append(random.randint(1, 1000))
    random_initializations_var2.append(random.randint(1, 1000))

def execute_code_with_random_initialization(snippet, variables, num):
    # Prepare a dictionary of random values to initialize variables
    if len(variables) == 0:
        code = f"""{snippet}
    """
    elif len(variables) == 1:
        code = f"""{variables[0]} = {random_initializations_var1[num]}
{snippet}
    """
    else:
        code = f"""{variables[0]} = {random_initializations_var1[num]}
{variables[1]} = {random_initializations_var2[num]}        
{snippet}
    """
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
    for num in range(10):
        output.append(execute_code_with_random_initialization(simplifications[i], list(printed_vars[i]), num))
    outputs[i] = output

file_path = 'outputs_level1.json'
with open(file_path, "w") as write_file:
    json.dump(outputs, write_file)

print(f'the outputs of the simplified programs are stored in {file_path}')

 
