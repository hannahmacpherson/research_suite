import csv
import seaborn as sns
from matplotlib import pyplot as plt
import pandas as pd
import numpy as np
import sys
import logging
import openpyxl
from openpyxl import workbook
import json
import numpy as np
import pandas as pd
import xlrd
import csv
import os
from os import listdir
from os.path import isfile, join
import sys
from population_functions import *


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
    if bp_off_start < 0 or bp_off_end < 0:
        logging.error("Negative BP not allowed!")
        raise NegativeBpsNotAllowed

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


# takes csv input file and filters it by gene and polymerase to output a dataframe
def make_dataframe(amp_csv, gene, polymerase='all'):
    df = pd.read_csv(amp_csv)
    df = df.loc[df['gene'] == gene]
    if polymerase != "all":
        df = df.loc[df['polymerase'] == polymerase]
    rows = row_counter(df)
    if rows == 0:  # aka dataframe is empty
        sys.exit("Filtered data has zero rows, the gene or polymerase may be different to how they are written in your input file, or this gene may not be sequenced with the specified polymerase.")
    else:
        return df

# counts how many rows in dataframe. If you've sorted it, it will therefore tell you how many amps your data after this point is based on


def row_counter(df):
    row_count = len(df)
    return row_count

# works out the average number of amps per barcode in your (possibly filtered by gene/polymerase) dataframe


def average_amps_per_barcode(df):
    filtered_df = df[['barcode', 'sample_ID']]
    filtered_grouped_df = filtered_df.groupby(
        ['barcode']).size().reset_index(name='counts')
    mean_amps_per_bc = filtered_grouped_df['counts'].mean()
    return mean_amps_per_bc


def barcode_success_rate(df):
        # creates a dataframe with a % success rate per barcode (NB only two columns in resulting dataframe + index)
        x, y = 'barcode', 'pass_fail'
        # sorts dataframe to group it by both barcode and pass/fail. Gives pass/fail for each barcode a score out of 1
        counted_df = df.groupby(x)[y].value_counts(normalize=True)
        # converts this score into a percentage and labels the column accordingly
        percentage_df = counted_df.mul(100)
        percentage_df = percentage_df.rename(
            'percentage_success').reset_index()
        # only keeps the success rate (%) of the pass column
        success_rate_df = percentage_df.loc[percentage_df['pass_fail'] == "PASSED"].reset_index(
            drop=True)
        # get rid of pass_fail column because now every line says PASS lol
        success_rate_df = success_rate_df.drop(columns='pass_fail')
        return success_rate_df

# what it says on the tin, saves the dataframe to a csv file in your local area


def save_df_to_csv_tabbed(df, gene, polymerase='all'):
    df.to_csv(f'{gene}_{polymerase}_polymerase_percentage_success_data.csv',
              sep='\t', index=False)

# sorts dataframe by % success, then prints out the worst x you specify


def worst_barcodes(df, number_of_barcodes=5):
    # in case number_of_barcodes comes as a string, converting to integer
    number_of_barcodes_int = int(number_of_barcodes)
    success_rate_df = barcode_success_rate(df)
    success_rate_df = success_rate_df.sort_values(
        by='percentage_success', ascending=True)
    chop_by_number_of_bc = success_rate_df[:number_of_barcodes_int]
    # convert to string so you don't print the index
    printable_version = chop_by_number_of_bc.to_string(index=False)
    return printable_version


def best_barcodes(df, number_of_barcodes=5):
    # sorts dataframe by % success, then prints out the worst x you specify
    # in case number_of_barcodes comes as a string, converting to integer
    number_of_barcodes_int = int(number_of_barcodes)
    success_rate_df = barcode_success_rate(df)
    success_rate_df = success_rate_df.sort_values(
        by='percentage_success', ascending=False)
    chop_by_number_of_bc = success_rate_df[:number_of_barcodes_int]
    # convert to string so you don't print the index
    printable_version = chop_by_number_of_bc.to_string(index=False)
    return printable_version


