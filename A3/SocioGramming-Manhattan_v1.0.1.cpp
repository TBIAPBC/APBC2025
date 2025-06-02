#include <stdio.h>
#include <stdlib.h>
#include <vector>
#include <fstream>
#include <sstream>
#include <iostream>

using namespace std;




//##--------------------------------------------------------Class Function -----------------------------------------------------##
class psdoGraph{

  public:
    //values for the weights and path
    float NS = -9999999;
    float WE = -9999999;
    float DIA = -9999999;
    float path = -9999999;
    //values for the nodes and adjacent nodes, as previous node aswell 
    string pos = "#";
    string WEaj = "#";
    string NSaj = "#";
    string DIAaj = "#";
    string prevN = "#";
    string whereTo = "#";

};


//##--------------------------------------------------------Graph Function -----------------------------------------------------##
vector<psdoGraph> mkpsdGrph(vector<vector<float>>  cstMtrx, bool diag = false ){

  vector<psdoGraph> Graph = {};
  vector<vector<float>> NSM = {}, WEM = {}, DIAM = {};
  int counter = 0, mSize;
  
  
  //with the empty vector the separation of the matrices
  for( vector<float> data : cstMtrx){
    
    //counter for switch case 
    if(data.empty() == true){ 
        counter++;
        continue;
    }
    switch(counter){
      //for each case an ovn matrix
      case 0:
        NSM.push_back(data);
        break;
        
      case 1:
        WEM.push_back(data);
        break;
      
      case 2:
        DIAM.push_back(data);
        break;
        
      default:
        break;
    }
  }


  //for the case of HV2, where imho it is not possible to make a graph, as some NS point to nodes where there are none
  if(DIAM.empty() == false) diag = true;
  if( NSM[0].size() != WEM.size()){
      cout << "Test HV2, didn't understand to make it work"<< endl;
      exit(EXIT_FAILURE);
  }
 counter = 0;
 
 
 //here the creation of the pseudoGraph(with no build in functions)
 for(int n = 0; n < NSM[0].size(); n++){
    for(int i = 0; i < WEM.size(); i++){
        
        //while not at the bottom or the right outer corner weigth values, node position and adjacent nodes for the graph  
        if( n < NSM.size() && i < WEM[0].size()){
          psdoGraph Node;
          Graph.push_back(Node);
          Graph[counter].NS = NSM[n][i];
          Graph[counter].WE = WEM[n][i];
          Graph[counter].pos = to_string(n)  + " " + to_string(i);
          Graph[counter].NSaj = to_string(n+1)  + " " + to_string(i);
          Graph[counter].WEaj = to_string(n)  + " " + to_string(i+1);
          
         //if -d option 
          if(diag == true){
          Graph[counter].DIA = DIAM[n][i];
          Graph[counter].DIAaj = to_string(n+1)  + " " + to_string(i+1);
          }
          counter++;
        
        // special case for the rigth corner, as no West-east are possible 
        }else if( n < NSM.size()){
          psdoGraph Node;
          Graph.push_back(Node);
          Graph[counter].NS = NSM[n][i];
          Graph[counter].pos = to_string(n)  + " " + to_string(i);
          Graph[counter].NSaj = to_string(n+1)  + " " + to_string(i);
          counter++;
          
          
        // special case for the bottom, as no north-south are possible
        }else if(i < WEM[0].size()){
          psdoGraph Node;
          Graph.push_back(Node);
          Graph[counter].WE = WEM[n][i];
          Graph[counter].pos = to_string(n)  + " " + to_string(i);
          Graph[counter].WEaj = to_string(n)  + " " + to_string(i+1);
          counter++;
        
        //in every other case which actually should be possible
        }else{
          psdoGraph Node;
          Graph.push_back(Node);
          Graph[counter].pos = to_string(n)  + " " + to_string(i);
          counter++;
        }
    }
 }
 
  return Graph;

}



