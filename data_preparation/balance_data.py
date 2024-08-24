import re

def filter_snippets(input_file, output_file, max_examples=200000):
    with open(input_file, 'r') as file:
        data = file.read()

    # Split the data into individual examples
    examples = data.strip().split('\n\n')

    clone_0 = []
    clone_1 = []

    for example in examples:
        if '# is clone\n0' in example and len(clone_0) < max_examples:
            clone_0.append(example)
        elif '# is clone\n1' in example and len(clone_1) < max_examples:
            clone_1.append(example)

        if len(clone_0) >= max_examples and len(clone_1) >= max_examples:
            break

    # Combine the filtered examples
    filtered_examples = clone_0 + clone_1

    with open(output_file, 'w') as file:
        file.write('\n\n'.join(filtered_examples))

    print(f'Filtered {len(clone_0)} examples of clone 0 and {len(clone_1)} examples of clone 1.')

# Usage
input_file = 'level_3//clone_pairs_level3.txt'
output_file = 'balanced_dataset3.txt'
filter_snippets(input_file, output_file)