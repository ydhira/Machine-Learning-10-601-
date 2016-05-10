import math
from decimal import *


table2 = [ [0.0532,    0.0413,    0.0625 ,   0.0625 ,   0.0275  ,  0.0428],
        [0.0591,    0.0064,    0.0630,    0.0317,    0.0598,    0.0023],
        [0.0083,    0.0182,    0.0103,    0.0523,    0.0517,    0.0554],
        [0.0596,    0.0357,    0.0634,    0.0093,    0.0626,    0.0610]
    ]

for i in range (len(table2)):
    for j in range (len(table2[0])):
        table2[i][j] = float(table2[i][j])

def calculateInfo(table):

    print table
    tableSumColumn = [] ##length = 4
    tableSumRow = [] ##length = 6

       
    for i in range(len(table)):
        x = float(0)
        for j in range(len(table[0])):
            x += table[i][j]
        tableSumColumn.append(x)

    for i in range(len(table[0])):
        y = float(0)
        for j in range(len(table)):
            y += table[j][i]
        tableSumRow.append(y)

    #######################################PART(i)###########################
    HJointXY =0
    for i in range(len(table)):
        for j in range(len(table[0])):
            if ( table[i][j] > 0 ):
                HJointXY += float(table[i][j]) * float(math.log(float(1) / float(table[i][j]),2))
                

    #######################################PART(ii)###########################
    HX = float(0)
    for i in range(len(table)):
        x = float(0)
        for j in range(len(table[0])):
            x += table[i][j]
        if ( x> 0 and (1/x>0)):
            HX += x *  float(math.log((float(1)/x),2))


    #######################################PART(iii)###########################
    HY = float(0)
    for i in range(len(table[0])):
        y = float(0)
        for j in range(len(table)):
            y += table[j][i]
        if ( y> 0 and (1/y>0)):
            HY += y *  float(math.log((float(1)/y),2))

    #######################################PART(iv)###########################
    tableXgivenY = []

    for k in range(len(table)):
        l = []
        for g in range(len(table[0])):
            l.append(0)
        tableXgivenY.append(l)
        
    
    for i in range(len(table[0])): ## go til 15
       
        for j in range(len(table)): ## all the years
            if (tableSumRow[i] > 0):
                tableXgivenY[j][i] = (table[j][i]/tableSumRow[i])
            else:
                tableXgivenY[j][i] = l.append(0)

    HXgivenYList = [] ##length = 6
    for i in range(len(tableXgivenY[0])):
        HXgivenvalueY = float(0)
        for j in range(len(tableXgivenY)):
            if ( (tableXgivenY[j][i] > 0) and ((1/(tableXgivenY[j][i]))>0)):
                HXgivenvalueY += tableXgivenY[j][i] * float(math.log((float(1)/tableXgivenY[j][i]),2))
        HXgivenYList.append(HXgivenvalueY)

    HXgivenY = float(0)
    for i in range(len(HXgivenYList)):
        HXgivenY += tableSumRow[i]* HXgivenYList[i]

    #######################################PART(v)###########################
    tableYgivenX = []
    for i in range(len(table)):
        l = []
        for j in range(len(table[0])):
            if (tableSumColumn[i]!= 0):
                l.append(table[i][j]/tableSumColumn[i])
            else:
                l.append(float(0))
        tableYgivenX.append(l)

    HYgivenXList = [] ##length = 4
    for i in range(len(tableYgivenX)):
        HYgivenvalueX = 0
        for j in range(len(tableYgivenX[0])):
            if ( (tableYgivenX[i][j] > 0) and ((1/(tableYgivenX[i][j]))>0)):
                HYgivenvalueX += tableYgivenX[i][j] * float(math.log((float(1)/tableYgivenX[i][j]),2))
        HYgivenXList.append(HYgivenvalueX)

    HYgivenX = 0
    for i in range(len(tableYgivenX)):
        HYgivenX += tableSumColumn[i]* HYgivenXList[i]

    #######################################PART(vi)###########################

    infoXY = HX - HXgivenY

    

    #######################################PART(viii)###########################

    CHem = 0
    for i in range(len(table[0])):
        CHem += table[0][i] * Decimal(math.log(( Decimal(1)/table[1][i]), 2))

    print "CH(P(Y|X=1),P(Y|X=2)) = " , CHem

    #######################################PART(ix)###########################

    CHme = 0
    for i in range(len(table[0])):
        CHme += table[1][i] * Decimal(math.log(( Decimal(1)/table[0][i]), 2))

    print "CH(P(Y|X=2),P(Y|X=1)) = " , CHme

    #######################################PART(x)###########################

    HYgivenX1 = 0
    for i in range(len(table[0])):
        HYgivenX1 += table[0][i] * Decimal(math.log(( Decimal(1)/table[0][i]), 2))

    KLem = CHem - HYgivenX1

    print "KL(P(Y|X=1),P(Y|X=2)) = ", KLem

    #######################################PART(xi)###########################

    HYgivenX2 = 0
    for i in range(len(table[0])):
        HYgivenX2 += table[1][i] * Decimal(math.log(( Decimal(1)/table[1][i]), 2))

    KLme = CHme - HYgivenX2

    print "KL(P(Y|X=2),P(Y|X=1)) = " ,KLme
    return infoXY

#calculateInfo(table2)
