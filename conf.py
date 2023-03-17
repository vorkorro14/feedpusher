# time
PLANNING_HORIZON = 5 # steps
CONTROL_RATE = 10 # Hz
TIMESTEP = 0.1 # seconds
SIMULATION_MAX_STEPS = 200 # steps

# line
LINE_START_POINT = (0, 0) # (m, m)
LINE_END_POINT = (0, 40) # m, m

# robot params
ROBOT_START_X = 0 # m
ROBOT_START_Y = 5 # m
ROBOT_START_YAW = 0.785 # radian    
ROBOT_START_TURN_ANGLE = 0 # radian
ROBOT_VELOCITY = 2 # m/s
ROBOT_LENGTH = 2.45 # m
TURN_ANGLE_CONSTRAINT = 0.3 # radian
TURN_VELOCITY_CONSTRAINT = 0.13 # radian/s

# algorithm params
b1 = 0.7
b2 = -5
b3 = -8

#line alignment precision
LINEAR_ERROR = 0.05
ANGULAR_ERROR = 0.01
