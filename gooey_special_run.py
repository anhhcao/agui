from sys import argv
from tempfile import mkstemp
from os import remove
from subprocess import Popen
from aparser import parse_special as parse

if len(argv) != 2:
    print('Arity error')
    exit()

data, info = parse(argv[1])
name = info['problem']
reference = info['reference']
if not reference: # empty string is falsy
    reference = 'N/A'

# make temp file
_, path = mkstemp(prefix='gooey', suffix='.py')

file = open(path, 'w')

# write a the script that generates the gui
file.write(f'from gooey import Gooey, GooeyParser\n\
@Gooey(program_name=\'AGOOEY\')\n\
def main():\n\
\tparser = GooeyParser(description=\'Problem: {name}\\nReference: {reference}\')\n')

# for use with the dictionary
VALUE = 0
GUI_TYPE = 1
GUI_PARAMS = 2

# for some reason 
for k in data:
    e = data[k]
    if e[GUI_TYPE] == 'ENTRY' or e[GUI_TYPE] == 'SCALE': # no sliders in gooey?
        # entry = text box
        file.write(f'\tparser.add_argument(\'{k}\', metavar=\'{k}\', default=\'{e[VALUE]}\')\n')
    elif e[GUI_TYPE] == 'RADIO': # currently dropdown menus and not radio buttons
        # number of options is not predetermined, so can't use regex
        options = e[GUI_PARAMS].split(',')
        # create string list
        c = '['
        for o in options:
            c += f'\'{o}\',' # not wrapping o in quotes causes an error
        c += ']'
        file.write(f'\tparser.add_argument(\'{k}\', metavar=\'{k}\', choices={c}, default=\'{e[VALUE]}\')\n')
    else:
        print(f'GUI type {e[GUI_TYPE]} not implemented')
        exit()

file.write('\
\targs = parser.parse_args()\n\
\tprint(\'done\')\n\
main()')

file.close()

# run gui file in a subprocess
p = Popen(['python', path])
# wait for subprocess to finish before deleting the temp file
p.wait()

# remove temp file
remove(path)