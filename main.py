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


# Features in my head
# Click button -> Add shovel item
# Seed slot class, to make seed slot objects. -> shovel item? both is intrinsically "add item"
# rect.collidepoint(pygame.mouse.get_pos() will check if a point is inside a rect
# Line of Sight objects
# Vfx objects (particle) -> spritesheet?


# Define a tower object by extending pygame.sprite.Sprite
# the surface(s) drawn on the screen is an attribute of "Tower"
class Tower(pygame.sprite.Sprite):
    def __init__(self):
        # Take properties from parent "sprite" class
        super(Tower, self).__init__()

        # Define variables for drawing
        self.colour = (random.randint(0, 255), random.randint(0, 255), random.randint(0, 255))
        self.surf = pygame.Surface((50, 50))
        self.image = pygame.image.load("image/gorilla_idle.png").convert_alpha()
        self.image2 = pygame.image.load("image/gorilla_shoot.png").convert_alpha()
        self.state = 0
        # self.surf.fill(self.colour)
        self.surf.fill((255, 255, 255))
        self.rect = self.surf.get_rect(
            center=(pygame.mouse.get_pos())
        )
        self.surf.blit(self.image, (0, 0))
        self.surf.set_colorkey((255, 255, 255))
        # pygame.draw.circle(self.surf, self.colour, (25, 25), 25)

        # Define variables for logic
        self.placed = False
        self.timer = 0

        self.xy = (False, False)

    def update(self, place=False, x=0, y=0):
        # Follow mouse cursor IF not placed yet
        if not self.placed:
            self.rect.center = pygame.mouse.get_pos()
            if place:
                if 0 <= x <= 8 and 0 <= y <= 4:
                    self.add(x, y)
                else:
                    self.kill()
        else:
            # Tower Logic After Placed.
            if not place:  # Don't let the towers update if it's a place event
                self.mechanic()

    def add(self, x, y):
        if arena[y][x] == 0:
            self.placed = True
            self.rect.topleft = (113 + (x * 75), 113 + (y * 75))
            arena[y][x] = self
            self.xy = (x, y)
            # print(arena, str(math.floor((mousex - 100)/75)), str(math.floor((mousey - 100)/75)))

    def delete(self):
        arena[self.xy[1]][self.xy[0]] = 0
        self.kill()

    def mechanic(self):
        pass


class Shooter(Tower):
    # Tower subclass that shoots
    def mechanic(self):
        if self.timer == 43:  # shoot when timer is maxed out
            self.timer = 0
            self.shoot()
        else:
            self.timer += 1
            if self.timer == 18 and self.state == 1:
                self.state = 0
                self.surf.fill((255, 255, 255))
                self.surf.blit(self.image, (0, 0))

    def shoot(self):
        if enemy_row[self.xy[1]] != 0:
            self.surf.blit(self.image2, (0, 0))
            self.state = 1
            newProjectile = Projectile(self)
            projectiles.add(newProjectile)
            all_sprites.add(newProjectile)


class OverrideTower(Tower):
    # Anything that must be placed onto another tower rather than an empty square
    def __init__(self):
        super().__init__()

        self.required_tower = "Class of object for override"

    def add(self, x, y):
        # Check if object clicked is the tower needed to override
        if isinstance(arena[y][x], self.required_tower):
            self.add_mechanic(x, y)
        else:
            # Delete self else
            self.kill()

    def add_mechanic(self, x, y):
        # What to do when adding object? by default, just inserts this object over it
        super().add(x, y)


class Shovel(OverrideTower):
    # Placed on any tower that exists, deletes tower then self
    def __init__(self):
        super().__init__()
        self.image = pygame.image.load("image/net.png").convert_alpha()
        self.surf.fill((255, 255, 255))
        self.surf.blit(self.image, (0, 0))
        # Redefine required tower to be ANY tower
        self.required_tower = Tower

    def add_mechanic(self, x, y):
        arena[y][x].delete()
        self.kill()


class Text(pygame.sprite.Sprite):
    # Text just in case (mostly debug)
    def __init__(self):
        super(Text, self).__init__()
        self.value = "hold"
        self.font = pygame.font.SysFont("arial", 30)
        self.text = self.font.render(self.value, True, (0, 0, 0), (255, 255, 255))
        self.rect = self.text.get_rect(topleft=(100, 300))

    def update(self, newValue):
        self.value = newValue
        self.text = self.font.render(self.value, True, (0, 0, 0), (255, 255, 255))


class TowerSlot(pygame.sprite.Sprite):
    # clickable object that puts a tower into your hands.
    def __init__(self):
        super().__init__()
        self.surf = pygame.Surface((40, 60))
        self.surf.fill((255, 255, 255))
        self.rect = self.surf.get_rect(
            center=(80, 120)
        )

    def update(self, click = False):
        if self.rect.collidepoint(pygame.mouse.get_pos()) and click == True:
            self.add_tower()

    def add_tower(self):
        new_tower = Shooter()
        towers.add(new_tower)
        all_sprites.add(new_tower)