def best_and_worst_barcodes(df, number_of_barcodes=5):
    worst = worst_barcodes(df, number_of_barcodes)
    best = best_barcodes(df, number_of_barcodes)
    return best, worst


def percentage_success_for_particular_barcode(barcode, df):
    df_of_success_rates = barcode_success_rate(df)
    df_for_barcode = df_of_success_rates.loc[df_of_success_rates['barcode'] == barcode]
    df_as_string = df_for_barcode.to_string(index=False)
    print(df_as_string)


def number_of_amps_per_barcode(df):
    filtered_df = df[['barcode', 'sample_ID']]
    filtered_grouped_df = filtered_df.groupby(
        ['barcode']).size().reset_index(name='counts')
    return filtered_grouped_df


def plot_barcode_success_rate(amp_csv, gene, polymerase='all'):

    # making various bits of information i'll need
    df = make_dataframe(amp_csv, gene, polymerase)
    amps_per_bc = number_of_amps_per_barcode(df)
    success_rate = barcode_success_rate(df)
    number_of_amps = row_counter(df)

    # merging success rates with amps per barcode
    success_and_amps_per_bc = success_rate.merge(
        amps_per_bc, left_on='barcode', right_on='barcode')

    # plotting (always plotting)
    plt.figure(figsize=(18, 7))
    plot_order = success_and_amps_per_bc.sort_values(
        by='percentage_success', ascending=True).barcode.values

    plot = sns.barplot(x="barcode", y="percentage_success",
                       data=success_and_amps_per_bc, order=plot_order)
    plot.set(
        xlabel=f"{gene} Barcodes",
        ylabel="Percentage Success Rate",
        title=f'Percentage Success for {gene} Barcodes over a Total of {number_of_amps} Amplifications using {polymerase} Polymerase(s)'
    plt.setp(plot.get_xticklabels(), rotation=90)
    plt.setp(plot.set_yticklabels([0, 20, 40, 60, 80, 100]), rotation=90)


# saving report info to a text file for easier reading - decided not to actually use this but don't want to delete it despite not being finished
def save_analysis_info(amp_csv, gene, polymerase, mean_bc_amps, best_worst_barcodes, best, worst, number_of_barcodes, number_of_amps):

    line_1=f"Your input {amp_csv} contained {number_of_amps} amplifications specific to {gene} using {polymerase} polymerase(s)."
    line_2=f"\nThe mean number of amps per barcode was {mean_bc_amps:.2f}."
    best_info=f"\n\nYour best {number_of_barcodes} barcode options are:\n"
    worst_info=f"\n\nYour worst {number_of_barcodes} barcode options are:\n"

    to_write=line_1 + line_2

    if best_worst_barcodes == True:
        to_write=to_write + best_info + best

    analysis_file=open(f"amp_analysis_{gene}_{polymerase}.txt", "w")
    analysis_file.writelines(list_to_write)
    analysis_file.close()


# saves plot as you'd imagine
def save_plot_png(amp_csv, gene, polymerase='all'):
    plot=plot_barcode_success_rate(amp_csv, gene, polymerase)
    plt.savefig(f'barcode_success_graph_for_{gene}_{polymerase}.png')





# function to remove first line and make sequence one string
def tidy(sequence_file):
    lines=sequence_file.readlines()
    remove_first_line=lines[1:]
    remove_new_lines=[item[0:-2] for item in remove_first_line]
    tidied_sequence=''.join(remove_new_lines)
    return tidied_sequence



# function to find the forward primer and trim x basepairs upstream then the reverse and trim y basepairs downstream
# three different options for primers since HLA is v polymorphic and the likelihood of every sequence matching one primer is relatively low
def trim(tidied_sequence, number_of_extra_bps_upstream, number_of_extra_bps_downstream, sequence_name, forward_primer_option1, forward_primer_option2, forward_primer_option3, reverse_primer_complement_option1, reverse_primer_complement_option2, reverse_primer_complement_option3):
    start_position=tidied_sequence.find(forward_primer_option1)
    if start_position == -1:
        start_position=tidied_sequence.find(forward_primer_option2)
        if start_position == -1:
            start_position=tidied_sequence.find(forward_primer_option3)
    end_position=(tidied_sequence.find(reverse_primer_complement_option1))
    if end_position == -1:
        end_position=(tidied_sequence.find(
            reverse_primer_complement_option2)) + len(reverse_primer_complement_option2)
    else: end_position=(tidied_sequence.find(reverse_primer_complement_option1)) + len(reverse_primer_complement_option1)
    end_position += len(reverse_primer_complement_option1)
    if len(tidied_sequence[end_position:]) >= number_of_extra_bps_downstream:
        trim_off_end_part=tidied_sequence[:(
            end_position + number_of_extra_bps_downstream)]
    else:
        trim_off_end_part=tidied_sequence
    if len(tidied_sequence[:start_position]) >= number_of_extra_bps_upstream:
        trimmed_sequence=trim_off_end_part[(
            start_position - number_of_extra_bps_upstream):]
    else:
        trimmed_sequence=trim_off_end_part
    trimmed_sequence_length=len(trimmed_sequence)
    if trimmed_sequence_length == 0:
        print(
            f"Trimming failed for {sequence_name}, sequence likely doesn't contain a version of the forward and/or reverse primer.")
    return trimmed_sequence


# function to save new file with descriptive header ready for MAFFT
def save(folder, trimmed_sequence, sequence_name):
    file_name=sequence_name + "_trimmed.txt"
    top_line=f">{sequence_name}_trimmed\n"

    # saves it within the same folder as the input local sequence files
    with open(f"{folder}/{file_name}", 'w') as new_file:
        new_file.writelines([top_line, trimmed_sequence])



# function to combine tidy, trim and save to a given .txt file
def tidy_trim_save(folder, sequence_txt_file, number_of_extra_bps_upstream, number_of_extra_bps_downstream, forward_primer_option1, forward_primer_option2, forward_primer_option3, reverse_primer_complement_option1, reverse_primer_complement_option2, reverse_primer_complement_option3):

    with open(f"{folder}/{sequence_txt_file}") as sequence_file:

        sequence_name=sequence_txt_file[:-4]  # aka removing .txt from the end

        # using functions
        tidied_sequence=tidy(sequence_file)

        trimmed_sequence=trim(tidied_sequence, number_of_extra_bps_upstream, number_of_extra_bps_downstream, sequence_name, forward_primer_option1,
                              forward_primer_option2, forward_primer_option3, reverse_primer_complement_option1, reverse_primer_complement_option2, reverse_primer_complement_option3)

        save(folder, trimmed_sequence, sequence_name)

        print(f"{sequence_name}.txt exported.")


def make_all_dataframes(typing_report_name, imported_fmp_name, past_log_name):

    # locating files
    log_relative_path="import_files" + "/" + past_log_name
    past_typing_relative_path="import_files" + "/" + imported_fmp_name
    typing_report_relative_path="import_files" + "/" + typing_report_name

    # making pandas dataframe of typing file
    typing_df=pd.read_excel(typing_report_relative_path, index_col=None)
    typing_df['SampleID']=typing_df['SampleID'].astype(str)

    # making a dataframe of only the end of the sheet, to add back on at the end
    start_of_run_metrics_position=-26  #  should be the same everytime
    run_metrics_df=typing_df[start_of_run_metrics_position:]
    run_metrics_df=run_metrics_df.fillna('')

    # this will delete any rows without info for Barcode or Num reads - ie blank rows and all the info at the bottom of the sheet
    typing_df=typing_df[:-28]
    typing_df.dropna(subset=['Barcode', 'NumReads'], inplace=True)

    # making pandas DF of log of past uploads. This has barcode, cDNA, gDNA suggested ANRI code and reasons (should change suggested to submitted anri code?)
    past_log=pd.read_csv(log_relative_path)
    past_log['SampleID']=past_log['SampleID'].astype(str)


    # making pandas dataframe of imported_fmp_types file
    fmp_raw=pd.read_csv(past_typing_relative_path)
    fmp_raw['sampleID']=fmp_raw['sampleID'].astype(str)
    cohort_1_list=fmp_raw['sampleID'].to_list()
    fmp_raw=fmp_raw.set_index('sampleID')


    return typing_df, run_metrics_df, fmp_raw, past_log


def novels_in_upload(typing_df):

        # for making a list later on
        # then use this to check if a sample is confirmed by another sample in the typing file
        drop_not_novel=typing_df.dropna(
            subset=['MismatchDesc_cDNA', 'MismatchDesc_gDNA'], how='all')
        filling_na=drop_not_novel.fillna('empty')
        novs=filling_na.groupby(['Allele_cDNA', 'MismatchDesc_cDNA', 'Allele_gDNA',
                                'MismatchDesc_gDNA']).SampleID.agg(['count']).reset_index()

        # making a list
        novs=novs[novs['count'] > 1]
        novs_list=novs.values.tolist()

        return novs_list




def edit_imported_typing_file(dataframe, fmp_raw, past_log_raw, list_of_novels, row_counts):

        past_log_no_nan=past_log_raw.fillna('empty')

        # sets off all the new columns in one go
        dataframe['Automated_Quality_Checks']=dataframe.apply(
            quality_check, axis=1)
        dataframe['none_available']=dataframe.apply(none_available, axis=1)
        dataframe=previous_type_match(dataframe, fmp_raw)
        dataframe['perfect_match_to_reference']=dataframe.apply(
            perfect_match_reference, axis=1)
        dataframe=already_accepted(dataframe, past_log_raw)
        dataframe['novel_type']=dataframe.apply(novel_type, axis=1)
        dataframe=alleles_per_sample_count(dataframe, row_counts)
        dataframe['enough_alleles_per_sample']=dataframe.apply(
            too_many_alleles, axis=1)
        dataframe=novel_confirmation(dataframe, past_log_no_nan)

        dataframe['internal_novel_confirmation']=dataframe.apply(
            internal_novel_confirmation, axis=1)
        dataframe[['ANRI_code', 'manual_check_importance', 'ANRI_comment']
            ]=dataframe.apply(ANRI_code_and_comment, axis=1)


        return dataframe


def save_file(edited_typing_df, run_metrics_df, typing_report_name):


    # concatenating the typing bit with the run metrics
    edited_typing_df=edited_typing_df.append(pd.Series(), ignore_index=True)
    edited_typing_df=edited_typing_df.append(pd.Series(), ignore_index=True)
    entire_analysis=pd.concat([edited_typing_df, run_metrics_df])


    # saving 1) the entire analysis and 2) a typing report with suggestions

    # columns we dont want in the typing report
    # we are just keeping the suggested ANRI, manual check importance and reasons why this is suggested
    columns_to_drop=['Automated_Quality_Checks', 'none_available', 'match_previous_type', 'previous_type_zygosity', 'perfect_match_to_reference',
        'already_accepted', 'novel_type', 'alleles_per_sample', 'enough_alleles_per_sample', 'novel_confirmation', 'internal_novel_confirmation']
    typing_report_edited=entire_analysis.drop(columns_to_drop, axis=1)

    # sorting out what we're naming the files
    no_end_name=typing_report_name[:-4]
    edited_typing_report_name=f"{no_end_name}_typing_report.csv"
    entire_analysis_name=f"{no_end_name}_entire_analysis.csv"

    # saving
    typing_report_edited.to_csv(edited_typing_report_name, index=False)
    entire_analysis.to_csv(entire_analysis_name, index=False)
