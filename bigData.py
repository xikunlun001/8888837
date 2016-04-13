## Author Xi Chen
import numpy as np
import re
import StringIO
import pprint
import timeit
import copy
import itertools


file = "test.txt"

def isFloat(str):
    
    try:
        float(str)
        return True
    except ValueError:
        return False
        
# find decision set        
def findD(decision, table):
    decisionSet = []
    uniqueD = np.unique(decision)   # may also use set
    #uniqueD = list(uniqueD)
    for i in uniqueD:
        decisionSet.append(np.array(np.where(table == i)[0]).tolist())
    
    return decisionSet

# find  [(a,v)] in blocks, but only value       
def findA(data):
    attriSet =[]
    for column in data.T:
        uniqueA = np.unique(column)   # may also use set but need tolist()
        columnSet =[]
        for i in uniqueA:
            #attriSet.append(np.array(np.where(column == i)[0].tolist()))
            
            columnSet.append(np.where(column == i)[0].tolist())
        attriSet.append(columnSet)
    return attriSet
        
# find A*
def bigA(data):
    bigASet = []
    #transA = data.astype(np.str)
    transData = np.row_stack(data)
    transList = transData.tolist()
    
    uniqueData = [list(x) for x in set(tuple(x) for x in transList)]
    #print uniqueData[0]
    for i in uniqueData:
        bigASet.append([j for j,x in enumerate(transList) if x ==i])
        
    #print bigA
    return bigASet


# find a index of findA result, can use the same index to locate the a in(a,v)
def indexT(data, attributes, attriA):
    T = []
    number = len(data[:,0])
    for i in attributes:
        T += number * [i]
        
        
    attriIndex = copy.deepcopy(attriA)
    
    for n,i in enumerate(attriIndex):
        for m,j in enumerate(i):
            for o,a in enumerate(j):
                attriIndex[n][m][o] = T[0]
                T.pop(0)
                
    
    attriIndex = list(itertools.chain(*attriIndex))
    
    return attriIndex
    
                     
def upper(decisionSet, bigASet):
    upperSet = copy.deepcopy(decisionSet)
    

    for x, decision in enumerate(decisionSet):
        for n,i in enumerate(decision):
            for j in bigASet:
                if i in j:
                    break
            if len(j)>1:
                upperSet[x] = list(set(decision).union(j))
      
    return upperSet
        
def lower(decisionSet, bigASet):
    lowerSet = copy.deepcopy(decisionSet)
    
    for x, decision in enumerate(decisionSet):
        indices=[]
        for n,i in enumerate(decision):
            for j in bigASet:
                if (i in j) and (set(decision).union(j) != set(decision)):
                    indices.append(n)
                    break
            lowerSet[x] = [i for j, i in enumerate(lowerSet[x]) if j not in indices]
    lowerSet = [x for x in lowerSet if x != []]
            
                    
    #print lowerSet
    return lowerSet
 
     

def LEM2(B, attriSet, attriIndex):
    
    
    T_rules =[]
    # b is every decision set in all decisions
    for b in B:
        G = copy.deepcopy(b)
    
        while G != []:
            T = []
            T_G = []
            
            findMax = []
            MaxValue = 0
            
            IndexTemp =[]
            
            GCopy = list(itertools.chain(*G))
            attriSetCopy = list(itertools.chain(*attriSet))
            for n,i in enumerate(attriSetCopy):
                if set(i).intersection(GCopy) != []:
                    T_G.append(i)
                    IndexTemp.append(n)
                    findMax.append(len(set(i).intersection(GCopy)))
                    if len(set(i).intersection(GCopy) >= finMax):
                        MaxValue = len(set(i).intersection(GCopy)
                        
                    
            IndexCopy = [attriIndex[j] for j in indexTemp]
                
            while T =[] or set(T).union(b) != b:
                
                
                    

    

        
def main(file):
    
    data=[]
    
    f1 = open(file, 'r')
    f2 = open("newdata.txt", 'w')
    
    removeComments = []
    
    for line in f1.readlines():
        if "!" not in line:
            f2.write(line)
            
    f1.close()
    f2.close()
            
    
    
    f = open("newdata.txt", 'r')
    messData = f.read()
    pat = re.compile(r'(\<[\s\S]*\>)')
    betterData = re.sub(pat , '' , messData)
    attributes = re.findall(r'(\[[\s\S]*])', messData)
    attributes = re.split(r'\s+', attributes[0])
    attributes = attributes[1:-2]   #original code is [1:-1] including decision column
    attriNum = len(attributes)
    
    
    dataset = re.sub(r'(\<[\s\S]*\])','', messData)

    dataset = re.split(r'\s+', dataset)
    dataset = dataset [1:]
    
  
            
            
    #print dataset
    
    #  n = len(dataset)/(attriNum+1)
    # print n
    
    table = [list(t) for t in zip(*[iter(dataset)]*(attriNum+1))]  # original attriNum = attriNum(now) +1
    table = np.array(table)
    
    #print table
    
#convert numerical elements to float

    decision = table[:,-1]

    data = table[:,:-1]
    data =data.tolist()
    for i in data:
        for n,j in enumerate(i):
            if isFloat(j) == True:
                i[n] = float(j)
                
                
    data = np.array(data)
    #print data

# calculate d*
    decisionSet = findD(decision, table)


# calculate A*
    attriA = findA(data)

    bigASet = bigA(data)
    

    upper(decisionSet, bigASet)

    lower(decisionSet, bigASet)
    
    
    
    print indexT(data, attributes, attriA)
    
    #data = np.array(data)
    #Attributes.append(attributes.split())

    f.close()
    
    
    

    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    

start = timeit.default_timer()
main(file)
stop = timeit.default_timer()
print(stop-start)