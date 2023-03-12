import sys
import numpy as np
from shapely import LineString

from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *

from main_window import MainWindow

# TODO: own class for target trajectory

app = QApplication(sys.argv)

window = MainWindow()
window.show()

app.exec_()
