import sys
import re

class psdoGraph:    
    def __init__(self, pos = "#", NS = -999999.9, WE = -999999.9, path = -999999.9,   NSaj = "#", WEaj = "#", DIA = -999999.9, DIAaj = "#", prevN = "#", whereTo = "#", temp = -99999.9):
        self.pos = pos
        self.NSaj = NSaj
        self.WEaj = WEaj
        self.DIAaj = DIAaj
        self.prevN = prevN
        self.whereTo = whereTo
        self.path = path
        self.NS = NS
        self.WE = WE
        self.DIA = DIA
        self.temp = temp
    def __str__(self):
        return "pos: "+f"{self.pos}"+ ", NS: " +f"{self.NS}"+ ", NSaj: " +f"{self.NSaj}" + ", WE: " + f"{self.WE}"+ ", WEaj: " +f"{self.WEaj}" +", DIA: "+f"{self.DIA}"+", DIAaj: "+f"{self.DIAaj}" + ", path: " +f"{self.path}" + ", temp: " +f"{self.temp}" + ", prevN: " + f"{self.prevN}"+ ", whereTo: " + f"{self.whereTo}"



def mkGraph(Mtrx1, Mtrx2, Mtrx3, diag, trace):
    
    Graph = []
    diff_NM = len(Mtrx1[0]) - len(Mtrx2)
    diff_other = len(Mtrx2[0]) - len(Mtrx1)
    
    
    if(diag == False):
        Graph.append(psdoGraph("0 0", Mtrx1[0][0]  ,Mtrx2[0][0], 0,"1 0", "0 1"))
    else:
        Graph.append(psdoGraph("0 0", Mtrx1[0][0]  ,Mtrx2[0][0], 0 , "1 0", "0 1", Mtrx3[0][0], DIAaj = "1 1"))
        
    for n in range( (len(Mtrx1[0])) ):
        for i in range( (len(Mtrx2)+diff_NM) ):
            if(n == 0 and 0 < i < len(Mtrx1[0])-1):
                Graph.append(psdoGraph(str(0) + " " + str(i), Mtrx1[0][i]  ,Mtrx2[0][i], -1, str(1) + " "+ str(i), str(n) + " " +str(i+1), -2, str(1) + " " + str(i+1)))
                if(diag == True):
                    Graph[len(Graph)-1].DIAaj = str(n+1) + " " + str(i+1)
                    Graph[len(Graph)-1].DIA = Mtrx3[n][i]   
            elif(0 < i < len(Mtrx1[0])-1 and len(Mtrx2)-1 > n > 0):
                Graph.append(psdoGraph(str(n) + " " + str(i), Mtrx1[n][i]  ,Mtrx2[n][i], -1, str(n+1) + " "+ str(i), str(n) + " " +str(i+1), -2, str(n+1) + " " + str(i+1)))
                if(diag == True):
                    Graph[len(Graph)-1].DIAaj = str(n+1) + " " + str(i+1)
                    Graph[len(Graph)-1].DIA = Mtrx3[n][i]
            elif(i == 0 and len(Mtrx2)-1 > n > 0):
                Graph.append(psdoGraph(str(n) + " " + str(i), Mtrx1[n][i]  ,Mtrx2[n][i], -1, str(n+1) + " "+ str(i), str(n) + " " +str(i+1), -2, str(n+1) + " " + str(i+1)))
                if(diag == True):
                    Graph[len(Graph)-1].DIAaj = str(n+1) + " " + str(i+1)
                    Graph[len(Graph)-1].DIA = Mtrx3[n][i]
            if((i) == (len(Mtrx1[0])-1 ) and len(Mtrx2)-1 > n  ):
                Graph.append(psdoGraph(str(n) + " " + str(i), Mtrx1[n][i]  , -1, -1, str(n+1) + " "+ str(i), "#", -2))    
            if((n ) == (len(Mtrx2)-1) and  i < len(Mtrx1[0])-1 ):
                Graph.append(psdoGraph(str(n) + " " + str(i), -1  ,Mtrx2[n][i], -1, "#", str(n) + " " +str(i+1), -2))

    Graph.append(psdoGraph( str(len(Mtrx2)-1) + " " + str(len(Mtrx1[0])-1) ))      
                            
    BFSalgo(Graph,diag, trace)
 
