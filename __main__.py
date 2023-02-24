""" Main game file for the Pixel Runner game."""

# Disble pylint error for pygame unknown members
# pylint: disable=no-member
# pylint: disable=no-name-in-module

from random import randint, choice
import sys
from pygame.constants import (
    QUIT, KEYDOWN, K_SPACE, K_ESCAPE, USEREVENT, MOUSEBUTTONDOWN)
import pygame


class Player(pygame.sprite.Sprite):
    """Player class for the Pixel Runner game."""

    def __init__(self):
        super().__init__()

        # Load player images for walking and jumping
        player_walk_1 = pygame.image.load(
            'graphics/player/player_walk_1.png').convert_alpha()
        player_walk_2 = pygame.image.load(
            'graphics/player/player_walk_2.png').convert_alpha()
        self.player_walk = [player_walk_1, player_walk_2]
        self.player_index = 0
        self.player_jump = pygame.image.load(
            'graphics/player/jump.png').convert_alpha()

        # Set player image and rect
        self.image = self.player_walk[self.player_index]
        self.rect = self.image.get_rect(midbottom=(80, 300))
        self.gravity = 0

        # Load jump sound
        self.jump_sound = pygame.mixer.Sound('audio/jump.mp3')
        self.jump_sound.set_volume(0.2)

    def player_input(self):
        """Check for space bar press and apply gravity and jump sound."""

        keys = pygame.key.get_pressed()
        if keys[K_SPACE] and self.rect.bottom >= 300:
            self.gravity = -20
            self.jump_sound.play()

    def apply_gravity(self):
        """Apply gravity to player when jumping"""

        self.gravity += 1
        self.rect.y += self.gravity
        if self.rect.bottom >= 300:
            self.rect.bottom = 300

    def animation_state(self):
        """Animate player walking; do nothing when jumping"""

        if self.rect.bottom < 300:
            self.image = self.player_jump
        else:
            self.player_index += 0.1
            if self.player_index >= len(self.player_walk):
                self.player_index = 0
            self.image = self.player_walk[int(self.player_index)]

    def update(self):
        """Update player image and rect"""

        self.player_input()
        self.apply_gravity()
        self.animation_state()


class Obstacle(pygame.sprite.Sprite):
    """Obstacle class for the Pixel Runner game."""

    def __init__(self, sprite_type):
        super().__init__()

        # Load obstacle images based on input
        if sprite_type == 'fly':
            fly_1 = pygame.image.load('graphics/fly/fly1.png').convert_alpha()
            fly_2 = pygame.image.load('graphics/fly/fly2.png').convert_alpha()
            self.frames = [fly_1, fly_2]
            y_pos = 200
        else:
            snail_1 = pygame.image.load(
                'graphics/snail/snail1.png').convert_alpha()
            snail_2 = pygame.image.load(
                'graphics/snail/snail2.png').convert_alpha()
            self.frames = [snail_1, snail_2]
            y_pos = 300

        # Set obstacle image and rect based on input type
        self.animation_index = 0
        self.image = self.frames[self.animation_index]
        self.rect = self.image.get_rect(midbottom=(randint(900, 1100), y_pos))

    def animation_state(self):
        """Animate obstacles"""

        self.animation_index += 0.1
        if self.animation_index >= len(self.frames):
            self.animation_index = 0
        self.image = self.frames[int(self.animation_index)]

    def destroy(self):
        """Destroy obstacles when off screen"""

        if self.rect.x < -100:
            self.kill()

    def update(self):
        """Update obstacle image and rect"""

        self.animation_state()
        self.rect.x -= 6
        self.destroy()


def display_score():
    """Display score at top of screen during game"""

    current_time = int(pygame.time.get_ticks() / 1000) - START_TIME
    score_surface = test_font.render(
        f'Score: {current_time}', False, (64, 64, 64)).convert()
    score_rect = score_surface.get_rect(center=(400, 50))
    screen.blit(score_surface, score_rect)
    return current_time


