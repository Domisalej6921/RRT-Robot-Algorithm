import pygame
import math

class Robot:
    def __init__(self, startpos, robotimg, width, follow = None):
        self.m2p = 37779.52     # from metres to pixels

        self.leader = False # is the robot leading the others
        self.follow = follow

        self.x, self.y = startpos
        self.theta = 0
        self.w = width
        self.u = 30  # linear speed pix/sec
        self.w = 0  # rotational speed

        self.img = pygame.image.load(robotimg)  # Loads image for the robot
        # Set the size for the image
        image_size = (80, 80)

        # Scale the image to your needed size
        self.img = pygame.transform.scale(self.img, image_size)
        self.rotated = self.img
        self.rect = self.rotated.get_rect(center=(self.x, self.y))

    def move(self):
        pass

    def following(self):
        pass

    def dist(self, point1, point2):

        #Gets x and y coords for each point provided
        (x1, y1) = point1
        (x2, y2) = point2
        x1 = float(x1)
        x2 = float(x2)
        y1 = float(y1)
        y2 = float(y2)

        # Distance calc
        px = ( x1-x2 ) ** (2)
        py = ( y1-y2 ) ** (2)
        distance = ( px+py ) ** 0.5
        return distance

    def draw(self, map):
        map.blit(self.rotated, self.rect)

    def trail(self):
        pass

class Env:
    def __init__(self, dimensions):
        #Colors
        self.black = (0, 0, 0)
        self.white = (255, 255, 255)
        self.green = (0, 255, 0)
        self.blue = (0, 0, 255)
        self.red = (255, 0, 0)
        self.yel = (255, 255, 0)

        #Map Dimensions
        self.height, self.width = dimensions

        #Window Settings
        pygame.display.set_caption("Robot Sim")
        self.map = pygame.display.set_mode((self.width, self.height))

    def write_info(self):
        pass

    def robot_frame(self):
        pass

# init area ------------------------------------------------------------------------------------------------------------------------------------------------

pygame.init()
running = True
iterations = 0

# Start Pos
start = (200, 200)

# Map Dimensions
dims = (600, 1200)

# Env
environment = Env(dims)

# Robot
robot = Robot(start, r'E:\School Work\Cardiff Uni - Software Engineering Degree\Year 2\Projects\RRT-Robot-Algorithm\img\f1_car.png',
              width=80,
              follow=None)  # Change images address to one on local machine

# anim loop ----------------------------------------------------------------------------------------------------------------------------------------------
while running:
    # Creates anim loop while user wants program open, when quite, we break out of the loop
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    environment.map.fill(environment.black)
    robot.draw(environment.map)
    pygame.display.update()
    # Keeps track of the iterations
    iterations += 1