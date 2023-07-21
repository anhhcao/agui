#! /usr/bin/env python
#
#  python version of the tkrun program, specific for athena's athinput files
#  Should handle Athena++ (AX) as well as Athenak (AK)
#
#
#  14-jul-2023   parse athinput file, tagged with tkrun (V1) widgets
#                and output a tkrun-nable snippet of code
#  21-jul-2023   add argparse
#
#  @todo   keep 'comment/problem' and 'comment/reference'  and 'job/problem_id' (AX) 'job/basename' (AK)

import sys    
import argparse

def read_athinput(fname, mode=1, all=False):
    """   read an athena style athinput

       fname     filename
       mode      0  old athenav1
                 1  athena++        athena/inputs/mhd/athinput.linear_wave1d
                 2  athenak         athenak/inputs/tests/linear_wave_hydro.athinput

    """
    lines = open(fname).readlines()
    
    print("# Parsing %d lines in %s" % (len(lines),fname))
    ngui = 0

    # AthenaXXX input file for HYDRO linear wave tests

    keys = []
    for line in lines:
        line = line.strip()
        # print(line)
        if len(line) == 0:
            continue
        if line[0] == '<':
            key1 = line[1:]
            i = key1.find('>')
            key1 = key1[:i]
            continue
        # now we expect:
        #   "key = val    # help   #> tkrun"
        word = line.split()
        if len(word) < 3:
            continue
        if word[1] != '=':
            print("Parsing error, not finding = in: ",line)
            continue
        key2 = word[0]
        val2 = word[2]
        i1 = line.find('#')
        help2 = line[i1+1:].strip()
        i2 = help2.find('#>')
        if i2 > 0:
            gui2 = help2[i2+2:].strip().split()
            help2 = help2[:i2]
            ngui = ngui + 1
            if len(gui2) == 1:
                keys.append([key1,key2,val2,help2,gui2[0],''])
            else:
                keys.append([key1,key2,val2,help2,gui2[0],gui2[1]])   
            #print('%s=%s\\n%s#>%s' % (key2,val2,help2,gui2))
        else:
            # not a GUI line
            if all:
                keys.append([key1,key2,val2,help2,'ENTRY',''])
    print("# classic tkrun output")
    for i in range(len(keys)):
        k = keys[i]
        print('#> %s  %s_%s=%s   %s' % (k[4],k[0],k[1],k[2],k[5]))

#             somehow formatting with \n doesn't work
my_help = """
  This script converts an athinput file (AX and AK are both supported)
  to a shorthand notation.  Currently only "tkrun" format is supported.
"""

p = argparse.ArgumentParser(description=my_help)
p.add_argument('filename',  help='Input athintput file (required)')
p.add_argument('-a', '--all',  action='store_true', help='Force all keywords to be ENTRY widgets')
p.add_argument('-m', '--mode', type = int, default = 1, help='Output mode:  1=tkrun')


args = p.parse_args()

read_athinput(args.filename, mode=args.mode, all=args.all)
