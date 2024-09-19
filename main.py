import pygame
import sys
import random
import copy
import math
import itertools

# Initialize Pygame
pygame.init()

# Define the grid and square sizes
grid_size = (20, 20)
square_size = (45, 45)

# Calculate the size of the window
window_width = grid_size[0] * square_size[0]
window_height = grid_size[1] * square_size[1]
window_rect = pygame.Rect(0,0,window_width,window_height)

# Snake's head
head_position = [400,400]
head_speed = 2000
head_color = (100,0,0)
head_size = (15,15)
head = pygame.Rect(head_position[0], head_position[1], head_size[0], head_size[1])
head_is_moving = 0
movement_direction = None
game_score = 0

actions = {
    "up": None,
    "down": None,
    "left": None,
    "right": None,
    "random": None,
}

states = {
    "food",
    "obstacle",
    "border",
    "nothing",
}

SA = set()
for x in itertools.product(states, actions):
    SA.add(x)

# Heads fov

fov_diameter = 170

class Fovp:
    jump = 10
    diameter = fov_diameter
    start = [head.center[0] - diameter/2, head.center[1] - diameter/2]
    k = int(diameter/jump) +1
    lattice = []
    list = []
    rect = pygame.Rect(0,0,fov_diameter,fov_diameter)
    suspicious_food = []
    suspicious_obstacles = []

    def __init__(self):
        self.position = [0,0]
        self.rect = pygame.Rect(self.position[0], self.position[1], 2, 2)
        self.color = (40, 40, 40)

        self.detects = "nothing"

        self.SAW = {}

        for x in SA:
            self.SAW[x] = 0

        self.update_weights()

    def update_weights(self):
        for x in self.SAW:
            self.SAW[x] = random.randint(0,100)

    @classmethod
    def create_lattice(cls):
        cls.lattice = [[[0, 0] for _ in range(cls.k)] for _ in range(cls.k)]
        for i, row in enumerate(cls.lattice):
            for j, column in enumerate(row):
                cls.lattice[i][j] = Fovp()
                cls.list.append(cls.lattice[i][j])

    @staticmethod
    def update():
        if head_is_moving == True or l == 0:
            Fovp.start = [head.center[0] - Fovp.diameter/2, head.center[1] - Fovp.diameter/2]

            for i, row in enumerate(Fovp.lattice):
                for j, column in enumerate(row):
                    Fovp.lattice[i][j].position = [Fovp.start[0] + j * Fovp.jump, Fovp.start[1] + i * Fovp.jump]
                    Fovp.lattice[i][j].rect.center = Fovp.lattice[i][j].position

            Fovp.update_suspicions()

            for i, row in enumerate(Fovp.lattice):
                for j, column in enumerate(row):
                    Fovp.lattice[i][j].scan()

        for i, row in enumerate(Fovp.lattice):
            for j, column in enumerate(row):
                Fovp.lattice[i][j].draw()


    @staticmethod
    def update_suspicions():
        Fovp.rect.topleft = Fovp.start
        Fovp.suspicious_food.clear()
        Fovp.suspicious_obstacles.clear()

        for obstacle in Obstacle.list:
            if obstacle.rect.colliderect(Fovp.rect):
                Fovp.suspicious_obstacles.append(obstacle)
        for food in Food.list:
            if food.rect.colliderect(Fovp.rect):
               Fovp.suspicious_food.append(food)

    def draw(self):
        pygame.draw.rect(window, self.color, self.rect)

    def scan(self):

        self.detects = "nothing"
        self.color = (40, 40, 40)

        if not window_rect.collidepoint(self.position):
            self.detects = "border"
        else:
            noob = 0
            for obstacle in self.suspicious_obstacles:
                if obstacle.rect.collidepoint(self.position):
                    self.detects = "obstacle"
                    self.color = (200,200,200)
                    noob = 1
                    break
            if noob == 0:
                for food in self.suspicious_food:
                    if food.rect.collidepoint(self.position):
                        self.detects = "food"
                        self.color = (230,0,0)
                        break

