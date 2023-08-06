import PySimpleGUI as sg

sg.theme('DarkAmber')   # Add a touch of color
# All the stuff inside your window.
layout = [  [sg.Text('Text')],
            [sg.Text('Enter something on Row 2'), sg.InputText()],
            [sg.Radio("text1", "a", key='t1'), sg.Radio("text2", "a", key='t2')],
            [sg.Radio("text3", "b", key='t3'), sg.Radio("text4", "b", key='t4')],
            [sg.Slider(range=(10, 30), default_value=12,
            expand_x=True, enable_events=True,
            orientation='horizontal', key='-SL-')],
            [sg.Checkbox("1", key="1"), sg.Checkbox("2", key="2"), sg.Checkbox("3", key="3")],
            [sg.Button('Ok'), sg.Button('Cancel')] ]

# Create the Window
window = sg.Window('Window Title', layout)
# Event Loop to process "events" and get the "values" of the inputs
while True:
    event, values = window.read()
    if event == sg.WIN_CLOSED or event == 'Cancel': # if user closes window or clicks cancel
        break
    
    print('You entered ', values[0])
    if values['t1'] == True:
        print("text1")
    if values['t2'] == True:
        print("text2")
    if values['t3'] == True:
        print("text3")
    if values['t4'] == True:
        print("text4")
    print(int(values['-SL-']))
    if values['1'] == True:
        print("1")
    if values['2'] == True:
        print("2")
    if values['3'] == True:
        print("3")

window.close()