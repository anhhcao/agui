#! /usr/bin/env bash
#
# new 2023 style bash - works with tkrun now

 file1=foo       # help for input file1          #> IFILE file1=
 file2=bar       # help for output file2         #> OFILE file2=
  dir3=fum       # help for input dir3           #> IDIR  dir3=
  dir4=baz       # help for output dir4          #> ODIR  dir4=
 hello=world     # help for text entry hello     #> ENTRY hello=world
     a=1         # help for a, between 0 and 2   #> SCALE a=1       0:2:0.1
     b=2         # help for b, pick 1, 2 or 3    #> RADIO b=2       0,1,2
     c=3         # help for c, check any of 6    #> CHECK c=3       0,1,2,a,b,c

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
