import math

before =[90,85,73,90,90,53,68,90,78,89,83,83,83,82,65,79,83,60,47,77]
after =[95,89,76,92,91,53,67,88,75,85,85,87,85,85,68,87,84,71,46,75]

aveBefore = sum(before) / len(before)
aveAfter = sum(after) / len(after)

print aveBefore
print aveAfter

diff = []
for i in range(len(before)):
    diff.append(before[i] - after[i])


davg = sum(diff) / len(diff)
print "d average is ", davg
d = 0
for i in range(len(diff)):
    d += math.pow((diff[i] - davg),2)

sd = math.pow( d/19 , 0.5)
print "sd is ", sd

fileo = open('mcnemarData.txt', 'r')

count = 0
real = []
defaultAlgo = []
mineAlgo = []
for line in fileo:
    if (count != 0):
        listQ = line.split('\t')
        real.append(listQ[0])
        defaultAlgo.append(listQ[1])
        mineAlgo.append(listQ[2])
    count+=1

n00 =0
n01=0
n10=0
n11 = 0

for i in range(len(real)):
    if (defaultAlgo[i] == real[i] and mineAlgo[i] == real[i]):
        n00 +=1
    elif (defaultAlgo[i] == real[i] and mineAlgo[i] != real[i]):
        n01 +=1
    elif (defaultAlgo[i] != real[i] and mineAlgo[i] == real[i]):
        n10 +=1
    elif (defaultAlgo[i] != real[i] and mineAlgo[i] != real[i]):
        n11 +=1
    else:
        print ("shouldnt have come here")

M = ((math.pow((abs(n01 - n10) -1),2))/(n01+n10))
print M
    
