# main imports
# PySimpleGUIQt is many versions behind PySimpleGUI it seems
import PySimpleGUI as sg
from sys import argv, modules
from aparser import parse

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
    for k in data:
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