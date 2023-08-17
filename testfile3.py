file1="foo"                #> IFILE
 file2="bar"       # help for output file2         #> OFILE
  dir3="fum"       # help for input dir3           #> IDIR 
  dir4="baz"       # help for output dir4          #> ODIR 
 hello="world"     # help for text entry hello     #> ENTRY
     a=1         # help for a, between 0 and 2   #> SCALE       0:100:50
     b=2         # help for b, pick 1, 2 or 3    #> RADIO       0,1,2
     c="3,c"       # help for c, check any of 6    #> CHECK       0,1,2,a,b,c