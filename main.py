# PvZClone - A tower defense clone for practice programming by Lilly~
# Start date: 3/17/2022
# Github link: https://github.com/GavinHanHAHS/pvzclone

# import packages needed for project

import pygame
import math
import random

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
        self.colour = (random.randint(0, 255), random.randint(0, 255), random.randint(0, 255))
        self.surf = pygame.Surface((50, 50))
        self.surf.fill((255, 255, 255))
        self.rect = self.surf.get_rect(
            center=(pygame.mouse.get_pos())
        )
        self.surf.set_colorkey((255, 255, 255))
        pygame.draw.circle(self.surf, self.colour, (25, 25), 25)

        # Define variables for logic
        self.placed = False

    def update(self, place=False, x=0, y=0):
        # Follow mouse cursor IF not placed yet
        if not self.placed:
            self.rect.center = pygame.mouse.get_pos()
            if place:
                if arena[y][x] == 0:
                    self.add(x, y)
        else:
            if not place:  # Don't let the towers update if it's a place event
                pass
                # Logic when placed

    def add(self, x, y):
        self.placed = True
        self.rect.topleft = (113 + (x * 75), 113 + (y * 75))
        arena[y][x] = self
        # print(arena, str(math.floor((mousex - 100)/75)), str(math.floor((mousey - 100)/75)))


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
    mousex, mousey = pygame.mouse.get_pos()
    mousex, mousey = math.floor((mousex - 100) / 75), math.floor((mousey - 100) / 75)

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
                towers.update(True, mousex, mousey)

    # DRAWING
    # Wipe Screen to help Drawing
    screen.fill((220, 220, 220))

    # Draw filler elements
    pygame.draw.rect(screen, pink, pygame.Rect(0, 0, 100, SCREEN_HEIGHT))
    pygame.draw.rect(screen, pink, pygame.Rect(0, 0, SCREEN_WIDTH, 100))
    pygame.draw.rect(screen, pink, pygame.Rect(0, SCREEN_HEIGHT-125, SCREEN_WIDTH, 125))
    pygame.draw.rect(screen, pink, pygame.Rect(SCREEN_WIDTH-25, 0, 25, SCREEN_HEIGHT))
    for i in range(9):
        pygame.draw.rect(screen, pink, pygame.Rect(100 + (i * 75), 0, 2, SCREEN_HEIGHT))
    for i in range(5):
        pygame.draw.rect(screen, pink, pygame.Rect(0, 100 + (i * 75), SCREEN_WIDTH, 2))

    # Check over every sprite in sprite group all_sprites -> Draw them
    for entity in all_sprites:
        screen.blit(entity.surf, entity.rect)
    screen.blit(debug.text, debug.rect)

    # Update Tower Logic
    towers.update()
    debug.update(str(mousex) + " " + str(mousey))

    # Update the display
    pygame.display.flip()

    # Ensure program maintains a good frame rate
    clock.tick(60)
