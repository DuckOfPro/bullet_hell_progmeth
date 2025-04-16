import pygame
from bullet import Bullet
import copy

class BulletQueue():
    DEFAULT_SIZE = 10

    def __init__(self, bullet_factory_fn, size=DEFAULT_SIZE):
        self.inactive_list = [bullet_factory_fn() for _ in range(size)]
        self.active_list = []

    def consume(self):
        if len(self.inactive_list) == 0:
            print("NO BULLETS LEFT IN POOL")
            return None
        else:
            my_bullet = self.inactive_list[0]
            self.inactive_list.pop(0)
            self.active_list.append(my_bullet)
            #print(len(self.inactive_list)," Bullets left in pool")

            return my_bullet
    
    def check_activity(self):
        for bullet in self.active_list:
            if bullet.isActive() == False:
                self.restore(bullet)

    def restore(self, bullet):
        self.active_list.remove(bullet)
        self.inactive_list.append(bullet)
        
