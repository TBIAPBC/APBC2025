import java.io.File;
import java.io.FileWriter;
import java.io.IOException;
import java.util.Scanner;



public class SocioGramming_HelloWorld{
  public static void main(String[] args){
    String str_line = "";
    
    try{
    File inPut = new File("HelloWorld-test1.in");
    Scanner inData = new Scanner(inPut);
    str_line = inData.nextLine();
    
    inData.close();
    }
    catch(IOException e){
    e.printStackTrace();
    }
    
    try{
    FileWriter outPut = new FileWriter("HelloWorld-SocioGramming.out");
    outPut.write("Hello World!\n" +str_line);
    
    outPut.close();
    }
    catch(IOException e){
    e.printStackTrace();
    }
  }
}
