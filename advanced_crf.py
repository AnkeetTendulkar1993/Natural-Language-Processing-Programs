'''
Name: Ankeet Tendulkar
CSCI 544 Assignment 3
'''

import sys
import glob
import os
from hw3_corpus_tool import get_utterances_from_filename
import pycrfsuite

def convertToBigrams(tokens):
    listOfBigrams = []
    if(len(tokens) > 1):
        for i in range(0,(len(tokens) - 1)):
            listOfBigrams.append(tokens[i] + "_" + tokens[i+1])
    return listOfBigrams

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

    featureVectorOuter = []
    testLabel = []

    listOfUtterances,fileNames = iterateThroughAllFiles(directoryPath)

    for eachDialog in listOfUtterances:

        beginningOfDialog = '1'
        for eachUtterance in eachDialog:
            featureVector = []

            if beginningOfDialog == '1':
                featureVector.append('1')
                featureVector.append('0') #speaker changed or not
                beginningOfDialog = '0'
            else:
                featureVector.append('0')
                if eachUtterance[1] == prevSpeaker:
                    featureVector.append('0')
                else:
                    featureVector.append('1')

            prevSpeaker = eachUtterance[1]

            if(eachUtterance[2] is not None):
                tokensForFeature = []
                tokens = []
                pos = []
                for i in range(0,len(eachUtterance[2])):
                    tokens.append("Token_" + eachUtterance[2][i][0])
                    pos.append("POS_" + eachUtterance[2][i][1])
                    tokensForFeature.append(eachUtterance[2][i][0])

            if(eachUtterance[0] is not None):
                testLabel.append(eachUtterance[0])

            if(eachUtterance[2] is not None):
                featureVector.extend(tokens)
                featureVector.extend(pos)

                bigrams = convertToBigrams(tokensForFeature)
                featureVector.extend(bigrams)

            #print(featureVector)
            featureVectorOuter.append(featureVector)
    return featureVectorOuter,testLabel,fileNames

xsequence,ysequence,fileNamesTrain = process(sys.argv[1])

trainer = pycrfsuite.Trainer(verbose=False)

trainer.append(xsequence, ysequence)

trainer.set_params({
    'c1': 1.0,   # coefficient for L1 penalty
    'c2': 1e-3,  # coefficient for L2 penalty
    'max_iterations': 100,  # stop earlier

    # include transitions that are possible, but not observed
    'feature.possible_transitions': True
})

trainer.train('modelAdvanced.crfsuite')

print("Training Done...")

tagger = pycrfsuite.Tagger()
tagger.open('modelAdvanced.crfsuite')

xtest,ytest,fileNamesTest = process(sys.argv[2])

predictedLabels = tagger.tag(xtest)

count = 0
f = open(sys.argv[3],'w', encoding = 'latin1')
for i in range(0,len(xtest)):
    if(xtest[i][0] is '1') and (count < len(fileNamesTest)) :
        if(count != 0):
            f.write("\n")
        f.write("Filename=" + "\"" + fileNamesTest[count] + "\"" + "\n")
        count += 1
        f.write(predictedLabels[i] + "\n")
    else:
        f.write(predictedLabels[i] + "\n")

f.write("\n")
f.close()

print("Done")