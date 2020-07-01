



def trim(bp_off_start_string, bp_off_end_string, input_text_file):
    # annoyingly these are inputted as strings so have to convert basepair number to an integer
    bp_off_start = int(bp_off_start_string)
    bp_off_end = int(bp_off_end_string)

    # stopping negative bps from working
    if bp_off_start < 0 or bp_off_end < 0:
        warning = "You can't trim negative bps off, please reinput"
        print("")
        print (warning)
        print("")
        return warning
    print("")
    print(f"Trimming {bp_off_start}bp from the start of each sequence, and {bp_off_end}bp from the end of each sequence in {input_text_file}")
    print("")
    
    #reading input file by line
    sequence_file = open(input_text_file,'r')
    lines = sequence_file.readlines()
    #remove \n from ends if there is one (if not ignore because it's the last line)
    lines = [item[0:-1] if "\n" in item else item for item in lines]
    list_of_sequences = []
    #trimming and putting seq description and sequence together as a list
    for i in range(0,len(lines)):
        if '>' in lines[i]: # aka if it's the information line
            description = lines[i] + "\n" # making it a separate line
            sequence = lines[i+1] # sequence always comes after the description line
            if bp_off_end == 0:
                trimmed_sequence = sequence[bp_off_start:] + "\n"
            else: 
                trimmed_sequence = sequence[bp_off_start:-bp_off_end] + "\n"
            sample_list = [description, trimmed_sequence]
            list_of_sequences.append(sample_list)
    print("Status:")
    print("Sequence(s) Trimmed")
    
    #save file
    output_file_name = 'output_' + input_text_file 
    output_file = open(output_file_name, 'w')
    
    # writing output file with the new lines re-written in
    for description, trimmed_sequence in list_of_sequences:
        output_file.writelines([description, trimmed_sequence, "\n"])
    
    print(f"Trimmed sequence(s) saved to {output_file_name}")
    print("")