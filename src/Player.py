import pygame

from settings import (
    WINDOW_HEIGHT,
    WINDOW_WIDTH
)


class Player(pygame.sprite.Sprite):
    def __init__(self, pos, group, collision_sprites):
        super().__init__(group)
        self.IMAGES = {
            "down": [pygame.image.load(f'assets/images/player/down/{i}.png').convert_alpha() for i in range(4)],
            "left": [pygame.image.load(f'assets/images/player/left/{i}.png').convert_alpha() for i in range(4)],
            "right": [pygame.image.load(f'assets/images/player/right/{i}.png').convert_alpha() for i in range(4)],
            "up": [pygame.image.load(f'assets/images/player/up/{i}.png').convert_alpha() for i in range(4)],
        }
        self.frames = self.IMAGES["down"]
        self.frame_index = 0
        self.image = self.IMAGES["down"][0]
        self.rect = self.IMAGES["down"][0].get_frect(
            center=pos)
        self.hitbox_rect = self.rect.inflate(-40, -30)

        self.direction = pygame.math.Vector2(0, 0)
        self.speed = 300
        self.collision_sprites = collision_sprites

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

    def update(self, dt):
        self.input()
        self.move(dt)
        self.frame_index += 4 * dt
        self.image = self.frames[int(self.frame_index) % len(self.frames)]
