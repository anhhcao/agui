#! /usr/bin/env python
from PyQt5 import QtCore, QtWidgets

# utility imports
from re import match
from aparser import parse_generic as parse
from argparse import ArgumentParser
from os import getcwd, remove, mkdir, environ, path
from subprocess import Popen, PIPE
from importlib import import_module
from glob import glob
from sys import argv, exit

class MainWindow(QtWidgets.QMainWindow):

    def __init__(self, data, info):
        super(MainWindow, self).__init__()

        self.data = data
        self.info = info
        self.radio_groups = []
        self.sliders = {}
        self.input={}

        self.initUI()

    # removes the trailing zeroes then the dot from a string float x, then returns an int
    # utility function used by build_layout
    def rm_dot(self, x):
        # being too precise causes problems, but hopefully this is enough
        s = '%.8g' % float(x)
        dot_pos = s.rfind('.')
        if dot_pos < 0:
            return int(s)
        s = s.replace('.', '')
        return int(s)

    def initUI(self):
        self.pagelayout = QtWidgets.QVBoxLayout()       #page layout
        self.dbtnlayout = QtWidgets.QHBoxLayout()       #layout for the default buttons
        self.elmtlayout = QtWidgets.QVBoxLayout()   #layout for the added widgets, stacks elements
        
        self.problayout = QtWidgets.QHBoxLayout()
        self.reflayout = QtWidgets.QHBoxLayout()
        self.outdirlayout = QtWidgets.QHBoxLayout()

        #add layouts to the page
        #self.pagelayout.addLayout(self.infolayout)
        self.pagelayout.addLayout(self.elmtlayout)
        self.pagelayout.addLayout(self.dbtnlayout) 

        # to set bold
        # self.label.setStyleSheet("font-weight: bold")

        l1 = QtWidgets.QLabel('Problem:')
        l1.setStyleSheet("font-weight: bold")
        l2 = QtWidgets.QLabel(info['problem'])
        self.problayout.addWidget(l1)
        self.problayout.addStretch()
        self.problayout.addWidget(l2)

        reference = info['reference']
        l1 = QtWidgets.QLabel('Layout:')
        l1.setStyleSheet("font-weight: bold")
        if reference:
            l2 = QtWidgets.QLabel(reference)
        else:
            l2 = QtWidgets.QLabel('N/A')
        self.reflayout.addWidget(l1)
        self.reflayout.addStretch()
        self.reflayout.addWidget(l2)

        l1 = QtWidgets.QLabel('Output Directory:')
        l1.setStyleSheet("font-weight: bold")
        l1.setToolTip('The directory where the output file will be dumped')
        self.outdirlayout.addWidget(l1)
        self.outdirlayout.addStretch()
        btn = QtWidgets.QPushButton(self)
        btn.setText("browse")
        def browse_dir(t):
            file = QtWidgets.QFileDialog.getExistingDirectory(self, "Select Directory", "")
            t.setText(file)
        txt = QtWidgets.QLineEdit(self)
        btn.clicked.connect(lambda: browse_dir(txt))
        txt.setFixedWidth(250)
        txt.setText(cwd)
        self.outdirlayout.addWidget(btn)
        self.outdirlayout.addWidget(txt)

        self.elmtlayout.addLayout(self.problayout)
        self.elmtlayout.addLayout(self.reflayout)
        self.elmtlayout.addLayout(self.outdirlayout)

        #run, save, load, quit, help button
        btn = QtWidgets.QPushButton(self)
        btn.setText("run")
        btn.clicked.connect(lambda: self.run(txt))
        self.dbtnlayout.addWidget(btn)

        '''btn = QtWidgets.QPushButton(self)
        btn.setText("save")
        btn.clicked.connect(self.save)
        self.dbtnlayout.addWidget(btn)

        btn = QtWidgets.QPushButton(self)
        btn.setText("load")
        btn.clicked.connect(self.load)
        self.dbtnlayout.addWidget(btn)'''

        btn = QtWidgets.QPushButton(self)
        btn.setText("quit")
        btn.clicked.connect(self.quit)
        self.dbtnlayout.addWidget(btn)

        btn = QtWidgets.QPushButton(self)
        btn.setText("help")
        btn.clicked.connect(self.help)
        self.dbtnlayout.addWidget(btn)
        
        #set the main page layout
        widget = QtWidgets.QWidget()
        widget.setLayout(self.pagelayout) 
        scroll = QtWidgets.QScrollArea()    #add scrollbar
        scroll.setWidgetResizable(True)
        scroll.setWidget(widget)
        self.setGeometry(500, 100, 700, 500)
        self.setCentralWidget(scroll)

        self.createWidgetsFromGroups()
    
    def run(self, odir_input):
        print('run')
        cmd = f'{athena} -i {args.file} -d {odir_input.text()} output2/file_type=tab '

        for k in self.data:
            e = data[k]
            t = e['gtype']

            if t == 'RADIO':
                for r in self.input[k]:
                    if r.isChecked():
                        cmd += f'{k}={r.text()} '
                        break
            elif t == 'CHECK' and self.input[k]:
                cmd += f'{k}='
                for c in self.input[k]:
                    if c.isChecked():
                        cmd += f'{c.text()},'
                cmd = cmd[:-1] + ' '
            else:
                cmd += '%s=%s ' % (k, self.input[k].text())

        print(cmd)
        if args.run:
            if not path.exists(athena):
                print('Athena not found\nExiting')
            # open the plot in a subprocess
            # remove the forward slash at the end if there is one
            odir = odir_input.text()
            if odir[-1] == '/':
                odir = odir[:-1]
            # remove the hst file since it always gets appended to
            # intentional?
            h = glob(odir + '/*.hst')
            if len(h) > 0:
                remove(h[0])
            # will the tlim variable always be like this?
            # display_pbar(cmd, values['time/tlim'])
            p = Popen(cmd.split())
            p.wait()
            print(info)
            Popen(['python', 'plot1d.py', '-d', odir, '-n', info['problem']])
            Popen(['python', 'plot1d.py', '-d', odir, '--hst', '-n', info['problem'] + ' history'])

    def save(self):
        print('save')
    
    def load(self):
        print('load')
    
    def quit(self):
        self.close()
        print('quit')

    def help(self):
        print('help')
        w = HelpWindow(self.data)
        size = w.main_layout.sizeHint()
        size.setWidth(size.width() + 10)
        size.setHeight(size.height() + 10)
        w.show()

    def createWidgetsFromGroups(self):
        plabel = QtWidgets.QLabel('Parameters:')
        plabel.setStyleSheet("font-weight: bold")
        self.elmtlayout.addWidget(plabel)
        #self.elmtlayout.setSpacing(10)
        for k in data:
            e = data[k]
            t = e['gtype']
            tooltip = e['help'][1:].strip()
            if t == 'RADIO':
                new_group = QtWidgets.QButtonGroup()
                self.radio_groups.append(new_group)
                self.input[k] = []
                group_layout = QtWidgets.QHBoxLayout()
                label = QtWidgets.QLabel(f'\t{k}:')
                label.setToolTip(tooltip)
                group_layout.addWidget(label)
                group_layout.addStretch()

                for option in e['gparams'].split(','):
                    # option = option.strip()
                    radio_button = QtWidgets.QRadioButton(option)
                    self.input[k].append(radio_button)
                    new_group.addButton(radio_button)
                    group_layout.addWidget(radio_button)
                    if option == e['value']:
                        radio_button.setChecked(True)
                self.elmtlayout.addLayout(group_layout)

            elif t == "IFILE" or t == "OFILE":
                print("browse files button created")
                group_layout = QtWidgets.QHBoxLayout()
                label = QtWidgets.QLabel(f'\t{k}:')
                label.setToolTip(tooltip)
                group_layout.addWidget(label)
                group_layout.addStretch()
                btn = QtWidgets.QPushButton(self)
                btn.setText("browse")
                txt = QtWidgets.QLineEdit(self)
                def browse_file(t):
                    file = QtWidgets.QFileDialog.getOpenFileName(self, "Select File", "")[0]
                    t.setText(file)
                btn.clicked.connect(lambda _, t=txt: browse_file(t))
                txt.setFixedWidth(250)
                txt.setText(e['value'])
                group_layout.addWidget(btn)
                group_layout.addWidget(txt)
                self.elmtlayout.addLayout(group_layout)
                self.input[k] = txt

            elif t == "IDIR" or t == 'ODIR':
                print("browse directories button created")
                group_layout = QtWidgets.QHBoxLayout()
                label = QtWidgets.QLabel(f'\t{k}:')
                label.setToolTip(tooltip)
                group_layout.addWidget(label)
                group_layout.addStretch()
                btn = QtWidgets.QPushButton(self)
                btn.setText("browse")
                def browse_dir(t):
                    file = QtWidgets.QFileDialog.getExistingDirectory(self, "Select Directory", "")
                    t.setText(file)
                txt = QtWidgets.QLineEdit(self)
                btn.clicked.connect(lambda _, t=txt: browse_dir(t))
                txt.setFixedWidth(250)
                txt.setText(e['value'])
                group_layout.addWidget(btn)
                group_layout.addWidget(txt)
                self.elmtlayout.addLayout(group_layout)
                self.input[k] = txt

            elif t == "CHECK":
                print("checkbox created")
                group_layout = QtWidgets.QHBoxLayout()
                label = QtWidgets.QLabel(f'\t{k}:')
                label.setToolTip(tooltip)
                group_layout.addWidget(label)
                group_layout.addStretch()
                values = e['value'].split(',')
                self.input[k] = []
                for option in e['gparams'].split(','):
                    #option = option.strip()
                    checkbox = QtWidgets.QCheckBox(option, self)
                    self.input[k].append(checkbox)
                    group_layout.addWidget(checkbox)
                    if option in values:
                        checkbox.setChecked(True)
                self.elmtlayout.addLayout(group_layout)

            
            elif t == "ENTRY":
                print("textbox created")
                group_layout = QtWidgets.QHBoxLayout()
                label = QtWidgets.QLabel(f'\t{k}:')
                label.setToolTip(tooltip)
                group_layout.addWidget(label)
                group_layout.addStretch()
                txt = QtWidgets.QLineEdit(self)
                txt.setText(e['value'])
                txt.setFixedWidth(250)
                self.input[k] = txt
                group_layout.addWidget(txt)
                self.elmtlayout.addLayout(group_layout)

            elif t == "SCALE":
                group_layout = QtWidgets.QHBoxLayout()
                label = QtWidgets.QLabel(f'\t{k}:')
                label.setToolTip(tooltip)
                group_layout.addWidget(label)
                group_layout.addStretch()
                [minimum, maximum, increment] = e['gparams'].split(':')

                print("slider created")
                #creates a horizontal slider
                scaled_default = self.rm_dot(e['value'])
                label_slider = QtWidgets.QLineEdit(str(e['value']))
                label_slider.setAlignment(QtCore.Qt.AlignRight)
                label_slider.setFixedWidth(85)
                # the label slider is unique to this slider
                # so we will use it to identify the slider
                sliders[str(label_slider)] = {
                'key':e['value']+'_display',
                'factor':round(scaled_default / float(e['value']))
                }
                slider = QtWidgets.QSlider(self)
                slider.setOrientation(QtCore.Qt.Horizontal)
                slider.setSingleStep(self.rm_dot(increment))
                slider.setPageStep(self.rm_dot(increment))       #moves the slider when clicking or up/down
                slider.setRange(self.rm_dot(minimum), self.rm_dot(maximum))
                slider.setValue(scaled_default)

                slider.valueChanged.connect(lambda value, lbl=label_slider: self.updateLabel(lbl, value))
                
                slider.setFixedWidth(250)

                group_layout.addWidget(label_slider)
                group_layout.addWidget(slider)
                self.elmtlayout.addLayout(group_layout)
                self.input[k] = label_slider

    def updateLabel(self, label, value):
        label.setText(str(value/sliders[str(label)]['factor']))

