import ast
import os
import math
import sys
import numpy
from numpy import *

trainDataTable = []
testDataTable = []
trainYears = []
testYears = []

def makeDataMatrix(fileName):
    
    DataTable = []   # e.g 300000 x 1 for train
    fileo = open(fileName, 'r')
    allYears= []
    
    for line in fileo:

        listQ = line.split(',')
        allYears.append(int(listQ[0]))
        listQ = map(lambda x: float(x), listQ)
        listQ = listQ[1:]
        DataTable.append(listQ)

    fileo.close()
    DataTable = matrix(DataTable)
    DataTableArray = array(DataTable)
    #print trainDataTable[0]
    return (DataTableArray, allYears)

#got code from stackoverflow
def MAEaccu(testYears, predicted_years, kernel, K):
    
    mae = numpy.sum(numpy.absolute((numpy.array(testYears) - numpy.array(predicted_years))))
    print "mae accuracy for " + kernel + "  K =  ", K ,"is" , float(mae)/float(len(testYears))

#got code from stackoverflow                    
def RMSEaccu(testYears, predicted_years, kernel, K):
    rmse = numpy.sqrt(((numpy.array(predicted_years) - numpy.array(testYears)) ** 2).mean())  
    print "rmse accuracy for " + kernel + "  K =  ", K ,"is" ,rmse

def uniformKernel(K, trainDataTable, testDataTable,trainYears, testYears, neighboursIndexForAllInstances, distanceForAllInstances):
    
    i = 0
    predicted_years = []
    for testInstance in testDataTable:
        KNearestNeighbours = []
        for k in range(K):
            KNearestNeighbours.append(neighboursIndexForAllInstances[i][k])
            
        year = 0
        for knn in KNearestNeighbours:
            year += trainYears[knn]
        predicted_year = abs(year/K)
        #print predicted_year
        predicted_years.append(predicted_year)
        i += 1
        
    MAEaccu(testYears, predicted_years, "uniformRegression", K)
    RMSEaccu(testYears, predicted_years, "uniformRegression", K)

def uniformKernelClass(K, trainDataTable, testDataTable,trainYears, testYears, neighboursIndexForAllInstances, distanceForAllInstances):
    
    i = 0
    yearScore = {}
    predicted_years = []
    for testInstance in testDataTable:
        KNearestNeighbours = []
        for k in range(K):
            KNearestNeighbours.append(neighboursIndexForAllInstances[i][k])
            
        year = 0
        for knn in KNearestNeighbours:
            if trainYears[knn] in  yearScore:
                yearScore[trainYears[knn]] += 1
            else:
                yearScore[trainYears[knn]]= 1
            
        predicted_year = max(yearScore, key=yearScore.get)
        #print predicted_year
        predicted_years.append(predicted_year)
        i += 1
        
    MAEaccu(testYears, predicted_years, "uniformClassification", K)
    RMSEaccu(testYears, predicted_years, "uniformClassification", K)
        
def inverseDistance(K, trainDataTable, testDataTable,trainYears, testYears, neighboursIndexForAllInstances, distanceForAllInstances):
    
    i = 0
    predicted_years = []
    for testInstance in testDataTable:
        KNearestNeighbours = []
        weights = []
        for k in range(K):
            KNearestNeighbours.append(neighboursIndexForAllInstances[i][k])
            weights.append(1 / float(distanceForAllInstances[i][k]))
        

        year =0
        l = 0
        for j in KNearestNeighbours:
            
            year += (trainYears[j] * weights[l])

            l += 1
        predicted_years.append(abs(year/sum(weights)))

        i +=1
    MAEaccu(testYears, predicted_years, "inverseDistanceRegression", K)
    RMSEaccu(testYears, predicted_years, "inverseDistanceRegression", K)

def inverseDistanceClass(K, trainDataTable, testDataTable,trainYears, testYears, neighboursIndexForAllInstances, distanceForAllInstances):
    
    i = 0
    predicted_years = []
    yearScore = {}
    for testInstance in testDataTable:
        KNearestNeighbours = []
        weights = []
        for k in range(K):
            KNearestNeighbours.append(neighboursIndexForAllInstances[i][k])
            weights.append(1 / float(distanceForAllInstances[i][k]))
        

        year =0
        l = 0
        for j in KNearestNeighbours:
            
            if trainYears[j] in  yearScore:
                yearScore[trainYears[j]] += (trainYears[j] * weights[l])
            else:
                yearScore[trainYears[j]]= (trainYears[j] * weights[l])
            
            #year += (trainYears[j] * weights[l])

            l += 1
            
        predicted_year = max(yearScore, key=yearScore.get)
        #print predicted_year
        predicted_years.append(predicted_year)

        i +=1
    MAEaccu(testYears, predicted_years, "inverseDistanceClass", K)
    RMSEaccu(testYears, predicted_years, "inverseDistanceClass", K)
    
def gausian(K, trainDataTable, validationDataTable ,trainYears, VYears, neighboursIndexForAllInstances, distanceForAllInstances , sigma):

    i = 0
    predicted_years = []
    
    for vInstance in validationDataTable:
        KNearestNeighbours = []
        dist = []
        for k in range(K):
            KNearestNeighbours.append(neighboursIndexForAllInstances[i][k])
            dist.append(float(distanceForAllInstances[i][k]))

        l = 0
        num = 0
        den = 0
        gau = 0
        nearestN = KNearestNeighbours[0]
        for j in KNearestNeighbours:
            powl = ( float(dist[0]) - float(dist[l]) ) / float(sigma ** 2)

            gau = pow(e,(powl))
            num += gau * trainYears[j]
            den += gau
            l+= 1

        predicted_years.append(abs(num/den))
    
        i += 1

    RMSEaccu(VYears, predicted_years, "GausianRegression", K)


