# In the tables below, the probabilities are sequentially listed
# for values 0, 1, 2 (where appropriate)

# Battery age (A) can take 3 values: 0 = less than 1 year old
#                                1 = 2-3 years old
#                                2 =  >3 years old

PA = [0.2, 0.5, 0.3]

# Battery (B) can take two values:  1 = functional,  0 = dead
PBgivenA = [[0.01, 0.99],[0.10, 0.90],[0.25, 0.75]]


# Lights (L) can take 2 values: 1 = turn on, 0 = do not turn on
PLgivenB = [[1, 0],[0.02, 0.98]]
 

# Starter (S) can take 2 values: 1 = on, 0 = off
PS = [0.5, 0.5]

# "Engine turns over" (E) can take 2 values: 1 = yes, 0 = no
PEgivenSandB = [[[1, 0],[1,0]],[[1,0],[0.001,0.999]]]



# Fuel Pump (P) can take two values: 1 = OK, 0 = faulty.
PP = [0.001, 0.999]

# Fuel Line (N) can take two values: 1 = OK, 0 = faulty
PN = [0.001, 0.999]

# Fuel (F) can take two values: 1 = yes, 0 = no (empty)
PF = [0.05, 0.95]

# Fuel Gauge (G) can take two values: 1 = not empty, 0 = empty
PGgivenF = [[1, 0],[0.05, 0.95]]


# Fuel Subsystem (Y) can take two values: 1 = OK, 0 = faulty
PYgivenPNF = [ [[[1, 0], [1, 0]] , [ [1, 0], [1, 0]]], [[[1, 0], [1, 0]], [[1, 0],[0.001,0.999]]]  ]



# Spark Plug (K) can take two values: 1 = Clean, 0 = fouled
PK = [0.05, 0.95]

# Engine Starts (T) can take two values: 1 = yes, 0 = no
PTgivenKEY = [[ [[1, 0],[1, 0]],[[1, 0],[1, 0]]],[[[1, 0],[1, 0]],[[1, 0],[0.001, 0.999]]]]
############################################################################
SPA = [0.2, 0.5, 0.3]

# Battery (B) can take two values:  1 = functional,  0 = dead
SPBgivenA = [[0.01, 0.99],[0.10, 0.90],[0.25, 0.75]]


# Lights (L) can take 2 values: 1 = turn on, 0 = do not turn on
SPLgivenB = [[1, 0],[0.02, 0.98]]
 

# Starter (S) can take 2 values: 1 = on, 0 = off
SPS = [0.5, 0.5]

# "Engine turns over" (E) can take 2 values: 1 = yes, 0 = no
SPEgivenSandB = [[1, 0],[1,0],[1,0],[0.001,0.999]]



# Fuel Pump (P) can take two values: 1 = OK, 0 = faulty.
SPP = [0.001, 0.999]

# Fuel Line (N) can take two values: 1 = OK, 0 = faulty
SPN = [0.001, 0.999]

# Fuel (F) can take two values: 1 = yes, 0 = no (empty)
SPF = [0.05, 0.95]

# Fuel Gauge (G) can take two values: 1 = not empty, 0 = empty
SPGgivenF = [[1, 0],[0.05, 0.95]]


# Fuel Subsystem (Y) can take two values: 1 = OK, 0 = faulty
SPYgivenPNF = [ [1, 0], [1, 0] , [1, 0], [1, 0],[1, 0],[1, 0], [1, 0],[0.001,0.999]]



# Spark Plug (K) can take two values: 1 = Clean, 0 = fouled
SPK = [0.05, 0.95]

# Engine Starts (T) can take two values: 1 = yes, 0 = no
SPTgivenKEY = [[1, 0],[1, 0],[1, 0],[1, 0],[1, 0],[1, 0],[1, 0],[0.001, 0.999]]
############################################################################

class node:

    isLeaf = False
    B = []
    F = []
    BM = []
    FM = []
    children = []
    parent = []
    prob = []
    name = ""
    valuesTaken = 0
    simpleProb = []

    def __init__(self, prob, sProb, name, valuesTaken):
        self.prob = prob
        self.simpleProb = sProb
        self.name = name
        self.valuesTaken = valuesTaken
        self.children = []
        self.parent = []
        self.FM = []
        self.BM = []
        self.B = []
        self.F = []
        
        

    def setChildren(self,children):
        for child in children:
            self.children.append(child)
            child.parent.append(self)

    def toString(self):
        return self.name

    def getChildren(self):
        children = []
        for i in self.children:
            children.append(i.toString())
        return children   
    def getParents(self):
        parents = []
        for i in self.parent:
            parents.append(i.toString())
        return parents 

