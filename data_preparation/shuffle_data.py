import random

def parse_snippets(file_path):
    with open(file_path, 'r') as file:
        content = file.read()

    snippets = []
    blocks = content.strip().split("\n\n")
    
    for block in blocks:
        lines = block.strip().split("\n")
        snippet1 = []
        snippet2 = []
        is_clone = None
        
        current_snippet = None
        for line in lines:
            if line.startswith("# snippet1"):
                current_snippet = snippet1
            elif line.startswith("# snippet2"):
                current_snippet = snippet2
            elif line.startswith("# is clone"):
                # Correctly extract the integer value after '# is clone'
                is_clone = int(lines[lines.index(line) + 1].strip())
            else:
                current_snippet.append(line)
        snippet2.pop()
        snippets.append({
            "snippet1": "\n".join(snippet1),
            "snippet2": "\n".join(snippet2),
            "is_clone": is_clone
        })

    return snippets

def shuffle_snippet2(snippets, num_to_shuffle=7000):
    indices = list(range(len(snippets)))
    random.shuffle(indices)
    selected_indices = indices[:num_to_shuffle]
    
    # Shuffle selected snippets
    selected_snippets = [snippets[i] for i in selected_indices]
    snippet2_list = [snippet["snippet2"] for snippet in selected_snippets]
    random.shuffle(snippet2_list)
    
    for i, idx in enumerate(selected_indices):
        snippets[idx]["snippet2"] = snippet2_list[i]
        snippets[idx]["is_clone"] = 0  # Set clone status to 0 after shuffle
    return snippets

def write_snippets_to_file(snippets, output_file_path):
    with open(output_file_path, 'w') as file:
        for snippet in snippets:
            file.write("# snippet1\n")
            file.write(snippet["snippet1"] + "\n")
            file.write("# snippet2\n")
            file.write(snippet["snippet2"] + "\n")
            file.write(f"# is clone\n# {snippet['is_clone']}\n")
            file.write("\n")

# Paths
input_file = 'clone_level1.txt'
output_file = 'clone_level1_shuffled.txt'

# Process
snippets = parse_snippets(input_file)
shuffled_snippets = shuffle_snippet2(snippets, num_to_shuffle=7000)
write_snippets_to_file(shuffled_snippets, output_file)

print(f"Shuffled snippets saved to {output_file}")

# import random

# def parse_snippets(file_path):
#     with open(file_path, 'r') as file:
#         content = file.read()

#     snippets = []
#     blocks = content.strip().split("\n\n")  # Split blocks of code by double newlines
    
#     for block in blocks:
#         lines = block.strip().split("\n")
#         snippet1 = []
#         snippet2 = []
#         is_clone = None
        
#         current_snippet = None
#         for line in lines:
#             if line.startswith("# snippet1"):
#                 current_snippet = snippet1
#             elif line.startswith("# snippet2"):
#                 current_snippet = snippet2
#             elif line.startswith("# is clone"):
#                 # Correctly extract the integer value for 'is clone' line
#                 is_clone = line.split()[-1].strip()
#             else:
#                 current_snippet.append(line)
#         snippet2.pop()
#         snippets.append({
#             "snippet1": "\n".join(snippet1),
#             "snippet2": "\n".join(snippet2),
#             "is_clone": is_clone
#         })

#     return snippets

# def shuffle_snippet2(snippets, num_to_shuffle=300):
#     indices = list(range(len(snippets)))
#     random.shuffle(indices)
#     selected_indices = indices[:num_to_shuffle]
    
#     # Shuffle selected snippet2 sections
#     selected_snippets = [snippets[i] for i in selected_indices]
#     snippet2_list = [snippet["snippet2"] for snippet in selected_snippets]
#     random.shuffle(snippet2_list)
    
#     # Reassign shuffled snippet2 sections and update clone status
#     for i, idx in enumerate(selected_indices):
#         snippets[idx]["snippet2"] = snippet2_list[i]
#         snippets[idx]["is_clone"] = 0  # Set clone status to 0 after shuffle
    
#     return snippets

# def write_snippets_to_file(snippets, output_file_path):
#     with open(output_file_path, 'w') as file:
#         for snippet in snippets:
#             file.write("# snippet1\n")
#             file.write(snippet["snippet1"] + "\n")
#             file.write("# snippet2\n")
#             file.write(snippet["snippet2"] + "\n")
#             file.write(f"# is clone\n# {snippet['is_clone']}\n")
#             file.write("\n")

# # Paths
# input_file = 'clone_level1.txt'
# output_file = 'clone_level1_shuffled.txt'

# # Process
# snippets = parse_snippets(input_file)
# shuffled_snippets = shuffle_snippet2(snippets, num_to_shuffle=300)
# write_snippets_to_file(shuffled_snippets, output_file)

# print(f"Shuffled snippets saved to {output_file}")

