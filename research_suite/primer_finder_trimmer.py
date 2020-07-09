from utils import *
from parameters import *
import os
from os import listdir
from os import path
from os.path import isfile, join

# REVISIT
# REVISIT
# REVISIT
# REVISIT


def primer_finder_timmer():
    # locating the folder of local .txt sequence files

    dir = os.getcwd()
    local_files_path = dir + "/" + folder

    # making files in the folder into a list
    sequence_files_list_raw = listdir(local_files_path)
    sequence_files_list_checked = []

    # only using files which haven't previously been trimmed
    for sequence_file in sequence_files_list_raw:
        if sequence_file[-12:] != "_trimmed.txt" and sequence_file[-4:] == '.txt':
            sequence_files_list_checked.append(sequence_file)

    number_of_files = len(sequence_files_list_checked)

    # giving the user an update
    print(f"Attempting to trim {number_of_files} files:")
    print("")
    for sequence_file in sequence_files_list_checked:
        print(sequence_file)
    print("")
    print('###################################')
    print("")

    # setting off the trimming, and saving each sequence as a new file
    for sequence_file in sequence_files_list_checked:
        tidy_trim_save(folder, sequence_file, number_of_extra_bps_upstream, number_of_extra_bps_downstream, forward_primer_option1, forward_primer_option2,
                       forward_primer_option3, reverse_primer_complement_option1, reverse_primer_complement_option2, reverse_primer_complement_option3)
