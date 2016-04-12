## Author Xi Chen
import numpy as np
import re
import StringIO
import pprint
import timeit


file = "lastdata.txt"

def isFloat(str):
    
    try:
        float(str)
        return True
    except ValueError:
        return False
        
        
def findD(decision, table):
    decisionSet = []
    uniqueD = np.unique(decision)   # may also use set
    #uniqueD = list(uniqueD)
    for i in uniqueD:
        decisionSet.append(np.array(np.where(table == i)[0]))
    
    return decisionSet
        
def findA(data):
    attriSet =[]
    for column in data.T:
        uniqueA = np.unique(column)   # may also use set but need tolist()
        for i in uniqueA:
            attriSet.append(np.array(np.where(column == i)[0]))
    return attriSet
        

def bigA(data):
    bigA = []
    #transA = data.astype(np.str)
    transData = np.row_stack(data)
    transList = transData.tolist()
    
    uniqueData = [list(x) for x in set(tuple(x) for x in transList)]
    #print uniqueData[0]
    for i in uniqueData:
        bigA.append([j for j,x in enumerate(transList) if x ==i])
        
    #print bigA
        
        

    

        
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
    attributes = attributes[1:-1]
    attriNum = len(attributes)
    
    
    dataset = re.sub(r'(\<[\s\S]*\])','', messData)

    dataset = re.split(r'\s+', dataset)
    dataset = dataset [1:]
    
  
            
            
    #print dataset
    
    n = len(dataset)/attriNum
    print n
    
    table = [list(t) for t in zip(*[iter(dataset)]*attriNum)]
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

    bigA(data)

    #data = np.array(data)
    #Attributes.append(attributes.split())

    f.close()
    
    
    

    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    

start = timeit.default_timer()
main(file)
stop = timeit.default_timer()
print(stop-start)