//##--------------------------------------------------------Data Cleaning -----------------------------------------------------##

vector<vector<float>> cleanMe(vector<vector<string>> strLines, bool diag){

  vector<vector<float>> Mtrx1 ={}, Mtrx2 = {}, Mtrx3 ={}, cstMtrx = {};
  stringstream floNr;
  int NrMtrx = 0, counter = 0;
  string temp;
  char del = ' ';

  //each line of the input file is cleaned here
  for(int n = 0; n < strLines.size(); n++){
      //all # lines are reduce to one, to make it easier to handle the matrix size
      if( n < strLines.size()-1 && strLines[n][0][0] == '#' && strLines[n+1][0][0] == '#'){
        strLines.erase(strLines.begin() + n);
        n--;
        continue;
      }
      
      //trimming the front of each line
      while(strLines[n][0][0] == ' '){
        strLines[n][0].erase(strLines[n][0].begin());
      }
      
      //trimming at the end of each line
      while(strLines[n][0][strLines[n][0].size()] == ' '){
        strLines[n][0].erase(strLines[n][0].end());
      }
      
      //reducing all whitespaces to one, for split function
      for( int i = 0; i < strLines[n].size(); i++){
          for( int u = 0; u < strLines[n][i].size()-1; u++){
              if(strLines[n][i][u] == ' ' && strLines[n][i][u+1] == ' '){
                strLines[n][i].erase(strLines[n][i].begin() +u);
                u--;
              }
          }
      }
    
  }
  
 //adding a # for the HV2 file, for handling such chases
  if( strLines[0][0][0] != '#'){
      for( int n = 0; n < strLines.size(); n++){
          if(strLines[n][0].size() != strLines[n+1][0].size()){
              strLines.insert(strLines.begin() + n +1, vector<string>());
              strLines[n+1].push_back("#");
              break;
          }
      }
  }

  
  //for loop to make float matrices
  for( int n = 0; n < strLines.size(); n++){
      //jumping over the first line
      if( n == 0 && strLines[n][0][0] == '#'){
          continue;
      // counter for switch case, to put each matrix into the rigth spot
      }else if(strLines[n][0][0] == '#'){
          NrMtrx++;
          if(diag == false && NrMtrx ==2) goto looper;
          counter = 0;
          continue;
      }
      
      //here the switch
      switch(NrMtrx){
        case 0:
          Mtrx1.push_back(vector<float>());
          
          //each line into a sstream
          floNr << strLines[n][0];
          
          //here a split function with type conversion to float
          while(getline(floNr, temp, del)){
              Mtrx1[counter].push_back(stof(temp));
          }
          floNr.clear();
          counter++;
          break;
        
        //same as case 0
        case 1:
          Mtrx2.push_back(vector<float>());
          floNr << strLines[n][0]; 
          while(getline(floNr, temp, del)){
              Mtrx2[counter].push_back(stof(temp));
          }
          floNr.clear();
          counter++;
          break;
        
        //same as case 0
        case 2:
          Mtrx3.push_back(vector<float>());
          floNr << strLines[n][0]; 
          
          while(getline(floNr, temp, del)){
              Mtrx3[counter].push_back(stof(temp));
          }
          floNr.clear();
          counter++;
          break;
          
        default:
          break;
      }
      
  }
  looper:
  
  
  //all matrices into one to return them for the next function, after each an empty vector, to separate them later more easly
  for(vector<float> data : Mtrx1){
    cstMtrx.push_back(data);
  }
  cstMtrx.push_back(vector<float>());

  for(vector<float> data : Mtrx2){
    cstMtrx.push_back(data);
  }

  if(Mtrx3.empty() == false){
      cstMtrx.push_back(vector<float>());
      for(vector<float> data : Mtrx3){
        cstMtrx.push_back(data);
      }
  }

  return cstMtrx;
}

