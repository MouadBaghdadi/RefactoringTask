import ast
import astor
import argparse
from transformations.transformer import CodeTransformer
from tqdm import tqdm
# Initialize the transformer
transformer = CodeTransformer()

def use_main_tranformer(code_snippet):
    # Parse code snippet into AST
    tree = ast.parse(code_snippet)
    
    # Transform the AST
    transformed_tree = transformer.visit(tree)
    
    # Convert AST back to source code
    new_code_snippet = astor.to_source(transformed_tree).strip()
    
    return new_code_snippet

def process_code_files(input_file, output_file):
    with open(input_file, 'r') as infile:
        snippets = infile.read().strip().split('\n\n')

    with open(output_file, 'w+') as outfile:
        for idx,snippet_1 in enumerate(tqdm(snippets)):
          
            
            # make sure the main transformer is the first transformation being applied
            snippet_2 = use_main_tranformer(snippet_1)
            snippet_2 = transformer.apply_transformations(snippet_2)
            
            # Generate a clone
            
            # Write the results to the output file
            outfile.write(f"# snippet 1\n{snippet_1}\n")
            outfile.write(f"# snippet 2\n{snippet_2}\n")
            outfile.write("# clone\n1\n\n")  # Assuming snippet 2 is a clone of snippet 1

def main():
    parser = argparse.ArgumentParser(description="Process and transform Python code snippets.")
    
    parser.add_argument("--input", default="level1.1.txt" ,type=str, help='Path to the input file containing code snippets.')
    
    args = parser.parse_args()
    
    process_code_files(args.input, f"clones_{args.input}")

if __name__ == "__main__":
    main()
