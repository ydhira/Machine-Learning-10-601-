import InformationTheory
from decimal import *
import ast


def bubble_sort(items):
    """ Implementation of bubble sort """
    for i in range(len(items)):
        for j in range(len(items)-1-i):
            if items[j][0] > items[j+1][0]:
                items[j], items[j+1] = items[j+1], items[j]     # Swap!
    
    print items
    
def featureSelection():
    fileo = open( 'QuantizedTestData2.txt', 'r')
    myTable= []
    allYears = []
    uniqueYears = []
    noFeatures = 90
    count =0
    N = 16
    
    for line in fileo:

        listQ = ast.literal_eval(line)        
        if (int(listQ[0]) not in allYears):
            uniqueYears.append(int(listQ[0]))
        allYears.append(int(listQ[0]))
        listQ = map(lambda x: int(x), listQ)
        listQ = listQ[1:]
        myTable.append(listQ)


    fileo.close()
    uniqueYears = sorted(uniqueYears)
    featureK = []
    for i in range(len(uniqueYears)):
        l = []
        for j in range(N):
            l.append(0)
        featureK.append(l)
    

    infoL = []
    for i in range(noFeatures):                             ##for all the features
        if (i >0):
            for k in range (len(uniqueYears)):
                for l in range (N):
                    featureK[k][l] = 0
                
        for j in range (len(myTable)):                         ##go through all the instances    
            year = int(allYears[j])                              ##get the year value
            yearIndex = int(uniqueYears.index(year))                   ##see which index it is
            featureK[yearIndex][myTable[j][i]] += 1                ##add at that index
    
        lenallYears=len(uniqueYears)
        totalIns = 0
        
        for h in featureK:
            totalIns += sum(h)
        featureK = [map(lambda elem:float(elem)/float(totalIns), x) for x in featureK]
        ###I HAVE THE TABLE FOR ith FEATURE
        info = InformationTheory.calculateInfo(featureK)
        infoL.append(info)

    for i in range(len(infoL)):
        infoL[i] = (infoL[i], i)   
    bubble_sort(infoL)



featureSelection()    
    


