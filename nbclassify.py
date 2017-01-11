'''
Name: Ankeet Tendulkar
CSCI 544 Assignment 1
'''
import fnmatch
import os
import math
import sys

dataDictionary = {} 
  
def computeEmailGivenSpamAndHam(filePath):
    file = open(filePath, 'r', encoding = 'latin1')
    s = file.readlines()
    probabilityEmailGivenSpam = 0
    probabilityEmailGivenHam = 0
    for i in range(0, len(s)):
        listLine = []
        listLine = s[i].split()
        for word in listLine:
            if word in dataDictionary:
                try:
                    probabilityEmailGivenSpam += math.log(float(dataDictionary[word]['spam'])) # Spam
                    probabilityEmailGivenHam += math.log(float(dataDictionary[word]['ham'])) # Ham
                except:
                    probabilityEmailGivenSpam = 0.5
                    probabilityEmailGivenHam = 0.5
                    print("There is some issue....")
    
    return str(probabilityEmailGivenSpam) + " " + str(probabilityEmailGivenHam)        
    
    
def recursionThroughFiles(mainFolderPath):
    convertFileToDictionary()
    output = open('nboutput.txt', 'w', encoding = 'latin1')
    print("Recursing through all the files.....")
    for baseFolder, folderNames, nameOfFiles in os.walk(mainFolderPath):
        for textFileName in fnmatch.filter(nameOfFiles, '*.txt'):
            # Split the path to get the last directory 
            textFilePath = baseFolder + '/' + os.path.join(textFileName)
            #textFilePath = baseFolder + '\\' + os.path.join(textFileName)
            values = computeEmailGivenSpamAndHam(textFilePath).split()
            probabilityEmailGivenSpam = float(values[0])
            probabilityEmailGivenHam = float(values[1])
            label = 'NA'
            if probabilityEmailGivenSpam > probabilityEmailGivenHam:
                label = 'spam'
            else:
                label = 'ham' 
            output.write(label + " " + textFilePath + "\n")
    output.close()
    print("Output file generated.....")
    return

def convertFileToDictionary():
    print("Converting to Dictionary.....")
    file = open('nbmodel.txt', 'r', encoding = 'latin1')
    parameterFile = file.readlines()
    for eachLine in parameterFile:
        lineList = eachLine.split()
        if lineList[0] == 'probabilityOfSpam' or lineList[0] == 'probabilityOfHam':
            dataDictionary[lineList[0]] = float(lineList[1])
        else:    
            key = lineList[0]
            dict = {str(lineList[1]) : lineList[2], lineList[3] : lineList[4]}
            dataDictionary[key] = dict
    #print("Size of dictionary = {}".format(len(dataDictionary))) 
               
recursionThroughFiles(sys.argv[1])
#recursionThroughFiles("C:\\Users\\Ankeet Tendulkar\\Documents\\CSCI544\\Spam or Ham\\dev")