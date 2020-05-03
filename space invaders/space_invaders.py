import pygame
from pygame.locals import *
from ships import Player,Enemy
import os
import random

pygame.font.init()
pygame.init()
size = win_width, win_height = 750, 750

win = pygame.display.set_mode(size)
pygame.display.set_caption("Space Shooter")


# Background
BG = pygame.transform.scale(pygame.image.load(os.path.join("assets", "background-black.png")), (win_width, win_height))


def collide(obj1,obj2):
    offset_x = obj2.x - obj1.x
    offset_y = obj2.y - obj1.y
    return obj1.mask.overlap(obj2.mask, (offset_x , offset_y)) != None

def main():
    run = True
    FPS = 60
    lives = 5
    level = 0
    mainFont = pygame.font.SysFont('comicsans',50)
    lostLabel = mainFont.render(f'You Lost!!!', 1 , (255,255,255))

    lost_counter = 0

    enemies = []
    wave_length = 5
    enemy_vel = 1
    laser_vel = 6

    clock = pygame.time.Clock()

    player = Player(300,300) 
    player_vel = 6

    lost = False

    def redraw():
        win.blit(BG,(0,0))
        livesLabel = mainFont.render(f'lives: {lives}', 1 , (255,255,255))
        levelLabel = mainFont.render(f'level: {level}', 1 , (255,255,255))


        win.blit(levelLabel,(10,10))
        win.blit(livesLabel,(win_width - livesLabel.get_width() - 10, 10 ))

        for enemy in enemies:
            enemy.draw(win)

        player.draw(win)

        if lost:
            win.blit(lostLabel,(win_width//2 - lostLabel.get_width()//2 , win_height//2))

        pygame.display.update()
    
    while run:
        clock.tick(FPS)
        redraw()


        if lives <= 0 or player.health <= 0:
            lost = True
            lost_counter += 1

        if lost:
            if lost_counter >= FPS*3:
                run = False
            else:
                continue

        
        while len(enemies) == 0:
            level += 1
            wave_length += 4
            for i in range(wave_length):
                enemyX = random.randint(50,win_width - 100)
                enemyY = random.randint(-1500 - (level*100),-100)
                enemyColor = random.choice(['red','blue','green'])
                enemy = Enemy(enemyX,enemyY,enemyColor)
                enemies.append(enemy)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
        keys = pygame.key.get_pressed()

        if keys[pygame.K_a] and (player.x - player_vel > 0):
            player.x -= player_vel

        if keys[pygame.K_d] and (player.x + player_vel + player.get_width() < win_width):
            player.x += player_vel

        if keys[pygame.K_w]and (player.y - player_vel > 0):
            player.y -= player_vel

        if keys[pygame.K_s] and (player.y + player_vel + player.get_height() + 15 < win_height) :
            player.y += player_vel 
        
        if keys[pygame.K_SPACE]:
            player.shoot()

        for enemy in enemies[:]:
            enemy.move(enemy_vel)
            enemy.move_lasers(laser_vel,player)

            if random.randint(0,1.5*60) == 1:
                enemy.shoot()

            if collide(enemy, player):
                player.health -= 10
                enemies.remove(enemy)
            elif enemy.y + enemy.get_height() > win_height:
                lives -= 1
                enemies.remove(enemy)

            

        player.move_lasers(-laser_vel, enemies)

def mainMenu():
    title_font = pygame.font.SysFont('comicsans',60)
    run = True
    while run:
        win.blit(BG,(0,0))
        title_label = title_font.render('press your mouse button to begin...' , 1, (255,255,255))
        win.blit(title_label, (win_width//2 - title_label.get_width()//2,win_height//2 ))

        pygame.display.update()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
            if event.type == pygame.MOUSEBUTTONDOWN:
                main()

    pygame.quit()

mainMenu()