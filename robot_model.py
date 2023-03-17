import numpy as np
from abc import ABC, abstractmethod

from conf import ROBOT_START_X, \
    ROBOT_START_Y, ROBOT_START_YAW, \
    ROBOT_VELOCITY, ROBOT_LENGTH, \
    TURN_ANGLE_CONSTRAINT, TURN_VELOCITY_CONSTRAINT, TIMESTEP


class RobotModel(ABC):
    def __init__(self):
        self.x = ROBOT_START_X
        self.y = ROBOT_START_Y
        self.__orientation = ROBOT_START_YAW
        self.velocity = ROBOT_VELOCITY
        self.length = ROBOT_LENGTH
        self.turn_angle = 0
        self.turn_angle_constraint = TURN_ANGLE_CONSTRAINT
        self.turn_velocity_constraint = TURN_VELOCITY_CONSTRAINT

    @property
    def state(self) -> tuple:
        """Returns current state of the model

        Returns:
            tuple: (x, y, orientation, turn_angle). Current state.
        """
        return self.x, self.y, self.__orientation, self.turn_angle

    @state.setter
    def state(self, value):
        self.x, self.y, self.orientation, self.turn_angle = value

    def step(self, turn_angle: float=None, timestep: float=TIMESTEP) -> tuple:
        """Computes and applies changes of main model DOFs: \
        x, y, orientation and turn_angle. 
        I.e. this method implements evolution of the robot according to the model.

        Args:
            turn_angle (float): control signal, how to turn wheels in radians. \
            Absolute position. Left side is positive. \
            If no value provided, turn_angle is assumed as current turn_angle.

            timestep (float): step in time in the future. \
                What model state would be in timestep seconds.
        Returns:
            tuple: (x, y, orientation, turn_angle). Updated model DOFs. New state.
        """
        if turn_angle is None:
            turn_angle = self.turn_angle

        turn_angle_delta = np.clip(turn_angle - self.turn_angle, -self.turn_velocity_constraint*timestep,
                    self.turn_velocity_constraint*timestep)
        turn_angle = np.clip(self.turn_angle + turn_angle_delta, -self.turn_angle_constraint,
                        self.turn_angle_constraint)

        self._step(turn_angle, timestep)
        return self.state

    @abstractmethod
    def _step(self, turn_angle, timestep):
        raise NotImplementedError

    @abstractmethod
    def get_trajectory_curvature(self) -> float:
        """Computes current curvature of robot trajectory according to \
        its turn_angle

        Returns:
            float: current curvature of robot trajectory
        """
        raise NotImplementedError

    @property
    def orientation(self):
        return self.__orientation

    @orientation.setter
    def orientation(self, value):
        # TODO: do it in a better way
        self.__orientation = value
        if value > 2 * np.pi:
            self.__orientation = value - 2 * np.pi
        elif self.__orientation < -2 * np.pi:
            self.__orientation = value + 2 * np.pi
        else:
            self.__orientation = value


class CarRobotModel(RobotModel):
    def _step(self, turn_angle, timestep):
        self.orientation += (self.velocity*timestep) * self.get_trajectory_curvature()
        self.x += (self.velocity*timestep) * np.cos(self.orientation)
        self.y += (self.velocity*timestep) * np.sin(self.orientation)
        self.turn_angle = turn_angle
        return self.state

    def get_trajectory_curvature(self):
        return np.tan(self.turn_angle) / self.length

class TwoSegmentsRobotModel(RobotModel):
    def _step(self, turn_angle, timestep):
        self.orientation += (self.velocity*timestep) * self.get_trajectory_curvature()
        self.x += (self.velocity*timestep) * np.cos(self.orientation)
        self.y += (self.velocity*timestep) * np.sin(self.orientation)
        self.turn_angle = turn_angle
        return self.state

    def get_trajectory_curvature(self):
        return np.tan(self.turn_angle / 2) / (self.length / 2)
