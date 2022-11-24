import csv
import os

import shutil
from PyQt5 import QtCore, QtWidgets
from PyQt5.QtGui import QPixmap, QFont
from PyQt5.QtWidgets import *
import numpy as np

polar_plot = 'resources/polar_plot.png'
logo_image = 'resources/Logo.png'
graph = 'resources/polar_plot.png'
project_info = 'resources/project_info.csv'
result = 'resources/result.csv'
plotting_option = 'resources/plotting_option.csv'
data_polar_plot = "output/#3-2/angular_intensity/output_angular_intensity_bottom.txt"


class Plotting_Param(QWidget):
    def __init__(self):
        super().__init__()
        layout = QGridLayout()
        logo_image = self.logo_image()
        plotting = Plotting()
        plotting.setFixedSize(430, 500)
        exportation = Exportation()

        layout.addWidget(logo_image, 0, 0)
        layout.addWidget(plotting, 1, 0)
        layout.addWidget(exportation, 2, 0)
        self.setLayout(layout)

    def logo_image(self):
        label = QLabel()
        pixmap = QPixmap(logo_image)
        pixmap = pixmap.scaled(400, 400, QtCore.Qt.KeepAspectRatio)
        label.setPixmap(pixmap)
        label.resize(pixmap.width(), pixmap.height())
        return label


