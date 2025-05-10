import java.util.*;
import java.io.*;

public class SocioGramming_Administration
{
  
  //function to get first inputline
  private static ArrayList<Integer> getCost(String costLine)
  {
    ArrayList<Integer> costList = new ArrayList<>();
    
    //spliting the input string to integer list
    costLine = costLine.trim();
    for(String cst : costLine.split(" "))
    {
      costList.add(Integer.parseInt(cst));
    }
    
    costList.add(costList.get(1)-(costList.get(0)/2-1)); //Calculation for max cost of one Citypair, no matter the input
    
    
    return costList;
  }


  //function to get city names
  private static ArrayList<Character> getcapName(String capName)
  {
    ArrayList<Character> capList = new ArrayList<>();
    
    
    //processing the string input to a list of city names
    capName = capName.trim().replaceAll("  ", " "); 
    for(String cst : capName.split(" "))
    {
      capList.add(cst.charAt(0));
    }
  
    
    return capList;
  }
  
  //function for integer 2d arraylist from cost matrix
  private static ArrayList<ArrayList <Integer>> getMtrx(String Mtrx)
  {
  ArrayList<ArrayList<Integer>> cstMtrx = new ArrayList<>(); 
  ArrayList<String> strMtrx = new ArrayList<String>();
  
    //prepairing the input string matrix for integer 2d arraylist
    Mtrx = Mtrx.replaceAll("-", "0");
    Mtrx.trim();
    Mtrx = Mtrx.replaceAll("  ", " ");
    for(String cst : Mtrx.split("\n"))
    {
      strMtrx.add(cst);
    }
  
    
    //adapting the string list to integer 2d arraylist
    for(int n = 0; n < strMtrx.size(); n++)
    {
      cstMtrx.add(new ArrayList<Integer>());
      strMtrx.set(n, strMtrx.get(n).trim());
      for(String cst : strMtrx.get(n).split(" "))
      {
        cstMtrx.get(n).add(Integer.parseInt(cst));
      }
    }
   
    return cstMtrx;
  
  }
  
  
  //function for dictonary with city combination and cost
  private static Map<String, Integer> getDic( ArrayList<ArrayList <Integer>> cstMtrx, ArrayList<Character> capList, ArrayList<Integer> cstList)
  {
  
    Map<String, Integer> cityDic = new TreeMap<>();
    int lenMtrx = cstList.get(0);
    int maxCst = cstList.get(2);
    int mtrCst;
    String key = "";

    
    //processing the 2d arraylist with the cost with the list of city names to a dictonary
    for(int n = 0; n < cstMtrx.size(); n++)
    {
      
      for(int i = n+1; i < cstMtrx.get(n).size(); i++)
      {
        key = "";
        key += capList.get(n); 
        key += capList.get(i);
        if(cstMtrx.get(n).get(i) <= maxCst) cityDic.put(key, cstMtrx.get(n).get(i));
      }
    }
    
    return cityDic;
  }


