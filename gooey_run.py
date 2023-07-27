from sys import argv
from tempfile import mkstemp
from os import remove
from subprocess import Popen
from aparser import parse

if len(argv) != 2:
    print('Arity error')
    exit()

data, info = parse(argv[1])
name = info['problem']
reference = info['reference']
if not reference: # empty string is falsy
    reference = 'N/A'

# make temp file
_, path = mkstemp(suffix='.py')

file = open(path, 'w')

# write a the script that generates the gui
file.write(f'from gooey import Gooey, GooeyParser\n\
@Gooey(program_name=\'AGOOEY\')\n\
def main():\n\
\tparser = GooeyParser(description=\'Problem: {name}\\nReference: {reference}\')\n')

for k in data:
    file.write(f'\tparser.add_argument(\'{k}\', metavar=\'{k}\', default=\'{data[k]}\')\n')

file.write('\
\targs = parser.parse_args()\n\
main()')

file.close()

# run gui file in a subprocess
p = Popen(['python', path])
# wait for subprocess to finish before deleting the temp file
p.wait()

# remove temp file
remove(path)