#! /usr/bin/env python
from re import match
from aparser import parse_generic as parse
from argparse import ArgumentParser
from os import getcwd, environ

cwd = getcwd()

fstd = ('arial', 10)
fstd_bold = ('arial', 10, 'bold')

sliders = {}

# parse arguments
argparser = ArgumentParser(description='Runs the GUI for configuring an athinput file')
argparser.add_argument('--tk', action='store_true', help='uses PYSimpleGUI (tkinter) instead of PySimpleGUIQt', default=False)
argparser.add_argument('file', help='the athinput file to configure')
args = argparser.parse_args()

# import a version of PySimpleGUI
if args.tk:
    import PySimpleGUI as sg
else:
    import PySimpleGUIQt as sg

# removes the trailing zeroes then the dot from a string float x, then returns an int
def rm_dot(x):
    s = '%.8g' % float(x)
    dot_pos = s.rfind('.')
    if dot_pos < 0:
        return int(s)
    s = s.replace('.', '')
    return int(s)

def build_layout(data, info):
    global cwd
    layout = [[sg.Text('Problem:', font=fstd_bold), sg.Stretch(), sg.Text(info['problem'])]]
    reference = info['reference']
    if reference: # empty strings are falsy
        # in the future, go to the link and get the abstract if possible
        layout.append([sg.Text('Reference:', font=fstd_bold), sg.Stretch(), sg.Text(info['reference'])])
    else:
        layout.append([sg.Text('Reference:', font=fstd_bold), sg.Text('N/A')])
    layout.extend([[sg.Text('Output directory:', font=fstd_bold, tooltip='The directory where the output files will be dumped'), 
                        sg.In(size=(25, 0.75), 
                            enable_events=True, 
                            default_text=cwd, 
                            key='output-dir'),
                        sg.FolderBrowse(initial_folder=cwd)],
                  [sg.Text('Parameters:', font=fstd_bold)]])
    for k in data:
        e = data[k]
        # use this if removing the prefix and underscore is desired
        # row = [sg.Text(match('.*_(.+)', k).group(1))] 
        # otherwise use
        row = [sg.Text(k, tooltip=e['help'][1:].strip()), sg.Stretch()] # push to align right
        if e['gtype'] == 'SCALE':
            # getting scale params
            # min:max:increment?
            # (\d*\.?\d*) also accepts just dots, so beware
            m = match('(\d*\.?\d*):(\d*\.?\d*):(\d*\.?\d*)', e['gparams'])
            # scale = slider
            # build sliders differently depending on whether tk or qt is used
            if args.tk:
                slider = sg.Slider(
                    range=(float(m.group(1)), float(m.group(2))),
                    resolution=float(m.group(3)),
                    default_value=e['value'],
                    #expand_x=True,
                    enable_events=True,
                    key=k,
                    orientation='horizontal'
                )
            else:
                # if using qt, we need to prepare our own number display since one is not available by default
                scaled_default = rm_dot(e['value'])
                sliders[k] = {
                    'key':e['value']+'_display',
                    'factor':round(scaled_default / float(e['value']))
                }
                row.append(sg.Text(float(e['value']), key=sliders[k]['key']))
                slider = sg.Slider(
                    range=(rm_dot(m.group(1)), rm_dot(m.group(2))),
                    resolution=rm_dot(m.group(3)),
                    default_value=scaled_default,
                    #expand_x=True,
                    enable_events=True,
                    key=k,
                    orientation='horizontal'
                )
            row.append(slider)
        elif e['gtype'] == 'ENTRY':
            # entry = text box
            # size of textboxes seem ok by default when right justified
            # however, if changing the size is desired later, then remember that it is a pair not a single value like in the tkinter version
            row.append(sg.Input(
                e['value'], 
                enable_events=True, 
                #expand_x=True, 
                key=k,
                #justification='right'
                size=(20, 0.75)
            ))
        elif e['gtype'] == 'RADIO':
            # number of options is not predetermined, so can't use regex
            options = e['gparams'].split(',')
            for o in options:
                row.append(sg.Radio(o, k, key=k+o, default= o == e['value']))
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
    p = environ['AGUI'] if 'AGUI' in environ else cwd
    cmd = f'{p}/athena/bin/athena -i {input_file} -d {output_dir} '
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
    window = sg.Window('Athena Output', [[sg.Text(s)]], font=fstd)
    while True:
        event, _ = window.read()
        if event == sg.WIN_CLOSED:
            break
    window.close()

# builds and displays a new window containing the help information
def display_help(data):
    layout = [[sg.Text('Output directory:', font=fstd_bold), sg.Text('The directory where the output files will be dumped'), sg.Stretch()]]
    for k in data:
        e = data[k]
        layout.append([sg.Text(k + ':', font=fstd_bold), sg.Text(e['help'][1:].strip()), sg.Stretch()])
    window = sg.Window('Help', layout, font=fstd)
    while True:
        event, _ = window.read()
        if event == sg.WIN_CLOSED:
            break
    window.close()

# parse the input files
data, info, type = parse(args.file)

# start building gui
inner_layout = build_layout(data, info)
# pysgqt elements seem to be smaller than their tkinter counterparts, so it might be better to reduce the width scaling
scale_factor = 30
if args.tk:
    scale_factor = 40
win_size = (500, len(inner_layout) * scale_factor)
layout = [[sg.Column(inner_layout, size=win_size, scrollable=True)]]

# only allow verticle scroll for the tk version, otherwise a horizontal scroll bar will show up
if args.tk:
    layout[0][0].VerticalScrollOnly = True

sg.theme('DarkBlue13')

# create the main window
window = sg.Window('pysgqt_run', layout, size=win_size, font=fstd)

# primary event loop
while True:
    event, values = window.read()
    if event == sg.WIN_CLOSED or event == 'quit':
        break
    elif event == 'run':
        display_output(run(args.file, values['output-dir'], data, values))
    elif event == 'help':
        display_help(data)
    # update slider displays if using qt
    elif not args.tk and event in sliders:
        info = sliders[event]
        window[info['key']].update(values[event] / info['factor'])

window.close()
