# PvZClone - A tower defense clone for practice programming by Lilly~
# Start date: 3/17/2022
# Github link: https://github.com/GavinHanHAHS/pvzclone

# import packages needed for project

import pygame

# Import pygame.locals for easier access to key coordinates
from pygame.locals import (
    KEYDOWN,
    MOUSEBUTTONDOWN,
    QUIT,
)

# initialize pygame
pygame.init()

# Define constants for screen width/height
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600

# Create the screen object; size determined by screen constants
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("PvZClone")

# Setup the clock for a decent framerate
clock = pygame.time.Clock()


# Define a tower object by extending pygame.sprite.Sprite
# the surface(s) drawn on the screen is an attribute of "Tower"
class Tower(pygame.sprite.Sprite):
    def __init__(self):
        # Take properties from parent "sprite" class
        super(Tower, self).__init__()

        # Define variables for drawing
        self.surf = pygame.Surface((50, 50))
        self.surf.fill((181, 126, 220))
        self.rect = self.surf.get_rect(
            center=(pygame.mouse.get_pos())
        )

        # Define variables for logic
        self.placed = False

    def update(self, place=False):
        # Follow mouse cursor IF not placed yet
        if not self.placed:
            self.rect.center = pygame.mouse.get_pos()
            if place:
                self.placed = True
        else:
            # Logic when placed
            pass


# Define a group to hold
# * all sprites for drawing
# * all towers for logic
all_sprites = pygame.sprite.Group()
towers = pygame.sprite.Group()

# Main Loop
running = True
while running:
    # INPUT
    # Check Events
    for event in pygame.event.get():
        if event.type == QUIT:
            running = False
        elif event.type == KEYDOWN:
            if event.key == pygame.K_a:
                new_tower = Tower()
                towers.add(new_tower)
                all_sprites.add(new_tower)
        elif event.type == MOUSEBUTTONDOWN:
            mouse_buttons = pygame.mouse.get_pressed()
            if mouse_buttons[0]:
                towers.update(True)

    # DRAWING
    # Wipe Screen to help Drawing
    screen.fill((255, 255, 255))

    # Check over every sprite in sprite group all_sprites -> Draw them
    for entity in all_sprites:
        screen.blit(entity.surf, entity.rect)

    # Update Tower Logic
    towers.update()

    # Update the display
    pygame.display.flip()

    # Ensure program maintains a good frame rate
    clock.tick(60)
