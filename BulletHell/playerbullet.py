import pygame
from bullet import Bullet

class PlayerBullet(Bullet):
    
    DEFAULT_BULLET_SPEED = 10
    DEFAULT_BULLET_WIDTH = 10
    DEFAULT_BULLET_HEIGHT = 10
    DEFAULT_BULLET_DAMAGE = 1


    def __init__(self, window, windowWidth, windowHeight, spawn_x=0, spawn_y=0, width=DEFAULT_BULLET_WIDTH, height=DEFAULT_BULLET_HEIGHT):
        Bullet.__init__(self, window, windowWidth, windowHeight, spawn_x, spawn_y, width, height)
        self.ySpeed = -PlayerBullet.DEFAULT_BULLET_SPEED
        self.damage = PlayerBullet.DEFAULT_BULLET_DAMAGE

    