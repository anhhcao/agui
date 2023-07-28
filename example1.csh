#! /usr/bin/env csh
#
# OLD (t)csh

set file1   = foo       #> IFILE file1=
set file2   = bar       #> OFILE file2=
set dir3    = fum       #> IDIR  dir3=
set dir4    = baz       #> ODIR  dir4=
set hello   = world     #> ENTRY hello=world
set a       = 1         #> SCALE a=1       0:2:0.1
set b       = 2         #> RADIO b=2       0,1,2
set c       = 3,c       #> CHECK c=3,c     1,2,3,a,b,c

#
foreach _arg ($*)
  set $_arg
end

echo file1=$file1
echo file2=$file2
echo dir3=$dir3
echo dir4=$dir4
echo hello=$hello
echo a=$a
echo b=$b
echo c=$c
