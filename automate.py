import subprocess
import sys
import os

def run_script(script_name, args):

    subprocess.run(['python', script_name] + args, check=True)

def automate_process(level):
    level_folder = f"level_{level}"
    # simplify_script = os.path.join(level_folder, f"simplify_level{level}.py")
    dataset_file = os.path.join(level_folder, f"dataset{level}.txt")
    outputs_json = os.path.join(level_folder, f"outputs_level{level}.json")
    clones_json = os.path.join(level_folder, f"clones_level{level}.json")
    clone_pairs_txt = os.path.join(level_folder, f"clone_pairs_level{level}.txt")

    run_script('code_gen.py', [f'--level', f'{level}.2', '--filename', dataset_file])

    run_script('code_execution.py', [f'--level', f'{level}',f'--dataset-file', dataset_file, '--output-file', outputs_json])

    run_script('identify_clones.py', ['--input-file', outputs_json, '--output-file', clones_json])

    run_script('generating_binaries.py', ['--input-clones',clones_json,'--input-snippets', dataset_file, '--output-file', clone_pairs_txt])

    print(f"Process for level {level} completed successfully!")

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("usage: python automate.py <level>")
        sys.exit(1)

    level = sys.argv[1]
    if level not in ['1', '2', '3']:
        print("invalid level, choose 1, 2, or 3.")
        sys.exit(1)

    automate_process(level)
