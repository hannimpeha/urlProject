import sys
import os
from PyQt5.QtWidgets import *
from PyQt5.QtCore import QSize
from PyQt5.QtGui import QIcon


from Qtcontrollers.axes_properties import Axes_Properties
from Qtcontrollers.elements_structure import Elements_Structure
from Qtcontrollers.elements_structure_graph import Elements_Structure_Graph
from Qtcontrollers.logo_image import Logo_Image
from Qtcontrollers.plotting_param import Plotting_Param


class Real(QWidget):
    def __init__(self):
        super().__init__()
        self.making_file()
        self.making_tabs()

        layout = QGridLayout()
        layout.addWidget(self.menuBar)

        self.setMinimumSize(QSize(1680,960))
        self.setWindowTitle('JooAm Optical Simulator for Thin Film & Devices (J-OSTD)')


    def making_file(self):
        self.menuBar = QMenuBar()

        newAction = QAction(QIcon('new.png'), '&New', self)
        newAction.setShortcut('Ctrl+N')

        openAction = QAction(QIcon('open.png'), '&Open', self)
        openAction.triggered.connect(self.talk)
        openAction.setShortcut('Ctrl+O')

        exitAction = QAction(QIcon('exit.png'), '&Exit', self)
        exitAction.setShortcut('Ctrl+Q')

        fileMenu = self.menuBar.addMenu('&File')
        fileMenu.addAction(newAction)
        fileMenu.addAction(openAction)
        fileMenu.addAction(exitAction)


    def making_tabs(self):
        tab1 = QWidget()
        tab2 = QWidget()

        elem = [Elements_Structure_Graph(), Elements_Structure(), Logo_Image()]
        grid_tab1 = QGridLayout()
        positions = [(i, j) for i in range(4) for j in range(4)]

        for position, element in zip(positions, elem):
            grid_tab1.addWidget(element, *position)
        tab1.setLayout(grid_tab1)

        mlem = [Elements_Structure_Graph(), Axes_Properties(), Plotting_Param()]
        grid_tab2 = QGridLayout()
        positions = [(i, j) for i in range(4) for j in range(4)]

        for position, element in zip(positions, mlem):
            grid_tab2.addWidget(element, *position)
        tab2.setLayout(grid_tab2)

        tabs = QTabWidget()
        tabs.addTab(tab1, 'Structure')
        tabs.addTab(tab2, 'Result')
        grid = QVBoxLayout()
        grid.addWidget(tabs)

        self.setLayout(grid)

    def talk(self):
        self.dialog = QFileDialog()
        options = QFileDialog.DontResolveSymlinks | QFileDialog.ShowDirsOnly
        self.directory = QFileDialog.getExistingDirectory(self.dialog, "Open Folder", options=options)
        self.dialog.show()


if __name__ == "__main__":
    app = QApplication(sys.argv)
    path = os.path.join(os.path.dirname(sys.modules[__name__].__file__), 'favicon.ico')
    app.setWindowIcon(QIcon(path))
    window = Real()
    window.show()
    sys.exit(app.exec_())
