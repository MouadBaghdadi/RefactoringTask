import pandas as pd
import argparse
import tqdm
import sys 
import pandas 
import io
def run_code(code):
    # Redirect standard output to capture the prints
    old_stdout = sys.stdout
    sys.stdout = mystdout = io.StringIO()
    try:
        exec(code)
    except Exception as e:
        print(f"Error in execution: {e}")
    # Reset standard output
    sys.stdout = old_stdout
    return mystdout.getvalue().strip()

def extract_code_and_reformulation(data):
    original_code = []
    reformulation = []
    lines = data.split('\n')
    i = 0
    current_original_code = []

    while i < len(lines):
        line = lines[i]
        if line.lstrip().startswith('# reformulation'):
            # Skip the '# reformulation' line
            i += 1
            current_reformulation = []
            while i < len(lines) and lines[i].strip():
                current_reformulation.append(lines[i])
                i += 1
            # Join the reformulation code block and append
            reformulation.append('\n'.join(current_reformulation))
            # Append the collected original code block
            original_code.append('\n'.join(current_original_code))
            current_original_code = []
        elif line.strip():  # Include non-empty lines only
            current_original_code.append(line)
        i += 1

    # Add any remaining original code if no final reformulation marker is present
    if current_original_code:
        original_code.append('\n'.join(current_original_code))

    # Ensure both lists are of equal length
    while len(reformulation) < len(original_code):
        reformulation.append('')

    return original_code, reformulation


def validate_code(original_code, reformulated_code):
    try:
        original_output = run_code(original_code)    
        reformulated_output = run_code(reformulated_code)
        
        if original_output!=reformulated_output:
            print("original code :",original_code)
            print("reformulated code :",reformulated_code)
            print("orginal output :",original_output)
            print("reformulated output : ",reformulated_output)
        return original_output == reformulated_output
    except Exception as e:
        print(f"Error in validation: {e}")
        return False

def main():
    parser = argparse.ArgumentParser(description='Validate dataset of code reformulations')
    parser.add_argument('--filename', type=str, default='./reformulation.txt', help='The txt file to validate')
    
    args = parser.parse_args()
    with open(args.filename, 'r') as file:
        data = file.read()

    # Extract code and reformulations
    original_code, reformulation = extract_code_and_reformulation(data)

    # Prepare DataFrame
    df = pd.DataFrame(columns=['original_code', 'reformulation', 'is_valid'])

    for i in tqdm.tqdm(range(len(reformulation)), desc="Validating code"):
        if reformulation[i]:
            original = original_code[i]
            reform = reformulation[i]
            is_valid = validate_code(original, reform)
            df.loc[-1]=[ original,  reform,  is_valid]
            df.index = df.index + 1
            df = df.sort_index()
            
 
    all_rows_valid=(df['is_valid']==False).sum()
    if all_rows_valid==0:
        print("All rows are valid")
    else:
        print("Some rows are invalid")
        df[df['is_valid']==False].to_csv('invalid_rows.csv', index=False)

  

if __name__ == "__main__":
    main()
