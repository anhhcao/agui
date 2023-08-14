import sys
import os
from PyQt5 import QtCore, QtWidgets
import argparse
import re
import subprocess

class MainWindow(QtWidgets.QMainWindow):

    def __init__(self, parameters, param_file):
        super(MainWindow, self).__init__()

        self.groups = parameters
        self.radio_groups = []
        self.loadFile = None
        self.ofile = None
        self.saveFile = None
        self.param_file = param_file
        self.sliderMultiplier = []

        self.initUI()
    
    def initUI(self):
        self.pagelayout = QtWidgets.QVBoxLayout()       #page layout

        #run, save, load, quit, help buttons -> located in a toolbar
        toolbar = self.addToolBar("ToolBar")

        run_action = QtWidgets.QAction('Run', self)
        save_action = QtWidgets.QAction('Save', self)
        load_action = QtWidgets.QAction('Load', self)
        quit_action = QtWidgets.QAction('Quit', self)
        help_action = QtWidgets.QAction('Help', self)

        toolbar.addAction(run_action)
        toolbar.addSeparator()
        toolbar.addAction(save_action)
        toolbar.addSeparator()
        toolbar.addAction(load_action)
        toolbar.addSeparator()
        toolbar.addAction(quit_action)
        toolbar.addSeparator()
        toolbar.addAction(help_action)

        run_action.triggered.connect(self.run)
        save_action.triggered.connect(self.save)
        load_action.triggered.connect(self.load)
        quit_action.triggered.connect(self.quit)
        help_action.triggered.connect(self.help)
        
        #set the main page layout
        widget = QtWidgets.QWidget()
        widget.setLayout(self.pagelayout) 
        scroll = QtWidgets.QScrollArea()    #add scrollbar
        scroll.setWidgetResizable(True)
        scroll.setWidget(widget)
        self.setCentralWidget(scroll)

        self.createWidgetsFromGroups()
    
    def run(self):
        print('run')
    
    def save(self):
        contents = self.gatherData()
        # for i in self.contents:
        #     if i['name'] == self.ofile+":":
        #         self.saveFile = ''.join(i['default'])
        # self.update_and_save(self.inputFile, self.saveFile)
        default_file_path = self.param_file + ".key"
        file_path, _ = QtWidgets.QFileDialog.getSaveFileName(self, "Save File", default_file_path, "All Files (*)")
        if file_path:
            with open(file_path, "w") as file:
                for line in contents:
                    for key, value in line.items():
                        file.write(f"{key}{','.join(value)}")
                    file.write("\n")
            print("saved to " + file_path)
    
    def load(self):
        # options = QtWidgets.QFileDialog.Options()
        # file, _ = QtWidgets.QFileDialog.getOpenFileName(self, "Choose a File", "", "All Files (*)", options=options)
        # if file:
        #     self.close()
        #     subprocess.call(["python", "pyqt.py", file])
        options = QtWidgets.QFileDialog.Options()
        load_file = self.param_file +".key" if os.path.exists(self.param_file +".key") else ""
        file, _ = QtWidgets.QFileDialog.getOpenFileName(self, "Choose a File", load_file, "All Files (*)", options=options)
        #alter the values of each option
        if file:
            #turn the parameters in the file into a dictionary
            default_values = {}
            with open(file, "r") as f:
                for line in f:
                    label, value = line.strip().split(":")
                    label = label.split(":")[0]
                    value = value.split(",") if "," in value else [value]
                    default_values[label] = value
            print(default_values)
            
            #go through the elements in the widget
            for elements in range(self.pagelayout.count()):
                element = self.pagelayout.itemAt(elements).layout()
                if element is not None:
                    for widget_index in range(element.count()):
                        widget = element.itemAt(widget_index).widget()
                        
                        if isinstance(widget, QtWidgets.QLineEdit):
                            widget.setText(values[0])

                        elif isinstance(widget, QtWidgets.QRadioButton) or isinstance(widget, QtWidgets.QCheckBox):
                            if widget.text() == values[0]:
                                widget.setChecked(True)
                                values.pop(0)

                        elif isinstance(widget, QtWidgets.QSlider):
                            multiplier = self.sliderMultiplier.pop(0)
                            defaults[key].append(str(widget.value()/multiplier))
                            self.sliderMultiplier.append(multiplier)
                        

    
    def quit(self):
        self.close()
        print('quit')

    def help(self):
        print('help')

    def createWidgetsFromGroups(self):
        for group in self.groups:
            group_type, group_name, options, default_option, help = group

            if group_type == "RADIO":
                print("radio button created")
                new_group = QtWidgets.QButtonGroup()
                self.radio_groups.append(new_group)
                group_layout = QtWidgets.QHBoxLayout()
                label = QtWidgets.QLabel(group_name+":")
                label.setToolTip(help)
                group_layout.addWidget(label)
                for option in options:
                    option = option.strip()
                    radio_button = QtWidgets.QRadioButton(option)
                    new_group.addButton(radio_button)
                    group_layout.addWidget(radio_button)
                    if option in default_option:
                        radio_button.setChecked(True)
                self.pagelayout.addLayout(group_layout)

            elif group_type == "IFILE" or group_type == "OFILE" or group_type == "IDIR" or group_type == "ODIR":
                print("browse files button created")
                group_layout = QtWidgets.QHBoxLayout()
                label = QtWidgets.QLabel(group_name+":")
                label.setToolTip(help)
                group_layout.addWidget(label)
                btn = QtWidgets.QPushButton(self)
                btn.setText("browse...")
            
                txt = QtWidgets.QLineEdit(self)
                txt.setText(default_option)
                if group_type == "OFILE":
                    self.ofile = group_name
                    btn.clicked.connect(lambda checked, edit=txt: self.browse("OFILE", edit))
                else:
                    btn.clicked.connect(lambda checked, edit=txt: self.browse(None, edit))
                group_layout.addWidget(btn)
                group_layout.addWidget(txt)
                self.pagelayout.addLayout(group_layout)

            elif group_type == "CHECK":
                print("checkbox created")
                group_layout = QtWidgets.QHBoxLayout()
                label = QtWidgets.QLabel(group_name+":")
                label.setToolTip(help)
                group_layout.addWidget(label)
                for option in options:
                    option = option.strip()
                    checkbox = QtWidgets.QCheckBox(option, self)
                    group_layout.addWidget(checkbox)
                    if option in default_option:
                        checkbox.setChecked(True)
                self.pagelayout.addLayout(group_layout)

            elif group_type == "ENTRY":
                print("textbox created")
                group_layout = QtWidgets.QHBoxLayout()
                label = QtWidgets.QLabel(group_name+":")
                label.setToolTip(help)
                group_layout.addWidget(label)
                txt = QtWidgets.QLineEdit(self)
                txt.setText(default_option)
                group_layout.addWidget(txt)
                self.pagelayout.addLayout(group_layout)
            
            elif group_type == "SCALE":
                group_layout = QtWidgets.QHBoxLayout()
                label = QtWidgets.QLabel(group_name+":")
                label.setToolTip(help)
                group_layout.addWidget(label)
                options = ''.join(options)
                options = options.split(':')

                print("slider created")
                #creates a horizontal decimal slider
                decimals = len(str(options[2]).split('.')[1]) if '.' in str(options[2]) else 0
                multiplier = 10**decimals
                slider = QtWidgets.QSlider(self)
                slider.setOrientation(QtCore.Qt.Horizontal)
                slider.setSingleStep(int(float(options[2])*multiplier))
                slider.setPageStep(int(float(options[2])*multiplier))       #moves the slider when clicking or up/down
                slider.setRange(int(options[0])*multiplier, int(options[1])*multiplier)
                slider.setValue(int(float(default_option[0])*multiplier))

                label_slider = QtWidgets.QLabel(str(default_option[0]))
                slider.valueChanged.connect(lambda value, lbl=label_slider: self.updateLabel(lbl, value, multiplier))
                
                self.sliderMultiplier.append(multiplier)
                group_layout.addWidget(label_slider)
                group_layout.addWidget(slider)
                self.pagelayout.addLayout(group_layout)

            # Create a visual separator (horizontal line)
            separator = QtWidgets.QFrame()
            separator.setFrameShape(QtWidgets.QFrame.HLine)
            separator.setFrameShadow(QtWidgets.QFrame.Sunken)
            separator.setFixedHeight(1)  # Set a fixed height for the separator
            self.pagelayout.addWidget(separator)

    def updateLabel(self, label, value, multiplier):
        label.setText(str(value/multiplier))

    def browse(self, gtype, txt):
        options = QtWidgets.QFileDialog.Options()
        file, _ = QtWidgets.QFileDialog.getOpenFileName(self, "Choose a File", "", "All Files (*)", options=options)
        
        if file:
           txt.setText(file)
        if gtype == 'OFILE':
            self.saveFile = file
        
        print(file + " selected")

    def gatherData(self):
        layout_data = []

        for hbox_layout_index in range(self.pagelayout.count()):
            hbox_layout = self.pagelayout.itemAt(hbox_layout_index).layout()
            
            if hbox_layout is not None:
                # defaults = {'name': '',
                #             'default':[]}
                defaults = {}
                key = None

                for widget_index in range(hbox_layout.count()):
                    widget = hbox_layout.itemAt(widget_index).widget()
                    
                    if widget_index == 0 and isinstance(widget, QtWidgets.QLabel):
                        # defaults['name'] = widget.text()
                        defaults[widget.text()] = []
                        key = widget.text()

                    elif isinstance(widget, QtWidgets.QLineEdit):
                        defaults[key].append(widget.text())

                    elif isinstance(widget, QtWidgets.QRadioButton) or isinstance(widget, QtWidgets.QCheckBox):
                        if widget.isChecked():
                            defaults[key].append(widget.text())

                    elif isinstance(widget, QtWidgets.QSlider):
                        multiplier = self.sliderMultiplier.pop(0)
                        defaults[key].append(str(widget.value()/multiplier))
                        self.sliderMultiplier.append(multiplier)
                
                layout_data.append(defaults)
        return layout_data

    # def update_and_save(self, filepath):
        # with open(input_file_path, 'r') as input_file:
        #     lines = input_file.readlines()

        # updated_lines = []
        # for line in lines:
        #     if '#>' in line:
        #         parts = line.split('=')
        #         if len(parts) == 2:
        #             parts = line.split('=')
        #             if len(parts) == 2:
        #                     after = parts[1].split(' ', 1)
        #                     updated_line = parts[0]+"="+','.join(self.contents.pop(0)['default'])+after[1]
        #                     updated_lines.append(updated_line)
        #             else:
        #                 updated_lines.append(line)
        #         else:
        #             updated_lines.append(line)
        #     else:
        #         updated_lines.append(line)

        # with open(output_file_path, 'w') as output_file:
        #     output_file.writelines(updated_lines)

def parsefile(file):
    with open(file, "r") as f:
        # content = file.read()
        lines = f.readlines()

    groups = []
    pattern = r"\s*(\w+)\s*=\s*([^\s#]+)\s*#\s*([^\#]+)\s*#\s*>\s*(\w+)(?:\s+(\S+))?"
    for line in lines:
        match = re.match(pattern, line)
        if match:
            group_type = match.group(4)
            group_name = match.group(1)
            default_option = match.group(2)
            options = match.group(5).split(',') if match.group(5) else ""
            help = match.group(3)

            groups.append((group_type, group_name, options, default_option, help))
    
    return groups

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description="Dynamic GUI Builder")
    parser.add_argument("param_file", help="Path to the text file containing parameters")
    args = parser.parse_args()

    groups = parsefile(args.param_file)    

    app = QtWidgets.QApplication(sys.argv)
    w = MainWindow(groups, args.param_file)
    w.inputFile = args.param_file
    w.adjustSize()  #adjust to fit elements accordingly

    #sets a minimum window size
    w.setMinimumWidth(500) 
    w.setMinimumHeight(200)
    w.show()

    try:
        print('opening window')
        sys.exit(app.exec())
    except SystemExit:
        print('closing window')