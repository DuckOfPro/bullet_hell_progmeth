import pygame
from enemybullet import EnemyBullet
from textdisplay import TextDisplay
from bulletqueue import BulletQueue
import random
import math

class Enemy():
    DEFAULT_ENEMY_COLOR = (200, 0, 0)

    DEFAULT_ENEMY_X = 400
    DEFAULT_ENEMY_Y = 100

    DEFAULT_ENEMY_WIDTH = 50
    DEFAULT_ENEMY_HEIGHT = 80

    #DEFAULT_ENEMY_HEALTH = 40


    def __init__(self, window, windowWidth, windowHeight, x=DEFAULT_ENEMY_X, y=DEFAULT_ENEMY_HEIGHT,width=DEFAULT_ENEMY_WIDTH,height=DEFAULT_ENEMY_HEIGHT):
        self.window = window
        self.windowWidth = windowWidth
        self.windowHeight = windowHeight

        self.generate_bullet_queue(window, windowWidth, windowHeight)

        self.playerBulletPool = None

        self.phase = 0
        self.set_health(self.phase)
        self.healthText = TextDisplay(window, (0,20), "HP: " + str(self.health), (255,255,255))
        self.phaseText = TextDisplay(window, (0,0), "Phase: " + str(self.phase), (255,255,255))
        
        self.last_shot_time = pygame.time.get_ticks()
        self.last_moved = pygame.time.get_ticks()

        # self.generate_bullet_queue(window, windowWidth, windowHeight)
        # self.last_shot_time = pygame.time.get_ticks()
        # self.shoot_interval = 1000
#================================================================================================================================

        self.rect = pygame.Rect((x, y, width, height))
        self.x = x
        self.y = y
        self.xSpeed = 0
        self.ySpeed = 0
        self.width = width
        self.height = height

        self.should_get_time = True
        self.delayer = 0

    def update(self, color=DEFAULT_ENEMY_COLOR):
        self.x += self.xSpeed
        self.y += self.ySpeed
        
        self.rect.x = self.x 
        self.rect.y = self.y
        pygame.draw.rect(self.window, color, self.rect)
        self.check_bullet_collision()
        self.healthText.draw()
        self.phaseText.draw()

        self.bulletQueue.check_activity()
        for bullet in self.bulletQueue.active_list:
            bullet.update()

        self.move()
        self.phase_shot(self.phase)
        #current_time = pygame.time.get_ticks()
        #if current_time - self.last_shot_time >= self.shoot_interval:
        #    self.shoot_normal()
#======================================================================================
    PHASE_HEALTH = [5,5,5,5,5,5,5,5,5,5]

    def set_health(self, phase):
        self.health = Enemy.PHASE_HEALTH[phase]


    def check_bullet_collision(self):
        collisions = self.rect.collideobjectsall(self.playerBulletPool)
        if len(collisions) > 0:
            self.health -= 1
            self.healthText.setValue("HP: " + str(self.health))
            if self.health <= 0:
                self.phase += 1
                self.set_health(self.phase)
                self.healthText.setValue("HP: " + str(self.health))
                self.phaseText.setValue("Phase: " + str(self.phase))

        for bullet in collisions:
            bullet.despawn()


