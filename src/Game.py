import pygame

from random import randint

from pytmx.util_pygame import load_pygame

from settings import (
    WINDOW_HEIGHT,
    WINDOW_WIDTH,
    TILE_SIZE
)

from Player import Player
from CollisionSprite import Sprite, CollisionSprite
from groups import AllSprites


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
        self.all_sprites = AllSprites()
        self.collision_sprites = pygame.sprite.Group()

        self.setup()

        # sprites

    def setup(self):
        map = load_pygame('./assets/data/maps/world.tmx')

        for x, y, image in map.get_layer_by_name('Ground').tiles():
            Sprite(
                (x * TILE_SIZE, y * TILE_SIZE), image, self.all_sprites
            )

        for obj in map.get_layer_by_name('Objects'):
            CollisionSprite(
                (obj.x, obj.y), obj.image, (self.all_sprites, self.collision_sprites)
            )

        for obj in map.get_layer_by_name('Collisions'):
            CollisionSprite(
                (obj.x, obj.y),
                pygame.Surface(
                    (obj.width, obj.height)),
                self.collision_sprites
            )

        for obj in map.get_layer_by_name('Entities'):
            if obj.name == 'Player':
                self.player = Player(
                    (obj.x, obj.y), self.all_sprites, self.collision_sprites)

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
            self.all_sprites.draw(self.player.rect.center)
            pygame.display.update()

        pygame.quit()
