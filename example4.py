#! /usr/bin/env python
#
# new 2023 style python 

file1   = 'foo'       # help for input file1          #> IFILE file1=
file2   = 'bar'       # help for output file2         #> OFILE file2=
dir3    = 'fum'       # help for input dir3           #> IDIR  dir3=
dir4    = 'baz'       # help for output dir4          #> ODIR  dir4=
hello   = 'world'     # help for text entry hello     #> ENTRY hello=world
a       = 1           # help for a, between 0 and 2   #> SCALE a=1       0:2:0.1
b       = '2'         # help for b, pick 1, 2 or 3    #> RADIO b=2       0,1,2
c       = '3,c'       # help for c, check any of 6    #> CHECK c=3       1,2,3,a,b,c

#
import sys
for _arg in sys.argv[1:]:
    exec(_arg)

print('file1=',file1)
print('file2=',file2)
print('dir3=',dir3)
print('dir4=',dir4)
print('hello=',hello)
print('a=',a)
print('b=',b)
print('c=',c)
