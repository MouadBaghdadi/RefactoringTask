import ast
import astor
import argparse
import csv
from concurrent.futures import ThreadPoolExecutor, as_completed
from threading import local
from tqdm import tqdm
from transformations.transformer import CodeTransformer, transformation_names

# Create thread-local storage
thread_local = local()
csv_path = "meta.csv"

def get_transformer():
    if not hasattr(thread_local, 'transformer'):
        thread_local.transformer = CodeTransformer()
    return thread_local.transformer

def use_main_transformer(code_snippet):
    transformer = get_transformer()
    # Parse code snippet into AST
    tree = ast.parse(code_snippet)
    
    # Transform the AST
    transformed_tree = transformer.visit(tree)
    
    # Convert AST back to source code
    new_code_snippet = astor.to_source(transformed_tree).strip()
    
    return new_code_snippet

def process_single_snippet(snippet):
    transformer = get_transformer()
    # Apply transformations
    snippet_2 = use_main_transformer(snippet)
    snippet_2 = transformer.apply_transformations(snippet_2, csv_file_path=csv_path)
    
    return snippet, snippet_2

def process_code_files(input_file, output_file):
    with open(input_file, 'r') as infile:
        snippets = infile.read().strip().split('\n\n')

    with open(output_file, 'w+') as outfile:
        # Initialize tqdm for progress tracking
        progress_bar = tqdm(total=len(snippets), desc="Processing Snippets")
        
        # Use ThreadPoolExecutor to parallelize the processing
        with ThreadPoolExecutor() as executor:
            future_to_snippet = {executor.submit(process_single_snippet, snippet): snippet for snippet in snippets}
            
            for future in as_completed(future_to_snippet):
                snippet_1 = future_to_snippet[future]
                try:
                    snippet_1, snippet_2 = future.result()
                    # Write the results to the output file
                    outfile.write(f"# snippet 1\n{snippet_1}\n")
                    outfile.write(f"# snippet 2\n{snippet_2}\n")
                    outfile.write("# clone\n1\n\n")  # Assuming snippet 2 is a clone of snippet 1
                except Exception as e:
                    print(f"Exception occurred while processing snippet: {e}")
                finally:
                    progress_bar.update(1)  # Update progress bar for each completed future

        progress_bar.close()  # Close progress bar when done

def main():
    parser = argparse.ArgumentParser(description="Process and transform Python code snippets.")
    
    parser.add_argument("--input", default="level1.1.txt", type=str, help='Path to the input file containing code snippets.')
    
    args = parser.parse_args()
    with open(csv_path, 'w', newline='') as csv_file:
        writer = csv.writer(csv_file)
        writer.writerow(transformation_names)

    process_code_files(args.input, f"clones_{args.input}")

if __name__ == "__main__":
    main()
