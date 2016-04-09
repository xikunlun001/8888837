## Author Xi Chen
import numpy as np
import re
import StringIO
import pprint


file = "test.txt"

def isFloat(str):
    
    try:
        float(str)
        return True
    except ValueError:
        return False
        
        
def parseData(file):
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

    desicion = table[:,-1]
    data = table[:,:-1]
    data =data.tolist()
    for i in data:
        for n,j in enumerate(i):
            if isFloat(j) == True:
                i[n] = float(j)
                
                
    data = np.array(data)
    print data

    

    
    #data = np.array(data)
    #Attributes.append(attributes.split())

    f.close()


parseData(file)
