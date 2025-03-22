#!/usr/bin/env python3.12
import re

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

file_name = file_name.split(" ")

for n in file_name:
    if n == '-I':
        func_call2 = "-I"
    elif n == '-l':
        func_call1 = "-l"
    else:
        file_str = n

try:
    with open(file_str, "r") as data:
        datalines = data.read()
except:
    print(NameError)

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
datalines = re.sub("\\s+", " ", datalines)

if(func_call2 == '-I'):
   datalines = datalines.lower()
datalines = datalines.split(" ") 
func_call2 = ''

len_string = len(datalines)
if (datalines[len_string-1] == " " or datalines[len_string-1] == "\n" or datalines[len_string-1] == ""):
    datalines.pop()

datalines.sort()
file_str = file_str + ".out"

if (func_call1 == '-l'):
    dict_words = dict(sorted(case_unsense(datalines).items(), key = lambda x:x[1], reverse=True))
    
    with open(file_str, "w") as file:
        for k,v in dict_words.items():
            file.write( k + " " + str(v) + "\n")
    count_w = input("Count all words? y/n\n")
    if(count_w == 'y' or count_w == 'Y'):
        func_call1 = ''
        file_str = file_str + ".count.out"
        
if(func_call1 == '' and func_call2 == ''):
    dict_words = case_unsense(datalines)
    with open(file_str, "w") as file:
        file.write(str(len(dict_words.keys())) + " / " + str(len_string))  
