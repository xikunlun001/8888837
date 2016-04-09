## Author Xi Chen
import numpy as np
import re
import StringIO
import pprint


file = "test.txt"
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
    #caonima = re.split(r'\s+', caonima)
    attributes = re.split(r'\s+', attributes[0])
    attributes = attributes[1:-1]
    attriNum = len(attributes)
    
    
    dataset = re.sub(r'(\<[\s\S]*\])','', messData)

    dataset = re.split(r'\s+', dataset)
    dataset = dataset [1:]
    print dataset
    
    n = len(dataset)/attriNum
    print n
    
    data = [list(t) for t in zip(*[iter(dataset)]*attriNum)]
    data = np.array(data)
    print data
    

    
    #data = np.array(data)
    #Attributes.append(attributes.split())

    f.close()


parseData(file)