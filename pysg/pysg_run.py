# PySimpleGUIQt is many versions behind PySimpleGUI it seems
import PySimpleGUI as sg
from sys import argv
from re import match

# parses the athinput file and returns a dictionary
# use this to parse the entire file as well?
def parse(filename):
    file = open(filename, 'r')
    lines = file.readlines()
    data = {}
    info = {}
    prefix = ''
    # looking for name and abstract
    # assuming name and abstract lines have no comments in them
    for line in lines:
        # this regex matches the section line:
        # <[string]>
        m = match('^\s*<(.+)>.*', line)
        if m:
            prefix = m.group(1).strip()
            continue
        # this regex matches strings of the form:
        # [string] = [string with spaces] # comment
        m = match('^([^#]+)\s*=\s*([^#]+).*', line)
        if m:
            # strip the leading and trailing whitespace
            # dictionary entry is a list
            name = m.group(1).strip()
            if prefix == 'comment':
                info[name] = m.group(2).strip()
            else:
                data[f'{prefix}_{name}'] = m.group(2).strip()
    return data, info

def build_layout():

    # arity checking for argv done elsewhere
    data, info = parse(argv[1])
    layout = [[sg.Text('Problem: ' + info['problem'])]]
    reference = info['reference']
    if reference: # empty strings are falsy
        # in the future, go to the link and get the abstract if possible
        layout.append([sg.Text('Reference: ' + info['reference'])])
    else:
        layout.append([sg.Text('Reference: N/A')])
    layout.append([sg.Text('Parameters:')])
    keys = data.keys()
    for k in keys:
        # push to align right
        layout.append([sg.Text(k), sg.Push(), sg.Input(data[k], enable_events=True, size=25)])
    # add buttons to run/quit/help
    layout.append([sg.Button('Run'), sg.Button('Quit'), sg.Button('Help')])
    return layout

# could be put into main function if need be
if len(argv) != 2:
    print('Arity error')
    exit()

#start building gui
layout = [[sg.Column(build_layout(), size=(500, 500), scrollable=True, vertical_scroll_only=True)]]

# sg.theme('DarkBlue13')

# create the main window
window = sg.Window('run2', layout, size=(500, 500))

# primary event loop
while True:
    event, values = window.read()
    if event == sg.WIN_CLOSED:
        break

window.close()