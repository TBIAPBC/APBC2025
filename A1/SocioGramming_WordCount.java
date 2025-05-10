import java.io.*;
import java.util.*;



public class SocioGramming_WordCount{


  public static void main(String[] args){
    String str_line = "", strList[] = {}, lowerCase = "", outputList = "", fileName = "";
    ArrayList<String> strArray = new ArrayList<String>();
    ArrayList<Integer> turner = new ArrayList<Integer>();
    ArrayList<String> strTurner = new ArrayList<String>();
    Set<String> setList = new HashSet<>();
    Map<String, Integer> strMap = new TreeMap<>();
    
    for(String str : args)
    {
      if(str == "-I")
      {
        lowerCase = str;
      }
      else if( str == "-l")
      {
        outputList = str;
      }
      else
      {
        fileName = str;
      }
    }
    
    //data input
    try{
    File inPut = new File(fileName);
    Scanner inData = new Scanner(inPut);
      while(inData.hasNextLine()){  
        str_line = str_line + inData.nextLine() + " ";
      }
    inData.close();
    }
    catch(IOException e){
    e.printStackTrace();
    }
    
    //no pattern, and my english is not good enough to know what those ' are for
    str_line = str_line.replaceAll(",", " ");
    str_line = str_line.replaceAll("\\.", " ");
    str_line = str_line.replaceAll("\\[", " ");
    str_line = str_line.replaceAll("]", " ");
    str_line = str_line.replaceAll("!", " ");
    str_line = str_line.replaceAll("\"", " ");
    str_line = str_line.replaceAll("-", " ");
    str_line = str_line.replaceAll(":", " ");
    str_line = str_line.replaceAll("\\?", " ");
    str_line = str_line.replaceAll(";", " ");
    str_line = str_line.replaceAll("on't", "o not");
    str_line = str_line.replaceAll("o'er", "over");
    str_line = str_line.replaceAll("demon's", "demons");
    str_line = str_line.replaceAll("bosom's", "bosoms");
    str_line = str_line.replaceAll("'Tis", "it is");
    str_line = str_line.replaceAll("Night's", "Nights");
    str_line = str_line.replaceAll("cushion's", "cushion its");
    str_line = str_line.replaceAll("'", " ");
    str_line = str_line.replaceAll("\\s+", " ");
    
    //To lower case
    if(lowerCase == "-I")
    {
      str_line = str_line.toLowerCase();
    }
   
    
    //split by whitespace
    strList = str_line.split(" ");
    
    //Array sort
    Arrays.sort(strList);
    
    //Array to set to get unique elements
    Collections.addAll(setList, strList);
    
    //set to Arraylist and sorted
    for(String element : setList){
      strArray.add(element);
    }
    strArray.sort(null);
    
    //Arraylist added to Treemap
    for(String n : strArray)
    {
      strMap.put(n,0);
    }
    
    //List with all Strings iterated and ++ if in List for the Treemap value
    for(String n : strList){
      if(strMap.containsKey(n))
      {
        strMap.replace(n, strMap.get(n)+1);
      }
    }
    
    /*for (Map.Entry n : strMap.entrySet())       unclear error, idea make list with string and int
    {                                             then get max value, with index get string and delete it 
        turner.add(n.getValue());                 iterate to make output
        strTurner.add(n.getKey());
    }*/
    
    
   
   
   //output
   if(outputList == "-l")
   {
    for(Map.Entry entry : strMap.entrySet())
    {
      System.out.println(entry.getKey() + " " + entry.getValue());
    }
   }
   else
   {
    System.out.println( setList.size() + " / "+ strList.length);
   }
  
  
  }
}
