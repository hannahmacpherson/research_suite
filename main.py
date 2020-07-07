import sys
from utils.utils import trim, trim_2
from utils.barcode_report import barcode_report
from utils.primer_finder_trimmer import primer_finder_timmer
from utils.typing_report_analyser import typing_report_analyser
import argparse
import logging

# This just makes the output look nice
# Read here for better explanation: https://realpython.com/python-logging/

logging.basicConfig(format='%(asctime)s - %(message)s', level=logging.INFO)

main_parser = argparse.ArgumentParser(
    description="Hannah's helper suite!")

subparsers = main_parser.add_subparsers(title="tool_to_use", dest="cur_tool",
                                        help="Choose what analysis tool to use [seq_trim]")

seq_trim_sub = subparsers.add_parser('seq_trim', help="Trim sequence!")
bc_eval_sub = subparsers.add_parser('bc_eval', help="Evaluate barcodes")
primer_trimmer_sub = subparsers.add_parser('prim_trim', help="Trim primers")
typing_analyser_sub = subparsers.add_parser(
    'typing_analyser', help="Analyse typing report")


seq_trim_sub.add_argument('-s', '--start', type=int,
                          required=True, help="Only non-negative numbers please")

seq_trim_sub.add_argument('-e', '--end', type=int,
                          required=True, help="Only non-negative numbers please")

seq_trim_sub.add_argument('-f', '--file', type=str,
                          required=True, help="Path to input file")

bc_eval_sub.add_argument('-a', '--ampcsv', type=str,
                         required=True, help="csv file")

bc_eval_sub.add_argument('-g', '--gene', type=str,
                         required=True, help="gene")

bc_eval_sub.add_argument('-p', '--polymerase', type=str,
                         required=False, help="polymerase")


args = main_parser.parse_args()


def main():
    if args.cur_tool == "seq_trim":
        trim_2(args.start, args.end, args.file)
    elif args.cur_tool = "bc_eval":
        barcode_report(args.ampcsv, args.gene, args.polymerase)
    elif args.cur_tool = "primer_trimmer_sub":
        primer_finder_timmer()
    elif args.cur_tool = "typing_report_analyser":
        typing_report_analyser()
    else:
        print("Incorrect tool requested!")


# inputting from the terminal. Stopping it from working if you don't add the right number of inputs
if __name__ == "__main__":
    main()
