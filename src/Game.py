import pygame

from random import randint

from settings import (
    WINDOW_HEIGHT,
    WINDOW_WIDTH
)

from Player import Player
from CollisionSprite import CollisionSprite


class Game:
    def __init__(self):
        # setup
        pygame.init()
        self.display_surface = pygame.display.set_mode(
            (WINDOW_WIDTH, WINDOW_HEIGHT))
        pygame.display.set_caption("Ollo o piollo")
        self.clock = pygame.time.Clock()
        self.running = True

        # groups
        self.all_sprites = pygame.sprite.Group()
        self.collision_sprites = pygame.sprite.Group()
        # sprites
        self.player = Player(self.all_sprites, self.collision_sprites)
        for i in range(6):
            x, y = randint(0, WINDOW_WIDTH), randint(0, WINDOW_HEIGHT)
            w, h = randint(60, 100), randint(50, 100)
            CollisionSprite(
                (x, y), (w, h), (self.all_sprites, self.collision_sprites)
            )

    def run(self):
        while self.running:
            delta_time = self.clock.tick() / 1000

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False

            # update
            self.all_sprites.update(delta_time)

            # draw
            self.display_surface.fill('darkgrey')
            self.all_sprites.draw(self.display_surface)
            pygame.display.update()

        pygame.quit()
