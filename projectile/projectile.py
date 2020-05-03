import pygame
import os
import math
from math import pow,atan,sqrt,cos,sin


pygame.init()

size = WIDTH,HEIGHT = 1000,750

win = pygame.display.set_mode(size)
pygame.display.set_caption("Projectile Motion")

BG = pygame.transform.scale(pygame.image.load(os.path.join("assets", "background.jpg")), (WIDTH, HEIGHT))


class Ball:
    def __init__(self,x,y,radius,color):
        self.x = x
        self.y = y
        self.radius = radius
        self.color = color
        self.gravity = 20

    def draw(self,window):
        pygame.draw.circle(window,self.color,(self.x , self.y), self.radius )

    def move(self,time,vector,angle):
        Xcomp , Ycomp = self.calculateCompnents(vector,angle)

        self.y += round((self.gravity*(time/60)) - Ycomp )
        self.x += round(Xcomp)

    def findAngle(self,pos):
        sX = ball.x
        sY = ball.y
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
        sY = ball.y
        sX = ball.x
        vectorSpeed = power

        Xcomp = cos(angle) * vectorSpeed
        Ycomp = sin(angle) * vectorSpeed
        return Xcomp,Ycomp



ball = Ball(300,HEIGHT - 40,30,(255,0,0))

def main():
    run = True
    timeFalling = 0
    shoot = False

    FPS = 60
    clock = pygame.time.Clock()

    def redraw():
        win.blit(BG,(0,0))

        ball.draw(win)
        pygame.draw.line(win,(255,255,255),line[0],line[1])

        pygame.display.update()

    while run:
        clock.tick(FPS)

        pos = pygame.mouse.get_pos()
        line = [(ball.x,ball.y) , pos]
    

        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False

            if event.type == pygame.MOUSEBUTTONDOWN:
                if shoot == False:
                    shoot = True
                    x = ball.x
                    y = ball.y
                    timeFalling = 0
                    power = sqrt((line[1][1]-line[0][1])**2 +(line[1][0]-line[0][1])**2)/40
                    angle = ball.findAngle(pos)
                    
        if shoot:
            if ball.y <= HEIGHT - ball.radius - 10:
                timeFalling += 1
                ball.move(timeFalling,power,angle)
            else:
                shoot = False
                ball.y = HEIGHT - ball.radius - 10


        redraw()
main()