class Plotting(QWidget):
    def __init__(self):
        super().__init__()
        layout = QGridLayout()

        label = QLabel()
        label.setText("Plotting")
        label.setFont(QFont("Arial", 15, weight=QFont.Bold))
        layout.addWidget(label, 0, 0)

        layout_v = QVBoxLayout()
        layout_h = QHBoxLayout()
        self.qlabel = QLabel()
        self.qlabel.setText("Graph: ")
        layout_v.addWidget(self.qlabel)

        self.qlabel = QLabel()
        self.qlabel.setText("X-axis: ")
        layout_v.addWidget(self.qlabel)

        self.qlabel = QLabel()
        self.qlabel.setText("Y-axis: ")
        layout_v.addWidget(self.qlabel)

        self.qlabel = QLabel()
        self.qlabel.setText("Z-axis: ")
        layout_v.addWidget(self.qlabel)
        layout_h.addLayout(layout_v)

        v_layout = QVBoxLayout()
        self.combo = QComboBox()
        self.combo.setFixedSize(330, 30)
        v_layout.addWidget(self.combo)

        self.combo_x = QComboBox()
        self.combo_x.setFixedSize(330, 30)
        v_layout.addWidget(self.combo_x)

        self.combo_y = QComboBox()
        self.combo_y.setFixedSize(330, 30)
        v_layout.addWidget(self.combo_y)

        self.combo_z = QComboBox()
        self.combo_z.setFixedSize(330, 30)
        v_layout.addWidget(self.combo_z)
        layout_h.addLayout(v_layout)

        layout.addLayout(layout_h, 1, 0)
        self.combo.addItem("Mode Analysis (2D)", ["Thickness of b3p", "Thickness of npb"])
        self.combo.addItem("Mode Analysis (3D)", ["Thickness of b3p", "Thickness of npb"])
        self.combo.addItem("Current Efficiency (2D)", ["Thickness of b3p", "Thickness of npb"])
        self.combo.addItem("Current Efficiency (3D)", ["Thickness of b3p", "Thickness of npb"])
        self.combo.addItem("Emission Spectrum (2D)", ["Wavelength", "Angle"])
        self.combo.addItem("Emission Spectrum (3D)", ["Wavelength", "Angle"])
        self.combo.addItem("Power Dissipation Curve (2D)", ["In-plane Wavevector"])
        self.combo.addItem("Power Dissipation Curve (3D)", ["In-plane Wavevector"])
        self.combo.addItem("Microcavity Effect", ["Wavelength", "Angle"])
        self.combo.addItem("CIE 1931")
        self.combo.addItem("Polar Plot")

        self.combo.currentIndexChanged.connect(self.indexChangedx)
        self.combo_x.currentIndexChanged.connect(self.indexChangedy)
        self.combo_y.currentIndexChanged.connect(self.indexChangedz)
        self.combo_z.currentIndexChanged.connect(self.indexChanged)
        self.combo_y.currentIndexChanged.connect(self.indexNotChanged)

        label = QLabel()
        label.setText("Fixed Parameters:")
        layout.addWidget(label, 5, 0)

        self.table = QTableWidget()
        self.table.setRowCount(3)
        self.table.setColumnCount(2)
        self.table.setFixedSize(390, 40)
        self.table.setVerticalScrollMode(QAbstractItemView.ScrollPerPixel)
        header = self.table.horizontalHeader()
        header.setSectionResizeMode(0, QtWidgets.QHeaderView.ResizeToContents)
        header.setSectionResizeMode(1, QtWidgets.QHeaderView.Stretch)
        layout.addWidget(self.table, 6, 0)

        label = QLabel()
        label.setText("Axes Properties")
        label.setFont(QFont("Arial", 15, weight=QFont.Bold))
        label.setFixedSize(150, 20)
        layout.addWidget(label, 7, 0)

        self.table_axes = QTableWidget()
        self.table_axes.setRowCount(3)
        self.table_axes.setColumnCount(4)
        self.table.setFixedSize(430, 110)
        header = self.table_axes.horizontalHeader()
        header.setSectionResizeMode(0, QtWidgets.QHeaderView.ResizeToContents)
        header.setSectionResizeMode(1, QtWidgets.QHeaderView.Stretch)
        header.setSectionResizeMode(2, QtWidgets.QHeaderView.ResizeToContents)
        header.setSectionResizeMode(3, QtWidgets.QHeaderView.ResizeToContents)
        layout.addWidget(self.table_axes, 8, 0)

        self.indexChangedx(self.combo.currentIndex())
        self.indexChangedy(self.combo_x.currentIndex())
        self.indexChangedz(self.combo_y.currentIndex())
        self.indexNotChanged()
        self.indexChanged()

        btn = QPushButton()
        btn.setFixedSize(430, 25)
        btn.setText("Plot")
        btn.clicked.connect(self.onButtonClickedPlot)
        layout.addWidget(btn, 9, 0)

        self.setLayout(layout)


    def indexChangedx(self, index):
        self.combo_x.clear()
        data = self.combo.itemData(index)
        if data is not None:
            if self.combo.currentText() == "Mode Analysis (2D)":
                self.combo_x.addItem("Thickness of b3p", ["Optical Modes", "Air Mode",
                                                          "Substrate-Guided Mode",
                                                          "Wave-Guided Mode", "SPP Mode",
                                                          "Absorption", "NR Losses"])
                self.combo_x.addItem("Thickness of npb", ["Optical Modes", "Air Mode",
                                                          "Substrate-Guided Mode",
                                                          "Wave-Guided Mode", "SPP Mode",
                                                          "Absorption", "NR Losses"])
            elif self.combo.currentText() == "Mode Analysis (3D)":
                self.combo_x.addItem("Thickness of b3p", ["Thickness of npb"])
                self.combo_x.addItem("Thickness of npb", ["Thickness of bp3"])

            elif self.combo.currentText() == "Current Efficiency (2D)":
                self.combo_x.addItem("Thickness of b3p", ["Cd/A (photometry)", "W/mA/sr (radiometry)"])
                self.combo_x.addItem("Thickness of npb", ["Cd/A (photometry)", "W/mA/sr (radiometry)"])

            elif self.combo.currentText() == "Current Efficiency (3D)":
                self.combo_x.addItem("Thickness of b3p", ["Thickness of npb"])
                self.combo_x.addItem("Thickness of npb", ["Thickness of bp3"])

            elif self.combo.currentText() == "Emission Spectrum (2D)":
                self.combo_x.addItem("Wavelength", ["Intensity", "Intensity (p-pol)", "Intensity (s-pol)",
                                                    "Intensity (h-dipole, p-pol)", "Intensity (v-dipole, p-pol)"])
                self.combo_x.addItem("Angle", ["Intensity", "Intensity (p-pol)", "Intensity (s-pol)",
                                               "Intensity (h-dipole, p-pol)", "Intensity (v-dipole, p-pol)"])

            elif self.combo.currentText() == "Emission Spectrum (3D)":
                self.combo_x.addItem("Wavelength", ["Angle"])
                self.combo_x.addItem("Angle", ["Wavelength"])

            elif self.combo.currentText() == "Power Dissipation Curve (2D)":
                self.combo_x.addItem("In-plane Wavevector", ["Dissipated Power",
                                                             "Dissipated Power (p-pol)",
                                                             "Dissipated Power (s-pol)"])
            elif self.combo.currentText() == "Power Dissipation Curve (3D))":
                self.combo_x.addItem("In-plane Wavevector", ["Dissipated Power",
                                                             "Dissipated Power (p-pol)",
                                                             "Dissipated Power (s-pol)"])
            elif self.combo.currentText() == "Microcavity Effect":
                self.combo_x.addItem("Wavelength", ["Effective Quantum Efficiency", "Purcell Factor"])
                self.combo_x.addItem("Angle", ["Effective Quantum Efficiency", "Purcell Factor"])

            elif self.combo.currentText() == "CIE 1931":
                self.combo_x.addItems(data)
            elif self.combo.currentText() == "Polar Plot":
                self.combo_x.addItems(data)

    def indexChangedy(self, index):
        self.combo_y.clear()
        data = self.combo_x.itemData(index)
        if data is not None:
            if self.combo.currentText() == "Mode Analysis (2D)":
                self.combo_y.addItems(["Optical Modes", "Air Mode",
                                      "Substrate-Guided Mode",
                                      "Wave-Guided Mode", "SPP Mode",
                                      "Absorption", "NR Losses"])
            elif self.combo.currentText() == "Mode Analysis (3D)":
                if self.combo_x.currentText() =="Thickness of b3p":
                    self.combo_y.addItem("Thickness of npb", ["Optical Modes", "Air Mode",
                                                          "Substrate-Guided Mode",
                                                          "Wave-Guided Mode", "SPP Mode",
                                                          "Absorption", "NR Losses"])
                else:
                    self.combo_y.addItem("Thickness of b3p", ["Optical Modes", "Air Mode",
                                                              "Substrate-Guided Mode",
                                                              "Wave-Guided Mode", "SPP Mode",
                                                              "Absorption", "NR Losses"])

            elif self.combo.currentText() == "Current Efficiency (2D)":
                self.combo_y.addItems(["Cd/A (photometry)", "W/mA/sr (radiometry)"])

            elif self.combo.currentText() == "Current Efficiency (3D)":
                if self.combo_x.currentText() =="Thickness of b3p":
                    self.combo_y.addItem("Thickness of npb", ["Cd/A (photometry)",
                                                              "W/mA/sr (radiometry)"])
                else:
                    self.combo_y.addItem("Thickness of b3p", ["Cd/A (photometry)",
                                                              "W/mA/sr (radiometry)"])

            elif self.combo.currentText() == "Emission Spectrum (2D)":
                self.combo_y.addItems(["Intensity", "Intensity (p-pol)", "Intensity (s-pol)",
                                      "Intensity (h-dipole, p-pol)", "Intensity (v-dipole, p-pol)"])
            elif self.combo.currentText() == "Emission Spectrum (3D)":
                if self.combo_x.currentText() =="Wavelength":
                    self.combo_y.addItem("Angle", ["Intensity", "Intensity (p-pol)", "Intensity (s-pol)",
                                           "Intensity (h-dipole, p-pol)", "Intensity (v-dipole, p-pol)"])
                else:
                    self.combo_y.addItem("Wavelength", ["Intensity", "Intensity (p-pol)", "Intensity (s-pol)",
                                                   "Intensity (h-dipole, p-pol)", "Intensity (v-dipole, p-pol)"])

            elif self.combo.currentText() == "Power Dissipation Curve (2D)":
                self.combo_y.addItems(["Dissipated Power", "Dissipated Power (p-pol)",
                                       "Dissipated Power (s-pol)"])
            elif self.combo.currentText() == "Power Dissipation Curve (3D))":
                self.combo_y.addItem("Dissipated Power", ["Dissipated Power (p-pol)",
                                                          "Dissipated Power (s-pol)"])
                self.combo_y.addItem("Dissipated Power (p-pol)", ["Dissipated Power",
                                                          "Dissipated Power (s-pol)"])
                self.combo_y.addItem("Dissipated Power (s-pol)", ["Dissipated Power",
                                                                  "Dissipated Power (p-pol)"])
            elif self.combo.currentText() == "Microcavity Effect":
                self.combo_y.addItems(data)

            elif self.combo.currentText() == "CIE 1931":
                self.combo_y.addItems(data)

            elif self.combo.currentText() == "Polar Plot":
                self.combo_y.addItems(data)


    def indexChangedz(self, index):
        self.combo_z.clear()
        data = self.combo_y.itemData(index)
        if data is not None:
            if self.combo.currentText() == "Mode Analysis (2D)":
                self.combo_z.addItems(data)
            elif self.combo.currentText() == "Mode Analysis (3D)":
                self.combo_z.addItems(["Optical Modes", "Air Mode",
                                       "Substrate-Guided Mode",
                                       "Wave-Guided Mode", "SPP Mode",
                                        "Absorption", "NR Losses"])
            elif self.combo.currentText() == "Current Efficiency (2D)":
                self.combo_z.addItems(data)
            elif self.combo.currentText() == "Current Efficiency (3D)":
                self.combo_z.addItems(["Cd/A (photometry)", "W/mA/sr (radiometry)"])
            elif self.combo.currentText() == "Emission Spectrum (2D)":
                self.combo_z.addItems(data)
            elif self.combo.currentText() == "Emission Spectrum (3D)":
                self.combo_z.addItems(["Intensity", "Intensity (p-pol)", "Intensity (s-pol)",
                                       "Intensity (h-dipole, p-pol)", "Intensity (v-dipole, p-pol)"])
            elif self.combo.currentText() == "Power Dissipation Curve (2D)":
                self.combo_z.addItems(data)
            elif self.combo.currentText() == "Power Dissipation Curve (3D))":
                self.combo_z.addItems(["Dissipated Power", "Dissipated Power (p-pol)",
                                      "Dissipated Power (s-pol)"])
            elif self.combo.currentText() == "Microcavity Effect":
                self.combo_z.addItems(data)
            elif self.combo.currentText() == "CIE 1931":
                self.combo_z.addItems(data)
            elif self.combo.currentText() == "Polar Plot":
                self.combo_z.addItems(data)

    def indexNotChanged(self):
        self.table.clear()
        self.x=[]
        self.y=[]
        cols_element = ['Name', 'Measure']
        self.table.setHorizontalHeaderLabels(cols_element)

        if self.combo.currentText() == "Mode Analysis (2D)":
            if self.combo_x.currentText() =="Thickness of b3p":
                self.x.append("Thickness of npb")
                self.y.append("30")
            else:
                self.x.append("Thickness of b3p")
                self.y.append("30")
        elif self.combo.currentText() == "Current Efficiency (2D)":
            if self.combo_x.currentText() == "Thickness of b3p":
                self.x.append("Thickness of npb")
                self.y.append("30")
            else:
                self.x.append("Thickness of b3p")
                self.y.append("30")
        elif self.combo.currentText() == "Emission Spectrum (2D)":
            if self.combo_x.currentText() == "Wavelength":
                self.x.append("Angle")
                self.y.append("0")
            else:
                self.x.append("Wavelength")
                self.y.append("400")
        # elif self.combo.currentText() == "Power Dissipation Curve (2D)":
        #     if self.combo_x.currentText() == "Dissipated Power":
        #         self.x.append(["Dissipated Power (p-pol)", "Dissipated Power (s-pol)"])
        #         self.y.append(["400", "400"])
        #     elif self.combo_x.currentText() == "Dissipated Power (p-pol)":
        #         self.x.append(["Dissipated Power", "Dissipated Power (s-pol)"])
        #         self.y.append(["400", "400"])
        #     else:
        #         self.x.append(["Dissipated Power", "Dissipated Power (p-pol)"])
        #         self.y.append(["400", "400"])
        elif self.combo.currentText() == "Microcavity Effect":
            if self.combo_x.currentText() == "Wavelength":
                self.x.append("Angle")
                self.y.append("0")
            else:
                self.x.append("Wavelength")
                self.y.append("400")
        else:
            self.x.append("")
            self.y.append("")

        self.tempList = [[self.x, self.y]]
        self.num_row = len(self.tempList)

        for i in range(len(self.x)):
            self.num_row = i
            self.table.setItem(self.num_row, 0, QTableWidgetItem(self.x[i]))
            self.table.setItem(self.num_row, 1, QTableWidgetItem(self.y[i]))
        self.indexChanged()

    def indexChanged(self):
        self.table_axes.clear()
        cols_element = ["Axis", 'Name', 'Minimum', 'Maximum']
        self.table_axes.setHorizontalHeaderLabels(cols_element)
        self.axis = ["X-axis", "Y-axis", "Z-axis"]
        self.name = [self.combo_x.currentText(), self.combo_y.currentText(),
                     self.combo_z.currentText()]
        min_max = []
        for i in range(len(self.name)):
            if self.name[i] == "Thickness of b3p":
                min_max.append([10, 50])
            elif self.name[i] == "Thickness of npb":
                min_max.append([10, 50])

            elif self.name[i] == "Optical Modes":
                min_max.append([0.1, 0.3])
            elif self.name[i] == "Air Mode":
                min_max.append([0.1, 0.3])
            elif self.name[i] == "Substrate-Guided Mode":
                min_max.append([0.1, 0.3])
            elif self.name[i] == "Wave-Guided Mode":
                min_max.append([0.1, 0.3])
            elif self.name[i] == "SPP Mode":
                min_max.append([0.1, 0.3])
            elif self.name[i] == "Absorption":
                min_max.append([0.1, 0.3])
            elif self.name[i] == "NR Losses":
                min_max.append([0.1, 0.3])

            elif self.name[i] == "Wavelength":
                min_max.append([400, 700])
            elif self.name[i] == "Angle":
                min_max.append([0, 90])

            elif self.name[i] == "Cd/A (photometry)":
                min_max.append([11.5, 28.6])
            elif self.name[i] == "W/mA/sr (radiometry)":
                min_max.append([71, 217])

            elif self.name[i] == "Intensity":
                min_max.append([0.0, 3.0])
            elif self.name[i] == "Intensity (p-pol)":
                min_max.append([0.0, 3.0])
            elif self.name[i] == "Intensity (h-dipole, p-pol)":
                min_max.append([0.0, 3.0])
            elif self.name[i] == "Intensity (v-dipole, p-pol)":
                min_max.append([0.0, 3.0])

            elif self.name[i] == "In-plane Wavevector":
                min_max.append([0.0, 1.96])

            elif self.name[i] == "Dissipated Power":
                min_max.append([0, 412])
            elif self.name[i] == "Dissipated Power (p-pol)":
                min_max.append([0, 412])
            elif self.name[i] == "Dissipated Power (s-pol)":
                min_max.append([0, 412])

            elif self.name[i] == "Effective Quantum Efficiency":
                min_max.append([0.77, 0.87])
            elif self.name[i] == "Purcell Factor":
                min_max.append([0.87, 1.67])
            else:
                min_max.append(["-","-"])

        mat = np.array(min_max).transpose()
        self.min = mat[0]
        self.max = mat[1]

        self.tempList = [[self.axis, self.name, self.min, self.max]]
        self.num_row = len(self.tempList)

        for i in range(len(self.axis)):
            self.num_row = i
            self.table_axes.setItem(self.num_row, 0, QTableWidgetItem(self.axis[i]))
            self.table_axes.setItem(self.num_row, 1, QTableWidgetItem(self.name[i]))
            self.table_axes.setItem(self.num_row, 2, QTableWidgetItem(str(self.min[i])))
            self.table_axes.setItem(self.num_row, 3, QTableWidgetItem(str(self.max[i])))

    def onButtonClickedPlot(self):
        with open(plotting_option, 'w') as stream:
            writer = csv.writer(stream, lineterminator='\n')
            rowdata = [[self.combo.currentText()], [self.combo_x.currentText()],
                       [self.combo_y.currentText()], [self.combo_z.currentText()]]
            for item in rowdata:
                writer.writerow(item)

    def onChanged(self, text):
        self.qlabel.setText(text)
        self.qlabel.adjustSize()


