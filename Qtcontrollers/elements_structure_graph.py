from PyQt5 import QtCore
from PyQt5.QtGui import QPixmap, QFont
from PyQt5.QtWidgets import *
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from IPython.display import clear_output
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd


foo_file = 'resources/foo.png'
em_figure = 'resources/EML_graph.png'
txt_file = 'resources/text.csv'
em_file = 'resources/text_em.csv'

class Elements_Structure_Graph(QWidget):
    def __init__(self):
        super().__init__()

        df = pd.read_csv(txt_file, header=None)
        self.layer_name = df[1]
        self.material = df[2]
        self.refractive_index = df[3]
        self.thickness = np.asarray(df[4])
        self.unit = df[5]
        self.draw_fig()
        graph = Emission_Layer_Graph()

        label_name = QLabel()
        label_name.setText("Elements Structure Graph")
        label_name.setFont(QFont("Arial", 15, weight=QFont.Bold))

        label_image = QLabel()
        pixmap = QPixmap(foo_file)
        pixmap = pixmap.scaled(430, 430, QtCore.Qt.KeepAspectRatio)
        label_image.setPixmap(pixmap)

        layout = QVBoxLayout()
        layout.addWidget(label_name)
        layout.addWidget(label_image)
        layout.addWidget(graph)
        layout.setContentsMargins(0,0,0,0)
        self.setLayout(layout)

    def draw_fig(self):
        self.fig = plt.Figure(figsize=(4.5, 4.5))
        self.canvas = FigureCanvas(self.fig)
        self.ax = self.fig.add_subplot(111)

        tps = pd.DataFrame(list(zip(self.layer_name, self.thickness)), columns=['LayerName', 'Thickness'])
        tps.pivot_table(values=["Thickness"], columns="LayerName", aggfunc='sum')
        colors = ["red", "orange", "yellow", "chartreuse", "green", "springgreen",
                  "cyan", "azure", "blue", "violet", "magenta", "pink"]
        tps.set_index('LayerName').T.plot(kind='bar', stacked=True, ax=self.ax, color=colors, width=200)

        for index, rect in enumerate(self.ax.patches):
            height = rect.get_height()
            width = rect.get_width()
            x = rect.get_x()
            y = rect.get_y()

            label_text = f'{height}'
            label_x = x + width / 2
            label_y = y + height / 2
            if height > 0:
                self.ax.text(label_x, label_y, "%s %s" % (label_text, self.layer_name[index]), ha='center', va='center',
                             fontsize=8)

        self.ax.axes.get_xaxis().set_visible(False)
        self.ax.legend().remove()

        self.fig.savefig(foo_file, transparent=True)

    def draw(self):
        tps = self.write_graph().pivot_table(values=["Thickness"], columns="LayerName", aggfunc='sum')
        tps = tps.div(tps.sum(1), axis=0)
        tps.plot.bar(stacked=True, ax=self.ax)

    def write_graph(self):
        return pd.read_csv(txt_file, header=0)


class Emission_Layer_Graph(QWidget):
    def __init__(self):
        super().__init__()
        layout = QVBoxLayout()
        tab1 = QWidget()
        tab2 = QWidget()
        tab3 = QWidget()
        tab4 = QWidget()

        label_name = QLabel()
        label_name.setText("Emission Layer Graph")
        label_name.setFont(QFont("Arial", 15, weight=QFont.Bold))

        label = QLabel()
        sub_layout = QVBoxLayout()
        pixmap = QPixmap()
        pixmap = pixmap.scaled(430, 430, QtCore.Qt.KeepAspectRatio)
        label.setPixmap(pixmap)
        label.resize(pixmap.width(), pixmap.height())
        sub_layout.addWidget(label)

        tabs = QTabWidget()

        names = pd.read_csv(em_file, header=None)[1].tolist()

        if len(names)==1:
            tabs.addTab(tab1, names[0])
        elif len(names)==2:
            tabs.addTab(tab1, names[0])
            tabs.addTab(tab2, names[1])
        elif len(names)==3:
            tabs.addTab(tab1, names[0])
            tabs.addTab(tab2, names[1])
            tabs.addTab(tab3, names[2])
        else:
            tabs.addTab(tab1, names[0])
            tabs.addTab(tab2, names[1])
            tabs.addTab(tab3, names[2])
            tabs.addTab(tab4, names[3])

        tabs.setLayout(sub_layout)
        layout.addWidget(label_name)
        layout.addWidget(tabs)

        self.setLayout(layout)