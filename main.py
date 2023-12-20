'''
Side scroller with objects moving to the right to imitate the players movement
Enemies on the ground you have to jump over
enemies in the sky that if you jump and hit kill you
'''

'''
sources:
kids can code: http://kidscancode.org/blog/
Daniel Yoon
Jesse Segall 
Tech With Tim
'''

# import libraries and modules
import random

import pygame
from sys import exit
from random import randint, choice
import os

# Set up folder paths for game assets
game_folder = os.path.dirname(__file__)
graphics_folder = os.path.join(game_folder, 'graphics')
player_folder = os.path.join(game_folder, 'player')
audio_folder = os.path.join(game_folder, 'audio')

# Player class representing the game character
class Player(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        # Load player images for walking animation and jump
        player_walk_1 = pygame.image.load('graphics/player/running_1.png').convert_alpha()
        player_walk_2 = pygame.image.load('graphics/player/running_2.png').convert_alpha()
        self.player_walk = [player_walk_1, player_walk_2]
        self.player_index = 0
        self.player_jump = pygame.image.load('graphics/player/running_2.png').convert_alpha()
        self.image = self.player_walk[self.player_index]
        self.rect = self.image.get_rect(midbottom=(200, 300))
        self.gravity = 0

        # Load jump sound and set volume
        self.jump_sound = pygame.mixer.Sound('audio/audio_jump.mp3')
        self.jump_sound.set_volume(0.2)

    def player_input(self):
        # Check for key presses
        keys = pygame.key.get_pressed()
        
        # Check if the space key is pressed and the player is on the ground
        if keys[pygame.K_SPACE] and self.rect.bottom >= 300:
            # Set negative gravity to make the player jump
            self.gravity = -20
            
            # Play the jump sound
            self.jump_sound.play()
          

    def apply_gravity(self):
          # Apply gravity to simulate jumping and falling
        self.gravity += 1
        self.rect.y += self.gravity
        if self.rect.bottom >= 300:
            self.rect.bottom = 300

    def animation_state(self):
        # Manage player animation based on whether jumping or on the ground
        if self.rect.bottom < 300:
            self.image = self.player_jump
        else:
            self.player_index += 0.1
            if self.player_index >= len(self.player_walk):
                self.player_index = 0
            self.image = self.player_walk[int(self.player_index)]

     # Update player state based on input, gravity, and animation
    def update(self):
        self.player_input()
        self.apply_gravity()
        self.animation_state()


class Obstacle(pygame.sprite.Sprite):
    def __init__(self, type):
        super().__init__()

        # Check the type of obstacle and load corresponding images
        if type == 'explosion':
            explosion_1 = pygame.image.load('graphics/New folder/explosion.png').convert_alpha()
            explosion_2 = pygame.image.load('graphics/New folder/explosion_2.png').convert_alpha()
            self.frames = [explosion_1, explosion_2]
            y_pos = 210
        else:
            cactus_1 = pygame.image.load('graphics/cactus/cactus_1.png').convert_alpha()
            cactus_2 = pygame.image.load('graphics/cactus/cactus_2.png').convert_alpha()
            self.frames = [cactus_1, cactus_2]
            y_pos = 300

        # Initialize animation index and set the initial image and position
        self.animation_index = 0
        self.image = self.frames[self.animation_index]
        self.rect = self.image.get_rect(midbottom=(random.randint(900, 1200), y_pos))

    # manages te obstacles based on the frames
    def animation_state(self):
        self.animation_index += 0.1
        if self.animation_index >= len(self.frames): self.animation_index = 0
        self.image = self.frames[int(self.animation_index)]

    #update the obstacles animation, movement, etc.
    def update(self):
        self.animation_state()
        self.rect.x -= 6
        self.destroy()

    def destroy(self):
        # deletes the osbtacles when offscreen
        if self.rect.x <= -100:
            self.kill()


def display_score():
    # Calculate the current time in seconds and subtract the start time
    current_time = int(pygame.time.get_ticks() / 2000) - start_time
    # Renders the time as a text surfae
    score_surf = test_font.render(f'{current_time}', False, (64, 64, 64))
    score_rect = score_surf.get_rect(center=(400, 50))
    #draws the text surface on rectangle pos
    screen.blit(score_surf, score_rect)
    return current_time

# Check for collisions between the player sprite and the obstacle group
def collision_sprite():
    if pygame.sprite.spritecollide(player.sprite, obstacle_group, False):
         # If a collision occurs, empty the obstacle group and return False
        obstacle_group.empty()
        return False
    else:
        return True


pygame.init()
# Set up the game window, clock, font, and initial game state
screen = pygame.display.set_mode((800, 400))
pygame.display.set_caption('Runnin')
clock = pygame.time.Clock()
test_font = pygame.font.Font('font/Pixeltype.ttf', 50)
game_active = False
start_time = 0
score = 0
# Loads and plays the background music with volume set to 0.15
music = pygame.mixer.Sound('audio/Music.mp3')
music.set_volume(0.15)
music.play(loops=-1)  # Loops music forever

# Sprite groups for the player and obstacles
player = pygame.sprite.GroupSingle()
player.add(Player())
obstacle_group = pygame.sprite.Group()

# Load images for the sky and ground surfaces
sky_surface = pygame.image.load('graphics/Sky.png').convert_alpha()
ground_surface = pygame.image.load('graphics/Ground.png').convert_alpha()

# Elements in introduction screen
player_stand = pygame.image.load('graphics/player/Thumbs_up.png').convert_alpha()
player_stand = pygame.transform.rotozoom(player_stand, 0, 2)
player_stand_rect = player_stand.get_rect(center=(400, 200))

game_name = test_font.render('Running Running Running', False, (111, 196, 169))
game_name_rect = game_name.get_rect(center=(400, 80))

game_message = test_font.render('Press space to start', False, (111, 196, 169))
game_message_rect = game_message.get_rect(center=(400, 330))

# Set up an obstacle timer that triggers every 1500 milliseconds (1.5 seconds)
obstacle_timer = pygame.USEREVENT + 1
pygame.time.set_timer(obstacle_timer, 1500)

# Main game loop
# Check for Pygame events
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()
# Check events during active gameplay
        if game_active:
            # If the obstacle timer event occurs, add a new obstacle to the obstacle group
            if event.type == obstacle_timer:
                obstacle_group.add(Obstacle(choice(['explosion', 'cactus', 'cactus', 'cactus'])))
# Check events during the intro or game over screen
        else:
            if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                game_active = True
                start_time = int(pygame.time.get_ticks() / 2000)
# Update game elements based on game state
    if game_active:
        # Draws the sky
        screen.blit(sky_surface, (0, 0))
        #Draws the surface
        screen.blit(ground_surface, (0, 300))
        #Adds the score
        score = display_score()

        # Draw and update the player sprite
        player.draw(screen)
        player.update()

        # Draw and update the obstacle sprites
        obstacle_group.draw(screen)
        obstacle_group.update()

        game_active = collision_sprite()

    else:
        screen.fill((40, 150, 92))
        screen.blit(player_stand, player_stand_rect)
        # Render and display the game name
        score_message = test_font.render(f'Your score: {score}', False, (111, 196, 169))
        score_message_rect = score_message.get_rect(center=(400, 330))
        screen.blit(game_name, game_name_rect)
        # Display the game message or score message based on the player's score
        if score == 0:
            screen.blit(game_message, game_message_rect)
        else:
            screen.blit(score_message, score_message_rect)
    # sets the clock tick to 60 fps
    pygame.display.update()
    clock.tick(60)
