import PySimpleGUI as sg
from sys import argv, modules
from re import match

# import aparser
from os import environ
from importlib.util import spec_from_file_location as sffl, module_from_spec as mfs
spec = sffl('aparser', (environ['AGUI'] if 'AGUI' in environ else '~/agui') + '/aparser.py')
aparser = mfs(spec)
modules[spec.name] = aparser
spec.loader.exec_module(aparser)
parse = aparser.parse_special

def build_layout():
    # for use with the dictionary
    VALUE = 0
    GUI_TYPE = 1
    GUI_PARAMS = 2

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
        e = data[k]
        # use this if removing the prefix and underscore is desired
        # row = [sg.Text(match('.*_(.+)', k).group(1))] 
        # otherwise use
        row = [sg.Text(k), sg.Push()] # push to align right
        if e[GUI_TYPE] == 'SCALE':
            # getting scale params
            # min:max:increment?
            # (\d*\.?\d*) also accepts just dots, so beware
            m = match('(\d*\.?\d*):(\d*\.?\d*):(\d*\.?\d*)', e[GUI_PARAMS])

            # scale = slider
            row.append(sg.Slider(
                range=(float(m.group(1)), float(m.group(2))),
                resolution=float(m.group(3)),
                default_value=e[VALUE],
                #expand_x=True,
                enable_events=True,
                # key='something',
                orientation='horizontal'
            ))
        elif e[GUI_TYPE] == 'ENTRY':
            # entry = text box
            row.append(sg.Input(
                e[VALUE], 
                enable_events=True, 
                #expand_x=True, 
                # key='something', 
                #justification='right'
                size=25
            ))
        elif e[GUI_TYPE] == 'RADIO':
            # radios = []
            # number of options is not predetermined, so can't use regex
            options = e[GUI_PARAMS].split(',')
            for o in options:
                row.append(sg.Radio(o, k))
        else:
            print(f'GUI type {e[GUI_TYPE]} not implemented')
            exit()
        layout.append(row)
    # add buttons to run/quit/help
    layout.append([sg.Button('Run'), sg.Button('Quit'), sg.Button('Help')])
    return layout

# could be put into main function if need be
if len(argv) != 2:
    print('Arity error')
    exit()

# start building gui
layout = [[sg.Column(build_layout(), size=(500, 500), scrollable=True, vertical_scroll_only=True)]]

# sg.theme('DarkBlue13')

# create the main window
window = sg.Window('run2_special', layout, size=(500, 500))

# primary event loop
while True:
    event, values = window.read()
    if event == sg.WIN_CLOSED:
        break

window.close()