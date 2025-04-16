import pygame

import player
import enemy
import textdisplay

#=====================================================================
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
BLACK = (0,0,0)
FRAMES_PER_SECOND = 30
  

#=====================================================================
pygame.init()


#=====================================================================
window = pygame.display.set_mode((SCREEN_WIDTH,SCREEN_HEIGHT))
clock = pygame.time.Clock()


#=====================================================================

my_player = player.Player(window, SCREEN_WIDTH, SCREEN_HEIGHT)      

#=====================================================================

my_enemy = enemy.Enemy(window, SCREEN_WIDTH, SCREEN_HEIGHT)

#=====================================================================

my_player.enemyBulletPool = my_enemy.bulletQueue.active_list
my_enemy.playerBulletPool = my_player.bulletQueue.active_list


#=====================================================================

my_time = textdisplay.TextDisplay(window, (0, 400), "", (255,255,255))

#====================================
run = True
while run:
    window.fill(BLACK)

    my_player.update()
    my_enemy.update()

    my_time.setValue("Time Elapsed: " + str(int(pygame.time.get_ticks()/1000)))
    my_time.draw()



#===========================================================================
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
    
    pygame.display.update()
    clock.tick(FRAMES_PER_SECOND)

pygame.quit()