def BFSalgo(Graph, diag, trace):
    Vis = []
    unVis = []
    Layer1 = []
    Layer2 = []
    
    for n in range(len(Graph)):
        if(n == 0):
            Vis.append(Graph[0])
            Vis[0].path = 0
            Vis[0].temp = 0
        else:
            unVis.append(Graph[n])
                 
    
    while(len(unVis) !=0):
        if(len(Vis) == 1):
            Layer1.append(Vis[0])
        for n in Layer1:
            for i in unVis[:]: 
                if(n.WEaj == i.pos):
                    if( i.path > n.path + n.WE):
                        continue
                    n.whereTo = "E"
                    i.path = n.path + n.WE                  
                    i.prevN = n.pos
                    Layer2.append(i)
                    Vis.append(i)
                    unVis.remove(i)
                elif(n.NSaj == i.pos):
                    if( i.path > n.path + n.NS):
                        continue
                    n.whereTo = "S"
                    i.path = n.path + n.NS                  
                    i.prevN = n.pos
                    Layer2.append(i)
                    Vis.append(i)
                    unVis.remove(i)
                elif(diag == True and n.DIAaj == i.pos):
                    if( i.path > n.path + n.DIA):
                        continue
                    n.whereTo = "D"
                    i.path = n.path + n.DIA
                    i.prevN = n.pos    
                    Layer2.append(i)
                    Vis.append(i)
                    unVis.remove(i)
                    

        for L2 in Layer2:
            for L1 in Layer1:
                if( L1.WEaj == L2.pos and (L2.path < L1.path + L1.WE) ):
                    L1.whereTo = "E"
                    L2.prevN = L1.pos
                    L2.path = L1.path + L1.WE
                elif(L1.NSaj == L2.pos and (L2.path < L1.path + L1.NS) ):
                    L1.whereTo = "S"
                    L2.prevN = L1.pos
                    L2.path = L1.path + L1.NS
                elif(diag == True and (L1.DIAaj == L2.pos and (L2.path < L1.path + L1.DIA)) ):
                    L1.whereTo = "D"
                    L2.prevN = L1.pos
                    L2.path = L1.path + L1.DIA


      
        if(len(Vis) < 5):
            if((Vis[0].NS > Vis[0].WE) and (Vis[0].NS > Vis[0].DIA)):
                Vis[0].whereTo = "S"
            if((Vis[0].WE > Vis[0].NS) and (Vis[0].WE > Vis[0].DIA)):
                Vis[0].whereTo = "E"  
            if((Vis[0].DIA > Vis[0].NS) and (Vis[0].DIA > Vis[0].WE)):
                Vis[0].whereTo = "D"    
    
        Layer1.clear()
        for n in Layer2:
            Layer1.append(n)
        Layer2.clear()
                
        
    calcPath(Graph, trace)
        
def calcPath(Graph,trace):
    tracing = []
    Graph.reverse()
    pathWhere = Graph[0].prevN 
    
    print(Graph[0].path)
  
    
    if(trace == True):
        while( pathWhere != "0 0" ):
            for n in Graph[:]:
                if(n.pos ==  pathWhere):
                    tracing.append(n.whereTo)
                    pathWhere = n.prevN
                    Graph.remove(n)
                    break
            if(pathWhere == "0 0"):
                tracing.append(Graph[len(Graph)-1].whereTo)
                break
                
    tracing.reverse()    
    for n in tracing:
        print(n, end = "")
    print()    
    
    
    
def cleanMe(strLines, diag, trace):
    bgMtrx = []
    Mtrx1 = []
    Mtrx2 = []
    Mtrx3 = []
    counter = 0
    
    for n in range(len(strLines)):
        bgMtrx.append(re.sub(r"\s+", " ",strLines[n]).split())
    
    
    for n in range(len(bgMtrx)):
        if((len(bgMtrx)-1) > n and bgMtrx[n][0][0] == "#" and bgMtrx[n+1][0][0] == "#"):
            del bgMtrx[n]
        if( bgMtrx[0][0] != "#"):
            bgMtrx.insert(0, "#")
        if( (len(bgMtrx)-1) > n > 0 and bgMtrx[n][0] != "#" and len(bgMtrx[n]) != len(bgMtrx[n+1])):
            bgMtrx.insert(n+1, "#")
        
    for n in range(0, len(bgMtrx), 1):
        if( bgMtrx[n][0][0] == "#" and bgMtrx[n+1][0][0] == "#"):
            continue
        for i in range(len(bgMtrx[n])):
            try:
                bgMtrx[n][i] = float(bgMtrx[n][i])
            except:
                continue
        if(bgMtrx[n][0] == "#"):
            counter += 1  
        if(counter == 1):
            if(bgMtrx[n][0] == "#"):
                continue
            Mtrx1.append(bgMtrx[n])
        elif(counter == 2):
            if(bgMtrx[n][0] == "#"):
                continue
            Mtrx2.append(bgMtrx[n])
        elif( diag == True and counter == 3):
            if(bgMtrx[n][0] == "#"):
                continue
            Mtrx3.append(bgMtrx[n])
    
    if( diag == True and len(Mtrx3) == 0):
        print("Error: -d Option, but no Diagonal Input Data")
        sys.exit(0)
    
    mkGraph(Mtrx1, Mtrx2, Mtrx3, diag, trace)



def main():

    fileInput = ""
    dataLines = []
    args = sys.argv[1:]
    Graph = []
    diag = False
    trace = False
    
    for arg in args:
        if(arg == "-d"):
            diag = True
        elif(arg == "-t"):
            trace = True
        else:
            fileInput = arg
    
    try:
        with open(fileInput, "r") as data:
            for lines in data.readlines():
                if( lines == "\n"):
                    continue
                if( lines[0] == "#" and len(lines) < 6):
                    continue
                dataLines.append(lines.strip())
    except(IOError):
        print("Error: File not found!")
        sys.exit(0)
    
    
    cleanMe(dataLines, diag, trace)    



if __name__ == '__main__':
	main()
