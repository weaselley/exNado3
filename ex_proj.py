# Proj) 오락실 Pang 게임 만들기
# 1. 캐릭터는 아래 위치, 좌우 이동만
# 2. 스페이스 누르면 무기를 쏘아 올림
# 3. 큰 공 1개 가 나타나서 바운스
# 4. 무기에 닿으면 공은 작은 크기 2개로 분할, 가장 작은 크기의 공은 사라짐
# 5. 모든 공 없애면 게임 종료 (성공)
# 6. 캐릭터는 공에 닿으면 게임 종료 (실패)
# 7. 시간 제한 99초
# 8. FPS = 30

# background 640 x 480
# stage 640 x 50
# character 60 x 33
# weapon 20 x 430
# balls 160 x 160, 80 x 80, 40 x 40, 20 x 20

import pygame
import os

curr_dir_path = os.path.dirname(os.path.abspath(__file__))
image_path = curr_dir_path + "/userlib_pic/"
##############################
## pygame initialize
pygame.init()

screen_width = 640
screen_height = 480
screen = pygame.display.set_mode((screen_width, screen_height))

pygame.display.set_caption("Nado Game")

clock = pygame.time.Clock()

##############################
## 1. User game initialize (background, image, position, font, ...)
background = pygame.image.load(image_path + "background640x480.png")
stage = pygame.image.load(image_path + "stage_game.png")
stage_size = stage.get_rect().size
stage_height = stage_size[1]

character = pygame.image.load(image_path + "char_game.png")
character_size = character.get_rect().size
character_width = character_size[0]
character_height = character_size[1]
character_x_pos = screen_width / 2 - character_width / 2
character_y_pos = screen_height - stage_height - character_height
character_to_x = 0
character_speed = 0.5

weapon = pygame.image.load(image_path + "weapon_game.png")
weapon_size = weapon.get_rect().size
weapon_width = weapon_size[0]
weapons_lst = []
weapon_speed = 10 

pygame.image.load(image_path + "ball16_game.png")

ball_img_lst = [
    pygame.image.load(image_path + "ball16_game.png"),
    pygame.image.load(image_path + "ball8_game.png"),
    pygame.image.load(image_path + "ball4_game.png"),
    pygame.image.load(image_path + "ball2_game.png")
]
balls_speed = [-18, -15, -12, -9]
balls = []
balls.append({
    "pos_x" : 50, 
    "pos_y" : 50,
    "img_idx" : 0,
    "to_x" : 3,
    "to_y" : -6,
    "init_spd_y" : balls_speed[0]
})

weapon_to_remove = -1
ball_to_remove = -1

