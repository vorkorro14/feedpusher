from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtCore import Qt, QThreadPool

from conf import MAP_WIDTH, MAP_HEIGHT, ROBOT_START_X, ROBOT_START_Y, ROBOT_LENGTH
from robot import Robot

class MainWindow(QtWidgets.QMainWindow):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.setWindowTitle("MY APP")

        self.map = QtWidgets.QLabel()
        canvas = QtGui.QPixmap(MAP_WIDTH, MAP_HEIGHT)
        self.map.setPixmap(canvas)
        self.map.pixmap().fill(QtGui.QColor("white"))
        self.setCentralWidget(self.map)

        self.mouse_is_pressed = False
        self.start_point = None
        self.end_point = None
        self.threadpool = QThreadPool()
        self.draw_robot()

    def draw_line(self, x1, y1, x2, y2):
        painter = QtGui.QPainter(self.map.pixmap())
        pen = QtGui.QPen()
        pen.setWidth(2)
        painter.setPen(pen)
        painter.drawLine(x1, y1, x2, y2)
        painter.end()

    def draw_robot(self):
        painter = QtGui.QPainter(self.map.pixmap())
        pen = QtGui.QPen()
        pen.setWidth(2)
        pen.setColor(QtGui.QColor("red"))
        painter.setPen(pen)
        painter.drawRect(*self.robot_to_map((ROBOT_START_X, ROBOT_START_Y)), 
                         ROBOT_LENGTH*10, ROBOT_LENGTH*10)
        painter.end()

    def mousePressEvent(self, e: QtGui.QMouseEvent) -> None:
        self.start_point = (e.x(), e.y())

    def mouseMoveEvent(self, e: QtGui.QMouseEvent) -> None:
        self.map.pixmap().fill(QtGui.QColor("white"))
        self.draw_line(*self.start_point, e.x(), e.y())
        self.draw_robot()
        self.update()

    def mouseReleaseEvent(self, e: QtGui.QMouseEvent) -> None:
        self.end_point = (e.x(), e.y())

        robot_instance = Robot(self.map_to_robot(self.start_point), 
                               self.map_to_robot(self.end_point))
        # robot_instance = Robot(self.start_point, self.end_point)
        self.threadpool.start(robot_instance)


    def map_to_robot(self, point):
        return point[0], self.map.pixmap().height() - point[1]
    
    def robot_to_map(self, point):
        return point[0], self.map.pixmap().height() - point[1]