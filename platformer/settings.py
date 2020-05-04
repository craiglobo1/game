import os
import pygame

size = WIDTH,HEIGHT = 1000,750
FPS = 60

BG = pygame.transform.scale(pygame.image.load(os.path.join("assets", "background.jpg")), (WIDTH, HEIGHT))

ASSETS_FOLDER = r'F:\craigComp\Programming\python\game\platformer\assets'

# Player properties
PLAYER_ACC = 0.9    
PLAYER_FRICTION = -0.08
PLAYER_GRAV = 0.4
PLAYER_UPTHRUST = -15


#Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
YELLOW = (255, 255, 0)

#platforms
# PLATFORM_LIST = [(0,HEIGHT-40,GREEN,WIDTH,40),(WIDTH/2 - WIDTH/8,HEIGHT-200 ,RED),
#                 (0,HEIGHT-400),(WIDTH - WIDTH/4,HEIGHT-400,),
#                 (WIDTH/8,90)]

#Platform properties
PLATFORM_LIST = [(0,HEIGHT-40,GREEN,WIDTH,40)]

#EnemyProperties
ENEMY_SPEED = 3