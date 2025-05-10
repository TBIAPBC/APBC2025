import sys
import re
import math


#

#Function for parameter input from file
def getPrMtr(numStr):
    inputPrMtr = [int(n) for n in numStr.strip().split(" ")]
    numCap = inputPrMtr[0]
    costLim = inputPrMtr[1]
    print(numCap,costLim)
    return numCap, costLim

#function for names of capitals
def getNameCap(numStr):
    nameCap = re.sub(r"\s+"," ", numStr).strip().split(" ")
    print(nameCap)
    return nameCap


#function for data to matrix
def getCostMatrix(numStr):
    cstMtrx = []
    hlpMtrx = []
    hlpMtrx2 = ""
    
    #Input matrix to formatted matrix
    for n in range(0,len(numStr)):
        hlpMtrx.clear()
        hlpMtrx2 = re.sub(r"\s+", " ",numStr[n].strip())
        hlpMtrx = hlpMtrx2.split(" ")
        
        #formatted matrix to int matrix
        for y in hlpMtrx:
            if(y == '-'):
                hlpMtrx.insert(hlpMtrx.index(y), 0)
                hlpMtrx.remove(y)
                continue
            hlpMtrx.insert(hlpMtrx.index(y), int(y))
            hlpMtrx.remove(y)
        cstMtrx.append(hlpMtrx.copy())
    
    return cstMtrx
        

#calculation of the cost        
def calcCost(cstMtrx, numCap, costLim, nameCap, rndNmbr):
    capList = {}
    capName = []
    
    for n in range(0,len(cstMtrx)):
        for i in range(n+1,len(cstMtrx[n])):
            if(cstMtrx[n][i] < costLim):
                capList.update({nameCap[n]+nameCap[i]:cstMtrx[n][i]})
    
    permuteDic(capList, numCap, rndNmbr)            
    
def permuteDic(capList, numCap, rndNmbr):
    if rndNmbr > 2:
        print("System exit rndNmbr Dic")
        sys.exit(1)
    if len(capList) < 10:
        print("Sytem exit capList < 10")
        sys.exit(1)
    hlpList = []
    cityList = []
    posiList = []
    hlpDic = capList.copy()
    pattern = ""
    wordThing = ''
    
    #List of all Keys of the dictonary
    for k in capList.keys():
        pattern += k + " "
    print(len(capList), "len capList")
    
    #looping while List is smaller than number of captials allowes it
    while(len(cityList) != numCap/2):
        print(hlpDic)
        
        #every word is removed after it is added to the list from remaining in the dictonary
        for k in hlpDic.keys():
            cityList.append(k)
            hlpDic.pop(k)
            for i in range(0,len(cityList[len(cityList)-1])):
                wordThing = cityList[len(cityList)-1][i]
                hlpList = re.findall(wordThing +'.', pattern)
                for n in hlpList:
                    if n in hlpDic:
                        hlpDic.pop(n)
            break
            
    if len(cityList) != 0:
        posiList.append(cityList.copy())
    print(posiList, "PosiList", len(capList), len(cityList))
    
    #call of the function to remove 1 city combination from the main dictonary
    if len(capList) > 4 and len(cityList)  > 3:
        permuteCity(capList, cityList, numCap, rndNmbr)
    else:
        print("System Exit permuDic")
        sys.exit(1)
    
    print(hlpList, hlpDic, capList, cityList, posiList)
    



"""Code loops for no reason, although I have added a counter to stop it after 5 cycles"""
def permuteCity(capList, cityList, numCap, rndNmbr):
    print(capList, cityList)
    if rndNmbr > 2:
        print("System exit rndNmbr city")
        sys.exit(1)
    if len(cityList) != 0:
        print(cityList[0])
        capList.pop(cityList[0])
        rndNmbr += 1
        print(capList, rndNmbr)
        permuteDic(capList, numCap, rndNmbr)
    else:
        sys.exit(1)



def main():
    
    argStr = sys.argv[1:]
    fileName = None
    numCap = None
    costLim = None
    optionO = False
    numStr = []
    nameCap = []
    numInt = []
    rndNmbr = 0
    
    
    #Fileinput block
    for arg in argStr:
        if arg == '-o':
            optionO = True
        else:
            fileName = arg
    
    if not fileName:
        print("Usage: Administration.py [-o] <filename>")
        sys.exit(1)
        
    try:    
        with open(fileName, "r") as data:
            for n in data.readlines():
                numStr.append(n)
    except IOError:
        print(f"Error: Cannot open file {fileName}")
        sys.exit(1)

    #call function for input parameter                          
    numCap, costLim = getPrMtr(numStr[0])                           #"""ONE BLOCK"""
    #call funtion for names of capitals
    nameCap = getNameCap(numStr[1])                             #"""TO ONE FUNCTION CALL"""
    #call function for cost matrix
    numInt = getCostMatrix(numStr[2:])                          #"""INPUT IS CLEAR DIVIDABLE"""
    
    #call function for cost calculations
    calcCost(numInt, numCap, costLim, nameCap, rndNmbr)
    
    
    #print(numInt)
    
        
if __name__ == '__main__':
    main()
    
    
