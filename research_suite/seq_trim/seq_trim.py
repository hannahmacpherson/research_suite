import csv
import seaborn as sns
# from matplotlib import pyplot as plt
import pandas as pd
import numpy as np
import sys
import logging
# import openpyxl
# from openpyxl import workbook
# import json
# import numpy as np
# import pandas as pd
# # import xlrd
# import csv
# import os
# from os import listdir
# from os.path import isfile, join
# import sys
# from population_functions import *


def trim(bp_off_start_string, bp_off_end_string, input_text_file):
    # annoyingly these are inputted as strings so have to convert basepair number to an integer
    bp_off_start = int(bp_off_start_string)
    bp_off_end = int(bp_off_end_string)

    # stopping negative bps from working
    if bp_off_start < 0 or bp_off_end < 0:
        warning = "You can't trim negative bps off, please reinput"
        print("")
        print(warning)
        print("")
        return warning
    print("")
    print(f"Trimming {bp_off_start}bp from the start of each sequence, and {bp_off_end}bp from the end of each sequence in {input_text_file}")
    print("")

    # reading input file by line
    sequence_file = open(input_text_file, 'r')
    lines = sequence_file.readlines()
    # remove \n from ends if there is one (if not ignore because it's the last line)
    lines = [item[0:-1] if "\n" in item else item for item in lines]
    list_of_sequences = []
    # trimming and putting seq description and sequence together as a list
    for i in range(0, len(lines)):
        if '>' in lines[i]:  # aka if it's the information line
            description = lines[i] + "\n"  # making it a separate line
            # sequence always comes after the description line
            sequence = lines[i+1]
            if bp_off_end == 0:
                trimmed_sequence = sequence[bp_off_start:] + "\n"
            else:
                trimmed_sequence = sequence[bp_off_start:-bp_off_end] + "\n"
            sample_list = [description, trimmed_sequence]
            list_of_sequences.append(sample_list)
    print("Status:")
    print("Sequence(s) Trimmed")

    # save file
    output_file_name = 'output_' + input_text_file
    output_file = open(output_file_name, 'w')

    # writing output file with the new lines re-written in
    for description, trimmed_sequence in list_of_sequences:
        output_file.writelines([description, trimmed_sequence, "\n"])

    print(f"Trimmed sequence(s) saved to {output_file_name}")
    print("")

###
# Have added some things just to intro you to new concepts.
# 1. Logging 2. Argparse (main.py) 3. Custom exceptions
#
###

# Custom exceptions are any known errors that may occur


class NegativeBpsNotAllowed(Exception):
    pass


def trim_2(bp_off_start: int, bp_off_end: int, input_text_file: str):

    # any variables that you may need in your code should be initialized at the start unless
    # specific to a loop/function
    list_of_sequences = []

    # keep these variable names the same so you dont make new random variables

    # Notice, we don't need to explicilty say int() cause of argparse (main.py)
    try:
        if bp_off_start < 0 or bp_off_end < 0:
            raise NegativeBpsNotAllowed
    except NegativeBpsNotAllowed:
        logger.error("I am an error")

    logging.info(
        f"Trimming {bp_off_start}bp from the start of each sequence, and {bp_off_end}bp from the end of each sequence in {input_text_file}")

    sequence_file = open(input_text_file, 'r')
    lines = sequence_file.readlines()
    lines = [item[0:-1] if "\n" in item else item for item in lines]

    # I like this!
    for i in range(0, len(lines)):
        if '>' in lines[i]:
            description = lines[i] + "\n"
            sequence = lines[i+1]
            if bp_off_end == 0:
                trimmed_sequence = sequence[bp_off_start:] + "\n"
            else:
                trimmed_sequence = sequence[bp_off_start:-bp_off_end] + "\n"
            sample_list = [description, trimmed_sequence]
            list_of_sequences.append(sample_list)

    logging.info("Requested sequences have been trimmed successfully!")

    # Looks scary, just extracting only the file name by splitting at "/"
    # And then taking the last one so == [-1]

    output_file_name = f'output_{input_text_file.split("/")[-1]}'
    output_file = open(output_file_name, 'w')

    for description, trimmed_sequence in list_of_sequences:
        output_file.writelines([description, trimmed_sequence, "\n"])

    logging.info(f"Trimmed sequence(s) saved to {output_file_name}")

    return output_file_name
