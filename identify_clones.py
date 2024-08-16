import json
from tqdm import tqdm

with open('outputs_level1.json') as f:
    outputs = json.load(f)

clones = {}
function = 0
for i in tqdm(range(1000)):
    clone = set()
    skipi = False 
    print(f"function = {function}")
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
        if outputs[f"{i}"] == outputs[f"{j}"] and i != j :
            clone.add(i)
            clone.add(j)
    if clone:
        clones[function] = list(clone)
        function += 1

print(clones)

file_path = 'clones_level1.json'
with open(file_path, "w") as write_file:
    json.dump(clones, write_file)

print(f'the clones are stored in {file_path}')