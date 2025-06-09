import java.io.*;
import java.util.*;
import org.jgrapht.*;
import org.jgrapht.Graph;
import org.jgrapht.graph.*;
import org.jgrapht.alg.shortestpath.*;



public class SocioGramming_Manhattan_Project_v_0_197 {
    
    
    
    

//#----------------------------------------------MAIN FUNCTION-----------------------------------------------------#

     private static void getMtrx(ArrayList<String> iptLst){
    ArrayList<String> strMtrx = new ArrayList<>();
    ArrayList<ArrayList<Float>> Mtrx1 = new ArrayList<>();
    ArrayList<ArrayList<Float>> Mtrx2 = new ArrayList<>();
    ArrayList<ArrayList<Float>> Mtrx3 = new ArrayList<>();
    String anore = "";
    int counter = 0, nmbrMtrx = 1;
    
    for(int n = 0; n < iptLst.size(); n++){
        counter = iptLst.size();
        if(n < counter){
            if(iptLst.get(n).length() == 0){
                iptLst.remove(n);
                continue;
            }
            else if(iptLst.get(n).length() > 2 && iptLst.get(n).charAt(0) == '#' && iptLst.get(n).charAt(1) == '#'){
                  iptLst.remove(n);
                  continue;
            }
            else  if(n> 1 && n < counter && iptLst.get(n).charAt(0) == '#' && iptLst.get(n-1).charAt(0) == '#'){
                  continue;
              }
              else{
                  strMtrx.add(iptLst.get(n));
          }
        }
        else{
            break;
        }
    }
    counter = 0;
    
    for(int n = 0; n < strMtrx.size(); n++){
        if(strMtrx.get(n).charAt(0) == '#' ){
          continue;
        }
        else if(n > 2 && strMtrx.get(n).length() != strMtrx.get(n-1).length()){
          nmbrMtrx +=1;
          counter = 0;
        }
        if(strMtrx.get(n).charAt(0) != '#'){
          if(nmbrMtrx == 1){
                Mtrx1.add(new ArrayList<Float>());                
                for(String mtrx : strMtrx.get(n).trim().replaceAll("[ ]+"," ").split(" ")){
                  Mtrx1.get(counter).add(Float.parseFloat(mtrx));
          
             }
              counter += 1;
          }
          else if(nmbrMtrx == 2){
                Mtrx2.add(new ArrayList<Float>());
                for(String mtrx : strMtrx.get(n).trim().replaceAll("[ ]+"," ").split(" ")){
                  Mtrx2.get(counter).add(Float.parseFloat(mtrx));
          
              }
              counter += 1;
          }
          else if(nmbrMtrx == 3){
                Mtrx3.add(new ArrayList<Float>());
                for(String mtrx : strMtrx.get(n).trim().replaceAll("[ ]+"," ").split(" ")){
                  Mtrx3.get(counter).add(Float.parseFloat(mtrx));
          
              }
              counter += 1;
          }
        }
    }
    
    getPath(Mtrx1, Mtrx2, Mtrx3);
    
  }
     
 

//#----------------------------------------------Function for Graph-----------------------------------------------------#    

 public static void getPath(ArrayList<ArrayList<Float>> Mtrx1, ArrayList<ArrayList<Float>> Mtrx2, ArrayList<ArrayList<Float>> Mtrx3){
    
     
    SimpleDirectedWeightedGraph<String, DefaultWeightedEdge> diGraph = new SimpleDirectedWeightedGraph<String, DefaultWeightedEdge>(DefaultWeightedEdge.class);
     var vertex = "";
     var edgeWE = "";
     var edgeNS = "";
     var edgeDIA = "";
     var start = "";
     var end = "";

    
    for(int n = 0; n <  Mtrx1.get(0).size(); n++){
        for(int i = 0; i < Mtrx2.size(); i++){
            vertex = String.valueOf(n)+ " " + String.valueOf(i);
            diGraph.addVertex(vertex);
            
        }
    }
    
    for(int n = 0; n <  Mtrx1.get(0).size(); n++){
        for(int i = 0; i < Mtrx2.size()-1; i++){
            if(n < Mtrx1.get(0).size()-1){
            vertex = String.valueOf(n)+ " " + String.valueOf(i);
            edgeWE = String.valueOf(n)+ " " + String.valueOf(i+1);;
            edgeNS = String.valueOf(n+1)+ " " + String.valueOf(i);;
            DefaultWeightedEdge e1 = diGraph.addEdge(vertex, edgeNS);
            diGraph.setEdgeWeight(e1, -Mtrx1.get(n).get(i));
            DefaultWeightedEdge e2 = diGraph.addEdge(vertex, edgeWE);
            diGraph.setEdgeWeight(e2, -Mtrx2.get(n).get(i));
           }
            else{
                vertex = String.valueOf(n)+ " " + String.valueOf(i);
                edgeWE = String.valueOf(n)+ " " + String.valueOf(i+1);;
                DefaultWeightedEdge e2 = diGraph.addEdge(vertex, edgeWE);
                diGraph.setEdgeWeight(e2, -Mtrx2.get(n).get(i));
               }
            
        
        }
    }
    
    start = "0 0";
    end = String.valueOf(Mtrx1.get(0).size())+ " " + String.valueOf(Mtrx2.size());
    
    
    //DijkstraShortestPath<String, DefaultWeightedEdge> p = new DijkstraShortestPath<String, DefaultWeightedEdge>(diGraph, start, end);
    //System.out.println(p.getPathEdgeList());
  
  
  for (DefaultWeightedEdge edge : diGraph.edgeSet()) {
        System.out.println(diGraph.getEdgeSource(edge) + " --> " + diGraph.getEdgeTarget(edge) + " (weight: " + diGraph.getEdgeWeight(edge) + ")");
    }
    
 }    
     


//#----------------------------------------------MAIN FUNCTION-----------------------------------------------------#

	public static void main(String[] args){
	  var iptDt = "";
	  boolean optionD = false;
	  ArrayList<String> dataLst = new ArrayList<String>();
	
	
	  for(String arg : args){
	      try{
	          if(arg.equals("-d")) optionD = true;
	          else{
	              iptDt = arg;
	          }
	      }
	      
	      catch(Exception e){
	          e.printStackTrace();
	      }
	  }
	
	
	  try{
        
        File input = new File(iptDt);
        Scanner inData = new Scanner(input);
        while(inData.hasNextLine()){
            dataLst.add(inData.nextLine());
        }	
	  }
	  
	  catch(IOException e){
	      e.printStackTrace();
	  }
	
	
	  getMtrx(dataLst);
	  /*for(String data : dataLst){
	      System.out.println(data);
	  }*/
	
	
	
	
	
	
	}
}

