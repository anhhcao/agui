#! /usr/bin/env python
from tempfile import mkstemp
from os import remove, getcwd
from subprocess import Popen
from aparser import parse_generic as parse
from argparse import ArgumentParser

cwd = getcwd()

# parsing arguments
argparser = ArgumentParser(description='Creates a GUI script, then runs it. The GUI will allow for configuring the provided athinput file')
argparser.add_argument('file', help='the athinput file to configure')
args = argparser.parse_args()

# parsing input file
data, info, type = parse(args.file)
name = info['problem']
reference = info['reference']
if not reference: # empty string is falsy
    reference = 'N/A'

# make temp file
_, path = mkstemp(prefix='gooey', suffix='.py')

file = open(path, 'w')

# write a the script that generates the gui
file.write(f'from gooey import Gooey, GooeyParser\n\
@Gooey(program_name=\'gooey_run2\')\n\
def main():\n\
\tparser = GooeyParser(description=\'Problem: {name}\\nReference: {reference}\')\n\
\tparser.add_argument(\'output_dir\', help=\'The directory where the output files will be dumped\', metavar=\'output directory\', default=\'{cwd}\', widget=\'DirChooser\')\n')

# for some reason 
for k in data:
    e = data[k]
    if e['gtype'] == 'ENTRY' or e['gtype'] == 'SCALE': # no sliders in gooey?
        # entry = text box
        file.write('\tparser.add_argument(\'%s\', help=\'%s\', metavar=\'%s\', default=\'%s\')\n' % (k, e['help'][1:].strip(), k, e['value']))
    elif e['gtype'] == 'RADIO': # currently dropdown menus and not radio buttons
        # number of options is not predetermined, so can't use regex
        options = e['gparams'].split(',')
        # create string list
        c = '['
        for o in options:
            c += f'\'{o}\',' # not wrapping o in quotes causes an error
        c += ']'
        file.write('\tparser.add_argument(\'%s\', help=\'%s\', metavar=\'%s\', choices=%s, default=\'%s\')\n' % (k, e['help'][1:].strip(), k, c, e['value']))
    else:
        print('GUI type %s not implemented' & e['gtype'])
        exit()

file.write(f'\targs = parser.parse_args()\n\
\ts = \'{cwd}/athena/bin/athena -i {args.file} -d %s \' % args.output_dir\n')

for k in data:
    e = data[k]
    file.write(f'\ts += \'{k}=\' + getattr(args, \'{k}\') + \' \'\n')

file.write('\tprint(s)\nmain()')

file.close()

# run gui file in a subprocess
p = Popen(['python', path])
# wait for subprocess to finish before deleting the temp file
p.wait()

# remove temp file
remove(path)