#=========================================================================================================

    ENEMY_BULLET_POOL = 40


    DEFAULT_BULLET_X = 0
    DEFAULT_BULLET_Y = 0

    DEFAULT_BULLET_XSPEED = 0
    DEFAULT_BULLET_YSPEED = 10

    DEFAULT_BULLET_XACC = 0
    DEFAULT_BULLET_YACC = 0

    DEFAULT_BULLET_WIDTH = 30
    DEFAULT_BULLET_HEIGHT = 30
    DEFAULT_BULLET_WIDTHGROW = 0
    DEFAULT_BULLET_HEIGHTGROW = 0
    
    

    def generate_bullet_queue(self, window, windowWidth, windowHeight):
        self.bulletQueue = BulletQueue(lambda: EnemyBullet(window, windowWidth, windowHeight),size=Enemy.ENEMY_BULLET_POOL)
    
    def shoot_normal(self, relative= True, x=DEFAULT_BULLET_X, y=DEFAULT_BULLET_Y, xSpeed=DEFAULT_BULLET_XSPEED, ySpeed=DEFAULT_BULLET_YSPEED, xAcc=DEFAULT_BULLET_XACC, yAcc=DEFAULT_BULLET_YACC, width=DEFAULT_BULLET_WIDTH, height=DEFAULT_BULLET_HEIGHT,widthGrow=DEFAULT_BULLET_WIDTHGROW, heightGrow=DEFAULT_BULLET_HEIGHTGROW):
        #print(self.bulletQueue.inactive_list)
        bullet = self.bulletQueue.consume()
        if isinstance(bullet, EnemyBullet):
            if relative:
                bullet.assign_physics(self.x + self.width/2 - width/2 + x, self.y + y, xSpeed, ySpeed, xAcc, yAcc, width, height, widthGrow, heightGrow)
            else:
                bullet.assign_physics(x, y, xSpeed, ySpeed, xAcc, yAcc, width, height, widthGrow, heightGrow)

        
    #==============================================================================================================================================================================

    BOSS_MOVE_INTERVAL = 4000
    FPS = 30
    EDGE_FACTOR = 0.2

    def move(self, interval=BOSS_MOVE_INTERVAL, edgeFactor=EDGE_FACTOR):
        if self.phase == 0:
            return
        
        if self.current_time - self.last_moved >= interval:
                targetX = random.randrange(int(edgeFactor * self.windowWidth) , int((1 - edgeFactor) * self.windowWidth) - self.width)
                distance = targetX - self.x
                self.xSpeed = distance/(interval/30)
                self.last_moved = self.current_time

    def phase_shot(self, phase):

        self.current_time = pygame.time.get_ticks()

        if phase == 1:

            self.shoot_interval = Enemy.PHASE_ONE_INTERVAL
            if self.current_time - self.last_shot_time >= self.shoot_interval:
                self.shoot_line()
                self.last_shot_time = self.current_time
        
        elif phase == 2:
            self.shoot_interval = Enemy.PHASE_TWO_INTERVAL
            if self.current_time - self.last_shot_time >= self.shoot_interval:
                self.shoot_spread()
                self.last_shot_time = self.current_time

        elif phase == 3:
            
            
            self.shoot_interval = 3000
            if self.current_time - self.last_shot_time >= self.shoot_interval:
                self.shoot_spread(5, 6, 60)
                self.last_shot_time = self.current_time
                self.delayer = 1
            if self.current_time - self.last_shot_time >= self.shoot_interval - 2500 and self.delayer == 1:
                self.shoot_line(10, 0, 20, 20)
                self.delayer = 0
        
        elif phase == 4:

            self.shoot_interval = 5000
            if self.current_time - self.last_shot_time >= self.shoot_interval:
                self.shoot_line(8, 0, 24, 20, -0.5)
                self.delayer = 1
                self.last_shot_time = self.current_time
            elif self.current_time - self.last_shot_time >= self.shoot_interval - 4400 and self.delayer == 1:
                self.shoot_line(6, 0, 30, 30, -1)
                self.delayer = 2
            elif self.delayer == 2 and self.current_time - self.last_shot_time >= self.shoot_interval - 3900:
                self.shoot_line(4, 0, 24, 40, -0.5)
                self.delayer = 0

        elif phase == 9:

            pygame.quit()


    #==============================================================================================================================================================================
    # PHASE 1 - Straight Bullet Lines

    PHASE_ONE_SHOTS = 6
    PHASE_ONE_INTERVAL = 1500
    PHASE_ONE_YSPEED = 8
    PHASE_ONE_SIZE = 50

    def shoot_line(self, shots=PHASE_ONE_SHOTS, xspeed=0 ,yspeed=PHASE_ONE_YSPEED, size=PHASE_ONE_SIZE, yacc = 0):

        offset = random.randrange(0, int(self.windowWidth/shots))
        for i in range(shots):
            xPos = self.windowWidth/shots * i
            yPos = 0
            self.shoot_normal(False, xPos + offset, yPos, xspeed, yspeed, 0, yacc,size,size,0,0)
            
    #============================================================================================================================================================================


    PHASE_TWO_SHOTS = 7
    PHASE_TWO_INTERVAL = 1300
    PHASE_TWO_SPEED = 5
    PHASE_TWO_SIZE = 40

    def shoot_spread(self, shots=PHASE_TWO_SHOTS, speed=PHASE_TWO_SPEED, size=PHASE_TWO_SIZE):
        offset = random.randrange(-int(225/shots), int(225/shots))
        for i in range(shots):
            xPos = 0
            yPos = 0
            angle = math.radians(offset + i * int(225/shots))
            xSpeed = speed * math.cos(angle)
            ySpeed = speed * math.sin(angle)
            self.shoot_normal(True, xPos, yPos, xSpeed, ySpeed, 0,0,size,size,0,0)