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
                    print("There is some issue....")
    return str(probabilityEmailGivenSpam) + " " + str(probabilityEmailGivenHam)        
    
    
def recursionThroughFiles(mainFolderPath):
    convertFileToDictionary()
    output = open('nboutput1.txt', 'w', encoding = 'latin1') # Part 1
    #output = open('nboutput2.txt', 'w', encoding = 'latin1') # Part 2
    #output = open('nboutput3.txt', 'w', encoding = 'latin1') # Part 3
    print("Recursing through all the files.....")
    for baseFolder, folderNames, nameOfFiles in os.walk(mainFolderPath):
        for textFileName in fnmatch.filter(nameOfFiles, '*.txt'):
            # Split the path to get the last directory 
            #textFilePath = baseFolder + '/' + os.path.join(textFileName)
            #e = baseFolder.split("\\")
            e = baseFolder.split("/")
            folderType = e[len(e) - 1]
            #textFilePath = baseFolder + '\\' + os.path.join(textFileName)
            textFilePath = baseFolder + '/' + os.path.join(textFileName)
            values = computeEmailGivenSpamAndHam(textFilePath).split()
            probabilityEmailGivenSpam = float(values[0])
            probabilityEmailGivenHam = float(values[1])
            label = 'NA'
            if probabilityEmailGivenSpam > probabilityEmailGivenHam:
                label = 'spam'
            else:
                label = 'ham' 
            output.write(label + " " + textFilePath + " " + folderType + "\n")
    output.close()
    print("Output file generated.....")
    return

def convertFileToDictionary():
    print("Converting to Dictionary.....")
    file = open('nbmodel.txt', 'r', encoding = 'latin1') #Part 1
    #file = open('nbmodel2.txt', 'r', encoding = 'latin1') # Part 2
    #file = open('nbmodel3.txt', 'r', encoding = 'latin1') # Part 3
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
#recursionThroughFiles("C:\\Users\\Ankeet Tendulkar\\Documents\\CSCI544\\SpamorHam\\dev")

def calculatePrecisionRecallF1Score():
    outFile = open('nboutput1.txt','r', encoding='latin1') # Part 1
    #outFile = open('nboutput2.txt','r', encoding='latin1') # Part 2
    #outFile = open('nboutput3.txt','r', encoding='latin1') # Part 3
    correctClassSpam = 0
    correctClassHam = 0
    totalClassifySpam = 0
    totalClassifyHam = 0
    belongsInSpam = 0
    belongsInHam = 0
    
    precisionSpam = 0.0
    precisionHam = 0.0
    recallSpam = 0.0
    recallHam = 0.0
    F1Spam = 0.0
    F1Ham = 0.0    
     
    for eachLine in outFile:
        temp = eachLine.split()
        classification = temp[0]
        tem = temp[len(temp) - 1]
        fileName = tem.lower()

        if classification == fileName:           
            if classification.lower() == 'spam':
                correctClassSpam += 1
            if classification.lower() == 'ham':
                correctClassHam += 1
        if classification.lower() == 'spam':
            totalClassifySpam += 1       
        if classification.lower() == 'ham':
            totalClassifyHam += 1
        if 'spam' == fileName.lower():
            belongsInSpam += 1
        if 'ham' == fileName.lower():
            belongsInHam += 1
        
#     print("Correct class Spam = {}".format(correctClassSpam))        
#     print("Correct class Ham = {}".format(correctClassHam))
#     print("Total classify Spam = {}".format(totalClassifySpam))
#     print("Total classify Ham = {}".format(totalClassifyHam))
#     print("Total belongs to class Spam = {}".format(belongsInSpam))
#     print("Total belongs to  class Ham = {}".format(belongsInHam)) 
     
    try:
        precisionSpam = float(correctClassSpam)/float(totalClassifySpam)               
        precisionHam = float(correctClassHam)/float(totalClassifyHam)
        recallSpam = float(correctClassSpam)/float(belongsInSpam)
        recallHam = float(correctClassHam)/float(belongsInHam)
        F1Spam = (2.0 * float(precisionSpam) * float(recallSpam)) / (float(precisionSpam) + float(recallSpam))       
        F1Ham = (2.0 * float(precisionHam) * float(recallHam)) / (float(precisionHam) + float(recallHam))
    except:
        print("There is some issue....")
        
    print("Precision Spam = {}".format(precisionSpam))
    print("Precision Ham = {}".format(precisionHam))
    print("Recall Spam = {}".format(recallSpam))
    print("Recall Ham = {}".format(recallHam))
    print("F1 Spam = {}".format(F1Spam))
    print("F1 Ham = {}".format(F1Ham))
    
    outFile.close()       

calculatePrecisionRecallF1Score()                    