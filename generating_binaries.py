import itertools
import json
import os

file_path = os.path.join('level 2', 'clones_level2.json')

with open(file_path) as f:
    clones = json.load(f) 

def get_code_snippets(filename):
    """
    Reads the code snippets from the given file and returns a dictionary where keys are the snippet IDs 
    and values are the code snippets without the simplification part.
    """
    snippet_id = None
    snippet_code = []
    
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

data_filename = os.path.join('level 2', 'dataset2.txt')
output_filename = os.path.join('level 2', "clone_pairs_level2.txt")

snippets = get_code_snippets(data_filename)

# Generate binary pairs
binary_pairs = generate_binary_pairs(snippets, clones)

# Write binary pairs to the output file
write_binary_pairs_to_file(binary_pairs, output_filename)

print(f'clones and non clones pairs are generated in {output_filename}')