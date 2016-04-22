## Author Xi Chen
import numpy as np
import re
import StringIO
import pprint
import timeit
import copy
import itertools


file = "keller-train-ca.txt"

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
    #print decisionSet
    return decisionSet
    
def findDvalue(decision,table):
    dSet=[]
    decisionValue = np.unique(decision).tolist()

    #print decisionValue
    return decisionValue
    

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
        if type(column[0].item()) == float:
            
            uniqueValue = np.unique(column)
            uniqueValue.sort()
            #uniqueCopy = uniqueValue[1:]
            valueCol =[]
            indexCol =[]
            for m, i in enumerate(uniqueValue):
                # output ((a,v))
                #print "n", n
                #print m
                if m == (len(uniqueValue)-1):
                    break
                cutpoint = (uniqueValue[m]+uniqueValue[m+1])/2
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
            
        else:
            uniqueA = np.unique(column)   # may also use set but need tolist()
            columnSetIndex =[]
            columnSetValue =[]
            for i in uniqueA:
                #attriSet.append(np.array(np.where(column == i)[0].tolist()))
    
                columnSetIndex.append(np.where(column == i)[0].tolist())
                value = "("+str(attributes[n])+","+str(i)+")"
                columnSetValue.append(value)
            #print columnSetValue
            indexAV.append(columnSetIndex)
            #print attriSetIndex
            valueAV.append(columnSetValue)
 
            
        
    
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
            
            upperSet[x][n] = j
    for n,i in enumerate(upperSet):
        upperSet[n] =list(itertools.chain(*upperSet[n]))
        upperSet[n] = list(set(upperSet[n]))
    #print upperSet  
    return upperSet

# lower set of decision set   


def lower(decisionSet, bigASet):
    lowerSet = []
    dCopy = copy.deepcopy(decisionSet)
    
    for x, decision in enumerate(decisionSet):
        for n,i in enumerate(decision):
            for m,j in enumerate(bigASet):
                if i in j:
                    break
            if set(bigASet[m]).union(decision) != set(decision):
                dCopy[x][n] ="needToDel"
    for i in dCopy:
        lowerSet.append([item for item in i if item != "needToDel"])
        
    #print lowerSet
    return lowerSet
            
    
    
    
""""     
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
"""

# find data is numerical or symbolic
def typeOfData(data):
    
    if type(data[0][0]) != float:
        numerical =0
    if type(data[0][0]) == float:
        numerical =1
        
    return numerical
      
