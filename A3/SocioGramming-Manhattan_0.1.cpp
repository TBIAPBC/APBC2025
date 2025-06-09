#include <stdio.h>
#include <iostream>
#include <fstream>
#include <string>
#include <vector>
using namespace std;


static /*vector<string>*/ void getMtrx(vector<string> iptDt){
  int counter = 0;
  
  for(int n = 0; n < iptDt.size(); n++){
          
      if(iptDt[n].size() == 0){
          continue;
      }
      else if(n > 3 && iptDt[n].size() != 0 && iptDt[n-1].at(0) == '#' && iptDt[n].at(0) == '#' ){
        //counter ++;
        continue;
      }
      else{
          iptDt[counter] = iptDt[n];
          counter++;
      }
  }
  for(int n = iptDt.size(); n > counter;n--){
      iptDt.erase(iptDt.begin() + n);      
  
  }
  
  for(int n = 0; n < iptDt.size();n++){
      cout << iptDt[n] << "\n";
  }
}





 int main(int argc, char *argv[])
{
  bool optionD = false;
  string inputFile, lines, line;
  vector<string> iptDt = {};

  try{
      for(int n= 0; n < argc; n++){
          if(argv[n] == "-d"){
            optionD = true;
          }
          else{
            inputFile = argv[n];
          }
      }
  }
  catch(...){
      printf("Error, Wrong input: program [option] <filename>");
  }
  
  try{
      ifstream inData(inputFile);
      while(getline(inData, lines)){
          iptDt.push_back(lines);
      }
      inData.close();
  }
  catch(...){
      printf("Error: File not found");
  }
  
  /*getMtrx(iptDt);*/
  
  for(int n = 0; n < iptDt.size(); n++){
      cout << iptDt[n].size() << "\n";
  
  }



  return 0;
}
