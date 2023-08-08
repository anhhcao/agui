import sys
from PyQt5 import QtCore, QtGui, QtWidgets
import argparse
import re
import aparser

class MainWindow(QtWidgets.QMainWindow):

    def __init__(self, parameters):
        super(MainWindow, self).__init__()

        self.groups = groups
        self.radio_groups = []
        self.inputFile = None
        self.ofile = None
        self.saveFile = None
        self.contents = None

        self.initUI()
    
    def initUI(self):
        self.pagelayout = QtWidgets.QVBoxLayout()       #page layout
        self.dbtnlayout = QtWidgets.QHBoxLayout()       #layout for the default buttons
        self.elmtlayout = QtWidgets.QVBoxLayout()       #layout for the added widgets, stacks elements
        
        #add layouts to the page
        self.pagelayout.addLayout(self.dbtnlayout) 
        self.pagelayout.addLayout(self.elmtlayout)

        #run, save, load, quit, help button
        btn = QtWidgets.QPushButton(self)
        btn.setText("run")
        btn.clicked.connect(self.run)
        self.dbtnlayout.addWidget(btn)

        btn = QtWidgets.QPushButton(self)
        btn.setText("save")
        btn.clicked.connect(self.save)
        self.dbtnlayout.addWidget(btn)

        btn = QtWidgets.QPushButton(self)
        btn.setText("load")
        btn.clicked.connect(self.load)
        self.dbtnlayout.addWidget(btn)

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
    
    def run(self):
        print('run')
    
    def save(self):
        # if self.saveFile:
        #     try:
        #         with open(self.saveFile, 'w') as file:
        #             text = self.text_edit.toPlainText()
        #             file.write(text)
        #             print(f"Saved to {self.saveFile}")
        #     except Exception as e:
        #         print(f"Error saving file: {e}")
        # else:
        #     print("no file to save to")
        self.contents = self.gatherData()
        for i in self.contents:
            if i['name'] == self.ofile+":":
                self.saveFile = ''.join(i['default'])
        self.update_and_save(self.inputFile, self.saveFile)
    
    def load(self):
        print('load')
    
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
                self.elmtlayout.addLayout(group_layout)

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
                self.elmtlayout.addLayout(group_layout)

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
                self.elmtlayout.addLayout(group_layout)

            elif group_type == "ENTRY":
                print("textbox created")
                group_layout = QtWidgets.QHBoxLayout()
                label = QtWidgets.QLabel(group_name+":")
                label.setToolTip(help)
                group_layout.addWidget(label)
                txt = QtWidgets.QLineEdit(self)
                txt.setText(default_option)
                group_layout.addWidget(txt)
                self.elmtlayout.addLayout(group_layout)
            
            elif group_type == "SCALE":
                group_layout = QtWidgets.QHBoxLayout()
                label = QtWidgets.QLabel(group_name+":")
                label.setToolTip(help)
                group_layout.addWidget(label)
                options = ''.join(options)
                options = options.split(':')

                print("slider created")
                #creates a horizontal decimal slider
                slider = QtWidgets.QSlider(self)
                slider.setOrientation(QtCore.Qt.Horizontal)
                slider.setSingleStep(int(float(options[2])*100))
                slider.setPageStep(int(float(options[2])*100))       #moves the slider when clicking or up/down
                slider.setRange(int(options[0])*100, int(options[1])*100)
                slider.setValue(int(float(default_option[0])*100))

                label_slider = QtWidgets.QLabel(str(default_option[0]))
                slider.valueChanged.connect(lambda value, lbl=label_slider: self.updateLabel(lbl, value))
                
                group_layout.addWidget(label_slider)
                group_layout.addWidget(slider)
                self.elmtlayout.addLayout(group_layout)

    def updateLabel(self, label, value):
        label.setText(str(value/100))

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

        print(self.elmtlayout.count())

        for hbox_layout_index in range(self.elmtlayout.count()):
            hbox_layout = self.elmtlayout.itemAt(hbox_layout_index).layout()
            
            if hbox_layout is not None:
                defaults = {'name': '',
                            'default':[]}

                for widget_index in range(hbox_layout.count()):
                    widget = hbox_layout.itemAt(widget_index).widget()
                    
                    if widget_index == 0 and isinstance(widget, QtWidgets.QLabel):
                        defaults['name'] = widget.text()

                    elif isinstance(widget, QtWidgets.QLineEdit):
                        defaults['default'].append(widget.text())

                    elif isinstance(widget, QtWidgets.QRadioButton) or isinstance(widget, QtWidgets.QCheckBox):
                        if widget.isChecked():
                            defaults['default'].append(widget.text())

                    elif isinstance(widget, QtWidgets.QSlider):
                        defaults['default'].append(str(widget.value()/100))
                
                layout_data.append(defaults)
        return layout_data

    def update_and_save(self, input_file_path, output_file_path):
        with open(input_file_path, 'r') as input_file:
            lines = input_file.readlines()

        updated_lines = []
        for line in lines:
            if '#>' in line:
                parts = line.split('=')
                if len(parts) == 2:
                    parts = line.split('=')
                    if len(parts) == 2:
                            after = parts[1].split(' ', 1)
                            updated_line = parts[0]+"="+','.join(self.contents.pop(0)['default'])+after[1]
                            updated_lines.append(updated_line)
                    else:
                        updated_lines.append(line)
                else:
                    updated_lines.append(line)
            else:
                updated_lines.append(line)

        with open(output_file_path, 'w') as output_file:
            output_file.writelines(updated_lines)

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description="Dynamic GUI Builder")
    parser.add_argument("param_file", help="Path to the text file containing parameters")
    args = parser.parse_args()

    with open(args.param_file, "r") as file:
        # content = file.read()
        lines = file.readlines()

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
    # print(aparser.parse_generic(args.param_file)) #not used, format into fields later

    app = QtWidgets.QApplication(sys.argv)
    w = MainWindow(groups)
    print(w.saveFile)
    w.inputFile = args.param_file
    w.show()

    print(args.param_file + " argsss")

    try:
        print('opening window')
        sys.exit(app.exec())
    except SystemExit:
        print(w.saveFile)
        print('closing window')