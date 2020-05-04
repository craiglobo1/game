
# Sprite classes for platform game
import pygame
from settings import *
vec = pygame.math.Vector2
import math
import os

class Spritesheet:
    # utility class for loading and parsing spritesheets
    def __init__(self, filename):
        self.spritesheet = pygame.image.load(filename).convert()

    def get_image(self, x, y, width, height):
        # grab an image out of a larger spritesheet
        image = pygame.Surface((width, height))
        image.blit(self.spritesheet, (0, 0), (x, y, width, height))
        image = pygame.transform.scale(image, (width // 2, height // 2))
        return image

class Player(pygame.sprite.Sprite):

    def __init__(self,game):
        super().__init__()
        self.game = game
        self.image = pygame.Surface((25, 40))
        self.image.fill(YELLOW)
        self.rect = self.image.get_rect()
        self.rect.center = (WIDTH / 2, HEIGHT / 2)
        self.pos = vec(WIDTH / 2, HEIGHT / 2)
        self.vel = vec(0, 0)
        self.acc = vec(0, 0)
        self.dead = False
        self.mask = pygame.mask.from_surface(self.image)

    def update(self):
        self.acc = vec(0, PLAYER_GRAV)
        keys = pygame.key.get_pressed()
        if keys[pygame.K_a]:
            self.acc.x = -PLAYER_ACC
    

        if keys[pygame.K_d]:
            self.acc.x = PLAYER_ACC

        # apply friction
        self.acc.x += self.vel.x * PLAYER_FRICTION

        # equations of motion
        self.vel += self.acc
        self.pos += self.vel + 0.5 * self.acc
        
        # wrap around the sides of the screen
        if self.pos.x > WIDTH:
            self.pos.x = 0
        if self.pos.x < 0:
            self.pos.x = WIDTH

        self.rect.midbottom = self.pos
    def jump(self):
        self.rect.y += 1
        hits = pygame.sprite.spritecollide(self, self.game.platforms, False)
        self.rect.y -= 1
        if hits:
            self.vel.y = PLAYER_UPTHRUST


class Platform(pygame.sprite.Sprite):
    def __init__(self,x,y,color=BLUE,w=WIDTH/4,h=20,):
        super().__init__()
        self.image = pygame.Surface((w,h))
        self.image.fill(color)
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y


class Ball(pygame.sprite.Sprite):
    def __init__(self,x,y,radius,color,game):
        super().__init__()
        self.x = x
        self.y = y
        self.radius = radius
        self.color = color
        self.gravity = 20
        self.image = pygame.transform.scale(pygame.image.load(os.path.join(ASSETS_FOLDER,'ball.png')),(25,25)).convert()
        self.image.set_colorkey(WHITE)
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.mask = pygame.mask.from_surface(self.image)

    def stationary(self,pos):
        self.rect.x,self.rect.y = pos[0]+5,pos[1]-35
        self.x,self.y = pos[0]+5,pos[1]-35

    def move(self,time,vector,angle):
        Xcomp , Ycomp = self.calculateCompnents(vector,angle)

        self.y += round((self.gravity*(time/60)) - Ycomp )
        self.x += round(Xcomp)

        self.rect.x,self.rect.y = self.x,self.y

    def findAngle(self,pos):
        sX = self.x
        sY = self.y
        try:
            angle = math.atan((sY - pos[1]) / (sX - pos[0]))
        except:
            angle = math.pi / 2

        if pos[1] < sY and pos[0] > sX:
            angle = abs(angle)
        elif pos[1] < sY and pos[0] < sX:
            angle = math.pi - angle
        elif pos[1] > sY and pos[0] < sX:
            angle = math.pi + abs(angle)
        elif pos[1] > sY and pos[0] > sX:
            angle = (math.pi * 2) - angle

        return angle


    def calculateCompnents(self,power,angle):
        sY = self.y
        sX = self.x
        vectorSpeed = power

        Xcomp = math.cos(angle) * vectorSpeed
        Ycomp = math.sin(angle) * vectorSpeed
        return Xcomp,Ycomp
        
class Enemy(pygame.sprite.Sprite):
    def __init__(self,height):
        super().__init__()
        self.image = pygame.transform.scale(pygame.image.load(os.path.join(ASSETS_FOLDER,'enemy.png')),(120,80)).convert()
        self.image.set_colorkey(WHITE)
        self.rect = self.image.get_rect()
        self.rect.center = (WIDTH//2,height)
        self.flip = False
        self.mask = pygame.mask.from_surface(self.image)
    
    def move(self):
        if self.flip:
            self.rect.x -= ENEMY_SPEED
        else:
            self.rect.x += ENEMY_SPEED