# Font
game_font = pygame.font.Font(None, 40)
total_time = 100
start_ticks = pygame.time.get_ticks()
game_result = "Game Over"

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

    # user input
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                character_to_x -= character_speed
            elif event.key == pygame.K_RIGHT:
                character_to_x += character_speed
            elif event.key == pygame.K_SPACE:
                weapon_x_pos = character_x_pos + (0.5 * character_width) - (0.5 * weapon_width)
                weapon_y_pos = character_y_pos
                weapons_lst.append([weapon_x_pos, weapon_y_pos])
      
        if event.type == pygame.KEYUP:
            if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT:
                character_to_x = 0
    
    ####################
    ## Game processing
    character_x_pos += character_to_x * dt
    character_x_pos = (0) if (character_x_pos < 0) else ( (screen_width - character_width) if (character_x_pos > screen_width - character_width) else character_x_pos)
    
    character_rect = character.get_rect()
    character_rect.left = character_x_pos
    character_rect.top = character_y_pos
    
    weapons_lst = [[w[0], w[1] - weapon_speed] for w in weapons_lst]
    weapons_lst = [[w[0], w[1]] for w in weapons_lst if w[1] > 0]

    for ball_idx, ball_val in enumerate(balls):
        ball_pos_x = ball_val["pos_x"]
        ball_pos_y = ball_val["pos_y"]
        ball_img_idx = ball_val["img_idx"]
        ball_size = ball_img_lst[ball_img_idx].get_rect().size
        ball_width = ball_size[0]
        ball_height = ball_size[1]

        if ball_pos_x < 0 or ball_pos_x > screen_width - ball_width:
            ball_val["to_x"] *= -1
        
        if ball_pos_y > screen_height - stage_height - ball_height:
            ball_val["to_y"] = ball_val["init_spd_y"]
        else:
            ball_val["to_y"] += 0.4 # 이거 떨어지게도 해야 하잖아

        ball_val["pos_x"] += ball_val["to_x"]
        ball_val["pos_y"] += ball_val["to_y"]
    ####################
    ## Collision check
    character_rect = character.get_rect()
    character_rect.left = character_x_pos
    character_rect.top = character_y_pos
    for ball_idx, ball_val in enumerate(balls):
        ball_pos_x = ball_val["pos_x"]
        ball_pos_y = ball_val["pos_y"]
        ball_img_idx = ball_val["img_idx"]
        ball_rect = ball_img_lst[ball_img_idx].get_rect()
        ball_rect.left = ball_pos_x
        ball_rect.top = ball_pos_y

        if character_rect.colliderect(ball_rect):
            running = False
            break
        
        for weapon_idx, weapon_val in enumerate(weapons_lst):
            weapon_pos_x = weapon_val[0]
            weapon_pos_y = weapon_val[1]

            weapon_rect = weapon.get_rect()
            weapon_rect.left = weapon_pos_x
            weapon_rect.top = weapon_pos_y

            if weapon_rect.colliderect(ball_rect):
                weapon_to_remove = weapon_idx
                ball_to_remove = ball_idx

                if ball_img_idx < 3:
                    ball_width_ = ball_rect.size[0]
                    ball_height_ = ball_rect.size[1]

                    small_ball_rect = ball_img_lst[ball_img_idx + 1].get_rect()
                    small_ball_width = small_ball_rect.size[0]
                    small_ball_height = small_ball_rect.size[1]

                    balls.append({
                                    "pos_x" : ball_pos_x + (0.5 * ball_width_) - (0.5 * small_ball_width), 
                                    "pos_y" : ball_pos_y + (0.5 * ball_height_) - (0.5 * small_ball_height), 
                                    "img_idx" : ball_img_idx + 1,
                                    "to_x" : -3,
                                    "to_y" : -6,
                                    "init_spd_y" : balls_speed[ball_img_idx + 1]
                                })
                    balls.append({
                                    "pos_x" : ball_pos_x + (0.5 * ball_width_) - (0.5 * small_ball_width), 
                                    "pos_y" : ball_pos_y + (0.5 * ball_height_) - (0.5 * small_ball_height), 
                                    "img_idx" : ball_img_idx + 1,
                                    "to_x" : +3,
                                    "to_y" : -6,
                                    "init_spd_y" : balls_speed[ball_img_idx + 1]
                                })
                break
        else:
            continue
        break
# 위의 else, continue, break 설명
# balls = [1, 2, 3, 4]
# weapons = [11, 22, 3, 44]

# for b_idx, b_val in enumerate(balls):
#     print("ball : ", b_val)
#     for w_idx, w_val in enumerate(weapons):
#         print("weapons : ", w_val)
#         if b_val == w_val:
#             print("공과 무기가 충돌") 
#             break

#     else:
#         continue
#     break

# for 바깥조건:
#     바깥동작
#     for 안쪽조건:
#         안쪽동작
#         if 충돌하면:
#             break
#     else:
#         continue
#     break

    if ball_to_remove > -1:
        del balls[ball_to_remove]
        ball_to_remove = -1
    
    if weapon_to_remove > -1:
        del weapons_lst[weapon_to_remove]
        weapon_to_remove = -1

    if len(balls) == 0:
        game_result = "Mission complete"
        running = False
    ####################
    ## Screen update
    screen.blit(background, (0, 0))
    
    for x, y in weapons_lst:
        screen.blit(weapon, (x, y))
    
    for idx, val in enumerate(balls):
        ball_pos_x = val["pos_x"]
        ball_pos_y = val["pos_y"]
        ball_img_idx = val["img_idx"]
        screen.blit(ball_img_lst[ball_img_idx], (ball_pos_x, ball_pos_y))

    screen.blit(stage, (0, screen_height - stage_height))
    screen.blit(character, (character_x_pos, character_y_pos))        

    elapsed_time = (pygame.time.get_ticks() - start_ticks) * 0.001 # ms order to s order
    timer = game_font.render("Time: {}".format(int(total_time - elapsed_time)), True, (255, 255, 255)) # int for rounding off fraction
    screen.blit(timer, (10, 10))

    if total_time - elapsed_time <= 0:
        game_result = "Time Over"
        running = False

    pygame.display.update()

msg = game_font.render(game_result, True, (255, 255, 0))
msg_rect = msg.get_rect(center=(int(screen_width/2), int(screen_height/2)))
screen.blit(msg, msg_rect)
pygame.display.update()

pygame.time.delay(2000)
pygame.quit()
