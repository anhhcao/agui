#! /usr/bin/env python
import PySimpleGUI as sg
from re import match
from aparser import parse_generic as parse
from argparse import ArgumentParser
from os import getcwd

cwd = getcwd()

def build_layout(data, info):
    global cwd
    layout = [[sg.Text('Problem:', font=('arial', 10, 'bold')), sg.Text(info['problem'])]]
    reference = info['reference']
    if reference: # empty strings are falsy
        # in the future, go to the link and get the abstract if possible
        layout.append([sg.Text('Reference:', font=('arial', 10, 'bold')), sg.Text(info['reference'])])
    else:
        layout.append([sg.Text('Reference:', font=('arial', 10, 'bold')), sg.Text('N/A')])
    layout.extend([[sg.Text('Output directory:', font=('arial', 10, 'bold')), sg.Push(), sg.In(size=(25,1), enable_events=True, default_text=cwd, key='output-dir'),sg.FolderBrowse(initial_folder=cwd)],
                  [sg.Text('Parameters:', font=('arial', 10, 'bold'))]])
    for k in data:
        e = data[k]
        # use this if removing the prefix and underscore is desired
        # row = [sg.Text(match('.*_(.+)', k).group(1))] 
        # otherwise use
        row = [sg.Text(k), sg.Push()] # push to align right
        if e['gtype'] == 'SCALE':
            # getting scale params
            # min:max:increment?
            # (\d*\.?\d*) also accepts just dots, so beware
            m = match('(\d*\.?\d*):(\d*\.?\d*):(\d*\.?\d*)', e['gparams'])
            # scale = slider
            row.append(sg.Slider(
                range=(float(m.group(1)), float(m.group(2))),
                resolution=float(m.group(3)),
                default_value=e['value'],
                #expand_x=True,
                enable_events=True,
                key=k,
                orientation='horizontal'
            ))
        elif e['gtype'] == 'ENTRY':
            # entry = text box
            row.append(sg.Input(
                e['value'], 
                enable_events=True, 
                #expand_x=True, 
                key=k,
                #justification='right'
                size=25
            ))
        elif e['gtype'] == 'RADIO':
            # number of options is not predetermined, so can't use regex
            options = e['gparams'].split(',')
            for o in options:
                row.append(sg.Radio(o, k, key=k+o))
        else:
            print('GUI type %s not implemented' % e['gtype'])
            exit()
        layout.append(row)
    # add buttons to run/quit/help
    layout.extend([[sg.Text()], [sg.Button('Run', key='run'), sg.Button('Quit', key='quit'), sg.Button('Help', key='help')]])
    return layout

# collects the values from the GUI and builds the athena command
# returns a string
def run(input_file, output_dir, data, values):
    global cwd
    cmd = f'{cwd}/athena/bin/athena -i {input_file} -d {output_dir} '
    for k in data:
        e = data[k]
        # radio buttons are a special case
        # we have to loop through each button to see which is selected
        if e['gtype'] == 'RADIO':
            options = e['gparams'].split(',')
            for o in options:
                if values[k+o]:
                    cmd += f'{k}={o} '
                    break
        else:
            cmd += f'{k}={values[k]} '
    # also print it since its easier to copy the text that way
    print(cmd)
    return cmd

# builds and displays a new window containing only the athena command
def display_output(s):
    window = sg.Window('Athena Output', [[sg.Text(s)]], modal=True, font=('arial', 10))
    while True:
        event, _ = window.read()
        if event == sg.WIN_CLOSED:
            break
    window.close()

# builds and displays a new window containing the help information
def display_help(data):
    layout = []
    for k in data:
        e = data[k]
        layout.append([sg.Text(k + ':', font=('arial', 10, 'bold')), sg.Text(e['help'][1:].strip())])
    window = sg.Window('Help', layout, modal=True, font=('arial', 10))
    while True:
        event, _ = window.read()
        if event == sg.WIN_CLOSED:
            break
    window.close()

# parse the arguments
argparser = ArgumentParser(description='Runs the GUI for configuring an athinput file')
argparser.add_argument('file', help='the athinput file to configure')
args = argparser.parse_args()

# parse the input files
data, info, type = parse(args.file)

# start building gui
inner_layout = build_layout(data, info)
layout = [[sg.Column(inner_layout, size=(500, len(inner_layout) * 40), scrollable=True, vertical_scroll_only=True)]]

sg.theme('DarkBlue13')

# create the main window
window = sg.Window('pysg_run2', layout, size=(500, len(inner_layout) * 40), font=('arial', 10))

# primary event loop
while True:
    event, values = window.read()
    if event == sg.WIN_CLOSED or event == 'quit':
        break
    elif event == 'run':
        display_output(run(args.file, values['output-dir'], data, values))
    elif event == 'help':
        display_help(data)

window.close()