class Exportation(QWidget):
    def __init__(self):
        super().__init__()

        self.image = polar_plot
        self.path = os.getcwd()
        self.name = "2PPlAn_33PYMPM"
        # with open(project_info, "r") as pi:
        #     self.name = pi.readline()
        self.data_path = data_polar_plot

        layout = QGridLayout()
        layout.setContentsMargins(0,0,0,0)
        label = QLabel()
        label.setText("Exportation")
        label.setFont(QFont("Arial", 15, weight=QFont.Bold))
        layout.addWidget(label, 0, 0)

        hlayout = QHBoxLayout()
        label = QLabel()
        label.setText("Path: ")
        hlayout.addWidget(label)

        lineEdit = QLineEdit()
        lineEdit.setText(self.path)
        lineEdit.setFixedSize(250, 20)
        hlayout.addWidget(lineEdit)

        btn = QPushButton()
        btn.setText("Browse")
        btn.clicked.connect(self.talk)
        hlayout.addWidget(btn)

        layout.addLayout(hlayout, 1, 0)

        hlayout = QHBoxLayout()
        label = QLabel()
        label.setText("Type: ")
        hlayout.addWidget(label)

        check_text = QCheckBox()
        check_text.setText("Text")
        check_text.setChecked(True)
        check_text.setStyleSheet("QCheckBox::indicator { width: 20px; height: 20px;}")
        hlayout.addWidget(check_text)

        check_image = QCheckBox()
        check_image.setText("Image")
        check_text.setChecked(True)
        check_image.setStyleSheet("QCheckBox::indicator { width: 20px; height: 20px;}")
        hlayout.addWidget(check_image)

        #hlayout.setAlignment(QtCore.Qt.AlignLeft)

        layout.addLayout(hlayout, 2, 0)

        hlayout = QHBoxLayout()
        label = QLabel()
        label.setText("Name: ")
        hlayout.addWidget(label)

        lineEdit = QLineEdit()
        lineEdit.setText(self.name)
        lineEdit.setFixedSize(250, 20)
        hlayout.addWidget(lineEdit)

        self.btn = QPushButton()
        self.btn.setText("Export")

        if(check_text.setChecked(True)):
            btn.clicked.connect(self.handleTextSave)
        elif (check_image.setChecked(True)):
            btn.clicked.connect(self.handleImageSave)

        hlayout.addWidget(self.btn)

        layout.addLayout(hlayout, 3, 0)
        self.setLayout(layout)

    def talk(self):
        self.dialog = QFileDialog()
        options = QFileDialog.DontResolveSymlinks | QFileDialog.ShowDirsOnly
        self.directory = QFileDialog.getExistingDirectory(self.dialog, "Open Folder", options=options)
        self.dialog.show()
        return self.directory

    def handleImageSave(self):
        self.name.join(".png")
        real_path = os.path.join(self.path, self.name)
        # shutil.copy(self.image, str(real_path))
        with open(self.image, "rb") as real_image:
            data = real_image.read()
        with open(real_path, "wb") as stream:
            stream.write(data)

    def handleTextSave(self):
        self.name.join(".txt")
        real_path = os.path.join(self.path, self.name)
        with open(real_path, 'w') as stream:
            stream.write(open(self.data_path, "r").read())
            stream.close()