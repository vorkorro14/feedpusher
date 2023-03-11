import numpy as np

from conf import ROBOT_START_X, \
    ROBOT_START_Y, ROBOT_START_YAW, \
    ROBOT_VELOCITY, ROBOT_LENGTH, \
    TURN_ANGLE_CONSTRAINT, TURN_VELOCITY_CONSTRAINT


class RobotModel:
    def __init__(self):
        self.x = ROBOT_START_X
        self.y = ROBOT_START_Y
        self.__orientation = ROBOT_START_YAW
        self.velocity = ROBOT_VELOCITY
        self.length = ROBOT_LENGTH
        self.turn_angle = 0
        self.turn_angle_constraint = TURN_ANGLE_CONSTRAINT
        self.turn_velocity_constraint = TURN_VELOCITY_CONSTRAINT

    def step(self, u, turn_angle):
        self.orientation += self.velocity * u
        self.x += self.velocity * np.cos(self.orientation)
        self.y += self.velocity * np.sin(self.orientation)
        self.turn_angle = turn_angle

    @property
    def orientation(self):
        return self.__orientation

    @orientation.setter
    def orientation(self, value):
        self.__orientation = value
        if value > 2 * np.pi:
            self.__orientation = value - 2 * np.pi
        elif self.__orientation < -2 * np.pi:
            self.__orientation = value + 2 * np.pi
        else:
            self.__orientation = value
