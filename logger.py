from shapely import LineString
import matplotlib.pyplot as plt
from conf import MAP_HEIGHT, MAP_WIDTH


class Logger:
    def __init__(self):
        # TODO: make it more flexible by adding an ability to add attributes 
        self.robot_trajectory_x = []
        self.robot_trajectory_y = []
        self.turn_velocity = []
        self.turn_angle = []
        self.robot_trajectory_orientation = []
        self.mpoints = []

    def plot(self, target_line: LineString, line_orientation: float):
        # visualization
        # TODO: rewrite
        fg_01 = plt.figure()
        ax_01 = plt.gca()
        ax_01.set_xlim(MAP_WIDTH)
        ax_01.invert_xaxis()
        ax_01.set_ylim(MAP_HEIGHT)
        ax_01.invert_yaxis()
        ax_01.plot(self.robot_trajectory_x,self.robot_trajectory_y,label='Robot Path')
        ax_01.plot(target_line.xy[0],target_line.xy[1],label='Desired Path')
        #ax_01.plot([p.x for p in mpoints], [p.y for p in mpoints],label='Points')

        fg_2 = plt.figure()

        ax_21 = fg_2.add_subplot(231)
        ax_21.title.set_text("Orientation")
        nsteps = len(self.robot_trajectory_orientation)
        ax_21.plot(range(0, nsteps), 
                   self.robot_trajectory_orientation)
        ax_21.plot(range(0, nsteps),
                   [line_orientation for j in range(0, nsteps)])

        ax_22 = fg_2.add_subplot(232)
        ax_22.title.set_text("Turn angle")
        ax_22.plot(range(0, len(self.turn_angle)), self.turn_angle)

        ax_23 = fg_2.add_subplot(233)
        ax_23.title.set_text("Turn velocity")
        ax_23.plot(range(0, len(self.turn_velocity)), self.turn_velocity)

        ax_24 = fg_2.add_subplot(234)
        ax_24.title.set_text("X")
        ax_24.plot(range(0, len(self.robot_trajectory_x)), self.robot_trajectory_x)

        ax_25 = fg_2.add_subplot(235)
        ax_25.title.set_text("Y")
        ax_25.plot(range(0, len(self.robot_trajectory_y)), self.robot_trajectory_y)

        fg_01.savefig("map.jpg")
        fg_2.savefig("logs.jpg")