//##--------------------------------------------------------MaxValue Path-----------------------------------------------------##

vector<psdoGraph> BFS_AlgoMax(vector<psdoGraph> Graph, bool diag){ 
  
  vector<psdoGraph> unVis ={};
  vector<psdoGraph> Layer1 = {};
  vector<psdoGraph> Layer2 = {};
  vector<psdoGraph> Vis ={};
  
 //first I made the assumption, that starting point and end are at the beginning and the end of the obj vector
 Graph[0].path = 0;
 unVis = Graph;
 
 //very inefficient BFS algo, but everything done from scratch
 while(unVis.empty() == false){
 
    
    //so the visit nodes is empty and the starting point at the beginning of the unvisited nodes
    if(Vis.empty() == true){
      Vis.push_back(unVis.front());
      unVis.erase(unVis.begin());
      
      //as the starting point had 3 clear adjacent nodes I need to find them
      for( int n = 0; n < unVis.size(); n++){
            
            //when I found them I gave them the position of the starting as previous node and the value for the path, as the direction
            if(Vis[0].WEaj == unVis[n].pos){
                unVis[n].prevN = Vis[0].pos;
                unVis[n].path = Vis[0].WE;
                unVis[n].whereTo = "E";
                
                //I push them into the visited nodes and into another layer for further preparation and deleted them from the unvisited
                Vis.push_back(unVis[n]);
                Layer1.push_back(unVis[n]);
                unVis.erase(unVis.begin() +n);
                
            }else if(Vis[0].NSaj == unVis[n].pos){
                unVis[n].prevN = Vis[0].pos;
                unVis[n].path = Vis[0].NS;
                unVis[n].whereTo = "S";
                Vis.push_back(unVis[n]);
                Layer1.push_back(unVis[n]);
                unVis.erase(unVis.begin() +n);
            
            //if -d option was activated
            }else if(diag == true && Vis[0].DIAaj == unVis[n].pos){
                unVis[n].prevN = Vis[0].pos;
                unVis[n].path = Vis[0].DIA;
                unVis[n].whereTo = "D";
                Vis.push_back(unVis[n]);
                Layer1.push_back(unVis[n]);
                unVis.erase(unVis.begin() +n);
   
            }         
      }
      
    }
    
  //this is the main loop until no unvisited nodes are left
  for(int n = 0; n < Layer1.size(); n++){
    
    //checking if the adjacent node is in unvisited and not "marked" already, setting all values pushing it into to next layer and erasing it from unvisited
    for(int i = 0; i < unVis.size();i++){
        if(Layer1[n].WEaj == unVis[i].pos){
            if(unVis[i].prevN == "#"){
              unVis[i].prevN = Layer1[n].pos;
              unVis[i].path = Layer1[n].path + Layer1[n].WE;
              unVis[i].whereTo = "E";
              Layer2.push_back(unVis[i]);
              unVis.erase(unVis.begin() +i);
            }
        }else if(Layer1[n].NSaj == unVis[i].pos){
            if(unVis[i].prevN == "#"){
              unVis[i].prevN = Layer1[n].pos;
              unVis[i].path = Layer1[n].path + Layer1[n].NS;
              unVis[i].whereTo = "S";
              Layer2.push_back(unVis[i]);
              unVis.erase(unVis.begin() +i);
            }
        }else if(diag == true && Layer1[n].DIAaj == unVis[i].pos){
            if(unVis[i].prevN == "#"){
              unVis[i].prevN = Layer1[n].pos;
              unVis[i].path = Layer1[n].path + Layer1[n].DIA;
              unVis[i].whereTo = "D";
              Layer2.push_back(unVis[i]);
              unVis.erase(unVis.begin() +i);
            }
        }
     
     
      }
  }
   
  //here the very inefficient part as I go through all the layers again to check for a better path
  for(int n = 0; n < Layer1.size(); n++){
    
    //I believe that it is possible to miss something
    for(int i = 0; i < Layer2.size();i++){
        if(Layer1[n].WEaj == Layer2[i].pos){
            if(Layer2[i].path < Layer1[n].path + Layer1[n].WE){
              Layer2[i].prevN = Layer1[n].pos;
              Layer2[i].path = Layer1[n].path + Layer1[n].WE;
              Layer2[i].whereTo = "E";
            }
        }else if(Layer1[n].NSaj == Layer2[i].pos){
            if(Layer2[i].path < Layer1[n].path +Layer1[n].NS){
              Layer2[i].prevN = Layer1[n].pos;
              Layer2[i].path = Layer1[n].path + Layer1[n].NS;
              Layer2[i].whereTo = "S";
            }
        }else if( diag == true && Layer1[n].DIAaj == Layer2[i].pos){
            if(Layer2[i].path < Layer1[n].DIA){
              Layer2[i].prevN = Layer1[n].pos;
              Layer2[i].path = Layer1[n].path +  Layer1[n].DIA;
              Layer2[i].whereTo = "D";
            }
        }
     
     
      }
  }   

  //pushing all from layer2 inte visited
  for( psdoGraph data: Layer2){
    Vis.push_back(data);
  }
  //making them the new layer1 for the next loop
  Layer1 = Layer2;
  //clearing the layer2 for the next loop
  Layer2.clear();

  }
 
 
  return Vis;

}


