import csv
import os

from PyQt5 import QtCore, QtWidgets
import matplotlib.pyplot as plt
import numpy as np
from PyQt5.QtGui import QFont
from IPython.display import clear_output
from matplotlib import animation
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.backends.backend_qt5agg import NavigationToolbar2QT as NavigationToolbar
from Qtcontrollers.logo_image import *
import functools

file = 'resources/text.csv'
file_em = 'resources/text_em.csv'
file_emz = 'resources/text_emz.txt'
file_p = 'resources/text_p.csv'
path_p = 'resources/properties'
em_figure = 'resources/EML_graph.png'
project_info = 'resources/project_info.csv'
arrow = 'resources/arrow.png'


class Elements_Structure(QWidget):
    def __init__(self):
        super().__init__()
        layout = QVBoxLayout()
        layout.setContentsMargins(0,0,0,0)

        label = QLabel()
        label.setText("Elements Structure")
        label.setFont(QFont("Arial", 15, weight=QFont.Bold))
        layout.addWidget(label)

        grid = QGridLayout()
        connectButton = QPushButton('Add')
        connectButton.clicked.connect(self.onConnectButtonClicked)
        connectButton.setFixedSize(230, 30)

        removeButton = QPushButton('Delete')
        removeButton.clicked.connect(self.onRemoveButtonClicked)
        removeButton.setFixedSize(230, 30)

        es_table = self.init_es_table()
        drawButton = QPushButton("Save")
        drawButton.clicked.connect(self.handleSave)
        drawButton.setFixedSize(230, 30)

        el_table = Emission_Layer()
        emission_zone_setting = Emission_Zone_Setting()
        grid.addWidget(connectButton, 0, 0)
        grid.addWidget(removeButton, 0, 1)
        grid.addWidget(drawButton, 0, 2)

        layout.addLayout(grid)
        layout.addWidget(es_table)

        layout.addWidget(el_table)
        layout.addWidget(emission_zone_setting)

        self.setLayout(layout)

    def init_es_table(self):

        self.table = QTableWidget()
        self.table.setRowCount(12)
        self.table.setColumnCount(7)
        self.cols_element = ['L#', 'LayerName', 'Material', 'RefractiveIndex', 'Thickness',
                             'Unit' ,'Properties']
        self.table.setHorizontalHeaderLabels(self.cols_element)

        self.layer_name = ["Al", "TPBi", "TPBi", "mCBP", "mCBP", "TCTA_B3PYMPM", "TCTA",
                           "NPB", "NPB", "TAPC", "ITO_Geomatec", "glass_Eagle2000"]
        self.material = ["Al", "TPBi", "TPBi", "mCBP", "mCBP", "TCTA_B3PYMPM", "TCTA",
                         "NPB", "NPB", "TAPC", "ITO_Geomatec", "glass_Eagle2000"]
        self.refractive_index = ["Al.dat", "TPBi.dat", "TPBi.dat", "mCBP.dat", "mCBP.dat",
                                 "TCTA_B3PYMPM.dat", "TCTA.dat", "NPB.dat", "NPB.dat",
                                 "TAPC.dat", "ITO_Geomatec.dat", "glass_Eagle2000.dat"]

        self.thickness = [100, 100, 10, 20, 20, 20, 20, 30, 20, 50, 70, 0]
        self.tempList = [[self.layer_name, self.material, self.thickness]]
        self.num_row = len(self.tempList)
        self.table.setFixedSize(700, 250)

        for i in range(len(self.layer_name)):
            self.num_row = i
            self.table.setItem(self.num_row, 0, QTableWidgetItem(str(self.num_row)))
            self.table.setItem(self.num_row, 1, QTableWidgetItem(self.layer_name[i]))
            self.table.setItem(self.num_row, 2, QTableWidgetItem(self.material[i]))
            self.table.setItem(self.num_row, 4, QTableWidgetItem(str(self.thickness[i])))

        i = 0
        for j in range(len(self.layer_name)):
            self.table.setItem(i, 3, QTableWidgetItem(j))
            label = QLabel()
            layout = QHBoxLayout()
            layout.setContentsMargins(0,0,0,0)

            ri_name = self.refractive_index[j]

            another_label = QLabel()
            another_label.setText(ri_name)
            layout.addWidget(another_label)

            button = QPushButton()
            button.setText("b")
            button.setFixedSize(25, 25)
            layout.addWidget(button)

            label.setLayout(layout)
            self.table.setCellWidget(i, 3, label)

            self.table.setItem(i, 5, QTableWidgetItem(j))
            measure = QComboBox()
            measure.addItems(["nm", "um", "pm"])
            self.table.setCellWidget(i, 5, measure)

            self.table.setItem(i, 6, QTableWidgetItem(j))
            selectButton = QPushButton()
            selectButton.setText("Settings")
            selectButton.setFixedSize(140, 20)
            selectButton.clicked.connect(self.saveDirectory)
            self.table.setCellWidget(i, 6, selectButton)
            i += 1

        header = self.table.horizontalHeader()
        header.setSectionResizeMode(0, QtWidgets.QHeaderView.ResizeToContents)
        header.setSectionResizeMode(1, QtWidgets.QHeaderView.ResizeToContents)
        header.setSectionResizeMode(2, QtWidgets.QHeaderView.ResizeToContents)
        header.setSectionResizeMode(3, QtWidgets.QHeaderView.Stretch)
        header.setSectionResizeMode(4, QtWidgets.QHeaderView.ResizeToContents)
        header.setSectionResizeMode(5, QtWidgets.QHeaderView.ResizeToContents)
        header.setSectionResizeMode(6, QtWidgets.QHeaderView.Stretch)


        self.table.horizontalHeader().setStretchLastSection(True)
        self.table.setSelectionMode(QAbstractItemView.MultiSelection)
        return self.table

    def saveDirectory(self):
        real_path = []
        for item in self.layer_name:
            path = os.getcwd()
            path_interim = os.path.join(path, path_p)
            path_real = os.path.join(path_interim, item)+".csv"
            real_path.append(path_real)

        for property_path in real_path:
            with open(property_path, 'w') as stream:
                writer = csv.writer(stream, lineterminator='\n')
                for row in self.read_csv():
                    writer.writerow(row)

    def read_csv(self):
        data = []
        with open(file_p, 'r') as f:
            rows = f.readlines()
            rows = list(map(lambda x: x.strip(), rows))
            for row in rows:
                row = row.split(',')
                data.append(row)
        return data

    def onConnectButtonClicked(self):
        self.currentRowCount = self.table.rowCount()
        self.table.insertRow(self.currentRowCount)

    @QtCore.pyqtSlot()
    def onRemoveButtonClicked(self):
        button = self.sender()
        if button:
            row = self.table.indexAt(button.pos()).row()
            self.table.removeRow(row)

    def handleSave(self):
        with open(file, 'w') as stream:
            writer = csv.writer(stream, lineterminator='\n')
            for row in range(self.table.rowCount()):
                rowdata = []
                for column in range(self.table.columnCount()):
                    item = self.table.item(row, column)
                    if item is not None:
                        rowdata.append(item.text())
                writer.writerow(rowdata)


