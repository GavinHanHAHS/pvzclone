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


class Text(pygame.sprite.Sprite):
    def __init__(self):
        super(Text, self).__init__()
        self.value = "hold"
        self.font = pygame.font.SysFont("arial", 30)
        self.text = self.font.render(self.value, True, (0, 0, 0), (255, 255, 255))
        self.rect = self.text.get_rect(topleft=(100, 300))

    def update(self, newValue):
        self.value = newValue
        self.text = self.font.render(self.value, True, (0, 0, 0), (255, 255, 255))


# initialize pygame
pygame.init()


# GLOBAL VARIABLES
# Define constants for screen width/height
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600

# Create the screen object; size determined by screen constants
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("PvZClone")

# Setup the clock for a decent framerate
clock = pygame.time.Clock()

# Add a grid that has towers inserted into it. (row, column) format
# --> should this be an arena object?
arena = [[0, 0, 0, 0, 0, 0, 0, 0, 0],
         [0, 0, 0, 0, 0, 0, 0, 0, 0],
         [0, 0, 0, 0, 0, 0, 0, 0, 0],
         [0, 0, 0, 0, 0, 0, 0, 0, 0],
         [0, 0, 0, 0, 0, 0, 0, 0, 0]]

pink = (227, 143, 224)

debug = Text()

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
    screen.fill((220, 220, 220))

    # Draw filler elements
    pygame.draw.rect(screen, pink, pygame.Rect(0, 0, 100, SCREEN_HEIGHT))
    pygame.draw.rect(screen, pink, pygame.Rect(0, 0, SCREEN_WIDTH, 100))
    pygame.draw.rect(screen, pink, pygame.Rect(0, SCREEN_HEIGHT-50, SCREEN_WIDTH, 50))
    pygame.draw.rect(screen, pink, pygame.Rect(SCREEN_WIDTH-25, 0, 25, SCREEN_HEIGHT))

    # Check over every sprite in sprite group all_sprites -> Draw them
    for entity in all_sprites:
        screen.blit(entity.surf, entity.rect)
    screen.blit(debug.text, debug.rect)

    # Update Tower Logic
    towers.update()
    x, y = pygame.mouse.get_pos()
    debug.update(str(x) + " " + str(y))

    # Update the display
    pygame.display.flip()

    # Ensure program maintains a good frame rate
    clock.tick(60)
