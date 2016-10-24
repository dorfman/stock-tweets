#!/usr/bin/python

import sys
from sys import argv

# sys used for command line args
# use:  sys.argv

# correlation algorithm v1
#  author: Ben Carter and Henry Dorfman
#
#  Description:
#  - simple algorithm for assigning weights to words in a sentence
#  - upon user input, will save the correlated weights in a user given file
#
#  - Two run types:
#     - Training Set: input a sentence an expected sentiment score; used for initial word-to-weight training
#     - Sentence Evalutaion: input a sentence get a general sentiment score
#
#  - Correlation File:
#     - will keep a running dictionary of words and their weights
#     - will be updated everytime the user specifies the file, regardless of run type


# check for template correlation file
corChoice = input("Do you want to enter a template correlation file? (Y/N) ")
if (corChoice.capitalize() == "Y"):
   fileName = input("Please enter correlation file name: ")
   corr_template_file = open(fileName, 'r+')





# specify the run type for the program
#  - Training Set (T):
#     - train the correlation template file
#     - in this mode, score is provided by the user
#  - Sentence Evaluation (E):
#     - evaluate a sentence based on the correlation file
#     - in this mode, score is calculated by the algorithm updated by training sets
print ("Please select a run type\n - Training Set [T]\n - Sentence Evaluation [E]")
runChoice = input("Enter a choice (T/E): ")

while (runChoice[0].capitalize() != "T" and runChoice[0].capitalize() != "E"):
   print ("\nPlease select a run type\n - Training Set [T]\n - Sentence Evaluation [E]")
   runChoice = input("Enter a choice (T/E): ")

if (runChoice[0].capitalize() == "T"):
   print ("\n*** running in Training Set Mode ***\n")
elif (runChoice[0].capitalize() == "E"):
   print ("\n*** running in Sentence Evaluation Mode ***\n")


# correlation code
choice = input("correlate a sentence? (Y/N) ")

while (choice.capitalize() == 'Y'):
   # grab and parse the sentence
   sentence = input("Enter a sentence of max 10 words: ")

   words = sentence.split()
	for word in words:
      print (word)

    print()

   # evaluate the list of words based on given score
   score = input("Enter an associated sentiment score: ")

###
#  TO DO: - code the trainer and evaluator

   choice = input("correlate another sentence? (Y/N) ")

print ("Now exiting...")

if (corChoice.capitalize == "Y"):
   corr_template_file.close()

print ("Goodbye")

