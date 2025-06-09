import sys
import re
import networkx as nx

def getMtrx(dataLines, dignl):
    print(dignl)
    lineNmbr = 0
    lenMtrx = 0
    counter = False
    frstMtrx = []
    hlpMtrx = []
    strMtrx1 = []
    strMtrx2 = []
    strMtrx3 = []
    
    for lines in dataLines:
        if(lines[0] != '#' and lines[0] != '\n'):
            frstMtrx.append(re.sub(r"\s+", " ",lines.strip()))
        elif(len(frstMtrx) != 0 and frstMtrx[len(frstMtrx)-1] == '#'):
            continue
        else:
            frstMtrx.append("#")
    if(dignl != True):        
        for n in range(len(frstMtrx)):
            if( frstMtrx[n][0] == '#'):
                continue
            elif(n > 3 and len(frstMtrx[n].split(" ")) != lineNmbr):
                hlpMtrx = frstMtrx[n].split(" ")
                strMtrx2.append(list(map(int, hlpMtrx)))
            else:
                hlpMtrx = frstMtrx[n].split(" ")
                strMtrx1.append(list(map(int, hlpMtrx)))
                lineNmbr = len(strMtrx1[0])
    if(dignl == True):        
        for n in range(len(frstMtrx)):
            if( frstMtrx[n][0] == '#'):
                lineNmbr += 1
            elif(lineNmbr == 1):
                hlpMtrx = frstMtrx[n].split(" ")
                strMtrx1.append(list(map(float, hlpMtrx)))
            elif(lineNmbr == 2):
                hlpMtrx = frstMtrx[n].split(" ")
                strMtrx2.append(list(map(float, hlpMtrx)))
            elif(lineNmbr ==3):
                hlpMtrx = frstMtrx[n].split(" ")
                strMtrx3.append(list(map(float, hlpMtrx)))
       
    if(dignl != True):
        getDMX(dignl, strMtrx1, strMtrx2)
    else:
        getDMX(dignl, strMtrx1, strMtrx2, strMtrx3)
 
 
 
def getDMX(dignl, strMtrx1, strMtrx2, *args):
    if len(args) != 0:
        strMtrx3 = args[0]
    
    graph = nx.DiGraph()
    print(len(strMtrx1), " ",len(strMtrx1[0]), "\n",len(strMtrx2), " ",len(strMtrx2[0]))
    
    if(dignl != True):
        for n in range(0,len(strMtrx1[0])+1):
            for i in range(0,len(strMtrx2)+1):
                x = str(n) + " " + str(i)
                y = str(n) + " " + str(i+1)
                if( i+1 < len(strMtrx2)+1 and n < len(strMtrx1[0])+1):
                    graph.add_edges_from(x, y)
                    #print(strMtrx2[n][i])
                    print(x," ", y)
                x = str(n) + " " + str(i)
                y = str(n+1) + " " + str(i)
                if (n+1 < len(strMtrx1[0])+1 and i < len(strMtrx2)+1):
                    print(x," ", y, "\n")
                    #print(strMtrx1[i])
                    graph.add_edges_from(x, y)
                

                
    print(graph, graph.nodes(), graph.edges())
    
    
            
        
def main():
    dataLines = []
    args = sys.argv[1:]
    delim = False
    oprtrMtrx = False
    fileName = ""
    dirGraph = nx.DiGraph()
    
    for arg in args:
        if arg == "-d":
            delim = True
        else:
            fileName = arg

    try:
        with open(fileName, "r") as data:
            dataLines = data.readlines()
            
    except IOError:
        print(f"Error: Cannot open File {fileName}") ###need input dataname
        sys.exit(1)
        
    if(re.search(".*HVD.*", fileName)):
        oprtrMtrx = True
        
    getMtrx(dataLines, oprtrMtrx)




if __name__ == '__main__':
    main()
