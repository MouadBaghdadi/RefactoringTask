import json
from tqdm import tqdm
import os
import argparse

def main():
    # Argument parsing
    parser = argparse.ArgumentParser(description="Identify clones in the output JSON files")
    parser.add_argument('--input-file', required=True, help='Path to the input JSON file with outputs')
    parser.add_argument('--output-file', required=True, help='Path to the output JSON file to store clones')
    args = parser.parse_args()

    # Load the outputs from the specified file
    with open(args.input_file) as f:
        outputs = json.load(f)

    clones = {}
    function = 0
    for i in tqdm(range(1000)):
        clone = set()
        skipi = False 
        for k in range(function):
            if i in list(clones.values())[k-1]:
                skipi = True
                continue
        if skipi:
            continue
        for j in range(1000):
            skipj = False
            for k in range(function):
                if j in list(clones.values())[k-1]:
                    skipj = True
                    continue
            if skipj:
                continue
            if outputs[f"{i}"] == outputs[f"{j}"] and i != j:
                clone.add(i)
                clone.add(j)
        if clone:
            clones[function] = list(clone)
            function += 1

    # Save the clones to the specified output file
    with open(args.output_file, "w") as write_file:
        json.dump(clones, write_file)

    print(f'The clones are stored in {args.output_file}')

if __name__ == "__main__":
    main()