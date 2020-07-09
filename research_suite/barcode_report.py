from utils import *
from matplotlib import pyplot as plt

def barcode_report(amp_csv, gene, polymerase="all"):
    
    print("")
    print(f"How many best/worst barcodes do you want to be given in your report?")
    print("")


    # define if you want a certain number of best/worst barcodes in your final report
    number_of_barcodes_valid = False

    while number_of_barcodes_valid == False:
        number_of_barcodes = input()
        try:
            number_of_barcodes = int(number_of_barcodes)
            if number_of_barcodes > -1:
                number_of_barcodes_valid = True
            else: 
                number_of_barcodes_valid = False
                print("Please type a number 0 or above")
        except TypeError:
            print("Please type a number")

    

    print("")
    print(f"Generating full barcode report for {amp_csv} for {gene} for amplifications using {polymerase} polymerase(s)")
    print("")


    # make a dataframe specific to your gene and polymerase (if stated) from your csv file of amps
    amp_dataframe = make_dataframe(amp_csv, gene, polymerase)

    # how many amps are you taking into account in the above dataframe?
    number_of_amps = row_counter(amp_dataframe)

    # what's the mean number of amps per barcode used?
    mean_bc_amps = average_amps_per_barcode(amp_dataframe)

    # create a dataframe of success rate per barcode 
    success_df = barcode_success_rate(amp_dataframe)

    # create a dataframe for best and worst barcodes (unless you wanted 0 in the input above)
    if number_of_barcodes != 0:
        best_worst_barcodes = True
        best_and_worst_barcodes(amp_dataframe, number_of_barcodes)
    else:
        best_worst_barcodes = False


  
    print("##################################")
    print('Start of Report')
    print("##################################")

    print("")
    print(f"Your input {amp_csv} contains {number_of_amps} amplifications specific to {gene} using {polymerase} polymerase(s)")
    print(f"The mean number of amps per barcode is {mean_bc_amps:.2f}")

    if best_worst_barcodes == True:
        print("")
        print("Your best barcode options are:")
        print("")
        best = best_and_worst_barcodes(amp_dataframe, number_of_barcodes)[0]
        print(best)

        print("")
        print("Your worst barcode options are:")
        print("")
        worst = best_and_worst_barcodes(amp_dataframe, number_of_barcodes)[1]
        print(worst)

    print("")
    print("Plotting success rate per barcode...")
    print("")

    # plotting barcode success rates
    plot = plot_barcode_success_rate(amp_csv, gene, polymerase)
    plt.show()

    print("")
    print("")

    print("Would you like a saved csv of your barcodes and their percentage success rates? (Y/N)")
    save_bc_printable = input()
    save_bc_printable = save_bc_printable.lower()
    while save_bc_printable != "y" and save_bc_printable != "n":
        print("Please type Y or N. Would you like a saved csv of your barcodes and their percentage success rates? (Y/N)")
        save_bc_printable = input()
        save_bc_printable = save_bc_printable.lower()
    if save_bc_printable == "y":
        to_save = barcode_success_rate(amp_dataframe)
        save_df_to_csv_tabbed(to_save, gene, polymerase)

    