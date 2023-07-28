import PySimpleGUI as sg

problems = [['Linear wave propagation', 1],
            ['Riemann problems', 1],
            ['Rayleigh–Taylor instability', 1],
            ['Kelvin–Helmholtz instability', 1]]

def new_problem_tab():
    global problems
    # find which of the problems was selected
    for p in problems:
        if values[p[0]] == True:
            break
    tab_id = f'{p[0]} {p[1]}'
    new_tab = sg.Tab(tab_id, [[sg.Text(f'This is a problem tab for {tab_id}')]], key=tab_id)
    # prase, fill the tab, etc, here
    window['tabs'].add_tab(new_tab)
    # auto-select new tab
    p[1] += 1
    window[tab_id].select()

# returns the main tab
def mainTab():
    elements = [[sg.Text('Choose a problem to run:')]]
    for p in problems:
        elements.append([sg.Radio(p[0], 'problems', key=p[0])])
    elements.append([sg.Button('Configure')])
    return sg.Tab('Choose Problem', elements)

# just for aesthetics
sg.theme('DarkBlue13')

# format is as follows:
# [[row1Stuff, moreRow1Stuff], [row2Stuff, moreRow2Stuff], [row3Stuff, ,preRow3Stuff]]
layout = [[
    sg.TabGroup([[mainTab()]], key='tabs', size=(500, 500)) # everything happens in this tab group
]]

# create the main window
window = sg.Window('pysg test', layout, size=(500, 500))

# primary event loop
while True:
    event, values = window.read()
    if event == 'Configure':
        new_problem_tab()
    if event == sg.WIN_CLOSED:
        break

window.close()