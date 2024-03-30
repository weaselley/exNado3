import pygame
import os

curr_dir_path = os.path.dirname(os.path.abspath(__file__))
##############################
## pygame initialize
pygame.init()

screen_width = 480
screen_height = 640
screen = pygame.display.set_mode((screen_width, screen_height))

pygame.display.set_caption("Nado Game")

clock = pygame.time.Clock()

##############################
## 1. User game initialize (background, image, position, font, ...)

##############################
## 2. Event loop
running = True
while running:
    dt = clock.tick(60) # frame per second

    ####################
    ## Event processing
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
    
    ####################
    ## Game processing
    
    ####################
    ## Collision check
    
    ####################
    ## Screen update
    pygame.display.update()

pygame.quit()
