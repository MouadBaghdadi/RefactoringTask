import itertools
import json
import os
import argparse

def get_code_snippets(filename):
    """
    Reads the code snippets from the given file and returns a dictionary where keys are the snippet IDs 
    and values are the code snippets without the simplification part.
    """
    with open(filename, 'r') as file:
        lines = file.read()
    
    snippets_list = lines.split("# ")[1::2]
    snippets = {}
    
    for snippet in snippets_list:
        snippet_id, snippet_code = snippet.split('\n', 1)
        snippets[snippet_id] = snippet_code
    
    return snippets

def generate_binary_pairs(snippets, clones):
    """
    Generates all binary pairs of code snippets and labels them as either clones (1) or not clones (0).
    """
    binary_pairs = []

    # Generate clone pairs (label 1)
    for key, indices in clones.items():
        for pair in itertools.combinations(indices, 2):
            snippet1, snippet2 = snippets[f'{pair[0]}'], snippets[f'{pair[1]}']
            binary_pairs.append((snippet1, snippet2, 1))

    # Generate non-clone pairs (label 0)
    all_keys = list(clones.keys())
    for key1, key2 in itertools.combinations(all_keys, 2):
        for idx1 in clones[key1]:
            for idx2 in clones[key2]:
                snippet1, snippet2 = snippets[f'{idx1}'], snippets[f'{idx2}']
                binary_pairs.append((snippet1, snippet2, 0))
    
    return binary_pairs

def write_binary_pairs_to_file(binary_pairs, output_filename):
    """
    Writes the binary pairs and their labels to the specified output file.
    """
    with open(output_filename, 'w') as file:
        for i, (snippet1, snippet2, label) in enumerate(binary_pairs):
            file.write(f"# snippet 1\n{snippet1}")
            file.write(f"# snippet 2\n{snippet2}")
            file.write(f"# is clone\n{label}\n\n")

def main():
    # Argument parsing
    parser = argparse.ArgumentParser(description="Generate binary pairs of code snippets and their clone labels")
    parser.add_argument('--input-clones', required=True, help='Path to the input JSON file with clone data')
    parser.add_argument('--input-snippets', required=True, help='Path to the input file with code snippets')
    parser.add_argument('--output-file', required=True, help='Path to the output file to store binary pairs')
    args = parser.parse_args()

    # Load clones from the specified file
    with open(args.input_clones) as f:
        clones = json.load(f)

    # Load code snippets from the specified file
    snippets = get_code_snippets(args.input_snippets)

    # Generate binary pairs
    binary_pairs = generate_binary_pairs(snippets, clones)

    # Write binary pairs to the output file
    write_binary_pairs_to_file(binary_pairs, args.output_file)

    print(f'Clones and non-clones pairs are generated in {args.output_file}')

if __name__ == "__main__":
    main()