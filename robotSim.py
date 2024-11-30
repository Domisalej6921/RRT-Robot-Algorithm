import pygame
import math


class Robot:
    def __init__(self, startpos, robotimg, width, follow=None):
        self.m2p = 3779.52  # from metres to pixels

        self.leader = False  # is the robot leading the others
        self.follow = follow

        self.x, self.y = startpos  # x and y coords
        self.theta = 0  # Orientation Angle
        self.trail_set = []  # Trail of the robot
        self.a = 30  # distance from the center of the robot to the wheel (OG value 20)
        self.w = width  # width of the robot
        self.u = 30  # linear speed pix/sec
        self.W = 0  # rotational speed (rad/sec)

        self.img = pygame.image.load(robotimg)  # Loads image for the robot
        # Set the size for the image
        image_size = (80, 80)

        # Scale the image to your needed size
        self.img = pygame.transform.scale(self.img, image_size)
        self.rotated = self.img
        self.rect = self.rotated.get_rect(center=(self.x, self.y))

    def move(self, event = None):
        # Update the robot's x-coordinate based on its linear speed, orientation, and rotational speed
        self.x += (self.u * math.cos(self.theta) - self.a * math.sin(self.theta) * self.W)*dt

        # Update the robot's y-coordinate based on its linear speed, orientation, and rotational speed
        self.y += (self.u * math.sin(self.theta) + self.a * math.cos(self.theta) * self.W)*dt
        self.theta += self.W * dt

        # Apply a damping factor to the rotational speed to prevent it from increasing too rapidly
        self.W *= 0.59  # Damping factor

        # Rotate the robot's image based on its orientation angle
        self.rotated = pygame.transform.rotozoom(self.img, math.degrees(-self.theta), 1)
        self.rect = self.rotated.get_rect(center=(self.x, self.y))

        if self.leader:
            if event is not None:
                if event.type == pygame.KEYDOWN:
                    # Change the robot's linear and rotational speed based on the key pressed
                    # 0.001 m/sec = 0.1 cm / sec
                    if event.key == pygame.K_UP:
                        self.u += 0.001 * self.m2p
                    elif event.key == pygame.K_DOWN:
                        self.u -= 0.001 * self.m2p
                    elif event.key == pygame.K_LEFT:
                        self.W += 0.001 * self.m2p
                    elif event.key == pygame.K_RIGHT:
                        self.W -= 0.001 * self.m2p
            else:
                self.following()

    def following(self):
        # Get the first point in the trail set of the robot being followed
        target = self.follow.trail_set[0]
        # Calculate the difference in x-coordinates between the target and the current robot
        delta_x = target[0] - self.x
        # Calculate the difference in y-coordinates between the target and the current robot
        delta_y = target[1] - self.y
        # Update the robot's linear speed based on the target's position and the robot's orientation
        self.u = delta_x*math.cos(self.theta)+delta_y*math.sin(self.theta)
        # Update the robot's rotational speed based on the target's position and the robot's orientation
        self.W = (-1/self.a)*math.sin(self.theta)*delta_x+(1/self.a)*math.cos(self.theta)*delta_y

    def dist(self, point1, point2):

        # Gets x and y coords for each point provided
        (x1, y1) = point1
        (x2, y2) = point2
        x1 = float(x1)
        x2 = float(x2)
        y1 = float(y1)
        y2 = float(y2)

        # Distance calc
        px = (x1 - x2) ** (2)
        py = (y1 - y2) ** (2)
        distance = (px + py) ** 0.5
        return distance

    def draw(self, map):
        map.blit(self.rotated, self.rect)

    def trail(self, pos, map, color):
        # Iterate through the trail set to draw lines between consecutive points
        for i in range(0, len(self.trail_set) - 1):
            # Draw a line on the map from the current point to the next point in the trail set
            pygame.draw.line(map, color, (self.trail_set[i][0], self.trail_set[i][1]),
                             (self.trail_set[i + 1][0], self.trail_set[i + 1][1]))
        # If the trail set exceeds a certain size, remove the oldest point
        if self.trail_set.__sizeof__() > 2000:
            self.trail_set.pop(0)
        # Add the current position to the trail set
        self.trail_set.append(pos)


class Env:
    def __init__(self, dimensions):
        # Colors
        self.black = (0, 0, 0)
        self.white = (255, 255, 255)
        self.green = (0, 255, 0)
        self.blue = (0, 0, 255)
        self.red = (255, 0, 0)
        self.yel = (255, 255, 0)

        # Map Dimensions
        self.height, self.width = dimensions

        # Window Settings
        pygame.display.set_caption("Robot Sim")
        self.map = pygame.display.set_mode((self.width, self.height))

    def write_info(self):
        pass

    def robot_frame(self):
        pass


def robot_simulate(Robot, event =None):
    Robot.move(event=event)
    Robot.draw(environment.map)
    Robot.trail((Robot.x, Robot.y), environment.map, environment.red)

# init area ------------------------------------------------------------------------------------------------------------------------------------------------



pygame.init()
running = True
iterations = 0

dt = 0  # Time Step
lasttime = pygame.time.get_ticks()

# Start Pos
start = (200, 200)

# Map Dimensions
dims = (600, 1200)

# Env
environment = Env(dims)

# Robots
robots_number = 5
robots = []
robot = Robot(start,
              r'E:\School Work\Cardiff Uni - Software Engineering Degree\Year 2\Projects\RRT-Robot-Algorithm\img\f1_car.png',
              width=80,
              follow=None)  # Change images address to one on local machine

#---------------------------------------------------------------------------------------------------------------------------------
# Robots setup
robots.append(Robot(start, r'E:\School Work\Cardiff Uni - Software Engineering Degree\Year 2\Projects\RRT-Robot-Algorithm\img\f1_car.png', width=80))
robots[0].leader = True

# following robots
for i in range(1, robots_number):
    robot = Robot((start[0]-i*100, start[1]), r'E:\School Work\Cardiff Uni - Software Engineering Degree\Year 2\Projects\RRT-Robot-Algorithm\img\f1_car.png', 80, robots[i-1])
    robots.append(robot)

# anim loop ----------------------------------------------------------------------------------------------------------------------------------------------
while running:
    # Creates anim loop while user wants program open, when quite, we break out of the loop
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        for robot in robots:
            if not robot.leader and iterations < 1:
                continue
            robot_simulate(robot, event)
    for robot in robots:
        if not robot.leader and iterations < 1:
            continue
        robot_simulate(robot, event)

    pygame.display.update()
    environment.map.fill(environment.black)

    # Update Time Step
    dt = (pygame.time.get_ticks() - lasttime) / 1000  # secs
    lasttime = pygame.time.get_ticks()

    # Keeps track of the iterations
    iterations += 1