def confusionMatrix(testYears, predictedYears):
    #print min(testYears)
    #print max(testYears)
    confusionMatrix = []
    for i in range (20):
        l = []
        for j in range(20):
            l.append(0)
        confusionMatrix.append(l)

    for i in range(len(testYears)):
         #print testYears[i] - 1990
         #print predictedYears[i] - 1990
         confusionMatrix[testYears[i] - 1991][predictedYears[i] - 1991] += 1

            
    filep = open('confusionMatrix.txt', 'w')
    for l in confusionMatrix:
        filep.write(str(l))
        filep.write("\n")
        
    filep.close()
    return    

def gausianClass(K, trainDataTable, validationDataTable ,trainYears, VYears, neighboursIndexForAllInstances, distanceForAllInstances , sigma):

    i = 0
    predicted_years = []
    yearScore = {}
    for vInstance in validationDataTable:
        KNearestNeighbours = []
        dist = []
        for k in range(K):
            KNearestNeighbours.append(neighboursIndexForAllInstances[i][k])
            dist.append(float(distanceForAllInstances[i][k]))

        l = 0
        num = 0
        den = 0
        gau = 0
        nearestN = KNearestNeighbours[0]
        for j in KNearestNeighbours:
            powl = ( float(dist[0]) - float(dist[l]) ) / float(sigma ** 2)

            gau = pow(e,(powl))

                    
            if trainYears[j] in  yearScore:
                yearScore[trainYears[j]] += gau
            else:
                yearScore[trainYears[j]]= gau


            l+= 1

        predicted_year = max(yearScore, key=yearScore.get)
        #print predicted_year
        predicted_years.append(predicted_year)
        
        i += 1

    RMSEaccu(VYears, predicted_years, "GausianClass", K)
    confusionMatrix(VYears, predicted_years)    
    
    
def findDistance(trainDataTable, testDataTable):
    
    trainDataTableSquare = square(trainDataTable)
    fileo = open('top10V.txt','w') # index of smallest elements
    filep = open('DistancesV.txt','w')   #distances of the smallest elements

    for testInstance in testDataTable:

        testInstanceSquare = square(testInstance)
        xxbar = (-2) * numpy.multiply(trainDataTable , transpose(testInstance))
        #print xxbar
        
        x2addxbar2 = numpy.add(trainDataTableSquare, testInstanceSquare)
        dist = numpy.add(x2addxbar2, xxbar)
       
        sum2 = numpy.sum(dist, axis=1)

        tenNeigh = matrix.argsort(sum2)

        tenN = []
        dist = []
        for i in range(10):
           tenN.append(tenNeigh[i])
           dist.append(sum2[tenNeigh[i]])

        fileo.write(str(tenN))
        fileo.write('\n')
        filep.write(str(dist))
        filep.write('\n')

    fileo.close()
    filep.close()

    
    
(trainDataTable, trainYears) = makeDataMatrix('DT_training.txt')
(testDataTable, testYears) = makeDataMatrix('DT_test.txt')
(validationDataTable, validationYears) = makeDataMatrix('DT_validation.txt')

#findDistance(trainDataTable, validationDataTable)

neighboursIndexForAllInstances = []
distanceForAllInstances = []
neighboursIndexForAllInstancesV = []
distanceForAllInstancesV = []

fileo = open('top10.txt','r')
filep = open('Distances.txt', 'r')
fileVtop = open('top10V.txt','r')
fileVDist = open('DistancesV.txt','r')

#10 neighbours for test Data
for line in fileo:

    listQ = ast.literal_eval(line)
    neighboursIndexForAllInstances.append(listQ)
    
fileo.close()

#distances for those neighbours TestData
for line in filep:

    listQ = ast.literal_eval(line)
    distanceForAllInstances.append(listQ)
    
filep.close()

#10 neighbours for validation Data
for line in fileVtop:

    listQ = ast.literal_eval(line)
    neighboursIndexForAllInstancesV.append(listQ)
    
fileVtop.close()

#distances for those neighbours ValidationData
for line in fileVDist:

    listQ = ast.literal_eval(line)
    distanceForAllInstancesV.append(listQ)
    
fileVDist.close()


#findDistance(trainDataTable, testDataTable)
K = [1,2,5,10]

for k in K:
    uniformKernel(k, trainDataTable, testDataTable,trainYears, testYears, neighboursIndexForAllInstances, distanceForAllInstances)
    inverseDistance(k, trainDataTable, testDataTable,trainYears, testYears, neighboursIndexForAllInstances, distanceForAllInstances)
    gausian(k, trainDataTable, testDataTable ,trainYears, testYears, neighboursIndexForAllInstances, distanceForAllInstances , 0.1) #best sigma found was 0.1

for k in K:
    uniformKernelClass(k, trainDataTable, testDataTable,trainYears, testYears, neighboursIndexForAllInstances, distanceForAllInstances)
    inverseDistanceClass(k, trainDataTable, testDataTable,trainYears, testYears, neighboursIndexForAllInstances, distanceForAllInstances)
    gausianClass(k, trainDataTable, testDataTable ,trainYears, testYears, neighboursIndexForAllInstances, distanceForAllInstances, 0.5) #best sigma found was 0.5


##sigma = [0.1,0.5,1.0,2.0]
##for s in sigma:
##    gausianClass(10, trainDataTable, validationDataTable ,trainYears, validationYears, neighboursIndexForAllInstancesV, distanceForAllInstancesV , s)

#using sigma = 0.5
#gausianClass(10, trainDataTable, testDataTable ,trainYears, testYears, neighboursIndexForAllInstances, distanceForAllInstances , 0.5)

