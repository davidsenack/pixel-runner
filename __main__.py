import __main__
import pygame
from sys import exit
from random import randint


def display_score():
    current_time = int(pygame.time.get_ticks() / 1000) - start_time
    score_surface = test_font.render(
        f'Score: {current_time}', False, (64, 64, 64)).convert()
    score_rect = score_surface.get_rect(center=(400, 50))
    screen.blit(score_surface, score_rect)
    return current_time


def display_intro():
    # Background and player image
    screen.fill((94, 129, 162))
    screen.blit(player_stand, player_stand_rect)

    # Top text
    top_text_surface = test_font.render(
        'Pixel Runner', False, (94, 192, 162)).convert()
    top_text_rect = top_text_surface.get_rect(center=(400, 50))
    screen.blit(top_text_surface, top_text_rect)

    if score <= 0:
        # Bottom text
        bottom_text_surface = test_font.render(
            'Press Space to Start', False, (94, 192, 162)).convert()
        bottom_text_rect = bottom_text_surface.get_rect(center=(400, 350))
        screen.blit(bottom_text_surface, bottom_text_rect)
    else:
        # Score bottom text
        score_text_surface = test_font.render(
            f'Your Score: {score}', False, (94, 192, 162)).convert()
        score_text_rect = score_text_surface.get_rect(center=(400, 350))
        screen.blit(score_text_surface, score_text_rect)


def obstacle_movement(obstacle_list):
    if obstacle_list:
        for obstacle_rect in obstacle_list:
            obstacle_rect.x -= 5

            if obstacle_rect.bottom >= 300:
                screen.blit(snail_surface, obstacle_rect)
            else:
                screen.blit(fly_surface, obstacle_rect)

        obstacle_list = [
            obstacle for obstacle in obstacle_list if obstacle.x > -100]

        return obstacle_list
    else:
        return []


pygame.init()
screen = pygame.display.set_mode((800, 400))
pygame.display.set_caption("Runner")
clock = pygame.time.Clock()
test_font = pygame.font.Font('font/Pixeltype.ttf', 50)
game_active = True
start_time = 0
score = 0

sky_surface = pygame.image.load('graphics/Sky.png').convert()
ground_surface = pygame.image.load('graphics/ground.png').convert()

# score_surface = test_font.render('Score: 0', False, (64, 64, 64)).convert()
# score_rect = score_surface.get_rect(center=(400, 50))

# Obstacles
snail_surface = pygame.image.load('graphics/snail/snail1.png').convert_alpha()
fly_surface = pygame.image.load('graphics/fly/fly1.png').convert_alpha()

obstacle_rect_list = []

player_surface = pygame.image.load(
    'graphics/player/player_walk_1.png').convert_alpha()
player_rect = player_surface.get_rect(midbottom=(80, 300))
player_gravity = 0

# Intro screen
player_stand = pygame.image.load(
    'graphics/player/player_stand.png').convert_alpha()
player_stand = pygame.transform.rotozoom(player_stand, 0, 2.5)
player_stand_rect = player_stand.get_rect(center=(400, 200))

# Timer
obstacle_timer = pygame.USEREVENT + 1
pygame.time.set_timer(obstacle_timer, 1500)

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                pygame.quit()
                exit()

        if game_active:
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE and player_rect.bottom >= 300:
                    player_gravity = -20

            if event.type == pygame.MOUSEBUTTONDOWN:
                if player_rect.collidepoint(event.pos) and player_rect.bottom >= 300:
                    player_gravity = -20

        if not game_active:
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    game_active = True
                    player_rect.midbottom = (80, 300)
                    # snail_rect.midbottom = (600, 300)
                    start_time = int(pygame.time.get_ticks() / 1000)

            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    game_active = True
                    player_rect.midbottom = (80, 300)
                    # snail_rect.midbottom = (600, 300)
                    start_time = int(pygame.time.get_ticks() / 1000)

        if event.type == obstacle_timer and game_active:
            if randint(0, 2):
                obstacle_rect_list.append(snail_surface.get_rect(
                    bottomright=(randint(900, 1100), 300)))
            else:
                obstacle_rect_list.append(fly_surface.get_rect(
                    bottomright=(randint(900, 1100), 200)))

    if game_active:
        screen.blit(sky_surface, (0, 0))
        screen.blit(ground_surface, (0, 300))

        # pygame.draw.rect(screen, '#c0e8ec', score_rect)
        # screen.blit(score_surface, score_rect)
        score = display_score()

        # snail_rect = snail_rect.move(-6, 0)
        # if snail_rect.x <= -100: snail_rect.x = 800
        # screen.blit(snail_surface, snail_rect)

        # Player
        player_gravity += 1
        player_rect.y += player_gravity
        if player_rect.bottom >= 300:
            player_rect.bottom = 300
        screen.blit(player_surface, player_rect)

        # Obstacle movement
        obstacle_rect_list = obstacle_movement(obstacle_rect_list)

        # Collision
        # if snail_rect.colliderect(player_rect):
        #    game_active = False

    else:
        display_intro()

    pygame.display.update()
    clock.tick(60)
