import sys
import ast
import math
import heapq

uniqueYears = [1991, 1992, 1993, 1994, 1995, 1996, 1997, 1998, 1999,
               2000, 2001, 2002, 2003, 2004, 2005, 2006, 2007, 2008,
               2009, 2010]
    
# Segregating out instances that take a particular value
# attributearray is an N x 1 array.
def segregate(attributearray, value):
    outlist = []
    for i in range(len(attributearray)):
        if (attributearray[i] == value):
            outlist.append(i)  #  Append "i" to outlist
    return outlist


# Assuming labels take values 1..M.
def computeEntropy(labels):
    entropy = float(0)
    for i in uniqueYears:
        probability_i = float(len(segregate(labels, i))) / float(len(labels))
        if (probability_i != 0):
            entropy -= probability_i * math.log(probability_i)
    return entropy


def computeSplitEntropy(labels):
    entropy = float(0)
    #print labels
    for i in range(len(labels)):
        probability_i = float(labels[i])/ float(sum(labels))
        if (probability_i != 0):
            entropy -= probability_i * math.log(probability_i)
    #print "split entropy is ", entropy
    return entropy

# Find most frequent value. Assuming labels take values 1..M 
def mostFrequentlyOccurringValue(labels):
    bestCount = -sys.maxint
    bestId = None
    for i in uniqueYears:
        count_i = len(segregate(labels,i))
        if (count_i > bestCount):
           # print "went in"
            bestCount = count_i
            bestId = i
    return bestId

class  dtree:
    nodeGainRatio = float(0.0)
    nodeInformationGain= float(0.0)
    isLeaf = False
    majorityClass = 0
    bestAttribute = 0
    children = []
    parent = []
    noFeatures = 10
    N = 4
    name = ""

    def __init__(self,attributes, labels):
        self.parent = None
        self.children = []
        self.buildTree (attributes, labels)

    def buildTree (self,attributes, labels):
       # print "start to make a tree , ",self
        numInstances = len(labels)
        nodeInformation = 0
        if (len(labels) > 0):
            nodeInformation = numInstances * computeEntropy(labels)
            
        self.majorityClass = mostFrequentlyOccurringValue(labels)
        #print self.majorityClass

        if (nodeInformation == float(0)):  # This is a "pure" node
            self.isLeaf = True
            return

        # First find the best attribute for this node
        bestAttribute = None
        bestInformationGain = float(-sys.maxint)
        bestGainRatio = float(-sys.maxint)
        
        for X in range (self.noFeatures):
            attributeXcol = []
            
            for k in range (numInstances):
                attributeXcol.append(attributes[k][X])
                
            conditionalInfo = 0
            attributeEntropy = 0
            attributeCount = []
            for p in range (4):
                attributeCount.append(0)
            for Y in range (4):
                ids = segregate(attributeXcol, Y) # get ids of all instances
                                                    # for which attribute X == Y
 
                attributeCount[Y] = len(ids)
                
                labelsid = []
                for l in ids:
                    labelsid.append(labels[l])

                if (len(labelsid)!=0):    
                    conditionalInfo += attributeCount[Y] * computeEntropy(labelsid);
                    
            attributeInformationGain = nodeInformation - conditionalInfo
            splitEntropy = computeSplitEntropy(attributeCount)

            gainRatio = 0.0
            if (splitEntropy != 0):
                
                gainRatio = float(attributeInformationGain) / float(splitEntropy)

            if (gainRatio > bestGainRatio):
                bestInformationGain = attributeInformationGain
                bestGainRatio = gainRatio
                bestAttribute = X

        #If no attribute provides andy gain, this node cannot be split further
        if (bestGainRatio == float(0)):
            self.isLeaf = True
            return

        # Otherwise split by the best attribute
        self.bestAttribute = bestAttribute
        self.nodeGainRatio = bestGainRatio
        self.nodeInformationGain = bestInformationGain
        attributeXcol = []
        
        for k in range (numInstances):
            attributeXcol.append(attributes[k][self.bestAttribute])
            
        for Y in range (4):
            
            ids = segregate(attributeXcol, Y)
            #if (len(ids) >0):
            labelsid = []
            attributeids = []
            for l in ids:
                labelsid.append(labels[l])
                attributeids.append(attributes[l])
            child = dtree(attributeids, labelsid)
            child.parent = self
            self.children.append(child)

        return

    def countNodes(self,noNodes):
        if (self.isLeaf):
            noNodes +=1
            #return noLeaves
        else:
            for i in self.children:
                noNodes += i.countNodes(noNodes)
        
        return noNodes        




# instance is a list [9,0,1 ... ] labels for the
# attributes with 10 values inside it
def classify(tree, instance):
    
    if (tree.isLeaf):
        
        return tree.majorityClass

    bestAttribute = tree.bestAttribute
    j = instance[bestAttribute]
    newT = tree.children[j]

    return classify(newT, instance)

    
def countLeaves(decisiontree):
    if decisiontree.isLeaf:
        return 1
    else:
        n = 0
        for child in decisiontree.children:
            n += countLeaves(child)
    return n

# Check if a node is a twig
def isTwig(decisionTree):
    if (decisionTree.isLeaf):
        return False
    for child in decisionTree.children:
        if not child.isLeaf:
            return False
    return True

# Make a heap of twigs.  The default heap is empty
def collectTwigs(decisionTree, heap):
    if isTwig(decisionTree):
        heapq.heappush(heap,(decisionTree.nodeInformationGain, decisionTree))
    else:
        for child in decisionTree.children:
            collectTwigs(child,heap)
    return heap

