import numpy as np
from shapely import Point, LineString, shortest_line, distance
from shapely.ops import nearest_points
import matplotlib.pyplot as plt

nsteps = 200

A1 = 0
A2 = 0
B1 = 40
B2 = 40
robot_x = 0
robot_y = 5
robot_orientation = 0.785

robot_trajectory_x = []
robot_trajectory_y = []

robot_velocity = 0.2   
target_line = LineString([(A1, A2), (B1, B2)])
line_orientation = np.arctan((B2 - A2) / (B1 - A1)) if B1 - A1 != 0 else 0  # Check that. from -p1/2 to pi/2

V_CONSTRAINT = 0.013
DELTA_CONSTRAINT = 0.3

b1 = 0.5
b2 = -5
b3 = -10

delta = 0
l = 2.45
u = 0   

V_plot = []
delta_plot = []
robot_trajectory_orientation = []

prev_m_point = Point(A1, A2)
mpoints = []


for i in range(0, nsteps):
    robot_pos = Point(robot_x, robot_y)
    u = np.tan(delta)/l
    v_tilda = robot_orientation - line_orientation
    #print(normal)
    m_point = nearest_points(target_line, robot_pos)[0]
    mpoints.append(m_point)
    print(nearest_points(target_line, robot_pos))
    sigma = -((m_point.y - prev_m_point.y)/distance(m_point, prev_m_point))*(m_point.x - robot_x) + \
        ((m_point.x - prev_m_point.x)/distance(m_point, prev_m_point))*(m_point.y - robot_y)
    z1 = int(np.sign(sigma)) * distance(m_point, robot_pos) # np.sign(np.pi/2 + line_orientation - np.abs(robot_orientation)))
    prev_m_point = m_point
    z2 = np.sin(v_tilda)
    z3 = np.cos(v_tilda) * (u)
    #print(z1, z2, z3)
    gamma = b1*z1+b2*z2+b3*z3
    f = z2*z3**2/(1-z2**2)  
    beta = np.cos(v_tilda)*(l*u**2+1/l)/robot_velocity
    V = (f + gamma)/beta
    V = np.clip(V, -V_CONSTRAINT, V_CONSTRAINT)
    V = -V if abs(v_tilda) > np.pi/2 else V
    delta = np.clip(delta+V, -DELTA_CONSTRAINT, DELTA_CONSTRAINT)
    robot_orientation += robot_velocity * u

    # modeling
    if robot_orientation > 2*np.pi:
        robot_orientation -= 2*np.pi
    elif robot_orientation < -2*np.pi:
        robot_orientation += 2*np.pi
    robot_x += robot_velocity * np.cos(robot_orientation)
    robot_y += robot_velocity * np.sin(robot_orientation)
    # logging
    robot_trajectory_x.append(robot_x)
    robot_trajectory_y.append(robot_y)
    robot_trajectory_orientation.append(robot_orientation)
    V_plot.append(V)
    delta_plot.append(delta)


# visualization
fg_01 = plt.figure()
ax_01 = plt.gca()

ax_01.plot(robot_trajectory_x,robot_trajectory_y,label='Robot Path')
ax_01.plot(target_line.xy[0],target_line.xy[1],label='Desired Path')
#ax_01.plot([p.x for p in mpoints], [p.y for p in mpoints],label='Points')

fg_2 = plt.figure()

ax_21 = fg_2.add_subplot(231)
ax_21.title.set_text("Orientation")
ax_21.plot(range(0, nsteps),robot_trajectory_orientation)
ax_21.plot(range(0, nsteps),[line_orientation for j in range(0, nsteps)])

ax_22 = fg_2.add_subplot(232)
ax_22.title.set_text("Delta")
ax_22.plot(range(0, nsteps), delta_plot)

ax_23 = fg_2.add_subplot(233)
ax_23.title.set_text("V")
ax_23.plot(range(0, nsteps),V_plot)

ax_24 = fg_2.add_subplot(234)
ax_24.title.set_text("X")
ax_24.plot(range(0, nsteps),robot_trajectory_x)
ax_24.plot([0,nsteps],target_line.xy[0])

ax_25 = fg_2.add_subplot(235)
ax_25.title.set_text("Y")
ax_25.plot(range(0, nsteps),robot_trajectory_y)
ax_25.plot([0,nsteps],target_line.xy[1])

plt.show()