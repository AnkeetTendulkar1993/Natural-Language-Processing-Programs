'''
Name: Ankeet Tendulkar
CSCI 544 Assignment 3
'''

import sys
import os
import glob
from hw3_corpus_tool import get_utterances_from_filename

def getFileName(pathOfFile):
    newPath = os.path.abspath(pathOfFile)
    head,csvFileName = os.path.split(newPath)
    return csvFileName

def iterateThroughAllFiles(directoryPath):
    formattedData = []
    namesOfFiles = []
    dialog_filenames = sorted(glob.glob(os.path.join(directoryPath, "*.csv")))
    for dialog_filename in dialog_filenames:
        formattedData.append(get_utterances_from_filename(dialog_filename))
        namesOfFiles.append(getFileName(dialog_filename))
    return formattedData,namesOfFiles

def process(directoryPath):
    correctLabels = []
    listOfUtterances,fileNames = iterateThroughAllFiles(directoryPath)
    for eachDialog in listOfUtterances:
        for eachUtterance in eachDialog:
            correctLabels.append(eachUtterance[0])
    return correctLabels

predictedLabels = []
f = open(sys.argv[2])
lines = f.readlines()
for i in range(0,len(lines)):
    if((not lines[i].startswith("Filename=")) and (not lines[i] == "\n")):
        predictedLabels.append(lines[i].strip())

correctLabels = process(sys.argv[1])

count = 0
for i in range(0,len(predictedLabels)):
    if (correctLabels[i] == predictedLabels[i]):
        count += 1

print("Number of correct labels = {}/{}".format(count,len(correctLabels)))
accuracy = (float(count)/float(len(correctLabels))) * 100
print("Accuracy = {}".format(accuracy))