def buildSampleTree():
    batteryAge = node(PA, SPA, 'batteryAge', 3)
    lights = node(PLgivenB, SPLgivenB , 'lights', 2)
    battery = node(PBgivenA, SPBgivenA, 'battery', 2)
    engineTurnsOver = node(PEgivenSandB, SPEgivenSandB, 'engineTurnsOver', 2)
    starter = node(PS, SPS,'starter', 2)
    sparkPlug = node(PK, SPK,'sparkPlug', 2)
    fuelPump = node(PP, SPP,'fuelPump', 2)
    fuelLine = node(PN , SPN,'fuelLine', 2)
    fuel = node(PF, SPF,'fuel', 2)
    fuelSubsystem = node(PYgivenPNF,SPYgivenPNF ,'fuelSubsystem', 2)
    fuelGauge = node(PGgivenF,SPGgivenF,'fuelGauge' , 2)
    engineStarts = node(PTgivenKEY, SPTgivenKEY,'engineStarts', 2)

    #setting the parents and children
    
    batteryAge.setChildren([battery])  
    battery.setChildren([lights,engineTurnsOver ])
    starter.setChildren([engineTurnsOver])
    engineTurnsOver.setChildren([engineStarts])
    sparkPlug.setChildren([engineStarts])
    fuelPump.setChildren([fuelSubsystem])
    fuelLine.setChildren([fuelSubsystem])
    fuel.setChildren([fuelSubsystem , fuelGauge])
    fuelSubsystem.setChildren([engineStarts])
    
    #set the leaves
    lights.isLeaf = True
    engineStarts.isLeaf = True
    fuelGauge.isLeaf = True    
    
    return [batteryAge, battery,lights, starter,engineTurnsOver,fuelPump,
            fuelLine,fuel,fuelGauge,fuelSubsystem,sparkPlug, engineStarts]


def initializeEvidence(tree, listN):
    SOURCE= []
    SINK = []
    E = []

    count = 0
    for i in tree:
        if (len(i.parent) == 0):
            SOURCE.append(i)
            
        if (len(i.children) == 0):
            SINK.append(i)
            
        if (listN[count] != -1):
            E.append(i)
        count += 1
    
    # Initially set everything to 0.
    # Note the difference in how forward and backward beliefs are initialized
    for X in tree:
        l = []
        b = []
        for v in range (X.valuesTaken):
            X.F.append(0)
            X.B.append(0)
        

        #c = []   
        for Z in range(len(X.children)):
            p = [] 
            for v in range (X.valuesTaken):
                p.append(0)
            X.FM.append(p)
            #c.append(p)
        #X.FM.append(c)

         
        for Y in X.parent:
            p2 = []
            for v in range (Y.valuesTaken):
                p2.append(0)
            X.BM.append(p2)
        
                



    # Initialize forward belief for source nodes
    for X in SOURCE:
        for v in range(X.valuesTaken):
            #print X.F[v] , X.prob[v]
            X.F[v] = X.prob[v]

    # Initialize backward belief for sink nodes
    for X in SINK:
        for v in range(X.valuesTaken):
            X.B[v] = 1

    # Initialize Backward messages for all nodes (redundant for SINK nodes)
    for X in tree:
        for Z in range(len(X.parent)):
            for z in range(X.parent[Z].valuesTaken):
                X.BM[Z][z] = 1

    # Initialize beliefs for Evidence nodes. 
    # Remember that the that the default values were initialized to 0
    #for t in tree:
        #print t.F
    for X in E:
        for i in range(X.valuesTaken):       
            X.F[i] = 1
            X.B[i] = 1


    return (tree, SOURCE, SINK,E)

    
#A,B,L,S,E,P,N,F,G,Y,K,T

#pSet is a set of nodes
#X is a node, , x is value taken by X

def getfwdbelief(FM, Pset, FixedNodes, inPvalueSet, X, x,psetOriginal):
    #localPset = close(Pset)  # To avoid destroying the original Pset
    FB = float(0)   
    P = Pset[0]
    Pset = Pset[1:]
    
    for v in range (P.valuesTaken):
        
        if (P in FixedNodes and FixedNodes[P] != v):
            continue
        PvalueSet = [inPvalueSet, v]
        if  (len(Pset) == 0):
            d =  float(0)
            for i in (X.simpleProb):
                d += i[x]
            
            FB += float(P.FM[P.children.index(X)][v]) * d
        else:
            FB += float(P.FM[P.children.index(X)][v]) * getfwdbelief(FB,Pset,FixedNodes,PvalueSet,X,x, psetOriginal)

    return float(FB)


