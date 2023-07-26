from sys import argv, modules
from tempfile import mkstemp
from os import remove
from subprocess import Popen

# import aparser
from os import environ
from importlib.util import spec_from_file_location as sffl, module_from_spec as mfs
spec = sffl('aparser', (environ['AGUI'] if 'AGUI' in environ else '~/agui') + '/aparser.py')
aparser = mfs(spec)
modules[spec.name] = aparser
spec.loader.exec_module(aparser)
parse = aparser.parse

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

keys = data.keys()

for k in keys:
    file.write(f'\tparser.add_argument(\'{k}\', metavar=\'{k}\', default=\'{data[k]}\')\n')

file.write('\
\targs = parser.parse_args()\n\
main()')

file.close()

p = Popen(['python', path])
p.wait()

# remove temp file
remove(path)