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
background = pygame.image.load(curr_dir_path + '/userlib_pic/background480x640.png')

character = pygame.image.load(curr_dir_path + '/userlib_pic/character70x70.png')
character_size = character.get_rect().size
character_width = character_size[0]
character_height = character_size[1]
character_x_pos = screen_width / 2 - character_width / 2
character_y_pos = screen_height - character_height
to_x = 0
to_y = 0

character_speed = 0.3

# Collision
enemy = pygame.image.load(curr_dir_path + '/userlib_pic/enemy70x70.png')
enemy_size = enemy.get_rect().size
enemy_width = enemy_size[0]
enemy_height = enemy_size[1]
enemy_x_pos = screen_width / 2 - enemy_width / 2
enemy_y_pos = screen_height / 2 - enemy_height / 2

# Font
game_font = pygame.font.Font(None, 40)

total_time = 10
start_ticks = pygame.time.get_ticks()

##############################
## 2. Event loop
running = True
while running:
    dt = clock.tick(60) # frame per second
    # print("fps : " + str(clock.get_fps()))

    ####################
    ## Event processing
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        
        # user input
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                to_x -= character_speed
            elif event.key == pygame.K_RIGHT:
                to_x += character_speed
            elif event.key == pygame.K_UP:
                to_y -= character_speed
            elif event.key == pygame.K_DOWN:
                to_y += character_speed
        
        if event.type == pygame.KEYUP:
            if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT:
                to_x = 0
            elif event.key == pygame.K_DOWN or event.key == pygame.K_UP:
                to_y = 0

    ####################
    ## Game processing
    character_x_pos += to_x * dt
    character_y_pos += to_y * dt

    character_x_pos = (0) if (character_x_pos < 0) else ( (screen_width - character_width) if (character_x_pos > screen_width - character_width) else character_x_pos)
    character_y_pos = (0) if (character_y_pos < 0) else ( (screen_height - character_height) if (character_y_pos > screen_height - character_height) else character_y_pos)

    character_rect = character.get_rect()
    character_rect.left = character_x_pos
    character_rect.top = character_y_pos

    enemy_rect = enemy.get_rect()
    enemy_rect.left = enemy_x_pos
    enemy_rect.top = enemy_y_pos

    ####################
    ## Collision check
    if character_rect.colliderect(enemy_rect):
        print("충돌했어요")
        running = False
    
    ####################
    ## Screen update
    # screen.fill((0, 0, 255))
    screen.blit(background, (0, 0))
    screen.blit(character, (character_x_pos, character_y_pos))
    screen.blit(enemy, (enemy_x_pos, enemy_y_pos))

    elapsed_time = (pygame.time.get_ticks() - start_ticks) * 0.001 # ms order to s order
    timer = game_font.render(str(int(total_time - elapsed_time)), True, (255, 255, 255)) # int for rounding off fraction
    screen.blit(timer, (10, 10))

    if total_time - elapsed_time <= 0:
        print("타임 아웃")
        running = False

    pygame.display.update()

pygame.time.delay(2000)

pygame.quit()
