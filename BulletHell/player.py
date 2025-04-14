import pygame
from playerbullet import PlayerBullet

from bulletqueue import BulletQueue
from textdisplay import TextDisplay
#=====================================================

class Player:


    DEFAULT_PLAYER_COLOR = (0, 255, 0)

    DEFAULT_PLAYER_X = 200
    DEFAULT_PLAYER_Y = 500

    DEFAULT_PLAYER_WIDTH = 20
    DEFAULT_PLAYER_HEIGHT = 20

    DEFAULT_PLAYER_SPEED = 6
    

    def __init__(self, window, windowWidth, windowHeight):
        self.window = window
        self.windowWidth = windowWidth
        self.windowHeight = windowHeight

#================================================================================================================================
        # deprecated
        # self.generate_bullet(window, windowWidth, windowHeight)
        self.generate_bullet_queue(window, windowWidth, windowHeight)

        self.enemyBulletPool = None

        self.hits = 0
        self.hitText = TextDisplay(window, (0,500), "Hits Taken: " + str(self.hits), (255,255,255))
#================================================================================================================================

        self.rect = pygame.Rect((Player.DEFAULT_PLAYER_X, Player.DEFAULT_PLAYER_Y, Player.DEFAULT_PLAYER_WIDTH, Player.DEFAULT_PLAYER_HEIGHT))
        self.width = Player.DEFAULT_PLAYER_WIDTH
        self.height = Player.DEFAULT_PLAYER_HEIGHT
        self.maxWidth = windowWidth - self.width
        self.maxHeight = windowHeight - self.height
        self.x = Player.DEFAULT_PLAYER_X
        self.y = Player.DEFAULT_PLAYER_Y
        self.xSpeed = 0
        self.ySpeed = 0

#=======================================================

    def update(self):
        self.handle_movement()
        self.x += self.xSpeed
        self.y += self.ySpeed

        if self.x < 0:
            self.x = 0
        elif self.x > self.maxWidth:
            self.x = self.maxWidth
        if self.y < 0:
            self.y = 0
        elif self.y > self.maxHeight:
            self.y = self.maxHeight

        self.rect.x = self.x
        self.rect.y = self.y
        pygame.draw.rect(self.window, Player.DEFAULT_PLAYER_COLOR, self.rect)

        self.bulletQueue.check_activity()
        for bullet in self.bulletQueue.active_list:
            bullet.update()

        self.check_bullet_collision()
        self.hitText.draw()

#===========================================================

    def check_bullet_collision(self):
        collisions = self.rect.collideobjectsall(self.enemyBulletPool)
        if len(collisions) > 0:
            self.hits += 1
            self.hitText.setValue("Hits Taken: " + str(self.hits))
        for bullet in collisions:
            bullet.despawn()


#===========================================================

    def go_left(self):
        self.xSpeed = -Player.DEFAULT_PLAYER_SPEED
    
    def go_right(self):
        self.xSpeed = Player.DEFAULT_PLAYER_SPEED

    def go_up(self):
        self.ySpeed = -Player.DEFAULT_PLAYER_SPEED

    def go_down(self):
        self.ySpeed = Player.DEFAULT_PLAYER_SPEED

    def stop_x(self):
        self.xSpeed = 0
    
    def stop_y(self):
        self.ySpeed = 0

    def handle_movement(self):
 
        for event in pygame.event.get(pygame.KEYDOWN):
            if event.type == pygame.KEYDOWN:
                if(event.key == pygame.K_LEFT):
                    self.go_left()
                elif(event.key == pygame.K_RIGHT):
                    self.go_right()
           
            if event.type == pygame.KEYDOWN:
                if(event.key == pygame.K_UP):
                    self.go_up()
                elif(event.key == pygame.K_DOWN):
                    self.go_down()

            if event.type == pygame.KEYDOWN:
                if(event.key == pygame.K_SPACE):
                    self.shoot()
                    print("Shoot")
        for event in pygame.event.get(pygame.KEYUP):
            if event.type == pygame.KEYUP:
                if(event.key == pygame.K_LEFT or pygame.K_RIGHT):
                    self.stop_x()
            if event.type == pygame.KEYUP:
                if(event.key == pygame.K_UP or pygame.K_DOWN):
                    self.stop_y()
#===============================================================                        

    PLAYER_BULLET_POOL = 15

# deprecated    
#    def generate_bullet(self, window, windowWidth, windowHeight):
#        self.sampleBullet = lambda: PlayerBullet(window, windowWidth, windowHeight)

    def generate_bullet_queue(self, window, windowWidth, windowHeight):
        self.bulletQueue = BulletQueue(lambda: PlayerBullet(window, windowWidth, windowHeight),size=Player.PLAYER_BULLET_POOL)

    def shoot(self):
        #print(self.bulletQueue.inactive_list)
        bullet = self.bulletQueue.consume()
        if isinstance(bullet, PlayerBullet):
            bullet.spawn(self.x + self.width/4, self.y)
