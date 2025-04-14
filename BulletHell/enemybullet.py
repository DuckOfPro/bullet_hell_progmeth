import pygame
from bullet import Bullet

class EnemyBullet(Bullet):
    DEFAULT_BULLET_WIDTH = 10
    DEFAULT_BULLET_HEIGHT = 10

    def __init__(self, window, windowWidth, windowHeight, spawn_x=0, spawn_y=0, width=DEFAULT_BULLET_WIDTH, height=DEFAULT_BULLET_HEIGHT):
        Bullet.__init__(self, window, windowWidth, windowHeight, spawn_x, spawn_y, width, height)

        self.xAcc = 0
        self.yAcc = 0
        self.widthGrow = 0
        self.heightGrow = 0

    def assign_physics(self, x, y, xSpeed, ySpeed, xAcc=0, yAcc=0, width=DEFAULT_BULLET_WIDTH, height=DEFAULT_BULLET_HEIGHT,widthGrow=0, heightGrow=0):
        self.active = True

        self.rect.x = x
        self.rect.y = y
        self.xSpeed = xSpeed
        self.ySpeed = ySpeed
        self.xAcc = xAcc
        self.yAcc = yAcc

        self.rect.width = width
        self.rect.height = height
        self.widthGrow = widthGrow
        self.heightGrow = heightGrow


    def update(self, color=(255,255,255)):
        #if self.isActive():
        self.rect.x += self.xSpeed
        self.rect.y += self.ySpeed
        self.xSpeed += self.xAcc
        self.ySpeed += self.yAcc
        
        self.rect.width += self.widthGrow
        self.rect.height += self.heightGrow

        pygame.draw.rect(self.window, color, self.rect)
        self.despawn_check()

