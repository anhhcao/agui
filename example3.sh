#! /usr/bin/env bash
#
# new 2023 style bash 

 file1=foo       # help for input file1          #> IFILE
 file2=bar       # help for output file2         #> OFILE
  dir3=fum       # help for input dir3           #> IDIR 
  dir4=baz       # help for output dir4          #> ODIR 
 hello=world     # help for text entry hello     #> ENTRY
     a=1         # help for a, between 0 and 2   #> SCALE       0:2:0.1
     b=2         # help for b, pick 1, 2 or 3    #> RADIO       0,1,2
     c=3,c       # help for c, check any of 6    #> CHECK       0,1,2,a,b,c

#
for arg in "$@"; do
  export "$arg"
done

echo file1=$file1
echo file2=$file2
echo dir3=$dir3
echo dir4=$dir4
echo hello=$hello
echo a=$a
echo b=$b
echo c=$c