  //main function to cycle through the possible city combinations 
  private static ArrayList<ArrayList <String>> calcCity( Map<String, Integer> cityDic, ArrayList<ArrayList<String>> fnlLst, ArrayList<Integer> cstList, ArrayList<Character> capList)
  {
    ArrayList<String> dicList = new ArrayList<>();
    ArrayList<String> cityCombi = new ArrayList<>();
    Map<String, Integer> copyDic = new TreeMap<>();
    copyDic.putAll(cityDic);
    int counter = 0, ttlCst = 0;
    
    
    
    do{
    dicList.clear();
    cityCombi.clear();
    for(String cityPair : copyDic.keySet()) dicList.add(cityPair);
    
    do
    {
      
      //adding the first element of the list 
      cityCombi.add(dicList.get(0));
      //removing it from the diconary
      copyDic.remove(cityCombi.get(0));
      //and the list
      dicList.remove(dicList.get(0));

      counter = dicList.size();
      for(int n = 0; n < counter; n++)
      {  
        if(dicList.isEmpty()) break;
        
        //check if city combination is part of the remaining list and if then remove it
        if(dicList.get(n).charAt(0) == cityCombi.get(cityCombi.size()-1).charAt(0) || 
                dicList.get(n).charAt(1) == cityCombi.get(cityCombi.size()-1).charAt(0) ||
                dicList.get(n).charAt(1) == cityCombi.get(cityCombi.size()-1).charAt(1) ||
                dicList.get(n).charAt(0) == cityCombi.get(cityCombi.size()-1).charAt(1)) 
        {   
        
            dicList.remove(dicList.get(n));
            n--;
            counter--;
        }
        
      }
      
      //if the list of all city combination is emtpy the collected list is being check
      if(dicList.isEmpty())
      {
      
        //for size
        if(cityCombi.size() == cstList.get(0)/2)
        {
          for(String cComb : cityCombi)
          {
            ttlCst += cityDic.get(cComb);
          }
          //for cost 
          if(ttlCst < cstList.get(1)) 
          {
            ttlCst = 0;
            
            // if length and cost are met, list is added
            fnlLst.add(new ArrayList<String>(cityCombi));
            //and then cycled and checked for conditions
            cityCombi = permuCity(cityCombi, cityDic,  cstList);
            if(cityCombi.size() == cstList.get(0)/2)
            {
              for(String cComb : cityCombi)
              {
                ttlCst += cityDic.get(cComb);
              }
              if(ttlCst < cstList.get(1)) 
              {
                ttlCst = 0;
                //and added
                fnlLst.add(new ArrayList<String>(cityCombi));
              }
            }
          }
          
        
        }
        else
        {
          cityCombi = permuCity(cityCombi, copyDic,  cstList);
          if(cityCombi.size() == cstList.get(0)/2)
          {
              for(String cComb : cityCombi)
              {
                ttlCst += cityDic.get(cComb);
              }
              if(ttlCst < cstList.get(1)) 
              {
                fnlLst.add(new ArrayList<String>(cityCombi));
              }
            }
        }
      
     
      }
      
      
    }while(!dicList.isEmpty());
    
    }while(capList.get(0) == copyDic.keySet().iterator().next().charAt(0));
    
    return fnlLst;
  }

  
  //function for list permutation
  public static ArrayList<String> permuCity( ArrayList<String> cityCombi, Map<String, Integer> cityDic,  ArrayList<Integer> cstList)
  {
    ArrayList<String> dicList = new ArrayList<>();
    ArrayList<String> copyCity = (ArrayList)cityCombi.clone();
    Map<String, Integer> copyDic = new TreeMap<>();
    copyDic.putAll(cityDic);
    int counter = 0, ttlCst = 0;
    
    
    cityCombi.clear();
    
    //cycling through all possible combinations of a viable list by remove the 2nd element of the list  
    for(int i = 1; i < copyCity.size(); i++)
    {
      
      dicList.clear();
      
      //copy remaining dictionary into list for checking
      for(String cityPair : cityDic.keySet()) dicList.add(cityPair);
      cityDic.remove(copyCity.get(i));
      dicList.remove(copyCity.get(i));
      
      
      while(cityCombi.size() < cstList.get(0)/2)
      {
        if(dicList.isEmpty()) break;
        cityCombi.add(dicList.get(0));
                
        dicList.remove(dicList.get(0));

        counter = dicList.size();
        for(int n = 0; n < counter; n++)
        {  
          if(dicList.isEmpty()) break;
        
          //check if city combination is part of the remaining list and if then remove it
          if(dicList.get(n).charAt(0) == cityCombi.get(cityCombi.size()-1).charAt(0) || 
                  dicList.get(n).charAt(1) == cityCombi.get(cityCombi.size()-1).charAt(0) ||
                  dicList.get(n).charAt(1) == cityCombi.get(cityCombi.size()-1).charAt(1) ||
                  dicList.get(n).charAt(0) == cityCombi.get(cityCombi.size()-1).charAt(1)) 
          {   
              dicList.remove(dicList.get(n));
              n--;
              counter--;
          }
        }
      }
      if(cityCombi.size() == cstList.get(0)/2)
      {
        for(String cComb : cityCombi)
        {
          ttlCst += copyDic.get(cComb);
        }
        if(ttlCst < cstList.get(1)) 
        {
          return cityCombi;
        }
      }
    }
   return copyCity; 
  }
  
  
  //function for minimum cost
  private static void optiCst(ArrayList<ArrayList <String>> fnlLst, Map<String, Integer> copyDic)
  {
    ArrayList<Integer> minCst = new ArrayList<>();
    ArrayList<Integer> minCombi = new ArrayList<>();
    int ttlCst = 0, minInt = 0;
    
    
    //calculating the cost of all combinations
    for(ArrayList<String> citi : fnlLst)
    {
      ttlCst = 0;
      for(int n = 0; n < citi.size(); n++)
      {
        ttlCst += copyDic.get(citi.get(n));
      }
      minCst.add(ttlCst);
      
    }
    
    
    //get the element with the lowest cost and in case that there are two or more minima, add all of them
    for(int n = 0; n < minCst.size() ; n++)
    {
      if(n == 0) minInt = minCst.get(n);
      else if(n !=0) if(minInt > minCst.get(n)) minInt = minCst.get(n);
    }
    for(int n = 0; n < minCst.size(); n++)
    {
      if(minCst.get(n) == minInt) minCombi.add(n);
    }
    for( Integer minV : minCombi) System.out.println(fnlLst.get(minV));
  }
  
  