class Emission_Layer(QWidget):
    def __init__(self):
        super().__init__()
        layout = QVBoxLayout()
        self.init_em_table()

        label = QLabel()
        label.setText("Emission Layer")
        label.setFont(QFont("Arial", 15, weight=QFont.Bold))
        layout.addWidget(label)

        grid = QGridLayout()
        connectButton = QPushButton('Add')
        connectButton.clicked.connect(self.onConnectButtonClicked)
        connectButton.setFixedSize(230, 30)

        removeButton = QPushButton('Delete')
        removeButton.clicked.connect(self.onRemoveButtonClicked)
        removeButton.setFixedSize(230, 30)

        drawButton = QPushButton("Save")
        drawButton.clicked.connect(self.handleSave)
        drawButton.setFixedSize(230, 30)


        grid.addWidget(connectButton, 0, 0)
        grid.addWidget(removeButton, 0, 1)
        grid.addWidget(drawButton, 0, 2)
        layout.addLayout(grid)
        layout.addWidget(self.table)
        self.setLayout(layout)

    def init_em_table(self):
        self.table = QTableWidget()
        self.table.setRowCount(4)
        self.table.setColumnCount(8)

        cols_element = ['L#', 'EMMaterials', 'Spectrum', 'Exciton Prop', 'QY',
                        'HDR', 'EMZone', 'Graph']
        self.table.setHorizontalHeaderLabels(cols_element)

        self.num = [4, 6, 8]
        self.em_materials = ["FCNlr", "Irppy2tmd", "Irmphmq2tmd"]
        self.spectrum = ["FCNlr", "Irppy2tmd", "Irmphmq2tmd"]
        self.exciton_prop = [1, 1, 1]
        self.qy = [90, 96, 96]
        self.hdr = [75, 75, 78]
        self.em_zone = ["constant", "linear_pos", "delta_50"]
        self.tempList = [[self.em_materials, self.spectrum, self.exciton_prop,
                          self.qy, self.hdr]]
        self.num_row = len(self.tempList)
        self.table.setFixedSize(700, 140)

        for i in range(len(self.em_materials)):
            self.num_row = i
            self.table.setItem(self.num_row, 0, QTableWidgetItem(str(self.num[i])))
            self.table.setItem(self.num_row, 1, QTableWidgetItem(self.em_materials[i]))
            self.table.setItem(self.num_row, 2, QTableWidgetItem(self.spectrum[i]))
            self.table.setItem(self.num_row, 3, QTableWidgetItem(str(self.exciton_prop[i])))
            self.table.setItem(self.num_row, 4, QTableWidgetItem(str(self.qy[i])))
            self.table.setItem(self.num_row, 5, QTableWidgetItem(str(self.hdr[i])))


        i = 0
        for j in range(len(self.em_materials)):
            self.table.setItem(i, 6, QTableWidgetItem(j))
            label = QLabel()
            layout = QHBoxLayout()
            layout.setContentsMargins(0,0,0,0)

            em_zone = self.em_zone[j]

            another_label = QLabel()
            another_label.setText(em_zone)
            layout.addWidget(another_label)

            button = QPushButton()
            button.setText("b")
            button.setFixedSize(25, 25)
            layout.addWidget(button)
            label.setLayout(layout)

            self.table.setCellWidget(i, 6, label)

            self.table.setItem(i, 7, QTableWidgetItem(j))
            selectButton = QPushButton()
            selectButton.setText("Plot")
            selectButton.setFixedSize(150, 20)
            # selectButton.clicked.connect(self.saveDirectory)
            self.table.setCellWidget(i, 7, selectButton)
            i += 1

        header = self.table.horizontalHeader()
        header.setSectionResizeMode(0, QtWidgets.QHeaderView.ResizeToContents)
        header.setSectionResizeMode(1, QtWidgets.QHeaderView.ResizeToContents)
        header.setSectionResizeMode(2, QtWidgets.QHeaderView.ResizeToContents)
        header.setSectionResizeMode(3, QtWidgets.QHeaderView.ResizeToContents)
        header.setSectionResizeMode(4, QtWidgets.QHeaderView.ResizeToContents)
        header.setSectionResizeMode(5, QtWidgets.QHeaderView.ResizeToContents)
        header.setSectionResizeMode(6, QtWidgets.QHeaderView.Stretch)
        header.setSectionResizeMode(7, QtWidgets.QHeaderView.Stretch)
        return self.table

    def onConnectButtonClicked(self):
        self.currentRowCount = self.table.rowCount()
        self.table.insertRow(self.currentRowCount)

    @QtCore.pyqtSlot()
    def onRemoveButtonClicked(self):
        button = self.sender()
        if button:
            row = self.table.indexAt(button.pos()).row()
            self.table.removeRow(row)

    def handleSave(self):
        with open(file_em, 'w') as stream:
            writer = csv.writer(stream, lineterminator='\n')
            for row in range(self.table.rowCount()):
                rowdata = []
                for column in range(self.table.columnCount()):
                    item = self.table.item(row, column)
                    if item is not None:
                        rowdata.append(item.text())
                writer.writerow(rowdata)


