import numpy as np
from shapely import Point, LineString, distance
from shapely.ops import nearest_points

from conf import b1, b2, b3, LINE_START_POINT
from robot_model import RobotModel
from logger import Logger


class Algorithm:
    def __init__(self, logger: Logger):
        self.b1 = b1
        self.b2 = b2
        self.b3 = b3
        self.prev_m_point = Point(LINE_START_POINT)
        self.logger = logger

    def step(self, robot: RobotModel,
             target_line: LineString, line_orientation: float
             ) -> tuple:
        # TODO: rewrite with better naming
        robot_pos = Point(robot.x, robot.y)
        curvature = robot.get_trajectory_curvature()
        v_tilda = robot.orientation - line_orientation
        m_point = nearest_points(target_line, robot_pos)[0]
        self.logger.mpoints.append(m_point)
        # print(nearest_points(target_line, robot_pos))
        ds = distance(m_point, self.prev_m_point)
        sigma = -((m_point.y - self.prev_m_point.y) / ds) * (m_point.x - robot.x) + \
            ((m_point.x - self.prev_m_point.x) / ds) * (m_point.y - robot.y)
        z1 = int(np.sign(sigma)) * distance(m_point, robot_pos)
        self.prev_m_point = m_point
        z2 = np.sin(v_tilda)
        z3 = np.cos(v_tilda) * curvature
        gamma = b1 * z1 + b2 * z2 + b3 * z3
        f = z2 * z3**2 / (1 - z2**2)
        beta = np.cos(v_tilda) * (robot.length * curvature**2 + 1 / robot.length) / robot.velocity
        V = (f + gamma)/beta
        V = np.clip(V, -robot.turn_velocity_constraint,
                    robot.turn_velocity_constraint)
        V = -V if abs(v_tilda) > np.pi/2 else V
        turn_angle = np.clip(robot.turn_angle + V, -robot.turn_angle_constraint,
                        robot.turn_angle_constraint)
        self.logger.V_plot.append(V)
        self.logger.delta_plot.append(turn_angle)
        #return turn_angle
        return robot.turn_angle_constraint
