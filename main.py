import numpy as np
from shapely import LineString

from conf import NSTEPS, LINE_START_POINT, LINE_END_POINT
from logger import Logger
from algorithm import Algorithm
from robot_model import RobotModel

# line definition
target_line = LineString([LINE_START_POINT, LINE_END_POINT])
line_orientation = np.arctan((LINE_END_POINT[1] - LINE_START_POINT[1]) /
                             (LINE_END_POINT[0] - LINE_START_POINT[0])) \
                                if (LINE_END_POINT[1] - LINE_START_POINT[1]) != 0 else 0  # Check that. from -p1/2 to pi/2

# initilizing Logger

logger = Logger(NSTEPS)
algorithm = Algorithm(logger)
robot = RobotModel()

for i in range(0, NSTEPS):
    # getting control
    turn_angle = algorithm.step(robot, target_line, line_orientation)

    # modeling
    robot.step(turn_angle)

    # logging
    logger.robot_trajectory_x.append(robot.x)
    logger.robot_trajectory_y.append(robot.y)
    logger.robot_trajectory_orientation.append(robot.orientation)

logger.plot(target_line, line_orientation)
