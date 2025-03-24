#include <float.h>
#include <iostream>
#include <fstream>
#include <vector>
#include <algorithm>


using namespace std;

int main (int argcount, char* argvalue[]) {
    if (argcount !=2) {
        cout << "Error: Two arguments needed." << endl;
        return 1;
    }

    string filename = argvalue[1];
    ifstream file;
    string line;

    file.open(filename);

    if (!file.is_open()) {
        cout << "Error: File cannot be opened." << endl;
        return 2;
    }

    cout << "Hello world!";


    while (getline (file, line)) {
        if (!file.eof()) {
            cout << endl << line;
        }
    }

    return 0;

}


