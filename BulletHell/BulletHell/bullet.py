import pygame

class Bullet():

    def __init__(self, window, windowWidth, windowHeight, spawn_x, spawn_y, width, height):
        self.window = window
        self.windowWidth = windowWidth
        self.windowHeight = windowHeight

        self.minWidth = -width
        self.minHeight = -height
        self.maxWidth = windowWidth + width
        self.maxHeight = windowHeight + height

        self.rect = pygame.Rect(spawn_x,spawn_y,width,height)
        self.xSpeed = 0
        self.ySpeed = 0
        self.active = False

    def update(self, color=(255,255,0)):
        #if self.isActive():
        self.rect.x += self.xSpeed
        self.rect.y += self.ySpeed
        pygame.draw.rect(self.window, color, self.rect)
        self.despawn_check()

    def despawn_check(self):
        if self.rect.x < self.minWidth or self.rect.x > self.maxWidth:
            self.active = False
        elif self.rect.y < self.minHeight or self.rect.y > self.maxHeight:
            self.active = False

    def spawn(self, spawn_x, spawn_y):
        self.active = True
        self.rect.x = spawn_x
        self.rect.y = spawn_y
        
    def despawn(self):
        self.active = False

    def isActive(self):
        return self.active
        