//##--------------------------------------------------------Calc Path -----------------------------------------------------##

void calcPath(vector<psdoGraph> Graph, bool trav){
  float path = Graph.back().path;
  string prev = Graph.back().prevN;
  vector<string> whereBeen = {};
  
  //backtracking the path for the directions
  if(trav == true){
      whereBeen.insert(whereBeen.begin(), Graph.back().whereTo);
      while( prev != "0 0"){
          for(int n = 0; n <  Graph.size(); n++ ){
              if(prev == Graph[n].pos){ 
                  prev = Graph[n].prevN;
                  whereBeen.insert(whereBeen.begin(), Graph[n].whereTo);
                  Graph.erase(Graph.begin()  + n);
                  break;
              }
          }
   
      }
  
  }

  //STDOUT
  cout << path << endl;
  if(trav == true){
    for(string data : whereBeen){
      cout << data;
    }
    cout << endl;
  }

}


//##--------------------------------------------------------Main Function -----------------------------------------------------##

int main(int argc, char *argv[]){
  vector<psdoGraph> Graph = {};
  vector<vector<string>> strLines = {};
  vector<vector<float>> cstMtrx = {};
  string inFile = " ", line = "", Nmbr = "";
  int counter = 0;
  bool diag = false;
  bool trav = false;
  
  try{
    for(int n = 1; n < argc; n++){
      if(argv[n][0] == '-' && argv[n][1] == 'd'){
          diag = true;
      }else if(argv[n][0] == '-' && argv[n][1] == 't'){
          trav = true;
      }else{
          inFile = argv[n];
      }
    }
  }catch(...){
      cout << "Wrong input format: [Option] <filename>" << endl;
  }
  
  try{
    ifstream dataLine(inFile);
    while(getline(dataLine, line)){
        if(line.size() == 0)continue;
        
        //each line directly in a vector (preparation would have been possible here already)
        strLines.push_back(vector<string>());
        strLines[counter].push_back(line);
        counter++;
    }
  }catch(...){
      cout << "Error: input file not found"<< endl;
  }
    
  
  //call for function to prepare data for Graph
  cstMtrx = cleanMe(strLines, diag);
  //call of function to make pseudoGraph with own class and creation design
  Graph = mkpsdGrph(cstMtrx, diag);
  //call of function to calculate max path with handwritten (inefficient) BFS algo
  Graph = BFS_AlgoMax(Graph, diag);
  //call of function for output
  calcPath(Graph, trav); 
  
  
  return 0;
}
