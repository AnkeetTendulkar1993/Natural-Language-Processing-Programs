'''
Name: Ankeet Tendulkar
CSCI 544 Assignment 2
'''

import sys
import fnmatch
import os
import random
import pickle
from collections import defaultdict

# Dictionary to store emails
emailDict = {}

# List of filepaths
listOfFileNames = []

# Dictionary of dictionary
dictOuter1 = {}
weightDict = defaultdict(int)

bias = 0

# Create Weight Dictionary 
def storeInWeightDictionary(textFilePath):
    wordsInEmail = emailDict[textFilePath]
    for word in wordsInEmail:
        if word not in weightDict:
            weightDict[word] = {}
            weightDict[word] = 0            
    return

# Creating Email Dictionary and Weight Dictionary
def recursionThroughFiles(mainFolderPath):
    numberOfSpamEmails = 0
    numberOfHamEmails = 0
    for baseFolder, folderNames, nameOfFiles in os.walk(mainFolderPath):
        for textFileName in fnmatch.filter(nameOfFiles, '*.txt'):
            try:
                # Name of base folder
                folderNameSpamOrHam = os.path.basename(baseFolder)
                
                # Creating Absolute path
                path = os.path.join(baseFolder,textFileName)
                textFilePath = os.path.abspath(path)
                #print(textFilePath)
                
                file = open(textFilePath,'r', encoding= 'latin1')
                s = file.readlines();
                
                # Store all the words of an email
                valueList = []
                for i in range(0, len(s)):
                    listInner = []
                    listInner = s[i].split()
                    for word in listInner:
                        valueList.append(word)
                
                emailDict[textFilePath] = valueList        
                           
                if folderNameSpamOrHam.lower() == "spam":
                    innerList = []
                    innerList.append(textFilePath)
                    innerList.append("spam")
                    listOfFileNames.append(innerList)
                    storeInWeightDictionary(textFilePath)
                    numberOfSpamEmails += 1
                    
                if folderNameSpamOrHam.lower() == "ham":
                    innerList = []
                    innerList.append(textFilePath)
                    innerList.append("ham")
                    listOfFileNames.append(innerList)
                    storeInWeightDictionary(textFilePath)
                    numberOfHamEmails += 1
                
            except:
                print("There is some issue....")        
    return str(numberOfSpamEmails) + " " + str(numberOfHamEmails)

# Train perceptron using current email file
def trainPerceptron(individualTextFile,bias):

    alpha = 0;
    
    # List consisting of words from email
    email = emailDict[individualTextFile[0]]
    
    if individualTextFile[1] == "spam":
        y = 1
    if individualTextFile[1] == "ham":
        y = -1

    for word in email:
        alpha += weightDict[word]

    alpha += bias    
    yalpha = y * alpha
    
    if yalpha <= 0:
        # Update weight dictionary and bias
        for eachWord in email:
            weightDict[eachWord] += y
        bias += y
                
    return bias   


# Function which covers all the iterations
def startIterations():
    try:
        # Creating a list of files and dictionary
        numberOfEmails = recursionThroughFiles(sys.argv[1]).split()
        
        count = 1
        bias = 0
        
        # For 20 iterations
        while(count <= 20):
            #print("Iteration {}".format(count))
            random.shuffle(listOfFileNames)
            for eachFile in listOfFileNames:
                bias = trainPerceptron(eachFile,bias)
                #print(eachFile)
                #print(weightDict)
                #print(bias)
            count += 1
            
        valueOfTheBias = bias
        weightDict['valueOfTheBias'] = valueOfTheBias
               
    except:
        print("There was some issue....")    

# Function to start the process    
startIterations()
with open('per_model.txt', 'wb') as handle: 
    pickle.dump(weightDict, handle)
    
print("Model Created....")