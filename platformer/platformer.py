import pygame
import os
import random
from math import sqrt

from settings import *
from sprites import *


class Game:
    def __init__(self):
        pygame.font.init()
        pygame.init()
        self.win = pygame.display.set_mode(size)
        pygame.display.set_caption("platformer")
        self.clock = pygame.time.Clock()
        self.running = True

    def new(self):
        self.score = 0
        self.shoot = False
        self.all_sprites = pygame.sprite.Group()
        self.platforms = pygame.sprite.Group()
        self.enemies = pygame.sprite.Group()

        self.player = Player(self)
        self.all_sprites.add(self.player)

        self.ball = Ball(self.player.rect.x,self.player.rect.y,10,RED,self)
        self.all_sprites.add(self.ball)
           
        
        PLATFORM_LIST = [(0,HEIGHT-40,GREEN,WIDTH,40)]
        NO_OF_LEVELS = 200
        platformHeight = HEIGHT-200
        widthChoices = [WIDTH/4,WIDTH/6,WIDTH/2,3*WIDTH/4,7*WIDTH/8,5*WIDTH/6]
        ENEMY_LIST = []

        enemyHeight = random.randint(10,50)
        enemyLevelThreshold = random.randint(20,25)

        #platform generation
        for i in range(NO_OF_LEVELS):
            noOfplatforms = random.choices([1,2],[0.8,0.2],k=1)[0]
            if noOfplatforms == 1:
                PLATFORM_LIST.append((random.randint(0,WIDTH-WIDTH/4),platformHeight,BLUE))
                platformHeight -= random.randint(200,270)
            elif noOfplatforms == 2:
                platformWidth1 = random.choice([WIDTH/4,WIDTH/6,WIDTH/2,2*WIDTH/6,WIDTH/8,2*WIDTH/8])
                platformWidth2 = random.choice([3*WIDTH/4,7*WIDTH/8,5*WIDTH/6])
                PLATFORM_LIST.append((platformWidth1-WIDTH/8,platformHeight,BLUE))
                PLATFORM_LIST.append((platformWidth2-WIDTH/8,platformHeight,BLUE))
                platformHeight -= random.randint(200,290)
         
            if i % enemyLevelThreshold == 0:
                ENEMY_LIST.append(enemyHeight)
                enemyHeight -= random.randint(200,290)*enemyLevelThreshold
                enemyLevelThreshold = random.randint(20,25)
        

        for platform in PLATFORM_LIST:
            pl = Platform(*platform)
            self.platforms.add(pl)
            self.all_sprites.add(pl)
        
        for height in ENEMY_LIST:
            en = Enemy(height)
            self.enemies.add(en)
            self.all_sprites.add(en)

        self.run()
        pass
    
    def run(self):
        # Game Loop
        self.playing = True
        while self.playing:
            self.clock.tick(FPS)
            self.events()
            self.update()
            self.draw()

    def update(self):
        # Game Loop - Update


        #ball and player
        ballEnemyCollide = pygame.sprite.spritecollide(self.ball,self.enemies,False,pygame.sprite.collide_mask)
        if ballEnemyCollide:
            self.shoot = False
            ballEnemyCollide[0].kill()
            self.score += 100

        #COLLISIONS
        # player and platform
        if not(self.player.dead):
            if self.player.vel.y > 0:
                hits = pygame.sprite.spritecollide(self.player,self.platforms,False)
                if hits:
                    self.player.pos.y = hits[0].rect.top
                    self.player.vel.y = 0

        #Enemy and player
        playerEnemyCollide = pygame.sprite.spritecollide(self.player,self.enemies,False,pygame.sprite.collide_mask)
        if playerEnemyCollide:
            self.player.dead = True
            print('collide')

              
        # camera movement 
        if self.player.rect.top <= HEIGHT / 4:
            self.player.pos.y += abs(self.player.vel.y)
            for plat in self.platforms:
                plat.rect.y += round(abs(self.player.vel.y))
                if plat.rect.top >= HEIGHT:
                    plat.kill()
                    self.score += 10 
            for enemy in self.enemies:
                enemy.rect.y += round(abs(self.player.vel.y))

        # mantain ball location    
        if not(self.shoot):
            self.ball.stationary(self.player.pos)




        #On death reset
        if self.player.rect.y > HEIGHT or self.player.dead:
            for sprite in self.all_sprites:
                sprite.rect.y -= round(max(self.player.vel.y,10))
                if sprite.rect.bottom < 0:
                    sprite.kill()

        if len(self.platforms) == 0:
            self.playing = False

        # Update all sprites
        self.all_sprites.update()
            

    def events(self):        
        # Game Loop - events
        for event in pygame.event.get():
            # check for closing window
            if event.type == pygame.QUIT:
                if self.playing:
                    self.playing = False
                self.running = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    self.player.jump()

        #ball shooting
            if event.type == pygame.MOUSEBUTTONUP:
                if self.shoot == False:
                    pos = pygame.mouse.get_pos()
                    line = [(self.ball.rect.center[0],self.ball.rect.center[1]) , pos]
                    self.shoot = True
                    x = self.ball.rect.x
                    y = self.ball.rect.y
                    self.timeFalling = 0
                    self.power = sqrt((line[1][1]-line[0][1])**2 +(line[1][0]-line[0][1])**2)/15
                    self.angle = self.ball.findAngle(pos)

        if self.shoot:
            if self.ball.rect.y <= HEIGHT - self.ball.radius - 10:
                self.timeFalling += 1
                self.ball.move(self.timeFalling,self.power,self.angle)
            else:
                self.shoot = False
                self.ball.stationary(self.player.pos)

        #enemy movement
        for enemy in self.enemies:
            if enemy.rect.x + ENEMY_SPEED >= WIDTH - enemy.image.get_width() or enemy.rect.x - ENEMY_SPEED <= 0:
                enemy.flip = not(enemy.flip)
            enemy.move()


    
    def draw(self):
        # Game Loop - draw
        self.win.fill(BLACK)
        self.all_sprites.draw(self.win)

        if pygame.mouse.get_pressed()[0] and not(self.shoot):
            pos = pygame.mouse.get_pos()
            line = [(self.ball.rect.center[0],self.ball.rect.center[1]) , pos]
            pygame.draw.line(self.win,(255,255,255),line[0],line[1])

        self.draw_text(f'Score: {self.score}',30,WHITE,WIDTH/2,15)
        pygame.display.flip()

    def show_start_screen(self):
        # game splash/start screen
        title_font = pygame.font.SysFont('comicsans',60)
        run = True
        exit = False
        while run:
            self.win.blit(BG,(0,0))
            title_label = title_font.render('press your mouse button to begin...' , 1, (255,255,255))
            self.win.blit(title_label, (WIDTH//2 - title_label.get_width()//2,HEIGHT//2 ))

            pygame.display.update()
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    run = False
                if event.type == pygame.MOUSEBUTTONDOWN:
                    exit = True
            if exit:
                break

    def show_go_screen(self):
        # game over/continue
        # game splash/start screen
        title_font = pygame.font.SysFont('comicsans',60)
        run = True
        exit = False

        with open('highscore.txt','r') as rf:
            highscore = rf.read()

        if self.score > int(highscore):
            highscore = self.score
            with open('highscore.txt','w') as wf:
                wf.write(f'{self.score}')

        while run:
            self.win.blit(BG,(0,0))
            title_label = title_font.render(f'press your mouse button to begin...' , 1, (255,255,255))
            self.win.blit(title_label, (WIDTH//2 - title_label.get_width()//2,HEIGHT//2-50))

            title_label = title_font.render(f'HighScore: {highscore}' , 1, (255,255,255))
            self.win.blit(title_label, (WIDTH//2 - title_label.get_width()//2,HEIGHT//2))

            title_label = title_font.render(f'Score: {self.score}' , 1, (255,255,255))
            self.win.blit(title_label, (WIDTH//2 - title_label.get_width()//2,HEIGHT//2+50))

            pygame.display.update()
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    run = False
                if event.type == pygame.MOUSEBUTTONDOWN:
                    exit = True
            if exit:
                break
    
    def draw_text(self, text, size, color, x, y):
        font = pygame.font.SysFont('comicsans', size)
        text_surface = font.render(text, True, color)
        text_rect = text_surface.get_rect()
        self.win.blit(text_surface, (x - text_surface.get_width()//2,y))


g = Game()
g.show_start_screen()
while g.running:
    g.new()
    g.show_go_screen()
pygame.quit()