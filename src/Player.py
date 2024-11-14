
import pygame

from os import walk
from os.path import join

from settings import (
    WINDOW_HEIGHT,
    WINDOW_WIDTH
)


class Player(pygame.sprite.Sprite):
    def __init__(self, pos, group, collision_sprites):
        super().__init__(group)
        self.load_images()
        self.state, self.frame_index = "down", 0
        self.image = pygame.image.load(
            join('assets', 'images', 'player', 'down', '0.png')).convert_alpha()
        self.rect = self.image.get_frect(
            center=pos)
        self.hitbox_rect = self.rect.inflate(-40, -30)

        self.direction = pygame.math.Vector2(0, 0)
        self.speed = 300
        self.collision_sprites = collision_sprites

    def load_images(self):
        self.frames = {
            "down": [],
            "left": [],
            "right": [],
            "up": [],
        }
        for state in self.frames.keys():
            for folder, _, files in walk(f'./assets/images/player/{state}'):
                if files:
                    for file in sorted(files, key=lambda name: int(name.split(".")[0])):
                        full_path = f"{folder}/{file}"
                        surf = pygame.image.load(full_path).convert_alpha()
                        self.frames[state].append(surf)
        print(self.frames)

    def input(self):
        keys = pygame.key.get_pressed()
        self.direction.x = int(keys[pygame.K_RIGHT]) - int(keys[pygame.K_LEFT])
        self.direction.y = int(keys[pygame.K_DOWN]) - int(keys[pygame.K_UP])
        self.direction = self.direction.normalize() if self.direction else self.direction

    def move(self, dt):
        self.hitbox_rect.x += (self.direction.x * self.speed * dt)
        self.collision('horizontal')
        self.hitbox_rect.y += (self.direction.y * self.speed * dt)
        self.collision('vertical')
        self.rect.center = self.hitbox_rect.center

    def collision(self, direction):
        for sprite in self.collision_sprites:
            if sprite.rect.colliderect(self.hitbox_rect):
                if direction == "horizontal":
                    if self.direction.x > 0:
                        self.hitbox_rect.right = sprite.rect.left
                    if self.direction.x < 0:
                        self.hitbox_rect.left = sprite.rect.right
                if direction == "vertical":
                    if self.direction.y < 0:
                        self.hitbox_rect.top = sprite.rect.bottom
                    if self.direction.y > 0:
                        self.hitbox_rect.bottom = sprite.rect.top

    def animate(self, dt):
        if self.direction.x > 0:
            self.state = "right"
        if self.direction.x < 0:
            self.state = "left"
        if self.direction.y > 0:
            self.state = "down"
        if self.direction.y < 0:
            self.state = "up"

        if self.direction == pygame.math.Vector2(0, 0):
            self.frame_index = 0
            self.image = self.frames[self.state][int(
                self.frame_index) % len(self.frames[self.state])]
        else:
            self.frame_index += 5 * dt
            self.image = self.frames[self.state][int(
                self.frame_index) % len(self.frames[self.state])]

    def update(self, dt):
        self.input()
        self.move(dt)
        self.animate(dt)
