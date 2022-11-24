import matplotlib.pyplot as plt
import numpy as np
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from IPython.display import clear_output

equation = "0.5*x + 1"
# fig = plt.Figure(figsize=(2.5, 2.5))
# canvas = FigureCanvas(fig)
# x_range = 1
# x = np.array(x_range)
# y = eval(equation)
# ax = fig.add_subplot(111)
# ax.plot(x, y)


for i in range(50):
    clear_output(wait=True)
    x = np.linspace(-10, 10)
    y = eval(equation)
    plt.plot(x, y)
    plt.show()