from shapely import LineString
import matplotlib.pyplot as plt


class Logger:
    def __init__(self):
        # TODO: make it more flexible by adding an ability to add attributes 
        self.robot_trajectory_x = []
        self.robot_trajectory_y = []
        self.V_plot = []
        self.delta_plot = []
        self.robot_trajectory_orientation = []
        self.mpoints = []

    def plot(self, target_line: LineString, line_orientation: float):
        # visualization
        # TODO: rewrite
        fg_01 = plt.figure()
        ax_01 = plt.gca()

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
        ax_22.title.set_text("Delta")
        ax_22.plot(range(0, len(self.delta_plot)), self.delta_plot)

        ax_23 = fg_2.add_subplot(233)
        ax_23.title.set_text("V")
        ax_23.plot(range(0, len(self.V_plot)), self.V_plot)

        plt.show()
