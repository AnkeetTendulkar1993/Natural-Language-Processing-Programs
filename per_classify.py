'''
Name: Ankeet Tendulkar
CSCI 544 Assignment 2
'''

import sys
import fnmatch
import os
import pickle

emailDict = {}

def recursionThroughFiles(mainFolderPath,weightDict):
    numberOfSpamEmails = 0
    numberOfHamEmails = 0
    outputFile = open(sys.argv[2],'w',encoding = 'latin1')
    
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
            
                label = findClassification(textFilePath,weightDict)
                outputFile.write(label + " " + textFilePath + "\n")                
            except:
                print("There is some issue....") 
    outputFile.close()       
    return str(numberOfSpamEmails) + " " + str(numberOfHamEmails)

# Classification of the test file
def findClassification(individualTextFile,weightDict):

    alpha = 0;    
    # List consisting of words from email
    email = emailDict[individualTextFile]
    
    for word in email:
        alpha += weightDict[word]
        
    alpha += weightDict['valueOfTheBias']
    
    if alpha > 0:
        label = "spam"
    else:
        label = "ham"            
    return label   

# Function to start the process
def startIterations():
    try:
        with open('per_model.txt', 'rb') as handle: 
            weightDict = pickle.load(handle)
        # Creating a list of files and dictionary
        numberOfEmails = recursionThroughFiles(sys.argv[1],weightDict).split()    
        
    except:
        print("There was some issue....")    

# Start classification process    
startIterations()
print("Done....")