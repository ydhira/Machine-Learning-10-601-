import ast
import os
import math
import sys 

    

#Reads from the quantized train data
#Adds the data into the dictionary
#returns (x,y,z)
#x is the dict of the Quantized training data
#y is the dict of the counts of each years
#z is the total count of the instances 

def makingDicts():
    noFeatures = 90
    N = 16
    mleDict = {}
    mleYearCount = {}
    fileo = open('QuantizedTrainData.txt', 'r')

    count = 0
    limit=0
    
    for line in fileo:
        
        listQ = ast.literal_eval(line)
        year = int(listQ[0])
        listQ = listQ[1:]
        if year not in mleDict.keys():
            featureK = []
            
            for i in range(noFeatures):
                l = []
                for j in range(N):
                    l.append(0)
                featureK.append(l)
            
            mleDict[year] = featureK
            mleYearCount[year] = 1
            
        else:
             mleYearCount[year] += 1
             
        for i in range(noFeatures):
            fValue = int(listQ[i])
            mleDict[year][i][fValue] += 1

        count += 1
            

        
    #print mleDict
    return (mleDict, mleYearCount, count)

# gets the dict of the quantized train data.
# converts the dict into the probabilities
# using the MAximum Likelihood estimate
# writes into every file

def mle():

    mleDict, mleYearCount, count = makingDicts()
    yearProb = []
    
    for yearKey in mleDict.keys():
        Nc = mleYearCount[yearKey]
        yearProb.append(float(Nc) / float(count))
        tableV = mleDict[yearKey]
        mleDict[yearKey] = [map(lambda elem:float(elem)/float(Nc), x) for x in tableV]
    

    fileo = open('mle/yearProb.txt', 'w')
    fileo.write(str(yearProb))
    fileo.close()
    for yearKey in mleDict.keys():
        fileYear = open('mle/'+str(yearKey)+'.txt', 'w')
        for f in mleDict[yearKey]:
            fileYear.write(str(f))
            fileYear.write("\n")
        fileYear.close()

# gets the dict of the quantized train data.
# converts the dict into the probabilities
# using the Maximum aposteriori procedure 
# writes into every file

def mpostp():
    
    mleDict, mleYearCount, count = makingDicts()

    for yearKey in mleDict.keys():
        
        tableV = mleDict[yearKey]
        mleDict[yearKey] = [map(lambda elem:(float(elem) + (float(1)/float(16))), x) for x in tableV]

        tableV = mleDict[yearKey]
        deno = float(sum(tableV[0]))
        mleDict[yearKey] = [map(lambda elem:(float(elem)/float(deno)), x) for x in tableV]

        fileYear = open('map/'+str(yearKey)+'.txt', 'w')
        for f in mleDict[yearKey]:
            fileYear.write(str(f))
            fileYear.write("\n")
        fileYear.close()

# opens the mle or map files of every year
# gets the prediction of every year
# and predicts the year withe maximum value
# writes theconfusion matrix in the file

def predict(dirName):
    
    #testYears = []
    uniqueYears = [1991, 1992, 1993, 1994, 1995, 1996, 1997, 1998, 1999,
                   2000, 2001, 2002, 2003, 2004, 2005, 2006, 2007, 2008,
                   2009, 2010]
    myDict = {}
    
    
    index = 0
    for file in os.listdir(dirName):
        if (file != 'yearProb.txt' and file!= 'confusionMatrix.txt'):
            year = 0
            tableYear = []
            
            filek = open(dirName + "/"+file, 'r')
            for line in filek:
                featureK = ast.literal_eval(line)
                tableYear.append(featureK)
            myDict[uniqueYears[index]] = tableYear

            filek.close()
                
            index += 1
    
    yearProb = []
    confusionMatrix = []
    for i in range (20):
        l = []
        for j in range(20):
            l.append(0)
        confusionMatrix.append(l)
    
    filey = open('mle/yearProb.txt', 'r')
    for line in filey:
        yearProb = ast.literal_eval(line)

    #print type(yearProb[0])
    filey.close()
    nolines = 0
    fileo = open('QuantizedTestData2.txt', 'r')
    fileCOM = open("MLEPredictedYearComparison.txt", "w")
    topTen = [0,1,2,3,4,5,6,19,21,45]
    for line in fileo:
        listQ = ast.literal_eval(line)
        yearKey = int(listQ[0])

        listQ = listQ[1:]

        count = 0
        predictedYears = []

        for i in uniqueYears:
            C = float(0)
            for k in topTen:
            #for k in range (90):
                if (myDict[i][k][listQ[k]] != float(0)):
                    
                    C += (float(math.log(float(myDict[i][k][listQ[k]]), 2)))
                            
            C += (float(math.log(float(yearProb[count]), 2)))
            predictedYears.append(C)
            count += 1
        maxI=float(-sys.maxint)
        maxIndex = 0
        for i in range(len(predictedYears)):
            if (predictedYears[i] > maxI):
                maxI = predictedYears[i]
                maxIndex = i

        confusionMatrix[maxIndex][uniqueYears.index(yearKey)] += 1
        
        fileCOM.write(str(yearKey) + "," + str(uniqueYears[maxIndex]))
        fileCOM.write("\n")
        
    fileCOM.close()
    fileo.close()

    filep = open(dirName+'/confusionMatrix.txt', 'w')
    for l in confusionMatrix:
        filep.write(str(l))
        filep.write("\n")
        
    filep.close()
    return

# opens the confusion matrix and calctaes the accuracy
def calculateAcc(fileName):
    
    fileo = open(fileName, 'r')
    
    confTable = []
    for line in fileo:
        listQ = ast.literal_eval(line)
        confTable.append(listQ)

    fileo.close()
    count =0
    total = 0
    for i in range (20):
        count += int(confTable[i][i])
        total += sum(confTable[i])
    print "accuracy for " +fileName+" is " ,  float(count)/float(total) * 100 , "%"
    
#makingDicts()
#mle()    
#mpostp()
predict('map')
calculateAcc('map/confusionMatrix.txt')
