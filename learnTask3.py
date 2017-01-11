'''
Name: Ankeet Tendulkar
CSCI 544 Assignment 1
'''

import sys;
import fnmatch
import os
from string import punctuation

# Dictionary of dictionary
dictOuter = {}

# Enhancement Task 3
# Purpose is to remove the unnecessary punctuation marks and common words

punctuation = {'!','@','#','$','%','^','&','*','(',')','-','+','_','=','{','}','|','\\','[',']',':','"',';','\'',',','.','<','>','?','/','~','`'}
commonWords = {'a','A','the','The','THE', 'and', 'And', 'or', 'Or','if', 'If', 'IF', 'else', 'Else', 'ELSE', 'then', 'Then', 'THEN'}

def storeEmailSpam(textFilePath):
    file = open(textFilePath, "r", encoding = 'latin1')
    s = file.readlines();
    for i in range(0, len(s)):
        listInner = []
        listInner = s[i].split()
        for word in listInner:
            if (word not in punctuation) and (word not in commonWords):
            # if the word is present in the vocabulary
                if word in dictOuter:
                    temp = dictOuter[word]
                    # if that word has a key named spam
                    if 'spam' in temp:
                        dictOuter[word]['spam'] += 1
                    else:
                        dictOuter[word]['spam'] = 1
                else:
                    # The word is not present in vocabulary
                    dictOuter[word] = {}
                    dictOuter[word]['spam'] = 1
    return    

def storeEmailHam(textFilePath):
    file = open(textFilePath, "r", encoding = 'latin1')
    s = file.readlines();
    for i in range(0, len(s)):
        listInner = []
        listInner = s[i].split()
        for word in listInner:
            if (word not in punctuation) and (word not in commonWords):
                # if the word is present in the vocabulary
                if word in dictOuter:
                    temp = dictOuter[word]
                    # if that word has a key named spam
                    if 'ham' in temp:
                        dictOuter[word]['ham'] += 1
                    else:
                        dictOuter[word]['ham'] = 1
                else:
                    # The word is not present in vocabulary
                    dictOuter[word] = {}
                    dictOuter[word]['ham'] = 1 
    return    
       
def recursionThroughFiles(mainFolderPath):
    numberOfSpamEmails = 0
    numberOfHamEmails = 0
    for baseFolder, folderNames, nameOfFiles in os.walk(mainFolderPath):
        for textFileName in fnmatch.filter(nameOfFiles, '*.txt'):
            # Split the path to get the last directory 
            e = baseFolder.split("/")
            #e = baseFolder.split("\\")
            folderType = e[len(e) - 1]
            textFilePath = baseFolder + '/' + os.path.join(textFileName)
            #textFilePath = baseFolder + '\\' + os.path.join(textFileName)
            if folderType.lower() == "spam":
                storeEmailSpam(textFilePath)
                numberOfSpamEmails += 1
            if folderType.lower() == "ham":
                storeEmailHam(textFilePath)
                numberOfHamEmails += 1        
    return str(numberOfSpamEmails) + " " + str(numberOfHamEmails)

numberOfEmails = recursionThroughFiles(sys.argv[1]).split()
#numberOfEmails = recursionThroughFiles("C:\\Users\\Ankeet Tendulkar\\Documents\\CSCI544\\Spam or Ham\\train").split()
numberOfSpamEmails = int(numberOfEmails[0])
numberOfHamEmails = int(numberOfEmails[1])

print("Stored vocabulary in dictionary....")

totalEmails = numberOfSpamEmails + numberOfHamEmails
print("Total Emails = {}".format(totalEmails))
print("Total Spam = {}".format(numberOfSpamEmails))
print("Total Ham = {}".format(numberOfHamEmails))

probabilityOfSpam = float(numberOfSpamEmails)/float(totalEmails)
probabilityOfHam = float(numberOfHamEmails)/float(totalEmails)
vocabularySize = len(dictOuter)
numberOfSpamWords = 0
numberOfHamWords = 0

for key,val in dictOuter.items():
    for innerKey,innerVal in val.items():
        if innerKey == 'spam':
            numberOfSpamWords += innerVal
        if innerKey == 'ham':
            numberOfHamWords += innerVal

output = open('nbmodel3.txt', 'w', encoding = 'latin1')
output.write(str("probabilityOfSpam {}\n".format(probabilityOfSpam)))
output.write(str("probabilityOfHam {}\n".format(probabilityOfHam)))
 
for key,val in dictOuter.items():
    res = key
    if 'spam' not in val:
        val['spam'] = 0
    if 'ham' not in val:
        val['ham'] = 0   
    for type,value in val.items():
        if type == 'spam':
            pWordSpam = (float(value) + 1.0)/(float(numberOfSpamWords) + float(vocabularySize))
            res += " " + type + " " + str(pWordSpam)
        if type == 'ham':
            pWordHam = (float(value) + 1.0)/(float(numberOfHamWords) + float(vocabularySize))
            res += " " + type + " " + str(pWordHam)
    output.write(res + "\n")    

output.close()
print("Completed....")            
# #if __name__ == "__main__": main()