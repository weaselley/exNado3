# Quiz) 하늘에서 떨어지는 별 피하기 게임
# 1. 캐릭터는 화면 가장 아래에 위치, 좌우로만 이동 가능
# 2. 별은 화면 가장 위에서 떨어지고 랜덤으로 위치 결정
# 3. 캐릭터가 별을 피해야 다음 똥이 떨어짐
# 4. 캐릭터가 별과 충돌하면 게임 종료
# 5. FPS = 30

# background 480 x 640
# character 70 x 70
# enemy 70 * 70

import pygame
import os
import random

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
character_speed = 1

# Collision
enemy = pygame.image.load(curr_dir_path + '/userlib_pic/enemy70x70.png')
enemy_size = enemy.get_rect().size
enemy_width = enemy_size[0]
enemy_height = enemy_size[1]
enemy_x_pos = random.randint(0, screen_width - enemy_width)
enemy_y_pos = 0
to_y = 0.5
enemy_speed = 2

# Font
game_font = pygame.font.Font(None, 40)

start_ticks = pygame.time.get_ticks()

##############################
## 2. Event loop
running = True
while running:
    dt = clock.tick(30) # frame per second

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
        
        if event.type == pygame.KEYUP:
            if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT:
                to_x = 0
    
    ####################
    ## Game processing
    character_x_pos += to_x * dt
    character_x_pos = (0) if (character_x_pos < 0) else ( (screen_width - character_width) if (character_x_pos > screen_width - character_width) else character_x_pos)

    enemy_y_pos += to_y * dt
    if enemy_y_pos > screen_height:
        enemy_y_pos = 0
        enemy_x_pos = random.randint(0, screen_width - enemy_width)
    else:
        pass
    
    ####################
    ## Collision check
    character_rect = character.get_rect()
    character_rect.left = character_x_pos
    character_rect.top = character_y_pos

    enemy_rect = enemy.get_rect()
    enemy_rect.left = enemy_x_pos
    enemy_rect.top = enemy_y_pos

    if character_rect.colliderect(enemy_rect):
        print("충돌했어요")
        running = False
    
    ####################
    ## Screen update
    screen.blit(background, (0, 0))
    screen.blit(character, (character_x_pos, character_y_pos))
    screen.blit(enemy, (enemy_x_pos, enemy_y_pos))

    elapsed_time = (pygame.time.get_ticks() - start_ticks) * 0.001 # ms order to s order
    timer = game_font.render(str(int(elapsed_time)), True, (0, 0, 0)) # int for rounding off fraction
    screen.blit(timer, (10, 10))
    
    pygame.display.update()

pygame.time.delay(2000)
pygame.quit()
