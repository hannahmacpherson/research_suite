Hello, this script will chop however much you want off the start and end of each of your sequences and save them to a second file.

-----------------------------------------------

You will need: 

- a plain text .txt file as an input. This can have as many sequences as you want, but they must be in the format suggested in the example file. Each sequence must be headed by a descriptor with a '>' preceeding it.

-----------------------------------------------

What to do:

1) In the terminal, navigate to the folder where you have put both main.py and your input .txt file.

2) Type in what you want in the following way:

python3 trimmer.py bp_off_start bp_off_end input.txt 

-- where bp_off_start is the number of base pairs you want taken off the start and bp_off_end is the number off the end. NB if these add to more than the length of your sequence, you will just end up with no sequence. -- 

So for example, if I want to take 30bp off the start and 20bp off the end of every sequence in ilovegenetics.txt, I would type the following:

python3 trimmer.py 30 20 ilovegenetics.txt 

The script should then confirm what it's done and you should find the file in your folder.


-----------------------------------------------

Hannah 02/06/2020