def getfwdbeliefBM(FM, Pset, FixedNodes, inPvalueSet, X, x,psetOriginal):
    #localPset = close(Pset)  # To avoid destroying the original Pset
    FB = float(0)   
    P = Pset[0]
    Pset = Pset[1:]
    
    for v in range (P.valuesTaken):
        
        if (P in FixedNodes.keys() and FixedNodes[P] != v):
            continue
        PvalueSet = inPvalueSet.append(v)
        if  (len(Pset) == 0):
            d =  float(1)
            for i in (X.simpleProb):
                d *= i[x]
            
            FB += float(P.FM[P.children.index(X)][v]) * d
        else:
            FB += float(P.FM[P.children.index(X)][v]) * getfwdbelief(FB,Pset,FixedNodes,PvalueSet,X,x, psetOriginal)

    return float(FB)

def reverse(data_list):
    length = len(data_list)
    s = length

    new_list = [None]*length

    for item in data_list:
        s = s - 1
        new_list[s] = item
    return new_list

def believeProp(listN):
    tree = buildSampleTree()
    (tree2, SOURCE, SINK,E) = initializeEvidence(tree,listN)


    Vsort = tree2
    Vrevsort = reverse(tree2)

    for iterations in range (1):
        for X in Vsort:

            # In the forward pass, source nodes are not modified
            if X in SOURCE: continue

            # Compute forward belief at this node
            # The "getfwdbelief" routine is a little more detailed than the rest
            # of this code
            for x in range(X.valuesTaken):
                if X in E: continue
                X.F[x] = getfwdbelief(X.FM, X.parent, [], [], X, x, X.parent)
            

            # Compute forward messages to children
            c = 0
            for Z in X.children:
                for x in range(X.valuesTaken):
                    BMwithoutCurrentChild = 1
                    for K in X.children:
                        if (K == Z) :
                            continue
                        BMwithoutCurrentChild *= K.BM[K.parent.index(X)][x]
                        
                    X.FM[c][x] = float(X.F[x]) * float(BMwithoutCurrentChild)
                c+=1

            
        for X in Vrevsort:

            # In the reverse pass, sink nodes are not modified
            if X in SINK :
                continue

            # Backward belief
            for x in range(X.valuesTaken):

                if X in E:
                    continue

                X.B[x] = 1
                for C in X.children:
                    X.B[x] *= C.BM[C.parent.index(X)][x]
            

            # Backward messages to parents
            for Y in X.parent:
                # Make sure to clear FixY first, so that it has only ONE entry
                FixY = {}
                #for i in range(Y.valuesTaken):
                    #FixY.append(0)
                for y in range(Y.valuesTaken):
                    X.BM[X.parent.index(Y)][y] = 0
                    FixY[Y] = y
                    for x in range(X.valuesTaken):
                        X.BM[X.parent.index(Y)][y] += X.B[x] * getfwdbelief(X.FM,X.parent,FixY,[],X,x, X.parent)


    for x in tree2:
        print x.toString(),x.F , x.B
        
    posterior= []
    
    for i in range(len(tree2)):
        
        p =  [0]*tree2[i].valuesTaken
        posterior.append(p)

    c = 0
    for X in tree2:
        print X.toString()
        if X in E: continue
        sumP = 0;
        for x in range(X.valuesTaken):
            posterior[c][x] = X.F[x] * X.B[x]
            sumP += posterior[c][x]
        
        for x in range(X.valuesTaken):
            if (sumP != 0):
                posterior[c][x] = float(posterior[c][x])/float(sumP)
        c+=1
        
    for i in posterior:
        #print tree2[i].toString()
        for j in i:
            print j
    

    fuelLine = tree2[7]
    p = 0
    d = ((fuelLine.F[0] * fuelLine.B[0])+(fuelLine.F[1] * fuelLine.B[1]))
    if (d!=0):
        p = (fuelLine.F[1] * fuelLine.B[1]) / d
    print p

 
    fuelPump = tree2[5]
    p = 0
    d = ((fuelPump.F[0] * fuelPump.B[0])+(fuelPump.F[1] * fuelPump.B[1]))
    if (d!=0):
        p = (fuelPump.F[1] * fuelPump.B[1]) / d
    print p






believeProp([1,-1,0,-1,-1,-1,-1,-1,-1,-1,-1,-1])

#1,1,1,1,1,1,1,1,1,1,1,1
