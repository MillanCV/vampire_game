import pygame

from random import randint

from pytmx.util_pygame import load_pygame

from settings import (
    WINDOW_HEIGHT,
    WINDOW_WIDTH,
    TILE_SIZE
)

from Player import Player
from CollisionSprite import (Gun, Sprit e, CollisionSprite, Bullet)
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
        self.load_images()

        # groups
        self.all_sprites = AllSprites()
        self.collision_sprites = pygame.sprite.Group()
        self.bullet_sprites = pygame.sprite.Group()

        self.setup()

        # gun timer
        self.can_shoot = True
        self.shoot_time = 0
        self.shoot_cooldown = 500

        # enemy timer
        self.enemy_event = pygame.event.custom_type()
        pygame.time.set_timer(self.enemy_event, 300)
        self.spawn_positions = []

    def load_images(self):
        self.bullet_surf = pygame.image.load(
            'assets/images/gun/bullet.png').convert_alpha()

    def gun_timer(self):
        if not self.can_shoot:
            current_time = pygame.time.get_ticks()
            if current_time - self.shoot_time >= self.shoot_cooldown:
                self.can_shoot = True

        # sprites
    def input(self):
        if pygame.mouse.get_pressed()[0] and self.can_shoot:
            pos = self.gun.rect.center + self.gun.player_direction * 50
            Bullet(self.bullet_surf, pos, self.gun.player_direction,
                   (self.all_sprites, self.bullet_sprites))
            self.can_shoot = False
            self.shoot_time = pygame.time.get_ticks()

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
                self.gun = Gun(self.player, self.all_sprites)

    def run(self):
        while self.running:
            delta_time = self.clock.tick() / 1000

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False

            # update
            self.gun_timer()
            self.input()
            self.all_sprites.update(delta_time)

            # draw
            self.display_surface.fill('darkgrey')
            self.all_sprites.draw(self.player.rect.center)
            pygame.display.update()

        pygame.quit()
