'''
Name: Ankeet Tendulkar
CSCI 544 Assignment 2
'''

import fnmatch
import os
import math
import sys
import pickle

dataDictionary = {} 
  
def calculatePrecisionRecallF1Score():
    #with open('per_model.txt', 'rb') as handle: 
    #        weightDict = pickle.load(handle)
    
    # Based on name of output file    
    outFile = open(sys.argv[1],'r', encoding='latin1') # Part 1
    
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
        
        # Split the filepath to get the name of the folder        
        if "\\" in tem:
            fileN = tem.split("\\")
        if "/" in tem:
            fileN = tem.split("/")
        fileName = fileN[len(fileN) - 2]        
        
        if classification.lower() == fileName.lower():           
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
        try:
            precisionSpam = float(correctClassSpam)/float(totalClassifySpam)
        except Exception as e:
            print("precisionSpam = {}".format(e))
            precisionSpam = 0.0
        try:                       
            precisionHam = float(correctClassHam)/float(totalClassifyHam)
        except Exception as e:
            print("precisionHam = {}".format(e))
            precisionHam = 0.0
        try:
            recallSpam = float(correctClassSpam)/float(belongsInSpam)
        except Exception as e:
            print("recallSpam = {}".format(e))
            recallSpam = 0.0            
        try:
            recallHam = float(correctClassHam)/float(belongsInHam)
        except Exception as e:
            print("recallHam = {}".format(e))
            recallHam = 0.0
        try:
            F1Spam = (2.0 * float(precisionSpam) * float(recallSpam)) / (float(precisionSpam) + float(recallSpam))       
        except Exception as e:
            print("F1Spam = {}".format(e))
            F1Spam = 0.0
        try:
            F1Ham = (2.0 * float(precisionHam) * float(recallHam)) / (float(precisionHam) + float(recallHam))
        except Exception as e:
            print("F1Ham = {}".format(e))
            F1Ham = 0.0
    except:
        print("There is some issue....")
    
    print("-------------------------------------------------")    
    print("Precision Spam = {}".format(precisionSpam))
    print("Precision Ham = {}".format(precisionHam))
    print("Recall Spam = {}".format(recallSpam))
    print("Recall Ham = {}".format(recallHam))
    print("F1 Spam = {}".format(F1Spam))
    print("F1 Ham = {}".format(F1Ham))
    print("-------------------------------------------------")
    
    outFile.close()       

calculatePrecisionRecallF1Score()                    