# Prune a tree to have nLeaves leaves
# Assuming heappop pops smallest value
def pruneByIG(dTree, nLeaves):
    totalLeaves = countLeaves(dTree)
    #print "totalLeaves are , ", totalLeaves
    twigHeap = collectTwigs(dTree , [])
    
    while totalLeaves > nLeaves:
        #print "totalLeaves are , ", totalLeaves
        twig = heapq.heappop(twigHeap)[1]
        totalLeaves -= (len(twig.children) - 1) #Trimming the twig removes
                                                    #numChildren leaves, but adds
                                                    #the twig itself as a leaf
        #print "children removed are , ", len(twig.children)
        twig.chidren = None  # Kill the chilren
        twig.isLeaf = True
        twig.nodeInformationGain = 0
        
        # Check if the parent is a twig and, if so, put it in the heap
        parent = twig.parent
        #print parent
        if (parent != None):
            if isTwig(parent):
                heapq.heappush(twigHeap,(parent.nodeInformationGain, parent))
    return

#============================================================================#

# First pass : evaluate validation data and note the classification at each node
# Assuming that "valData" includes "attributes" and "labels"

# First create an empty list of error counts at nodes
def createNodeList(dTree, nodeError):

    stack = []
    stack.append (dTree)
    while(stack):
        tree = stack.pop()
        nodeError[tree] =0
        if (not tree.isLeaf):
            for child in tree.children:
                stack.append(child)

    return nodeError

# Pass a single instance down the tree and note node errors
def classifyValidationDataInstance(dTree, validationDataInstance, nodeError):
    if (dTree.majorityClass != validationDataInstance[0]):
        nodeError[dTree] += 1
    testAttributes = validationDataInstance[1:]
    if (not dTree.isLeaf):
        childNode = dTree.children[testAttributes[dTree.bestAttribute]]
        classifyValidationDataInstance(childNode, validationDataInstance, nodeError)
    return 

# Count total node errors for validation data
def classifyValidationData(dTree, validationData):
    nodeErrorCounts = createNodeList(dTree ,{})
    for instance in validationData:
        classifyValidationDataInstance(dTree, instance, nodeErrorCounts)
    return nodeErrorCounts


# Second pass:  Create a heap with twigs using nodeErrorCounts
def collectTwigsByErrorCount(decisionTree, nodeErrorCounts, heap):
    if isTwig(decisionTree):
        # Count how much the error would increase if the twig were trimmed
        twigErrorIncrease = nodeErrorCounts[decisionTree]
        for child in decisionTree.children:
            twigErrorIncrease -= nodeErrorCounts[child]
        heapq.heappush(heap,(twigErrorIncrease, decisionTree))
    else:
        for child in decisionTree.children:
            collectTwigsByErrorCount(child, nodeErrorCounts, heap)
    return heap



# Third pass: Prune a tree to have nLeaves leaves
# Assuming heappop pops smallest value
def pruneByClassificationError(dTree, validationData, nLeaves):
    # First obtain error counts for validation data
    nodeErrorCounts = classifyValidationData(dTree, validationData) # is a dict of tree:errors
    # Get Twig Heap
    twigHeap = collectTwigsByErrorCount(dTree, nodeErrorCounts, [])

    totalLeaves = countLeaves(dTree)
    while totalLeaves > nLeaves:
        twig = heapq.heappop(twigHeap)[1]
        totalLeaves -= (len(twig.children) - 1) #Trimming the twig removes
                                                    #numChildren leaves, but adds
                                                    #the twig itself as a leaf
        twig.chidren = None  # Kill the chilren
        twig.isLeaf = True
        twig.nodeInformationGain = 0

        # Check if the parent is a twig and, if so, put it in the heap
        parent = twig.parent
        if isTwig(parent):
            twigErrorIncrease = nodeErrorCounts[parent]
            for child in parent.children:
                twigErrorIncrease -= nodeErrorCounts[child]
            heapq.heappush(twigHeap,(twigErrorIncrease, parent))
    return

#=================================================================================#
    
def main():
    
    noFeatures = 10
    fileo = open('DT_Quantized_Train.txt','r')
    labels = []
    attributes = []
    count = 0
    uniqueYears = []
    for line in fileo:
        
        #if (count <1000):    
        listQ = ast.literal_eval(line)
       # listQ = line.split(',')
        labels.append(int(listQ[0]))
        
        if (int(listQ[0]) not in uniqueYears):
            
            #print int(listQ[0])
            uniqueYears.append(int(listQ[0]))
           
        listQ=listQ[1:]
        listQ = map(lambda x: int(x), listQ)
        attributes.append(listQ)
            
        #else:
         #   break
        #count+=1

    fileo.close()   
   # print (len(uniqueYears))
    myDtree = dtree(attributes,labels)

    fileValidate = open('DT_Quantized_validation.txt','r')
    validationData = []
    count = 0
    for line in fileValidate:
        #if (count <10):
        listQ = ast.literal_eval(line)
        listQ = map(lambda x: int(x), listQ)
        validationData.append(listQ)
        #else:
        #    break

        #count+=1

    fileValidate.close()
    pruneByIG(myDtree, 200)
    #pruneByClassificationError(myDtree,validationData,200)

    fileTest = open('DT_Quantized_Test.txt','r')
    count = 0
    same =0
    for line in fileTest:
        
        
        #if (count <105):
            
        listQ = ast.literal_eval(line)
        year = listQ[0]
        listQ = listQ[1:]
        classifiedClass = classify(myDtree, listQ)
       # print year , classifiedClass
        
        if(int(year) == classifiedClass):
            #print "Same"
            same +=1
        
            
       # listQ = line.split
        #else:
        #    break
        #print count
        count+=1
    
    print "overall accuracy is ", float(same)/float(count) * 100 
    fileTest.close()    
            
main()
