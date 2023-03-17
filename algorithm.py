import numpy as np
from shapely import Point, LineString, distance
from shapely.ops import nearest_points

from conf import b1, b2, b3, TIMESTEP
from robot_model import RobotModel


class Algorithm:
    def __init__(self):
        self.b1 = b1
        self.b2 = b2
        self.b3 = b3
        self.prev_m_point = Point(0, 0)

    def step(self, robot: RobotModel,
             target_line: LineString, line_orientation: float,
             timestep=TIMESTEP) -> tuple:
        # TODO: rewrite with better naming
        robot_pos = Point(robot.x, robot.y)
        curvature = robot.get_trajectory_curvature()
        orientation_diff = robot.orientation - line_orientation
        try:
            # find nearest trajectory point
            m_point = nearest_points(target_line, robot_pos)[0]
            # print(nearest_points(target_line, robot_pos))
            ds = distance(m_point, self.prev_m_point)
            sigma = -((m_point.y - self.prev_m_point.y) / ds) * (m_point.x - robot.x) + \
                ((m_point.x - self.prev_m_point.x) / ds) * (m_point.y - robot.y)
            z1 = int(np.sign(sigma)) * distance(m_point, robot_pos)
            self.prev_m_point = m_point
            z2 = np.sin(orientation_diff)
            z3 = np.cos(orientation_diff) * curvature
            gamma = b1 * z1 + b2 * z2 + b3 * z3
            f = z2 * z3**2 / (1 - z2**2)
            beta = np.cos(orientation_diff) * (robot.length * curvature**2 + 1 / robot.length) / (robot.velocity*timestep)
            turn_angle_delta = (f + gamma)/beta
        except ValueError:
            raise ValueError('Robot is too close to line ends.\n\
                             Start from another point, change line params or\n\
                             reduce MAX_SIMULATION_STEPS')
        turn_angle_delta = np.clip(turn_angle_delta, -robot.turn_velocity_constraint*timestep,
                    robot.turn_velocity_constraint*timestep)
        turn_angle_delta = -turn_angle_delta if abs(orientation_diff) > np.pi/2 else turn_angle_delta
        turn_angle = np.clip(robot.turn_angle + turn_angle_delta, -robot.turn_angle_constraint,
                        robot.turn_angle_constraint)
        return turn_angle
