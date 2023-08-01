#! /usr/bin/env python
from re import match
from aparser import parse_generic as parse
from argparse import ArgumentParser
from os import getcwd, mkdir, environ, path
from importlib import import_module

cwd = getcwd()

# fonts used in the GUI
fstd = ('Helvetica', 10)
fstd_bold = ('Helvetica', 10, 'bold')

# background colors used in the GUI
bgstd = '#2a2e32'
bgstd2 = '#23272b'

sliders = {}

# parse arguments
argparser = ArgumentParser(description='Runs the GUI for configuring an athinput file')
argparser.add_argument('--tk', action='store_true', help='uses PYSimpleGUI (tkinter) instead of PySimpleGUIQt', default=False)
argparser.add_argument('file', help='the athinput file to configure')
args = argparser.parse_args()

# import a version of PySimpleGUI
# if the selected one doesn't work, try the other
primary = 'PySimpleGUIQt'
backup = 'PySimpleGUI'

if args.tk:
    primary = 'PySimpleGUI'
    backup = 'PySimpleGUIQt'

'''try:
    sg = import_module(primary)
except:
    sg = import_module(backup)

'''
import PySimpleGUIQt as sg
# removes the trailing zeroes then the dot from a string float x, then returns an int
# utility function used by buidd_layout
def rm_dot(x):
    if args.tk:
        return float(x)
    # being too precise causes problems, but hopefully this is enough
    s = '%.8g' % float(x)
    dot_pos = s.rfind('.')
    if dot_pos < 0:
        return float(s)
    s = s.replace('.', '')
    return float(s)

def build_layout(data, info):
    global cwd
    layout = [[sg.Text('Problem:', font=fstd_bold, background_color=bgstd), sg.Stretch(), sg.Text(info['problem'], background_color=bgstd)]]
    reference = info['reference']
    if reference: # empty strings are falsy
        # in the future, go to the link and get the abstract if possible
        layout.append([sg.Text('Reference:', font=fstd_bold, background_color=bgstd), sg.Stretch(), sg.Text(info['reference'], background_color=bgstd)])
    else:
        layout.append([sg.Text('Reference:', font=fstd_bold, background_color=bgstd), sg.Stretch(), sg.Text('N/A', background_color=bgstd)])
    layout.extend([[sg.Text('Output directory:', font=fstd_bold, tooltip='The directory where the output files will be dumped', background_color=bgstd), 
                        sg.In(size=(25, 0.75), 
                            enable_events=True, 
                            default_text=cwd, 
                            key='output-dir',
                            background_color=bgstd2,
                            text_color='white'),
                        sg.FolderBrowse(initial_folder=cwd, button_color=('white', bgstd2))],
                  [sg.Text('Parameters:', font=fstd_bold, background_color=bgstd)]])
    for k in data:
        e = data[k]
        # use this if removing the prefix and underscore is desired
        # row = [sg.Text(match('.*_(.+)', k).group(1))] 
        # otherwise use
        row = [sg.Text(k, tooltip=e['help'][1:].strip(), background_color=bgstd), sg.Stretch()] # push to align right
        if e['gtype'] == 'SCALE':
            # getting scale params
            # min:max:increment?
            # (\d*\.?\d*) also accepts just dots, so beware
            m = match('(\d*\.?\d*):(\d*\.?\d*):(\d*\.?\d*)', e['gparams'])
            # scale = slider
            # build sliders differently depending on whether tk or qt is used
            scaled_default = rm_dot(e['value'])
            if not args.tk:
                # if using qt, we need to prepare our own number display since one is not available by default
                sliders[k] = {
                    'key':e['value']+'_display',
                    'factor':round(scaled_default / float(e['value']))
                }
                row.append(sg.Text(float(e['value']), key=sliders[k]['key'], background_color=bgstd))
            # rm_dot only does anything significant if we are using qt
            row.append(sg.Slider(
                range=(rm_dot(m.group(1)), rm_dot(m.group(2))),
                resolution=rm_dot(m.group(3)),
                default_value=scaled_default,
                enable_events=True,
                key=k,
                orientation='horizontal',
                background_color=bgstd
            ))
        elif e['gtype'] == 'ENTRY':
            # entry = text box
            # size of textboxes seem ok by default when right justified
            # however, if changing the size is desired later, then remember that it is a pair not a single value like in the tkinter version
            row.append(sg.Input(
                e['value'], 
                enable_events=True, 
                key=k,
                size=(20, 0.75),
                background_color=bgstd2,
                text_color='white'
            ))
        elif e['gtype'] == 'RADIO':
            # number of options is not predetermined, so can't use regex
            for o in e['gparams'].split(','):
                row.append(sg.Radio(o, k, key=k+o, default= o == e['value'], background_color=bgstd))
        else:
            print('GUI type %s not implemented' % e['gtype'])
            exit()
        layout.append(row)
    # add buttons to run/quit/help
    layout.extend([[sg.Text(background_color=bgstd)], [sg.Button('Run', key='run', button_color=('white', bgstd2)), sg.Button('Quit', key='quit', button_color=('white', bgstd2)), sg.Button('Help', key='help', button_color=('white', bgstd2))]])
    return layout

