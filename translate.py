#! /usr/bin/env python
from sys import argv, stdout
from aparser import parse_generic as parse
from argparse import ArgumentParser
from tempfile import mkstemp
from os import remove
from subprocess import Popen

argparser = ArgumentParser(prog='translate.py', description='Translates a file into tkrun readable format')
argparser.add_argument('-r', '--run', action='store_true', default=False)
argparser.add_argument('FILE')
argparser.add_argument('FORMAT')
args = argparser.parse_args()

if args.run:
    _, path = mkstemp()
    file = open(path, 'w')
else:
    file = stdout

data, info, type = parse(args.FILE)
for k in data:
    e = data[k]
    s = ''
    value = e['value']
    if args.FORMAT == 'csh':
        s += 'set '
    elif args.FORMAT == 'py' and value != 'True' and value != 'False':
        try:
            float(value)
            isnum = True
        except:
            isnum = False
        value = value if isnum else f'\"{value}\"'
    file.write('%s=%s %s #> %s %s=%s %s\n' % (k, value, e['help'], e['gtype'], k, e['value'], e['gparams']))

file.close()

if args.run:
    p = Popen(['tkrun', path])
    p.wait()
    remove(path)
    remove(path + '.tk')