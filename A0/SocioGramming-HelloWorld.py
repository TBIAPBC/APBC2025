#!/usr/bin/env python3.12

str_hello = "Hello World!"
str_line = ""

with open("HelloWorld-test1.in", "r") as data:
    str_line = data.readline()

#with open("HelloWorld-SocioGramming.out", "w") as file: now in the consol
print(str_hello + "\n" + str_line)
#    file.write()

