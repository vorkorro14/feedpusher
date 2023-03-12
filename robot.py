from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtCore import Qt, QRunnable, pyqtSlot

import numpy as np
from shapely import LineString

from conf import NSTEPS
from logger import Logger
from algorithm import Algorithm
from robot_model import RobotModel

class Robot(QRunnable):
    def __init__(self, line_start_point, line_end_point):
        super().__init__()
        # initilizing Logger

        self.logger = Logger(NSTEPS)
        self.algorithm = Algorithm(self.logger)
        self.robot_model = RobotModel()
        # line definition
        self.target_line = LineString([line_start_point, line_end_point])
        self.line_orientation = np.arctan((line_end_point[1] - line_start_point[1]) /
                                 (line_end_point[0] - line_start_point[0])) \
                                    if (line_end_point[1] - line_start_point[1]) != 0 else 0  # Check that. from -p1/2 to pi/2

    @pyqtSlot()
    def run(self):
        for i in range(0, NSTEPS):
            # getting control
            turn_angle = self.algorithm.step(self.robot_model, self.target_line, self.line_orientation)

            # modeling
            self.robot_model.step(turn_angle)

            # logging
            self.logger.robot_trajectory_x.append(self.robot_model.x)
            self.logger.robot_trajectory_y.append(self.robot_model.y)
            self.logger.robot_trajectory_orientation.append(self.robot_model.orientation)
        self.logger.plot(self.target_line, self.line_orientation)