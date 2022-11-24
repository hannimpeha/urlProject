import csv
from datetime import datetime
import socket
from PyQt5 import QtCore
from PyQt5.QtCore import QThread, QObject
from PyQt5.QtGui import QPixmap, QFont
from PyQt5.QtWidgets import *
# from selenium import webdriver
from ctypes import *
import sys


logo_image = 'resources/Logo.png'
so_file = "c/hannimpeha.so"
file_p = 'resources/text_p.csv'
project_info = 'resources/project_info.csv'


class Logo_Image(QWidget):
    def __init__(self):
        super().__init__()
        layout = QGridLayout()
        logo_image = self.logo_image()
        layout.addWidget(logo_image, 0, 0)
        properties = Properties()
        layout.addWidget(properties, 1, 0)
        execute = Execute()
        layout.addWidget(execute, 2, 0)
        project_into = Project_Info()
        layout.addWidget(project_into, 3, 0)
        self.setLayout(layout)


    def logo_image(self):
        label = QLabel()
        pixmap = QPixmap(logo_image)
        pixmap = pixmap.scaled(400, 400, QtCore.Qt.KeepAspectRatio)
        label.setPixmap(pixmap)
        label.resize(pixmap.width(), pixmap.height())
        return label


class Properties(QWidget):
    def __init__(self):
        super().__init__()

        layout = QGridLayout()
        label = QLabel()
        label.setText("Properties")
        label.setFont(QFont("Arial", 15, weight=QFont.Bold))
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

        # drawButton = QPushButton("Save")
        # drawButton.clicked.connect(self.handleSave)
        # drawButton.setFixedSize(230, 30)
        # layout.addWidget(drawButton, 6, 1)

        self.setLayout(layout)

    def handleSave(self):
        with open(file_p, 'w') as stream:
            writer = csv.writer(stream, lineterminator='\n')
            rowdata = [[self.lineEdit_wave.text()], [self.lineEdit_angle.text()],
                       [self.checkBox_mode.text()], [self.checkBox_emission.text()],
                       [self.checkBox_power.text()]]
            for item in rowdata:
                writer.writerow(item[0].strip('"').split(','))


class Execute(QWidget):
    def __init__(self):
        super().__init__()

        layout = QVBoxLayout()

        label = QLabel()
        label.setText("Progress")
        label.setFont(QFont("Arial", 15, weight=QFont.Bold))
        label.setFixedSize(100, 20)
        layout.addWidget(label)

        self.thread = QThread()
        self.worker = Worker()
        self.worker.moveToThread(self.thread)

        layout.addWidget(self.worker.pbar)
        layout.addWidget(self.worker.btn)

        textEdit = QTextEdit()
        textEdit.setFixedSize(400, 100)
        textEdit.setText(str(sys.stdout))
        layout.addWidget(textEdit)

        self.setLayout(layout)


class Worker(QObject):
    def __init__(self):
        super().__init__()
        self.step = 0
        self.btn = QPushButton('Run')
        self.btn.setFixedSize(410, 50)
        self.btn.move(40, 80)
        self.btn.clicked.connect(self.doWork)

        DEFAULT_STYLE = """
                            QProgressBar{
                                border: 1px solid grey;
                                border-radius: 8px;                     
                                text-align: center
                            }

                            QProgressBar::chunk {
                                background-color: lightblue;
                                width: 10px;
                                margin: 1px;
                            }
                        """

        self.pbar = QProgressBar()
        self.pbar.setGeometry(30, 40, 200, 40)
        self.pbar.setStyleSheet(DEFAULT_STYLE)
        self.pbar.setRange(0, 100)


    def doWork(self):
        self.btn.setText("Stop")

        my = cdll.LoadLibrary(so_file)
        my.main()

        # browser = webdriver.Chrome()
        # links = ['http://google.com']
        # for link in links:
        #     browser.get(link)
        #     self.step += 100 / len(links)
        #     self.pbar.setValue(self.step)
        #     if self.step >= 100:
        #         self.btn.setText('Finished')
        #         return
        # browser.close()


class Project_Info(QWidget):
    def __init__(self):
        super().__init__()
        layout = QHBoxLayout()

        layout1 = QGridLayout()
        label = QLabel()
        label.setText("Project Info")
        label.setFont(QFont("Arial", 15, weight=QFont.Bold))
        layout1.addWidget(label, 0, 0)

        label_name = QLabel()
        label_name.setText("Name")
        layout1.addWidget(label_name, 1, 0)

        label = QLabel()
        label.setText("Designer")
        layout1.addWidget(label, 2, 0)

        label = QLabel()
        label.setText("Analyzer")
        layout1.addWidget(label, 3, 0)

        label = QLabel()
        label.setText("Creation Date")
        layout1.addWidget(label, 4, 0)

        label = QLabel()
        label.setText("Modified Date")
        layout1.addWidget(label, 5, 0)

        label = QLabel()
        label.setText("IP Address")
        layout1.addWidget(label, 6, 0)

        self.name_label = QLineEdit()
        self.name_label.setFixedSize(180, 20)
        self.name_label.setText("2PPlAn_33PYMPM")
        layout1.addWidget(self.name_label, 1, 1)

        self.label_designer = QLabel()
        self.label_designer.setFixedSize(180, 20)
        self.label_designer.setText("Hannah Lee")
        layout1.addWidget(self.label_designer, 2, 1)

        self.label_analyzer = QLineEdit()
        self.label_analyzer.setFixedSize(180, 20)
        self.label_analyzer.setText("Hannah Lee")
        layout1.addWidget(self.label_analyzer, 3, 1)

        self.c_date = QLineEdit()
        self.c_date.setFixedSize(180, 20)
        self.c_date.setText(datetime.today().strftime('%Y-%m-%d'))
        layout1.addWidget(self.c_date, 4, 1)

        self.m_date = QLabel()
        self.m_date.setText(datetime.today().strftime('%Y-%m-%d'))
        layout1.addWidget(self.m_date, 5, 1)

        self.qlabel_ip = QLabel()
        self.qlabel_ip.setText(self.get_ip())
        layout1.addWidget(self.qlabel_ip, 6, 1)

        layout2 = QHBoxLayout()
        button = QPushButton()
        button.setText("Save")
        button.setFixedSize(100, 170)
        button.clicked.connect(self.handleSave)
        layout2.addWidget(button)

        layout.addLayout(layout1)
        layout.addLayout(layout2)
        self.setLayout(layout)

    def handleSave(self):
        with open(project_info, 'w') as stream:
            writer = csv.writer(stream, lineterminator='\n')
            rowdata = [[self.name_label.text()], [self.label_designer.text()],
                       [self.label_analyzer.text()], [self.c_date.text()],
                       [self.m_date.text()]]
            for item in rowdata:
                writer.writerow(item[0].strip('"').split(','))

    def get_ip(self):
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        try:
            s.connect(('10.255.255.255', 1))
            IP = s.getsockname()[0]
        except Exception:
            IP = '127.0.0.1'
        finally:
            s.close()
        return IP