class Emission_Zone_Setting(QWidget):
    def __init__(self):
        super().__init__()

        layout = QHBoxLayout()
        layout1 = QFormLayout()
        layout2 = QVBoxLayout()
        layout3 = QFormLayout()

        layout.addLayout(layout1)
        layout.addLayout(layout2)
        layout.addLayout(layout3)

        self.setLayout(layout)

        label = QLabel()
        label.setText("Emission Zone Setting")
        label.setFont(QFont("Arial", 15, weight=QFont.Bold))
        label.setFixedSize(180, 20)
        layout1.addRow(label)

        self.textLine_emit = QDoubleSpinBox()
        self.textLine_emit.setFixedSize(100, 20)
        self.textLine_emit.setValue(10)
        self.textLine_emit.valueChanged.connect(self.valueChanged)

        self.textLine_a = QDoubleSpinBox()
        self.textLine_a.setFixedSize(100, 20)
        self.textLine_a.setValue(0.5)
        self.textLine_a.valueChanged.connect(self.valueChanged)

        self.textLine_b = QDoubleSpinBox()
        self.textLine_b.setFixedSize(100, 20)
        self.textLine_b.setValue(1)
        self.textLine_b.valueChanged.connect(self.valueChanged)

        self.textLine_c = QDoubleSpinBox()
        self.textLine_c.setFixedSize(100, 20)
        self.textLine_c.setValue(2)
        self.textLine_c.valueChanged.connect(self.valueChanged)

        self.radiobutton_sheet = QRadioButton("Sheet")
        self.radiobutton_sheet.setChecked(True)
        self.radiobutton_sheet.toggled.connect(self.onClicked)
        layout1.addRow(self.radiobutton_sheet)

        self.radiobutton_constant = QRadioButton("Constant")
        self.radiobutton_constant.toggled.connect(self.onClicked)
        layout1.addRow(self.radiobutton_constant)

        self.radiobutton_linear = QRadioButton("Linear")
        self.radiobutton_linear.toggled.connect(self.onClicked)
        layout1.addRow(self.radiobutton_linear)

        self.radiobutton_exponential = QRadioButton("Exponential")
        self.radiobutton_exponential.toggled.connect(self.onClicked)
        layout1.addRow(self.radiobutton_exponential)

        self.radiobutton_gaussian = QRadioButton("Gaussian")
        self.radiobutton_gaussian.toggled.connect(self.onClicked)
        layout1.addRow(self.radiobutton_gaussian)

        self.valueChanged()

        formlayout = QFormLayout()
        self.label_emit = QLabel("Emit Range(nm): ")
        self.label_a = QLabel("Value a: ")
        self.label_b = QLabel("Value b: ")
        self.label_c = QLabel("Value c: ")
        formlayout.addRow(self.label_emit, self.textLine_emit)
        formlayout.addRow(self.label_a, self.textLine_a)
        formlayout.addRow(self.label_b, self.textLine_b)
        formlayout.addRow(self.label_c, self.textLine_c)

        layoutform = QFormLayout()
        self.qlabel = QTextEdit()
        self.qlabel.setFixedSize(220, 100)
        self.qlabel.setText("x = %s" %(self.textLine_a.value()))
        layoutform.addRow(QLabel("Equation: "))
        layoutform.addRow(self.qlabel)
        layout2.addLayout(formlayout)
        layout2.addLayout(layoutform)

        label = QLabel()
        label.setText("Emission Zone Graph")
        label.setFont(QFont("Arial", 15, weight=QFont.Bold))
        layout3.addRow(label)

        self.special_label = QLabel()
        self.special_label.setFixedSize(300, 300)
        self.fig = plt.Figure(figsize=(2.8, 1.7))
        self.canvas = FigureCanvas(self.fig)
        self.canvas.setParent(self.special_label)
        self.ax = self.fig.add_subplot(111)
        self.onClicked()
        self.ax.set_xlim([-10, 10])
        self.toolbar = NavigationToolbar(self.canvas, self.special_label)
        self.toolbar.setMinimumWidth(self.canvas.width())
        layout3.addWidget(self.toolbar)
        layout3.addRow(self.special_label)

    def drawing(self, equation):
        if self.radiobutton_sheet.isChecked():
            self.ax.axvline(equation)

        elif self.radiobutton_constant.isChecked():
            y = eval(equation)
            self.ax.plot(y)
        else:
            x = np.linspace(-10, 10)
            y = eval(equation)
            self.ax.plot(x, y)

    def valueChanged(self):
        self.radiobutton_sheet.type = "x = %s" %(self.textLine_a.value())
        self.radiobutton_constant.type = "%s" %(self.textLine_a.value())
        self.radiobutton_linear.type = "%s*x + %s" %(self.textLine_a.value(), self.textLine_b.value())
        self.radiobutton_exponential.type = "%s*np.exp(%s + x) + %s" %(
            self.textLine_a.value(), self.textLine_b.value(),self.textLine_c.value())
        self.radiobutton_gaussian.type = \
            "(%s*(np.sqrt(2*np.pi)))**(-1)*np.exp((x-%s)/(2*%s**2))" \
            % (self.textLine_b.value(), self.textLine_a.value(), self.textLine_c.value())


    def onClicked(self):
        if self.radiobutton_sheet.isChecked():
            equation = self.radiobutton_sheet.type
            self.qlabel.setText(equation)

            self.label_a.setEnabled(True)
            self.label_b.setEnabled(False)
            self.label_c.setEnabled(False)
            self.textLine_a.setEnabled(True)
            self.textLine_b.setEnabled(False)
            self.textLine_c.setEnabled(False)

            self.ax.axvline(equation)

        elif self.radiobutton_constant.isChecked():
            equation = self.radiobutton_constant.type
            self.qlabel.setText(equation)

            self.label_a.setEnabled(False)
            self.label_b.setEnabled(False)
            self.label_c.setEnabled(False)
            self.textLine_a.setEnabled(False)
            self.textLine_b.setEnabled(False)
            self.textLine_c.setEnabled(False)

            y = eval(equation)
            self.ax.plot(y)

        elif self.radiobutton_linear.isChecked():
            equation = self.radiobutton_linear.type
            self.qlabel.setText(equation)

            self.label_a.setEnabled(True)
            self.label_b.setEnabled(True)
            self.label_c.setEnabled(False)
            self.textLine_a.setEnabled(True)
            self.textLine_b.setEnabled(True)
            self.textLine_c.setEnabled(False)

            x = np.linspace(-10, 10)
            y = eval(equation)
            self.ax.plot(x, y)

        elif self.radiobutton_exponential.isChecked():
            equation = self.radiobutton_exponential.type
            self.qlabel.setText(equation)

            self.label_a.setEnabled(True)
            self.label_b.setEnabled(True)
            self.label_c.setEnabled(True)
            self.textLine_a.setEnabled(True)
            self.textLine_b.setEnabled(True)
            self.textLine_c.setEnabled(True)

            x = np.linspace(-10, 10)
            y = eval(equation)
            self.ax.plot(x, y)

        else:
            equation = self.radiobutton_gaussian.type
            self.qlabel.setText(equation)

            self.label_a.setEnabled(True)
            self.label_b.setEnabled(True)
            self.label_c.setEnabled(True)
            self.textLine_a.setEnabled(True)
            self.textLine_b.setEnabled(True)
            self.textLine_c.setEnabled(True)

            x = np.linspace(-10, 10)
            y = eval(equation)
            self.ax.plot(x, y)


