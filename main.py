import pygame
import sys
import random
import copy
import math

# Initialize Pygame
pygame.init()

# Define the grid and square sizes
grid_size = (20, 20)
square_size = (45, 45)

# Calculate the size of the window
window_width = grid_size[0] * square_size[0]
window_height = grid_size[1] * square_size[1]

# Snake's head
head_position = [400,400]
head_speed = 700
head_color = (100,0,0)
head = pygame.Rect(head_position[0], head_position[1], square_size[0], square_size[1])
head_is_moving = 0

# Heads fov
fov_jump = 15
fov_radi = 195
fov_start = [head.center[0] - square_size[0]/2 - fov_radi/2, head.center[1] - square_size[1]/2 - fov_radi/2]

k = int(fov_radi/fov_jump)
fov_points = [[[0, 0] for _ in range(k)] for _ in range(k)]

def update_fov():
    if head_is_moving == True:
        for i, row in enumerate(fov_points):
            for j, column in enumerate(row):
                fov_points[i][j] = [fov_start[0] + j * fov_jump, fov_start[1] + i * fov_jump]
                fov_rects[i][j].center = fov_points[i,j]

fov_rects = [[[0, 0] for _ in range(k)] for _ in range(k)]

for i, row in enumerate(fov_rects):
    for j, column in enumerate(row):
        fov_rects[i][j] = pygame.Rect(fov_points[i][j][0], fov_points[i][j][1], 2, 2)

def draw_fov_rects():
    for i, row in enumerate(fov_rects):
        for j, column in enumerate(row):
            pygame.draw.rect(window,(40,40,40),fov_rects[i][j])

def head_is_moving_updater():
    global head_is_moving
    if head_is_moving < 3:
        head_is_moving += 1
    else: head_is_moving = 0

def head_updater():
    head.topleft = head_position
    Obstacle.head_obstacle_collisions_hander()
    head_is_moving_updater()

# Random pair generator
def random_2d_position_generator():
    random_x = random.randint(0,window_width)
    random_y = random.randint(0, window_height)
    return [random_x,random_y]


# Game_Object class
class Game_Object:
    size = None
    number = None
    color = None

    global_object_list = [head]

    def generate_position(self):
        valid_position = False

        while valid_position == False:

            self.position = random_2d_position_generator()
            self.position[0] = min(self.position[0], window_width - self.size[0])
            self.position[1] = min(self.position[1], window_height - self.size[1])
            self.rect.topleft = self.position

            valid_position = True
            for game_object in self.global_object_list:
                if game_object is not self:
                    if self.rect.colliderect(game_object):
                        valid_position = False
                        break

    def __init__(self):
        self.rect = pygame.Rect(0,0,self.size[0],self.size[1])
        self.generate_position()
        self.global_object_list.append(self)

    def create(cls):
        while len(cls.list) < cls.number:
            cls.list.append(cls())

# Food properties
class Food(Game_Object):
    size = [30, 30]
    number = random.randint(70,130)
    color = (random.randint(200,245),random.randint(150,200),random.randint(40,100))
    list = []

# Obstacle properties
class Obstacle(Game_Object):
    size = [50, 50]
    number = random.randint(20,35)
    color = (random.randint(30,80),random.randint(0,50),random.randint(130,255))
    list = []

    @staticmethod
    def head_obstacle_collisions_hander():
        global head_position
        for obstacle in Obstacle.list:
            if head.colliderect(obstacle.rect):

                if keys[pygame.K_LEFT] and head_past_self.left + 2 > obstacle.rect.right:
                    head_position = [obstacle.rect.right, head_position[1]]
                    head.topleft = head_position

                if keys[pygame.K_RIGHT] and head_past_self.right - 2 < obstacle.rect.left:
                    head_position = [obstacle.rect.left - square_size[0], head_position[1]]
                    head.topleft = head_position

                if keys[pygame.K_UP] and head_past_self.top + 2 > obstacle.rect.bottom:
                    head_position = [head_position[0], obstacle.rect.bottom]
                    head.topleft = head_position

                if keys[pygame.K_DOWN] and head_past_self.bottom - 2 < obstacle.rect.top:
                    head_position = [head_position[0], obstacle.rect.top - square_size[1]]
                    head.topleft = head_position

# Creating shit
Obstacle.create(Obstacle)
Food.create(Food)

# Set up the display
window = pygame.display.set_mode((window_width, window_height))
pygame.display.set_caption("Snake Game Grid")

# Create a clock object
clock = pygame.time.Clock()
dt = 0

# Main loop
while True:

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

    # Fill the background with black
    window.fill((0, 175, 0))

    # # Draw the grid
    # for x in range(0, window_width, square_size[0]):
    #     for y in range(0, window_height, square_size[1]):
    #         rect = pygame.Rect(x, y, square_size[0], square_size[1])
    #         pygame.draw.rect(window, (0, 0, 0), rect, 1)

    #Refreshing the head movement tracking
    head_past_self = head.copy()
    head_is_moving = False

    # Keyboard control and head-obstacle collisions
    keys = pygame.key.get_pressed()

    if keys[pygame.K_LEFT]:
        head_position[0] = max(0, head_position[0] - dt * head_speed)
        head_updater()
    if keys[pygame.K_RIGHT]:
        head_position[0] = min(window_width - square_size[0], head_position[0] + dt * head_speed)
        head_updater()
    if keys[pygame.K_UP]:
        head_position[1] = max(0, head_position[1] - dt * head_speed)
        head_updater()
    if keys[pygame.K_DOWN]:
        head_position[1] = min(window_height - square_size[1], head_position[1] + dt * head_speed)
        head_updater()

    # print("Keys got pressed")
    # print("previous head position was: " + str(head_past_self.topleft))
    # print("current head poistion is: " + str(head.topleft))

    # Head-food collision
    if head_is_moving:
        for food in Food.list:
            if head.colliderect(food.rect):
                food.generate_position()

    update_fov()

        # Draw the head
    pygame.draw.rect(window, head_color, head)

    # Draw the food
    for food in Food.list:
        pygame.draw.rect(window, Food.color, food.rect)

    # Draw the Obstacles
    for obstacle in Obstacle.list:
        pygame.draw.rect(window, obstacle.color, obstacle.rect)

    # Tests
    draw_fov_rects()

    # Update the display
    pygame.display.flip()

    dt = clock.tick(60)/1000