# LEM2  B-- is upper or lower set of decision set
def LEM2(B, attriSet, data, decisionName):
    

    # extract (a,v) and [(a,v)] from attriSet
    attriValue = attriSet[0]
    attriIndex = attriSet[1]
    
    # The rule set list
    All_rules =[]
    print "B", len(B)
    
    # b is every decision set in all decisions
    for s,b in enumerate(B,start=0):
        T_rules=[]
        T_rules_index=[]
        G = copy.deepcopy(b)
        
        print "---------------------------------"
        #print G
    
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
                if list(set(i).intersection(G)) != []:
                    T_G.append(attriValueCopy[n])
                    T_G_Index.append(i)
                    
                    #dic_T_G = dict(zip(T_G, T_G_Index))
                    

                    

                
            while T ==[] or inT.union(b) != set(b):
                #find Max length

                #(set.intersection(*map(set, TIndex))).union(b) == set(b)
                findMax =[]
                
                for i in T_G_Index:
                    findMax.append(len(list(set(i).intersection(G))))
                
                MaxValue = max(findMax)
                findMax = np.array(findMax)
                MaxIndices = np.where((findMax == MaxValue))[0]
                #print "yes"
                if len(MaxIndices) == 1:
                    select_t_value = T_G[MaxIndices[0]]
                    select_t_index = T_G_Index[MaxIndices[0]]
                    
                
                bestIndices =[]
                #print "yes"
                if len(MaxIndices) >1:
                    #print T_G_Index
                    #print MaxIndices
                    candidateIndices = MaxIndices
                    candidateLength = np.array([len(T_G_Index[i]) for i in MaxIndices])
                    #print "yes"
                    #print candidateLength
                    #print np.array([len(T_G_Index[i]) for i in MaxIndices])
                    MinLength = min(candidateLength)
 
                    for n,i in enumerate(candidateLength):
                        #print "no"
                        if i == MinLength:
                            selectedIndex = candidateIndices[n]
                            break
                    
                    select_t_value = T_G[selectedIndex]
                    select_t_index = T_G_Index[selectedIndex]

                  
                T.append(select_t_value)
                #print T_G
                #print "select value", select_t_value
                TIndex.append(select_t_index)
                #print T_G; print T_G_Index
                #print G
                G = list(set(select_t_index).intersection(G))
                #print "G", G
                
                T_G_Copy =[]
                T_G_Index_Copy =[]
                for n, i in enumerate(T_G_Index):
                    if set(i).intersection(G) !=[]:
                        T_G_Copy.append(T_G[n])
                        T_G_Index_Copy.append(i)
                        
                #print T_G_Copy; print T_G_Index_Copy
                #print T_G_Copy
                #print T
                #print T_G
                T_G =[item for item in T_G_Copy if item not in T]
                #print T_G
                T_G_Index = [T_G_Index_Copy[n] for n,item in enumerate(T_G_Copy) if item not in T]
                #print T_G_Index
                inT =set.intersection(*map(set, TIndex))
                #print len(inT), inT.union(b) == set(b)
                # end while loop
    
            
            #T_Zip = zip(T,TInex)
            TIndex_Copy=copy.deepcopy(TIndex)
            T2= copy.deepcopy(TIndex_Copy)
            final_T_Index=[]
            #print TIndex
            #print TIndex_Copy
            #print "start for"
            for n, i in enumerate(TIndex):
                if len(TIndex_Copy) <=1:
                    #print "gunima"
                    break
                #print TIndex_Copy

                TIndex_Copy.remove(i)
                #print n
                #print TIndex_Copy
                RealT = list(set.intersection(*map(set, TIndex_Copy)))
                #print RealT

                #print RealT
                if set(RealT).union(b) ==set(b):
                    #print "yes"
                    final_T_Index.append(n)
                    #TIndex_Copy = T2
                    T2 = copy.deepcopy(TIndex_Copy)
                else:
                    #print "yes"
                    TIndex_Copy = copy.deepcopy(T2)
                    #print TIndex_Copy
            #print final_T_Index
            #print TIndex_Copy
            #print final_T_Index
            #print T
            if final_T_Index ==[]:
                T=T
                TIndex =TIndex
            else:
                T = [i for j,i in enumerate(T) if j not in final_T_Index]
                #print T
                TIndex = TIndex_Copy
            #print T
            #print TIndex
            oneDecisionRule  = '&'.join(map(str, T)) +"-->"+ str(decisionName[s])
            #print oneDecisionRule
            
            T_rules.append(oneDecisionRule)
            #print T
            #print TIndex
            #print T_rules
            
            intersectionTIndex = list(set.intersection(*map(set, TIndex)))
            T_rules_index.append(intersectionTIndex)
            
            #print G
            #G= [item for item in b if item not in list(set.union(*map(set, T_rules_index)))]
            G= list(set(b) -set.union(*map(set, T_rules_index)))
            
            #print "G" , G
        for i in T_rules:
            print i
            
            # end of while loop
            
        
                
                    



        
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
    decisionName = findDvalue(decision,table)


# calculate A*
    #attriA = findA(data, attributes)

    bigASet = bigA(data)
    #print bigASet
    
    data.tolist()

    print type(data[0][0].item())
 

    upperSet = upper(decisionSet, bigASet)
    #print upperSet

    lowerSet =lower(decisionSet, bigASet)
    
    #if type(data[0][0].item()) == float:
    attriA = cutpointFindA(data, attributes)
        #print "calculating cut points..."
        
    #print attriA[0]
    
    LEM2(lowerSet, attriA, data, decisionName)

    #cutpointFindA(data, attributes)
    
    #data = np.array(data)
    #Attributes.append(attributes.split())

    f.close()
    
    
    

    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    

start = timeit.default_timer()
main(file)
stop = timeit.default_timer()
print(stop-start)