# collects the values from the GUI and builds the athena command
# returns a string
def run(input_file, output_dir, data, values):
    if not path.exists(output_dir) and not display_conf_dir(output_dir):
        return
    global cwd
    p = environ['AGUI'] if 'AGUI' in environ else cwd
    cmd = f'{p}/athena/bin/athena -i {input_file} -d {output_dir} '
    for k in data:
        e = data[k]
        # radio buttons are a special case
        # we have to loop through each button to see which is selected
        if e['gtype'] == 'RADIO':
            for o in e['gparams'].split(','):
                if values[k+o]:
                    cmd += f'{k}={o} '
                    break
        elif not args.tk and e['gtype'] == 'SCALE':
            cmd += '%s=%s ' % (k, values[k] / sliders[k]['factor'])
        else:
            cmd += f'{k}={values[k]} '
    # also print it since its easier to copy the text that way
    print(cmd)
    return cmd

# builds and displays a new window containing only the athena command
def display_output(s):
    if s:
        window = sg.Window('Athena Output', [[sg.Text(s, background_color=bgstd)]], font=fstd, background_color=bgstd)
        while True:
            event, _ = window.read()
            if event == sg.WIN_CLOSED:
                break
        window.close()

# builds and displays a new window containing the help information
def display_help(data):
    layout = [[sg.Text('Output directory:', font=fstd_bold, background_color=bgstd), sg.Text('The directory where the output files will be dumped', background_color=bgstd), sg.Stretch()]]
    for k in data:
        layout.append([sg.Text(k + ':', font=fstd_bold, background_color=bgstd), sg.Text(data[k]['help'][1:].strip(), background_color=bgstd), sg.Stretch()])
    window = sg.Window('Help', layout, font=fstd, background_color=bgstd)
    while True:
        event, _ = window.read()
        if event == sg.WIN_CLOSED:
            break
    window.close()

def display_conf_dir(dir_path):
    layout = [[sg.Text(f'Directory {dir_path} does not exist. Create it?', background_color=bgstd)], [sg.Button('Yes', key='yes', button_color=('white', bgstd2)), sg.Button('No', key='no', button_color=('white', bgstd2))]]
    window = sg.Window('Directory Not Found', layout, font=fstd, background_color=bgstd)
    while True:
        event, _ = window.read()
        if event == 'no':
            break
        elif event == 'yes':
            mkdir(dir_path)
            break
    window.close()
    return event == 'yes'

# parse the input files
data, info, type = parse(args.file)

# start building gui
inner_layout = build_layout(data, info)
# pysgqt elements seem to be smaller than their tkinter counterparts, so it might be better to reduce the width scaling
scale_factor = 30
if args.tk:
    scale_factor = 40
win_size = (500, len(inner_layout) * scale_factor)
layout = [[sg.Column(inner_layout, size=win_size, scrollable=True, background_color=bgstd)]]

# only allow verticle scroll for the tk version, otherwise a horizontal scroll bar will show up
if args.tk:
    layout[0][0].VerticalScrollOnly = True

# create the main window
window = sg.Window('pysg_run', layout, size=win_size, font=fstd, background_color=bgstd2)

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
