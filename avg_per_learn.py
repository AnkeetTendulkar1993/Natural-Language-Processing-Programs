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

emailDict = {}
newList = []
bias = 0
# List of filenames
listOfFileNames = []
# Dictionary of dictionary
dictOuter1 = {}
weightDict = defaultdict(int)
averageWeightDict = defaultdict(int)


def storeInWeightDictionary(textFilePath):
    wordsInEmail = emailDict[textFilePath]
    for word in wordsInEmail:
        if word not in weightDict:
            weightDict[word] = {}
            weightDict[word] = 0  
            averageWeightDict = {}
            averageWeightDict = 0          
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
    
                path = os.path.join(baseFolder,textFileName)
                textFilePath = os.path.abspath(path)
                
                file = open(textFilePath,'r', encoding= 'latin1')
                s = file.readlines();
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

# Training perceptron using each file
def trainPerceptron(individualTextFile,bias,c,beta):

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
        # update the weight dictionary
        for eachWord in email:
            weightDict[eachWord] += y
            averageWeightDict[eachWord] += (y * c)
        bias += y
        beta += (y * c)
                
    return bias   


# Function which covers all the iterations
def startIterations():
    try:
        # Creating a list of files and dictionary
        numberOfEmails = recursionThroughFiles(sys.argv[1]).split()
        count = 1
        bias = 0
        c = 1
        beta = 0
        
        # For 30 iterations
        while(count <= 30):
            #print("Iteration {}".format(count))
            random.shuffle(listOfFileNames)
            for eachFile in listOfFileNames:
                bias = trainPerceptron(eachFile,bias,c,beta)
                c += 1
                #print(eachFile)
                #print(weightDict)
                #print(bias)
            count += 1
            
        
        
        for eachWordKey,value in averageWeightDict.items():
            averageWeightDict[eachWordKey] = float(weightDict[eachWordKey]) - (float(1.0/c) * float(averageWeightDict[eachWordKey]))
            
        beta = float(bias) - (float(1.0/float(c)) * float(beta))
        valueOfTheBias = beta
        averageWeightDict['valueOfTheBias'] = valueOfTheBias 
        #print(averageWeightDict) 
        
    except:
        print("There was some issue....")    

# Function to start process    
startIterations()

with open('per_model.txt', 'wb') as handle: 
    pickle.dump(averageWeightDict, handle)
    
print("Model Created....")