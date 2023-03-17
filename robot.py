from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtCore import Qt, QRunnable, pyqtSlot

import numpy as np
from shapely import Point, LineString, distance

from conf import PLANNING_HORIZON, CONTROL_RATE, TIMESTEP, \
    LINEAR_ERROR, ANGULAR_ERROR, SIMULATION_MAX_STEPS
from logger import Logger
from algorithm import Algorithm
from robot_model import TwoSegmentsRobotModel

class Robot(QRunnable):
    def __init__(self, line_start_point, line_end_point):
        super().__init__()
        # TODO: own class for target trajectory
        # initilizing Logger
        self.logger = Logger()
        self.done = False
        self.algorithm = Algorithm()
        self.robot_model = TwoSegmentsRobotModel()
        self.real_robot = TwoSegmentsRobotModel()
        # line definition
        self.target_line = LineString([line_start_point, line_end_point])
        self.line_orientation = np.arctan((line_end_point[1] - line_start_point[1]) /
                                 (line_end_point[0] - line_start_point[0])) \
                                    if (line_end_point[1] - line_start_point[1]) != 0 else np.pi/2  # Check that. from -p1/2 to pi/2

    @pyqtSlot()
    def run(self):
        for global_step_counter in range(SIMULATION_MAX_STEPS):
            # reading data from sensors
            self.robot_model.state = self.real_robot.state

            # planning
            # compute plan every CONTROL_RATE step 
            if global_step_counter % (CONTROL_RATE*TIMESTEP) == 0:
                trajectory_plan = []
                for i in range(PLANNING_HORIZON):
                    # getting control
                    turn_angle = self.algorithm.step(self.robot_model, 
                                                     self.target_line, 
                                                     self.line_orientation)

                    # modeling
                    self.robot_model.step(turn_angle)
                    trajectory_plan.append(turn_angle)
            print(global_step_counter)
            # sending plan to robot 
            turn_angle_command = trajectory_plan.pop(-1)
            self.real_robot.step(turn_angle=turn_angle_command)  

            # logging
            self.logger.robot_trajectory_x.append(self.real_robot.x)
            self.logger.robot_trajectory_y.append(self.real_robot.y)
            self.logger.robot_trajectory_orientation.append(self.real_robot.orientation)
            self.logger.turn_angle.append(self.real_robot.turn_angle)
            self.logger.turn_velocity.append(turn_angle_command - self.real_robot.turn_angle)

            # if robot comes close enough to the line, stop the simulation
            if distance(Point(self.real_robot.x, self.real_robot.y), self.target_line) < LINEAR_ERROR and \
                abs(self.line_orientation - self.real_robot.orientation) < ANGULAR_ERROR:
                self.done = True
                break

        if self.done:
            print("LINE IS REACHED.\n\nCheck map.jpg and logs.jpg")
        else:
            print("LINE IS NOT REACHED. INCREASE MAX_SIMULATION_STEPS")

        self.logger.plot(self.target_line, self.line_orientation)