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
def findA(data, attributes):
    attriSet =[]
    attriSetIndex=[]
    attriSetValue=[]
    for n,column in enumerate(data.T):
        uniqueA = np.unique(column)   # may also use set but need tolist()
        columnSetIndex =[]
        columnSetValue =[]
        for i in uniqueA:
            #attriSet.append(np.array(np.where(column == i)[0].tolist()))
    
            columnSetIndex.append(np.where(column == i)[0].tolist())
            value = "("+str(attributes[n])+","+str(i)+")"
            columnSetValue.append(value)
        #print columnSetValue
        attriSetIndex.append(columnSetIndex)
        #print attriSetIndex
        attriSetValue.append(columnSetValue)
    attriSet.append(attriSetValue)
    attriSet.append(attriSetIndex)
    #print attriSetValue
    #print attriSet
    return attriSet
 
# when dataset is numerical, do all cutpoints strategy first. And then output [(a,v)] and (a,v)
def cutpointFindA(data, attributes):
    indexAV=[]
    valueAV=[]
    AV=[]
    for n, column in enumerate(data.T):
        uniqueValue = np.unique(column)
        uniqueCopy = uniqueValue[1:]
        valueCol =[]
        indexCol =[]
        for m, i in enumerate(uniqueCopy):
            # output ((a,v))
            cutpoint = (uniqueValue[0]+i)/2
            value1 = "("+str(attributes[n])+","+str(uniqueValue[0])+".."+ str(cutpoint)+")"
            value2 =  "("+str(attributes[n])+","+str(cutpoint)+".."+str(uniqueValue[-1])+")"
            valueCol.append(value1)
            valueCol.append(value2)
            #print valueCol
            
            # output [(a,v)]
            indexSmall = np.where(column < cutpoint)[0].tolist()
            indexLarge = np.where(column > cutpoint)[0].tolist()
            indexCol.append(indexSmall)
            indexCol.append(indexLarge)
            
            
        valueAV.append(valueCol)
        indexAV.append(indexCol)
    
    AV.append(valueAV)
    AV.append(indexAV)
    #print valueAV    
    #print indexAV
    return AV

         
         
         
         
         
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


# upper set of decision set                    
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

# lower set of decision set        
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


# find data is numerical or symbolic
def typeOfData(data):
    
    if type(data[0][0]) != float:
        numerical =0
    if type(data[0][0]) == float:
        numerical =1
        
    return numerical
         
# LEM2  B-- is upper or lower set of decision set
def LEM2(B, attriSet, data):
    

    # extract (a,v) and [(a,v)] from attriSet
    attriValue = attriSet[0]
    attriIndex = attriSet[1]
    
    # The rule set list
    T_rules =[]
    
    # b is every decision set in all decisions
    for b in B:
        G = copy.deepcopy(b)
    
        while G != []:
            #(a,v) of rules
            T = []
            #[(a,v)] of rules
            TIndex=[]
            T_G = []
            T_G_Index =[]
            
            
            
            
            #GCopy = list(itertools.chain(*G))
            attriValueCopy = list(itertools.chain(*attriValue))
            attriIndexCopy = list(itertools.chain(*attriIndex))
            
            
            for n,i in enumerate(attriIndexCopy):
                if set(i).intersection(G) != []:
                    T_G.append(attriValueCopy[n])
                    T_G_Index.append(i)
                    

                    

                
            while T ==[] or set(TIndex).union(b) != b:
                #find Max length
                findMax =[]
                for i in T_G_Index:
                    findMax.append(len(i)):
                MaxValue = max(findMax)
                MaxIndices = [i for i, j in enumerate(findMax) if j == MaxValue]
                
                
                if len(MaxIndices) == 1:
                    select_t_value = T_G[MaxIndices[0]]
                    select_t_index = T_G_Index[MaxInices[0]]
                
                # select smallest cardinality of [t]
                # a list contains max len of [(a,v)] union d*
                bestIndices =[]
                if len(MaxIndices) >1:
                    for i in MaxIndices:
                        length = len(MaxIndices[i])
                        bestIndices.append(length)
                    MinValue = min(bestIndices)
                    MinIndices = [i for i,j in enumerate(bestIndices) if j == MinValue]
                    
                    # No matter len(MinIndices)=1 or >1, always select the 1st one
                    select_t_value = T_G[MaxIndices[MinIndices[0]]]
                    select_t_index = T_G_Index[MaxIndices[MinIndices[0]]]
                    
                T = set(T).union(select_t_value)
                TIndex = set(TIndex).union(select_t_index)
                G = set(select_t_index).intersection(G)
                

                
                    

    

        
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
    attriA = findA(data, attributes)

    bigASet = bigA(data)
    

    upper(decisionSet, bigASet)

    lower(decisionSet, bigASet)
    
    

    cutpointFindA(data, attributes)
    
    #data = np.array(data)
    #Attributes.append(attributes.split())

    f.close()
    
    
    

    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    

start = timeit.default_timer()
main(file)
stop = timeit.default_timer()
print(stop-start)