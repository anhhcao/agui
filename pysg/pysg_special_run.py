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
            prefix = m.group(1)
            continue
        # this regex matches strings of the form:
        # [string] = [string with spaces] # comment #> [string] [string]
        m = match('^([^#]+)\s*=\s*([^#]+).*#>\s+([^\s]+)(\s+.+|\s*)$', line)
        if m:
            # strip the leading and trailing whitespace
            # dictionary entry is a list
            data[f'{prefix}_{m.group(1)}'.strip()] = [
                m.group(2).strip(), 
                m.group(3).strip(), 
                m.group(4).strip()
            ]
            continue
        # this regex matches the name / abstract
        m = match('^([^#]+)\s*=\s*([^#]+).*$', line)
        if m:
            info[m.group(1).strip()] = m.group(2).strip()
    return data, info

def build_layout():
    # for use with the dictionary
    VALUE = 0
    GUI_TYPE = 1
    GUI_PARAMS = 2

    # arity checking for argv done elsewhere
    data, info = parse(argv[1])
    layout = [[sg.Text('Problem: ' + info['problem'])]]
    reference = info['reference']
    if len(reference) == 0:
        layout.append([sg.Text('Reference: N/A')])
    else:
        # in the future, go to the link and get the abstract if possible
        layout.append([sg.Text('Reference: ' + info['reference'])])
    layout.append([sg.Text('Parameters:')])
    keys = data.keys()
    for k in keys:
        e = data[k]
        # use this if removing the prefix and underscore is desired
        # row = [sg.Text(match('.*_(.+)', k).group(1))] 
        # otherwise use
        row = [sg.Text(k)]
        if e[GUI_TYPE] == 'SCALE':
            # push to align right
            row.append(sg.Push())

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
            # push to align right
            row.append(sg.Push())

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
            # push to align right
            row.append(sg.Push())
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