class Projectile(pygame.sprite.Sprite):
    # Projectile shot by Shooters
    def __init__(self, tower):
        super(Projectile, self).__init__()
        # self.colour = (random.randint(0, 255), random.randint(0, 255), random.randint(0, 255))
        self.colour = (0, 0, 0)
        self.surf = pygame.Surface((15, 15))
        self.surf.fill((255, 255, 255))
        self.rect = (self.surf.get_rect(
            center=(tower.rect.center[0], tower.rect.center[1] + random.randint(-7, 3))
        ))
        self.surf.set_colorkey((255, 255, 255))
        pygame.draw.circle(self.surf, self.colour, (7.5, 7.5), 7.5)

    def update(self):
        self.rect.move_ip(7, 0)
        if self.rect.left > SCREEN_WIDTH:
            self.kill()


class Enemy(pygame.sprite.Sprite):
    # Enemy that spawns on right side of screen and slowly moves left
    def __init__(self, location):
        super(Enemy, self).__init__()

        # Drawing Variables
        self.colour = (random.randint(0, 255), random.randint(0, 255), random.randint(0, 255))
        self.surf = pygame.Surface((40, 40))
        self.rect = self.surf.get_rect(
            center=(850, 70 + (75 * location))
        )
        self.image = pygame.image.load("image/key.png").convert()
        self.surf.blit(self.image, (0, 0))
        self.surf.set_colorkey((255, 255, 255))
        pygame.draw.circle(self.surf, self.colour, (20, 5), 5)

        # Logic Variables
        self.health = 2 + random.randint(2, 5)
        self.row = location - 1
        enemy_row[self.row] += 1

    def update(self):
        if self.health <= 0 or self.rect.right < 0:
            enemy_row[self.row] -= 1
            self.kill()
        else:
            self.rect.move_ip(-1, 0)


# initialize pygame
pygame.init()


# GLOBAL VARIABLES
# Define constants for screen width/height
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600

# Create the screen object; size determined by screen constants
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("PvZClone")

# Set Icon for Window
icon = pygame.image.load("image/icon.png").convert_alpha()
pygame.display.set_icon(icon)

# Image to draw to "Background"
bg = pygame.image.load("image/bg.png").convert()

# Setup the clock for a decent framerate
clock = pygame.time.Clock()

# Add a grid that has towers inserted into it. (row, column) format
# --> should this be an arena object?
arena = [[0, 0, 0, 0, 0, 0, 0, 0, 0],
         [0, 0, 0, 0, 0, 0, 0, 0, 0],
         [0, 0, 0, 0, 0, 0, 0, 0, 0],
         [0, 0, 0, 0, 0, 0, 0, 0, 0],
         [0, 0, 0, 0, 0, 0, 0, 0, 0]]

# Are there enemies in the row it's in?
enemy_row = [0, 0, 0, 0, 0]
# continues to shoot even while enemies are behind;
# maybe add a Line of Sight object attached to the tower object that groupcollides?


pink = (227, 143, 224)

# debug = Text()

# Define a group to hold
# * all sprites for drawing
# * all towers for logic
all_sprites = pygame.sprite.Group()
towers = pygame.sprite.Group()
projectiles = pygame.sprite.Group()
enemies = pygame.sprite.Group()


# Helpful Functions
def add_enemy(row):
    new_enemy = Enemy(row)
    enemies.add(new_enemy)
    all_sprites.add(new_enemy)


seedslot = TowerSlot()
all_sprites.add(seedslot)


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
                # Make a new tower & add to cursor
                new_tower = Shooter()
                towers.add(new_tower)
                all_sprites.add(new_tower)
            elif event.key == pygame.K_b:
                # make enemies spawn randomly OR on specific rows
                add_enemy(random.randint(1, 5))
            elif event.key == pygame.K_1:
                add_enemy(1)
            elif event.key == pygame.K_2:
                add_enemy(2)
            elif event.key == pygame.K_3:
                add_enemy(3)
            elif event.key == pygame.K_4:
                add_enemy(4)
            elif event.key == pygame.K_5:
                add_enemy(5)
            elif event.key == pygame.K_c:
                # Make a shovel object to delete towers
                new_shovel = Shovel()
                towers.add(new_shovel)
                all_sprites.add(new_shovel)
        elif event.type == MOUSEBUTTONDOWN:
            mouse_buttons = pygame.mouse.get_pressed()
            if mouse_buttons[0]:
                # If left click, give towers the appropriate information to process
                towers.update(True, mousex, mousey)
                seedslot.update(True)

    # DRAWING
    # Wipe Screen to help Drawing
    screen.blit(bg, (0, 0))
    # screen.fill((220, 220, 220))

    # Check over every sprite in sprite group all_sprites -> Draw them
    for entity in all_sprites:
        screen.blit(entity.surf, entity.rect)
    # screen.blit(debug.text, debug.rect)

    # Update Tower Logic
    towers.update()
    # debug.update(str(mousex) + " " + str(mousey))
    # debug.update(str(enemy_row))

    projectiles.update()
    enemies.update()

    # Handle projectile collision
    collision = pygame.sprite.groupcollide(enemies, projectiles, False, False)

    # for loops through a dictionary, enemy is key, projectile is value
    for enemy, projectile in collision.items():
        if projectile[0].rect.left >= enemy.rect.left + 10:
            # When the projectile goes into an appropriate amount of distance into
            # the sprite (aesthetics) delete the projectile and decrease enemy health
            enemy.health -= 1
            projectile[0].kill()

    # Update the display
    pygame.display.flip()

    # Ensure program maintains a good frame rate
    clock.tick(60)



