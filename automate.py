import subprocess
import sys
import os

def run_script(script_name, args):

    subprocess.run(['python', script_name] + args, check=True)

def automate_process(programs_num):
    level_folder = f"all_levels"
    for i in range(1,4):
        dataset_file = os.path.join(level_folder, f"dataset_level{i}.txt")
        outputs_json = os.path.join(level_folder, f"outputs_level{i}.json")
        clones_json = os.path.join(level_folder, f"clones_level{i}.json")
        clone_pairs_txt = os.path.join(level_folder, f"clone_pairs.txt")
    
        run_script('code_gen.py', ['--num_programs', programs_num, f'--level', f'{i}.2', '--filename', dataset_file])
    
        run_script('code_execution.py', [f'--level', f'{i}',f'--dataset-file', dataset_file, '--output-file',     outputs_json])

        run_script('identify_clones.py', ['--input-file', outputs_json, '--output-file', clones_json])

        run_script('generating_binaries.py', ['--input-clones',clones_json,'--input-snippets', dataset_file, '--output-file', clone_pairs_txt])

        os.remove(dataset_file)
        os.remove(outputs_json)
        os.remove(clones_json)

    print(f"Process for all levels completed successfully!")

if __name__ == "__main__":

    programs_num = sys.argv[2]
    print(sys.argv)
    automate_process(programs_num)
