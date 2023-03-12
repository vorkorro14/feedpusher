from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtCore import Qt, QThreadPool

from robot import Robot

class MainWindow(QtWidgets.QMainWindow):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.setWindowTitle("MY APP")

        self.label = QtWidgets.QLabel()
        canvas = QtGui.QPixmap(400, 300)
        self.label.setPixmap(canvas)
        self.label.pixmap().fill(QtGui.QColor("white"))
        self.setCentralWidget(self.label)
        self.mouse_is_pressed = False
        self.start_point = None
        self.end_point = None
        self.threadpool = QThreadPool()

    def draw_line(self, x1, y1, x2, y2):
        painter = QtGui.QPainter(self.label.pixmap())
        pen = QtGui.QPen()
        pen.setWidth(2)
        painter.setPen(pen)
        painter.drawLine(x1, y1, x2, y2)
        painter.end()

    def mousePressEvent(self, e: QtGui.QMouseEvent) -> None:
        self.start_point = (e.x(), e.y())

    def mouseMoveEvent(self, e: QtGui.QMouseEvent) -> None:
        self.label.pixmap().fill(QtGui.QColor("white"))
        self.draw_line(*self.start_point, e.x(), e.y())
        self.update()

    def mouseReleaseEvent(self, e: QtGui.QMouseEvent) -> None:
        self.end_point = (e.x(), e.y())
        robot_instance = Robot(self.start_point, self.end_point)
        self.threadpool.start(robot_instance)
