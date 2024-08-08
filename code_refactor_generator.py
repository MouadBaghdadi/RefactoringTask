
import tqdm
import hashlib
import time
import re
from refactor_library import refactor
from tinypy_generator import CodeGenerator
import argparse

class CodeRefactorGenerator(CodeGenerator):
    
    
    def generate_and_write_programs(self, num_programs, level, filename='data.txt', deduplicate=True):
        """We will change the output format to be the simplifed version"""
        
        
        start_time = time.time()   # Track the start time for performance measurement.
        start_mem = self.memory_usage() # Track the initial memory usage.
        max_tries = 1000 # Set the maximum number of tries for deduplication.
        num_tries = 0 # Initialize the number of tries counter.
        
        
        with open(filename,'w')as file:
            
            generated_programs = 0
            hashes=set()
            pbar=tqdm.tqdm(desc=f'Generating Level {level} Programs with their corresponding simplified version',total=num_programs)
            while generated_programs < num_programs:
                try:
                    root,program=self.generate_program(level)
                    code = program + "\n# reformulation"

                    output=refactor.RefactorFactory.chooseLevel(level).refactor(program)
                    result = f"""{code}\n{output}"""

                    program_hash = hashlib.sha256(result.encode('utf-8')).hexdigest()
                    if deduplicate:
                         if program_hash not in hashes:
                             hashes.add(program_hash) # Add the hash to the set if it's unique.
                             file.write(result + '\n\n') # Write the program to the file.
                             generated_programs += 1  # Increment the counter for generated programs.
                             pbar.update(1)
                             num_tries = 0 # Reset the tries counter.
                         else:
                             num_tries += 1 # Increment the tries counter.
                             if num_tries >= max_tries:
                                 print("Hit max tries in deduplication, stopping generation.")
                                 break # Stop generation if max tries are reached.
                    else:

                         file.write(result + '\n\n') # Write the program to the file without deduplication.
                         generated_programs += 1   # Increment the counter for generated programs.
                         pbar.update(1)
                         
                except Exception as e:
                    continue

                
    
   
    
def main():
    argparser = argparse.ArgumentParser()
    argparser.add_argument('--num_programs', type=int, default=50000, help='Number of programs to generate')
    argparser.add_argument('--level', type=str, default='1.1', help='Refactor level to use')
    argparser.add_argument('--filename', type=str, default='reformulation.txt', help='Output filename')
    argparser.add_argument('--deduplicate', type=bool,default=True, help='Deduplicate programs')
    args = argparser.parse_args()
    
    
    generator = CodeRefactorGenerator()
    generator.generate_and_write_programs(args.num_programs, args.level, args.filename, deduplicate=args.deduplicate)
    
if __name__ == "__main__":
    main()