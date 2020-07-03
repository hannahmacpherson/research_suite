import sys
from utils import * 

 
## inputting from the terminal. Stopping it from working if you don't add the right number of inputs
if __name__ == "__main__":
        try:
            trim(sys.argv[1], sys.argv[2], sys.argv[3])
        except IndexError:
            print("")
            print("You've inputted your variables wrong - make sure it's trimmer.py bp_off_start bp_off_end input_file.txt output_file.txt")
            print("")

