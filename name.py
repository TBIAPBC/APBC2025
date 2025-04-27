import sys
import math


# - - - - - - - - - READ COMMAND-LINE ARGUMENTS - - - - - - - - - 

try:
    inputfilename = (sys.argv[1])                             #saves name of inputfile as string
except IndexError:
    print("Too few arguments, inputfile is needed.")
try:                                                    #Optimization or Enumeration?
    if sys.argv[2] == "-o":
        OptimizationMode = True
        EnumerationMode = False
except IndexError:
    EnumerationMode = True
    OptimizationMode = False



# - - - - - - - - - READ INPUTFILE - - - - - - - - - 

with open (inputfilename , "r") as inputfile:
    
    lines = inputfile.readlines()                       #lines is a list

    #READ LINE 1 (NUMBER OF CITIES, COST LIMIT)
    line0 = lines[0].strip()                            #remove blank spaces
    line0 = line0.split()                               #split line0: a list is created, every part of line 1 gets its own index
    NumberOfCities = int(line0[0])
    CostLimit = int(line0[1])


    #READ LINE 2 (CITY NAMES)
    line1 = lines[1].split('#')                         #split the string at '#' into 2 substrings
    line1 = line1[0]                                    #now line1 contains only everything before the #
    line1 = line1.strip()                               #remove blank spaces
    CityNamesList = line1.split()                       #split line1: a list is created, every part of line 2 gets its own index
    #transform into dictionary
    CityNames = {}
    for index, value in enumerate(CityNamesList):           #.enumerate() iterates over index + value simultaniously
        CityNames.update({f"{value}": f"{index}"})          #we have a dict now, with the following format: "B" (key), "0" (Value)


    #READ LINE 3 TO N (COST MATRIX)
    CostMatrix = []                                         #CostMatrix[0][1] shows the cost of the city-pair with indices 0 and 1 (indicies according to CityNames-dictionary)
    
    for i in range(NumberOfCities):                         #this loop creates line by line
        i2 = i + 2                                          #skip the first 2 lines (not part of cost matrix)
        CostsRow = lines[i2].split('#')
        CostsRow = CostsRow[0]
        CostsRow = CostsRow.strip()
        CostsRowList = CostsRow.split()

        for i in range(len(CostsRowList)):                         
            if CostsRowList[i] == "-":                      #convert "-" to positive infinity (it´s not a real pair)
                CostsRowList[i] = math.inf                  
            else:
                CostsRowList[i] = int(CostsRowList[i])      #convert strings to int

        CostMatrix.append(CostsRowList)                     #append the line to the costmatrix



    #important objects: CityNames, CostMatrix, CostLimit




# - - - - - - - - - ENUMERATION-FUNCTION  - - - - - - - - - 

def EnumeratePairs(UnpairedCities, CurrentPartition, CurrentCost, AllSolutions):
     
    if len(UnpairedCities) == 0:                            
        SortedPartition = sorted([sorted(pair) for pair in CurrentPartition])
        if CurrentPartition not in AllSolutions:
            AllSolutions.append(CurrentPartition)
        return

    city1 = min(UnpairedCities)                             #UnpairedCities is the Set, containing Names only. A key is assigned to city1 
    RemainingCities = UnpairedCities - {city1}

    for city2 in RemainingCities:
        pair = sorted([city1, city2])                       #use sorted() to make avoid duplicates (so to not calculate both AB and BA)
        index1 = int(CityNames[city1])                      #get index from dictionary. 
        index2 = int(CityNames[city2])
        cost = CostMatrix[index1][index2]                   

        if CurrentCost + cost <= CostLimit:                    #the bound-strategy: only continue, if there is a chanche for success
            EnumeratePairs(RemainingCities - {city2}, 
                                CurrentPartition + [pair],
                                CurrentCost + cost,
                                AllSolutions)





# - - - - - - - - - OPTIMIZATION-FUNCTION  - - - - - - - - - 

def OptimalPairs(UnpairedCities, CurrentPartition, CurrentCost, BestSolutionCost, BestSolution):
     
    if len(UnpairedCities) == 0:                            
        if CurrentCost < BestSolutionCost[0]:
            BestSolutionCost[0] = CurrentCost
            BestSolution[:] = CurrentPartition
        return BestSolutionCost[0]


    city1 = min(UnpairedCities)                             #UnpairedCities is the Set, containing Names only. A key is assigned to city1 
    RemainingCities = UnpairedCities - {city1}

    for city2 in RemainingCities:
        pair = sorted([city1, city2])                       #use sorted() to make avoid duplicates (so to not calculate both AB and BA)
        index1 = int(CityNames[city1])                      #get index from dictionary. 
        index2 = int(CityNames[city2])
        cost = CostMatrix[index1][index2]                   

        if CurrentCost + cost < BestSolutionCost[0]:           #the bound-strategy: only continue, if there is a chanche for success
            BestSolutionCost[0] = OptimalPairs(RemainingCities - {city2}, 
                                CurrentPartition + [pair],
                                CurrentCost + cost,
                                BestSolutionCost,
                                BestSolution)
    
    return BestSolutionCost[0]



# - - - - - - - - - MASTER-FUNCTION  - - - - - - - - - 


def MasterFunction(CityNames, CostMatrix, CostLimit, EnumerationMode, OptimizationMode):
    CitySet = set(CityNames.keys())                       #create a Set containing only the city names
    
    if EnumerationMode:
        AllSolutions = []
        EnumeratePairs(CitySet, [], 0, AllSolutions)     #start the function with empty CurrentPartition, CurrentCost = 0
        FormattedSolutions = set()
        for solution in AllSolutions:
            SortedPairs = sorted(["".join(sorted(pair)) for pair in solution])
            FormattedSolution = " ".join(SortedPairs)
            FormattedSolutions.add(FormattedSolution)
    
    elif OptimizationMode:
        BestSolutionCost = [CostLimit]
        BestSolution = []
        OptimalPairs(CitySet, [], 0, BestSolutionCost, BestSolution)

    # - - - print solution - - - 
    if EnumerationMode:
        for solution in sorted(list(FormattedSolutions)):
            print(solution)
    elif OptimizationMode:
        print(BestSolutionCost[0])



# - - - - - - - - - CALL FUNCTIONS  - - - - - - - - - 
MasterFunction(CityNames, CostMatrix, CostLimit, EnumerationMode, OptimizationMode)




    