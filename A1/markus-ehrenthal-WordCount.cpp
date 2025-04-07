#include <float.h>
#include <iostream>
#include <fstream>
#include <vector>
#include <algorithm>
#include <cctype>
#include <map>
#include <sstream>

using namespace std;

bool comparepairs (const pair<string, int>& a, const pair<string, int>& b) {
    if (a.second != b.second) {
        return a.second > b.second;
    }
    else {
        return a.first < b.first;
    }
}


int main (int argcount, char* argvalue[]) {

    // Did user state a filename?
    if (argcount < 2) {
        cout << "Error: State file name." << endl;
        return 1;
    }

    // checking for arguments -l / -I

    bool lowercase = false;
    bool printwordlist = false;

    for (int i = 1; i < argcount; i++) {
        string argument = argvalue[i];
        if (argument == "-I") {
            lowercase = true;
        } else if (argument == "-l") {
            printwordlist = true;
        }
    }

    // open inputfile

    string inputfilename = argvalue[1];
    ifstream inputfile;

    inputfile.open(inputfilename);

    if (!inputfile.is_open()) {
        cout << "Unable to open file." << endl;
        return 2;
    }

// counting words

    int totalnumberofwords = 0;
    map<string, int> wordcount;
    string line;

    // change punctuation marks to spaces and optionally replace uppercase letters

    while (getline(inputfile, line)) {
        for (char& c : line) {
            if (ispunct(c)) {
                c = ' ';
            }
            else if (lowercase) {
                c = tolower(c);
            }
        }

        //transfer content from line to map increment wordcount

        istringstream linetoword(line);
        string word;
        while (linetoword >> word) {
            totalnumberofwords ++;
            wordcount[word] ++;
        }
    }

    inputfile.close();

//output

    if (printwordlist) {
        vector <pair <string, int> > wordlist;
        for (const auto& pair : wordcount) {
            wordlist.push_back(pair);
        }
        sort(wordlist.begin(), wordlist.end(), comparepairs);
        for (const auto& pair : wordlist) {
            cout << pair.first << ": " << pair.second << endl;
        }
    } else {
        cout << wordcount.size() << "/" << totalnumberofwords;
    }

}
