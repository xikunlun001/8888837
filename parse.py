## Author Xi Chen
import numpy as np

def parseData(file):
    myData =[]
    f = open(file, 'r')
    
    for line in f:
        if (line[0] != "<") and ("!" not in line) and (line.strip()):
            
            if line[0] != "[":
                myData.append(line.split())
            else:
                line = line[:-2]
                line = line[1:]
                #print line
                myData.append(line.split())
  
            
    myData = np.array(myData)
    
    print myData[:,0]
    print myData
    return myData
        
        
        
        
parseData("test.txt")