class HelpWindow(QtWidgets.QMainWindow):
    def __init__(self, data):
        super(HelpWindow, self).__init__()
        self.main_layout = QtWidgets.QVBoxLayout()
        for k in data:
            sublayout = QtWidgets.QHBoxLayout()
            l1 = QtWidgets.QLabel(k)
            l1.setStyleSheet("font-weight: bold")
            l2 = QtWidgets.QLabel(data[k]['help'])
            sublayout.addWidget(l1)
            sublayout.addWidget(l2)
            self.main_layout.addLayout(sublayout)

# building the gui

cwd = getcwd()

sliders = {}
checks = {}

athena = (environ['AGUI'] if 'AGUI' in environ else cwd) + '/athena/bin/athena'

# parse arguments
argparser = ArgumentParser(description='Runs the GUI for configuring an athinput file')
argparser.add_argument('-r', '--run',
                       action='store_true',
                       help='executes the athena command and plots the tab files on run',
                       default=False)
argparser.add_argument('-x', '--exe', help='the path to the athena executable')
argparser.add_argument('file', help='the athinput file to configure')
args = argparser.parse_args()

# parse the input files
data, info, _ = parse(args.file)

app = QtWidgets.QApplication(argv)
w = MainWindow(data, info)

# additions to the hint are needed to prevent the scrollbar from showing up
size = w.pagelayout.sizeHint()
size.setWidth(size.width() + 100)
size.setHeight(size.height() + 10)

w.resize(size)
w.show()

try:
    print('opening window')
    exit(app.exec())
except SystemExit:
    print('closing window')