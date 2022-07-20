import random
import pygame

pygame.init()

# 화면 크기 설정
screen_width = 480
screen_height = 640
screen = pygame.display.set_mode((screen_width, screen_height))

# 타이틀 설정
pygame.display.set_caption("Avoid_Knife Game")

#FPS
clock = pygame.time.Clock()

# 배경이미지
background = pygame.image.load("background.png")

# 캐릭터
character = pygame.image.load("character.png")
character_size = character.get_rect().size
character_width = character_size[0]
character_height = character_size[1]
character_x_pos = screen_width / 2 - character_width / 2
character_y_pos = screen_height - character_height

# 칼
knife = pygame.image.load("knife.png")
knife_size = knife.get_rect().size
knife_width = knife_size[0]
knife_height = knife_size[1]
knife_x_pos = random.randrange(0, screen_width - knife_width)
knife_y_pos = -knife_height
knife_speed = 1

# 이동
to_x = 0
to_y = 0
speed = 0.8

# 폰트
time_font = pygame.font.Font(None, 40)
red_font = pygame.font.Font(None, 150)

# 시간
start_ticks = pygame.time.get_ticks()
total_time = 10


running = True
while running:
    screen.blit(background, (0, 0))
    
    dt = clock.tick(60)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                to_x = -speed
            if event.key == pygame.K_RIGHT:
                to_x = speed
            if event.key == pygame.K_UP:
                to_y = -speed
            if event.key == pygame.K_DOWN:
                to_y = speed

        if event.type == pygame.KEYUP:
            if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT:
                to_x = 0
            if event.key == pygame.K_UP or event.key == pygame.K_DOWN:
                to_y = 0

    character_x_pos += to_x * dt
    character_y_pos += to_y * dt

    knife_y_pos += knife_speed * dt

    # 충돌 처리
    character_rect = character.get_rect()
    character_rect.left = character_x_pos
    character_rect.top = character_y_pos
    knife_rect = knife.get_rect()
    knife_rect.left = knife_x_pos
    knife_rect.top = knife_y_pos

    if character_rect.colliderect(knife_rect):
        running = False
        die_text = red_font.render("DIE!", True, (255, 15, 0))
        screen.blit(die_text, (screen_width / 2 - 30, 100))


    # 경계값 처리
    if character_x_pos < 0:
        character_x_pos = 0
    if character_x_pos > screen_width - character_width:
        character_x_pos = screen_width - character_width
    if character_y_pos < 0:
        character_y_pos = 0
    if character_y_pos > screen_height - character_height:
        character_y_pos = screen_height - character_height

    if knife_y_pos > screen_height:
        knife_y_pos = -knife_height
        knife_x_pos = random.randrange(0, screen_width - knife_width)

    # 타이머
    elapsed_time = (pygame.time.get_ticks() - start_ticks) / 1000
    timer = time_font.render(str(int(total_time - elapsed_time)), True, (255, 255,255))
    screen.blit(timer, (10, 10))

    if elapsed_time >= 10:
        running = False
        timeover_text = red_font.render("END", True, (255, 10, 0))
        screen.blit(timeover_text, (screen_width / 2 - 70, 100))

    screen.blit(character, (character_x_pos, character_y_pos))
    screen.blit(knife, (knife_x_pos, knife_y_pos))

    pygame.display.update()

pygame.time.delay(1000)

pygame.quit()
