def getMaxMin():

    fileo = open('train-1991-2010-2.txt', 'r')
    noFeatures = 90
    N = 16    
    mmList = []

    for i in range (noFeatures):
        l = []
        for j in range (2):
            l.append(0)
        mmList.append(l)

    #############GETTING THE MAX MIN VALUES#########
    count  = 0
    for line in fileo:
        
        listQ = line.split(',')
        listQ=listQ[1:]
        
        for i in range(noFeatures):
            if (float(listQ[i]) < mmList[i][0]):
                
                mmList[i][0] = float(listQ[i])
                
            elif (float(listQ[i]) > mmList[i][1]):
                
                mmList[i][1] = float(listQ[i])
        
    
    print"Got the max min values"
    return mmList

def quantizeTest():

    mmList = getMaxMin()
    mmList[0][0]  = 1.749
    bigTable = []
    allYears= []
    fileo = open('test-1991-2010.txt', 'r')
    noFeatures = 90
    N = 16    



    #############GETTING THE MAX MIN VALUES#########
    count  = 0
    for line in fileo:
        
        listQ = line.split(',')
        if (int(listQ[0]) not in allYears):
            allYears.append(int(listQ[0]))
            
        #listQ=listQ[1:]
        bigTable.append(listQ)
                    
    allYears = sorted(allYears)
    fileo.close()

    ###########MAKING THE BINS FOR ALL FEATURES######
    binLists = []
    for i in range(noFeatures):
        r = ((mmList[i][1] - mmList[i][0])/float(N))
        l = []
        
        for j in range(N):
            l.append(mmList[i][0] + (float(j+1) * r))
            
        binLists.append(l)
    print "made the bins"

    #########FIND THE INDEX THE FEATURE VALUE FALLS INTO AND REPLACE BY THAT#####

    for i in range(len(bigTable)):                      ##all the instances
        for j in range(1,noFeatures+1):                     ##all the features
            found = False
            for k in range(N):                          ## comparing which index it would be

                if ((float(bigTable[i][j])) <= float(binLists[j-1][k])):
                    found = True
                    bigTable[i][j] = int(k)
                    break
            if (found == False):
                bigTable[i][j]  = N-1
                
    target = open('QuantizedTestData2.txt', 'w')
    for i in range(len(bigTable)):
        target.write(str(bigTable[i]))
        target.write("\n")

    target.close()

quantizeTest()
