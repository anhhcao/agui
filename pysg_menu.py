#! /usr/bin/env python
from argparse import ArgumentParser
from importlib import import_module
from json import load
from subprocess import Popen

# parse arguments
argparser = ArgumentParser(description='Runs the GUI for configuring an athinput file')
argparser.add_argument('--tk', 
                       action='store_true', 
                       help='uses PYSimpleGUI (tkinter) instead of PySimpleGUIQt', 
                       default=False)
argparser.add_argument('-r', '--run',
                       action='store_true',
                       help='executes the athena command and plots the tab files on run',
                       default=False)
args = argparser.parse_args()

# import a version of PySimpleGUI
# if the selected one doesn't work, try the other
primary = 'PySimpleGUIQt'
backup = 'PySimpleGUI'

fstd_bold = ('Helvetica', 10, 'bold')

using_tk = args.tk

if using_tk:
    primary = 'PySimpleGUI'
    backup = 'PySimpleGUIQt'

try:
    sg = import_module(primary)
except:
    print(f'Falied to import {primary}. Falling back to {backup}')
    using_tk = not using_tk
    sg = import_module(backup)

# builds and displays a new window containing the help information
def display_help():
    layout = [
        [ 
            sg.Text('Athena Version:', font=fstd_bold)
        ],
        [
            sg.Text('\tThe version of Athena (must match the version of the executable) to be used.')
        ],
        [
            sg.Text('Athena Executable:', font=fstd_bold)
        ],
        [
            sg.Text('\tEither the path or the name of the Athena executable. \
if only a name is given, then it is assumed that the executable is in /usr/bin.')
        ],
        [
            sg.Text('Selecting Problems:', font=fstd_bold)
        ],
        [
            sg.Text('\tA problem can either be selected from the list of predefined problems \
or a custom problem can be chosen. Use the radio buttons to choose which method to use.')
        ]
    ]
    window = sg.Window('Help', layout)
    while True:
        event, _ = window.read()
        if event == sg.WIN_CLOSED:
            break
    window.close()

with open('athena_problems.json') as problems_json:
    problems = load(problems_json)

athena_problems = list(problems['athena'])
athenac_problems = list(problems['athenac'])
athenak_problems = list(problems['athenak'])

sg.theme('Default1')

layout = [
    [
        sg.Text('Athena Version:', font=fstd_bold),
        sg.Stretch(), 
        sg.Radio('Athena', 'versions', default=True, key='athena', enable_events=True), 
        sg.Radio('AthenaK', 'versions', key='athenak', enable_events=True), 
        sg.Radio('AthenaC', 'versions', key='athenac', enable_events=True)
    ],
    [
        sg.Text('Athena Executable:', font=fstd_bold), 
        sg.Stretch(), 
        sg.Input(size=(17.5, 0.75), default_text='./athena/bin/athena', key='exe'), 
        sg.FileBrowse(size = (6, 1) if using_tk else (125, 25))
    ],
    [
        sg.Radio('Load Problem:', 'origin', key='load_radio', font=fstd_bold, default=True),
        sg.Stretch(),
        sg.Input(size=(17.5, 0.75), key='load', default_text='./athinput.linear_wave1d'),
        sg.FileBrowse(size = (6, 1) if using_tk else (125, 25))
    ],
    [
        sg.Radio('Predefined Problem:', 'origin', key='predefined_radio', font=fstd_bold),
        sg.Stretch(), 
        sg.Combo(list(problems['athena']), default_value='linear wave 1d (TEST)', size=(30, 0.75), key='predefined_dropdown')
    ],
    [sg.Text()], # buffer
    [
        sg.Button('Configure'), 
        sg.Button('Quit'), 
        sg.Button('Help')
    ]
]

# create the main window
window = sg.Window('pysg test', layout, size=(500, 180))
# primary event loop
while True:
    event, values = window.read()
    if event == sg.WIN_CLOSED or event == 'Quit':
        break
    elif event == 'Configure':
        cmd = './pysg_run.py %s -x %s -r' % (problems[values['predefined_dropdown']] if values['predefined_radio'] else values['load'], values['exe'])
        print(cmd)
        if args.run:
            Popen(cmd.split())
    elif event == 'Help':
        print('help')
        display_help()
    elif event == 'athena':
        window['predefined_dropdown'].update(value=athena_problems[0], values=athena_problems)
    elif event == 'athenac':
        window['predefined_dropdown'].update(value=athenac_problems[0], values=athenac_problems)
    elif event == 'athenak':
        window['predefined_dropdown'].update(value=athenak_problems[0], values=athenak_problems)

window.close()