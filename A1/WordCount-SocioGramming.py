#!/usr/bin/env python3.12
import re

#function for the unsentive case
def case_unsense(test_list):
    for n in test_list:
        if n not in dict_words.keys():
            dict_words.update({n:1})
        else:
            dict_words[n] += 1
    return dict_words


func_call1 =  ""
func_call2 = ""
file_name = input()
file_str = ''
datalines = ""
count_w = ""
dict_words = {}

#Did't know the sys.arg[] function, but at the end of the day, something like this probably happens in the compiler, on the upside, it doesn't matter what argument is first/last
file_name = file_name.split(" ")
for n in file_name:
    if n == '-I':
        func_call2 = "-I"
    elif n == '-l':
        func_call1 = "-l"
    else:
        file_str = n

#open file
try:
    with open(file_str, "r") as data:
        datalines = data.read()
except:
    print(NameError)

#didn't know how to make an algorithmn for it, as there is no real pattern imho
datalines = datalines.replace("bosom's", 'bosom its')
datalines = datalines.replace("cushion's", 'cushion its')
datalines = datalines.replace("o'er", 'over')
datalines = datalines.replace("don't", 'do not')
datalines = datalines.replace("-", ' ')
datalines = datalines.replace(";", '')
datalines = datalines.replace(":", '')
datalines = datalines.replace("'", '')
datalines = datalines.replace('"', '')
datalines = datalines.replace(']', '')
datalines = datalines.replace('[', '')
datalines = datalines.replace("?", '')
datalines = datalines.replace('!', '')
datalines = datalines.replace('.', '')
datalines = datalines.replace(',', '')
datalines = datalines.replace('\n', ' ')
datalines = re.sub("\\s+", " ", datalines) # regex seemed appropiate in this chase

#depending on the arguments given by the input, simple lower() function
if(func_call2 == '-I'):
   datalines = datalines.lower()
datalines = datalines.split(" ") 
func_call2 = '' #set back to give the wordcount option

#don't know, I often have something at the end of the array, just incase to remove it
len_string = len(datalines)
if (datalines[len_string-1] == " " or datalines[len_string-1] == "\n" or datalines[len_string-1] == ""):
    datalines.pop()

#normal sort()
datalines.sort()
#preparation for the outputfile
file_str = file_str + ".out"

#multiple calls, function for dictonary countof thelist, stable sort, transform back to dict, because of sorted()
if (func_call1 == '-l'):
    dict_words = dict(sorted(case_unsense(datalines).items(), key = lambda x:x[1], reverse=True))  

#file open and writing dict with appearces
    with open(file_str, "w") as file:
        for k,v in dict_words.items():
            file.write( k + " " + str(v) + "\n")
    count_w = input("Count all words? y/n\n")
    #option for wordcount file
    if(count_w == 'y' or count_w == 'Y'):
        func_call1 = ''
        file_str = file_str + ".count.out"

#file open and word count writing
if(func_call1 == '' and func_call2 == ''):
    dict_words = case_unsense(datalines)
    with open(file_str, "w") as file:
        file.write(str(len(dict_words.keys())) + " / " + str(len_string))  
