import numpy as np
from shapely import Point, LineString, distance

from conf import PLANNING_HORIZON, CONTROL_RATE, TIMESTEP, \
    LINE_START_POINT, LINE_END_POINT, LINEAR_ERROR, ANGULAR_ERROR, \
    SIMULATION_MAX_STEPS
from logger import Logger
from algorithm import Algorithm
from robot_model import TwoSegmentsRobotModel

# TODO: own class for target trajectory
# line definition
target_line = LineString([LINE_START_POINT, LINE_END_POINT])
line_orientation = np.arctan((LINE_END_POINT[1] - LINE_START_POINT[1]) /
                             (LINE_END_POINT[0] - LINE_START_POINT[0])) \
                                if (LINE_END_POINT[0] - LINE_START_POINT[0]) != 0 else np.pi/2  # Check that. from -p1/2 to pi/2

# initilizing Logger
logger = Logger()

algorithm = Algorithm(logger)
robot_model = TwoSegmentsRobotModel()
real_robot = TwoSegmentsRobotModel()

for global_step_counter in range(SIMULATION_MAX_STEPS):
    # reading data from sensors
    robot_model.state = real_robot.state

    # planning
    # compute plan every CONTROL_RATE step 
    if global_step_counter % (CONTROL_RATE*TIMESTEP) == 0:
        trajectory_plan = []
        for i in range(PLANNING_HORIZON):
            # getting control
            turn_angle = algorithm.step(robot_model, target_line, line_orientation)

            # modeling
            robot_model.step(turn_angle)
            trajectory_plan.append(turn_angle)

    # sending plan to robot 
    turn_angle_command = trajectory_plan.pop(-1)
    real_robot.step(turn_angle=turn_angle_command)  

    # logging
    logger.robot_trajectory_x.append(real_robot.x)
    logger.robot_trajectory_y.append(real_robot.y)
    logger.robot_trajectory_orientation.append(real_robot.orientation)
    logger.turn_angle.append(real_robot.turn_angle)
    logger.turn_velocity.append(turn_angle_command - real_robot.turn_angle)

    # if robot comes close enough to the line, stop the simulation
    if distance(Point(real_robot.x, real_robot.y), target_line) < LINEAR_ERROR and \
        abs(line_orientation - real_robot.orientation) < ANGULAR_ERROR:
        break

logger.plot(target_line, line_orientation)
