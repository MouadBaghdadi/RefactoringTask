import json

def parse_text_file(input_file):
    with open(input_file, 'r') as file:
        lines = file.readlines()

    data = []
    original_code = []
    refactored_code = []
    in_output = False

    for line in lines:
        line = line.rstrip()
        if line.startswith("# output"):
            in_output = True
            continue
        elif line == "":
            if original_code and refactored_code:
                data.append({
                    "original_code": "\n".join(original_code).strip(),
                    "refactored_code": "\n".join(refactored_code).strip()
                })
            original_code = []
            refactored_code = []
            in_output = False
        elif in_output:
            refactored_code.append(line)
        else:
            original_code.append(line)

    # add the last code snippet if exists
    if original_code and refactored_code:
        data.append({
            "original_code": "\n".join(original_code).strip(),
            # "refactored_code": "\n".join(refactored_code).strip()
        })

    return data

def save_to_json(data, output_file):
    with open(output_file, 'w') as file:
        json.dump(data, file, indent=4)

input_file = 'TestData1.txt'
output_file = 'TestData1.json'

data = parse_text_file(input_file)
save_to_json(data, output_file)

print(f"Data has been successfully converted to {output_file}")