Fovp.create_lattice()
l = 0

def score(action):
    s = 0
    for i,point in enumerate(Fovp.list):
        s += point.SAW[(point.detects, action)]
    return s

def choose_action():
    for action in actions:
        actions[action] = score(action)
    return max(actions, key = actions.get)

def head_is_moving_updater():
    global head_is_moving
    head_is_moving = True

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
    size = [22, 22]
    number = random.randint(70,100)
    color = (random.randint(200,245),random.randint(150,200),random.randint(40,100))
    list = []

# Obstacle properties
class Obstacle(Game_Object):
    size = [60, 60]
    number = random.randint(50,65)
    color = (random.randint(30,80),random.randint(0,50),random.randint(130,255))
    list = []

    @staticmethod
    def head_obstacle_collisions_hander():
        global head_position
        global game_score
        for obstacle in Obstacle.list:
            if head.colliderect(obstacle.rect):
                game_score -= 1

                if (keys[pygame.K_LEFT] or movement_direction == "left") and head_past_self.left + 2 > obstacle.rect.right:
                    head_position = [obstacle.rect.right, head_position[1]]
                    head.topleft = head_position

                if (keys[pygame.K_RIGHT] or movement_direction == "right") and head_past_self.right - 2 < obstacle.rect.left:
                    head_position = [obstacle.rect.left - head_size[0], head_position[1]]
                    head.topleft = head_position

                if (keys[pygame.K_UP] or movement_direction == "up") and head_past_self.top + 2 > obstacle.rect.bottom:
                    head_position = [head_position[0], obstacle.rect.bottom]
                    head.topleft = head_position

                if (keys[pygame.K_DOWN] or movement_direction == "down") and head_past_self.bottom - 2 < obstacle.rect.top:
                    head_position = [head_position[0], obstacle.rect.top - head_size[1]]
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

    # Fill the background with green
    window.fill((0, 175, 0))

    #Refreshing the head movement tracking
    head_past_self = head.copy()
    head_is_moving = True

    action = choose_action()

    # Prints
    for act in actions:
        print(actions[act])

    print(max(actions, key=actions.get), max(actions.values()))
    print (game_score)

    if action == "random":
        action = random.choice(list(actions))

    movement_direction = action
    # Keyboard control and head-obstacle collisions
    keys = pygame.key.get_pressed()

    if any(keys):
        if keys[pygame.K_LEFT]:
            head_position[0] = max(0, head_position[0] - dt * head_speed)
            head_updater()
        if keys[pygame.K_RIGHT]:
            head_position[0] = min(window_width - head_size[0], head_position[0] + dt * head_speed)
            head_updater()
        if keys[pygame.K_UP]:
            head_position[1] = max(0, head_position[1] - dt * head_speed)
            head_updater()
        if keys[pygame.K_DOWN]:
            head_position[1] = min(window_height - head_size[1], head_position[1] + dt * head_speed)
            head_updater()
    else:
        if  action == "left" :
            head_position[0] = max(0, head_position[0] - dt * head_speed)
            head_updater()
        if  action == "right":
            head_position[0] = min(window_width - head_size[0], head_position[0] + dt * head_speed)
            head_updater()
        if  action == "up":
            head_position[1] = max(0, head_position[1] - dt * head_speed)
            head_updater()
        if  action == "down":
            head_position[1] = min(window_height - head_size[1], head_position[1] + dt * head_speed)
            head_updater()

    # Head-food collision
    if head_is_moving:
        for food in Food.list:
            if head.colliderect(food.rect):
                game_score += 100
                food.generate_position()

        # Draw the head
    pygame.draw.rect(window, head_color, head)

    # Draw the food
    for food in Food.list:
        pygame.draw.rect(window, Food.color, food.rect)

    # Draw the Obstacles
    for obstacle in Obstacle.list:
        pygame.draw.rect(window, obstacle.color, obstacle.rect)

    # fov
    Fovp.update()

    l = 1

    # Update the display
    pygame.display.flip()

    dt = clock.tick(60)/1000
    print (f"dt is {dt}")