def display_intro():
    """Displays intro screen at beginning of game and a different screen after game over"""

    # Player image
    player_stand = pygame.image.load(
        'graphics/player/player_stand.png').convert_alpha()
    player_stand = pygame.transform.rotozoom(player_stand, 0, 2)
    player_stand_rect = player_stand.get_rect(center=(400, 180))

    # Background and player image
    screen.fill((94, 129, 162))
    screen.blit(player_stand, player_stand_rect)

    # Top text
    top_text_surface = test_font.render(
        'Pixel Runner', False, (94, 192, 162)).convert()
    top_text_rect = top_text_surface.get_rect(center=(400, 50))
    screen.blit(top_text_surface, top_text_rect)

    if SCORE <= 0:
        # Bottom text
        bottom_text_surface = test_font.render(
            'Press Space to Start', False, (94, 192, 162)).convert()
        bottom_text_rect = bottom_text_surface.get_rect(center=(400, 350))
        screen.blit(bottom_text_surface, bottom_text_rect)
    else:
        # Score bottom text

        # Score text
        score_text_surface = test_font.render(
            f'Your Score: {SCORE}', False, (94, 192, 162)).convert()
        score_text_rect = score_text_surface.get_rect(center=(400, 320))
        screen.blit(score_text_surface, score_text_rect)

        # Play again or quit text
        small_font = pygame.font.Font('font/Pixeltype.ttf', 30)
        play_again_surface = small_font.render(
            'Press Space to Play Again or Esc to Quit', False, (94, 192, 162)).convert()
        play_again_rect = play_again_surface.get_rect(center=(400, 350))
        screen.blit(play_again_surface, play_again_rect)


def collision_sprite():
    """Check for collision between player and obstacles"""

    if pygame.sprite.spritecollide(player.sprite, obstacle_group, False):
        obstacle_group.empty()
        return False
    else:
        return True


def display_background():
    """Display background images"""

    sky_surface = pygame.image.load('graphics/Sky.png').convert()
    ground_surface = pygame.image.load('graphics/ground.png').convert()
    screen.blit(sky_surface, (0, 0))
    screen.blit(ground_surface, (0, 300))


def play_game_music():
    """Play background music"""
    
    bg_music = pygame.mixer.Sound('audio/music.wav')
    bg_music.play(loops=-1)
    bg_music.set_volume(0.3)


# Load game variables
pygame.init()
screen = pygame.display.set_mode((800, 400))
pygame.display.set_caption("Pixel Runner")
clock = pygame.time.Clock()
test_font = pygame.font.Font('font/Pixeltype.ttf', 50)
GAME_ACTIVE = False
START_TIME = 0
SCORE = 0

# Load game music
play_game_music()

# Load sprite groups
player = pygame.sprite.GroupSingle()
player.add(Player())
obstacle_group = pygame.sprite.Group()

# Load game timers
obstacle_timer = USEREVENT + 1
pygame.time.set_timer(obstacle_timer, 1500)

snail_animation_timer = USEREVENT + 2
pygame.time.set_timer(snail_animation_timer, 500)

fly_animation_timer = USEREVENT + 3
pygame.time.set_timer(fly_animation_timer, 200)

# Main game loop
while True:
    for event in pygame.event.get():
        # Quit game via mouse and keyboard events
        if event.type == QUIT:
            pygame.quit()
            sys.exit()

        if event.type == KEYDOWN:
            if event.key == K_ESCAPE:
                pygame.quit()
                sys.exit()
        # Create obstacles on game active state
        if GAME_ACTIVE:
            if event.type == obstacle_timer:
                obstacle_group.add(
                    Obstacle(choice(['fly', 'snail', 'snail'])))

        # Settings prior to game start or game active state
        if not GAME_ACTIVE:
            if event.type == KEYDOWN:
                if event.key == K_SPACE:
                    GAME_ACTIVE = True
                    START_TIME = int(pygame.time.get_ticks() / 1000)

            if event.type == MOUSEBUTTONDOWN:
                if event.button == 1:
                    GAME_ACTIVE = True
                    START_TIME = int(pygame.time.get_ticks() / 1000)

    # Game active state events
    if GAME_ACTIVE:

        # Draw background and score
        display_background()
        SCORE = display_score()

        # Draw player and obstacles
        player.draw(screen)
        player.update()
        obstacle_group.draw(screen)
        obstacle_group.update()

        # Collision
        GAME_ACTIVE = collision_sprite()

    else:
        # Draw intro screen
        display_intro()

    # Update display at 60 fps
    pygame.display.update()
    clock.tick(60)