class Properties(QWidget):
    def __init__(self):
        super().__init__()

        layout = QGridLayout()
        label = QLabel()
        label.setText("Properties")
        layout.addWidget(label, 0, 0)

        label = QLabel()
        label.setText("Wavelength Range (nm): ")
        layout.addWidget(label, 1, 0)

        self.lineEdit_wave = QLineEdit()
        self.lineEdit_wave.setFixedSize(230, 20)
        self.lineEdit_wave.setText("400,700,5")
        layout.addWidget(self.lineEdit_wave, 1, 1)

        label = QLabel()
        label.setText("Angle Range (degree): ")
        layout.addWidget(label, 2, 0)

        self.lineEdit_angle = QLineEdit()
        self.lineEdit_angle.setFixedSize(230, 20)
        self.lineEdit_angle.setText("0,90,10")
        layout.addWidget(self.lineEdit_angle, 2, 1)

        label = QLabel()
        label.setText("Calculation Types:")
        layout.addWidget(label, 3, 0)

        self.checkBox_mode = QCheckBox()
        self.checkBox_mode.setText("Mode Analysis")
        self.checkBox_mode.setCheckState(True)
        layout.addWidget(self.checkBox_mode, 3, 1)

        self.checkBox_emission = QCheckBox()
        self.checkBox_emission.setText("Emission Spectrum")
        self.checkBox_emission.setCheckState(True)
        layout.addWidget(self.checkBox_emission, 4, 1)

        self.checkBox_power = QCheckBox()
        self.checkBox_power.setText("Power Dissipation Curve")
        self.checkBox_power.setCheckState(True)
        layout.addWidget(self.checkBox_power, 5, 1)

        self.setLayout(layout)