	public static void main(String[] args)
	{
	  String inputFile = null, capName = "", costLine = "", Mtrx = "";
	  boolean optionO = false;
	  Map<String, Integer> cityDic = new TreeMap<>();
	  Map<String, Integer> copyDic = new TreeMap<>();
	  ArrayList<Integer> cstList = new ArrayList<>();
	  ArrayList<Character> capList = new ArrayList<>();
	  ArrayList<ArrayList <Integer>> cstMtrx = new ArrayList<>();
	  ArrayList<ArrayList <String>> fnlLst = new ArrayList<>();
	  cstMtrx.add(new ArrayList<Integer>());
	  
	  
	  
	  //Input parameters 
	  for(String arg : args)
	  {
	    try
	    {
	        if(arg.equals("-o"))
	        {
	            optionO = true;
	        }
	        else
	        {
	            inputFile = arg;
	        }
	    }
	    catch(Exception e)
	    {
	        e.printStackTrace();
	    }
	    
	  }
	  
	  
	  //file opening management
	  if(inputFile == null)
	  {
	      System.out.println("Error, Usage: [option] <filename>");
	      System.exit(1);
	  }
	  
	  try
	  {
	    File inptData = new  File(inputFile);
	    Scanner inData = new Scanner(inptData);
	    for(int n = 0; inData.hasNextLine(); n++)
	    {
	      
	      //separation of input lines for further processing
	      if(n == 0) costLine = inData.nextLine();
	      else if(n == 1) capName = inData.nextLine();
	      else Mtrx +=  inData.nextLine() + "\n";
	      
	    }
	  }
	  catch(Exception e)
	  {
	    System.out.println("Error, File not found");
	    e.printStackTrace();
	    System.exit(1);
	  }
	  
	  //get the cost and city number of first line
	  cstList = getCost(costLine);
	  
	  //get the list of city names
	  capList = getcapName(capName);
	  
	  //get the cost of the city combination as 2d arraylist
	  cstMtrx = getMtrx(Mtrx);
	  
	  //get a dictonary with citycombinations and cost
	  cityDic = getDic(cstMtrx, capList, cstList);
	  copyDic.putAll(cityDic);
	  
	  //get the list of all possible citycombinations below the cost
	  fnlLst = calcCity(copyDic, fnlLst, cstList, capList);
	  System.out.println(fnlLst);
	  
	  //minmum cost city cambination
	  if(optionO == true) optiCst(fnlLst, cityDic);
	
	
		
	}

}
