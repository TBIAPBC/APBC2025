#include <stdio.h>
#include <iostream>
#include <fstream>
#include <string>
using namespace std;


int main(void){

string str_in;

ifstream data; data.open("HelloWorld-test1.in");
getline(data, str_in);
data.close();

ofstream file; file.open("HelloWorld-SocioGramming.out");
file << "Hello World!\n" << str_in;
file.close();



}
