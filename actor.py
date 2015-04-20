import pygame
import random
import math

from collisions import ImpactSide

class Actor(object):
    MAIN_CHARACTER = ("characters/guy1.png",4, 8)

    _hash = None
    surface = None
    widthInTiles, heightInTiles = None, None
    position = (0,0)
    _tile_size = None
    DISSOLVE_DURATION_SECONDS = 1

    def __init__(self, surface, wTiles, hTiles):
        self._baseSurface = surface
        self._baseSurface.set_colorkey((1,1,1))
        self._hash = hash(self._baseSurface)
        self.widthInTiles = wTiles
        self.heightInTiles = hTiles
        self.points_per_tile = 0
        self._is_dissolving = False
        self.dissolved = False

    def start_dissolving(self):
        if not self._is_dissolving:
            self._is_dissolving = True
            self.tiles_to_dissolve = []

            for i in range(0, self.widthInTiles):
                for j in range(0, self.heightInTiles):
                    self.tiles_to_dissolve.append((i, j))

            self.total_tile_count = len(self.tiles_to_dissolve)

    @staticmethod
    def genMainCharacter():
        return Actor(pygame.image.load(Actor.MAIN_CHARACTER[0]), Actor.MAIN_CHARACTER[1], Actor.MAIN_CHARACTER[2])

    def update(self, delta, tile_size):
        if tile_size != self._tile_size:
            self.surface = pygame.transform.smoothscale(self._baseSurface, (self.widthInTiles*tile_size, self.heightInTiles*tile_size))
            self._tile_size = tile_size

        if self._is_dissolving:
            if len(self.tiles_to_dissolve) > 0:
                percent_to_dissolve = delta / Actor.DISSOLVE_DURATION_SECONDS
                num_tiles_to_dissolve = min(int(math.ceil(self.total_tile_count * percent_to_dissolve)), len(self.tiles_to_dissolve))

                to_dissolve = random.sample(self.tiles_to_dissolve, num_tiles_to_dissolve)
                for tile in to_dissolve:
                    self.tiles_to_dissolve.remove(tile)
                    self.surface.fill((1,1,1), pygame.Rect(tile[0] * tile_size, tile[1] * tile_size, tile_size, tile_size))
            else:
                self._is_dissolving = False
                self.dissolved = True


    def __hash__(self):
        return self._hash

    def __eq__(self, other):
        return hash(self) == hash(other)

    def get_rect(self):
        surf_rect = self.surface.get_rect()
        return surf_rect.move(*self.position)

class Block(Actor):
    def __init__(self, surface, wTiles, hTiles):
        Actor.__init__(self, surface, wTiles, hTiles)

LEFT, RIGHT = -1, 1
ENEMY_SPEED = 1

class Enemy(Actor):
    def __init__(self, surface, wTiles, hTiles, physics_manager):
        self.physics_manager = physics_manager
        self._horizontal_direction = LEFT
        Actor.__init__(self, surface, wTiles, hTiles)

    def update(self, delta, tile_size):
        Actor.update(self, delta, tile_size)

        if self._horizontal_direction == LEFT:
            rect = self.get_rect()
            floor_tile_filled = self.physics_manager.is_space_filled(pygame.Rect((rect.bottomleft[0] / tile_size) - 1, (rect.bottomleft[1] / tile_size) + 1, 1, 1))
            #mvmnt_space_filled = self.physics_manager.is_space_filled(pygame.Rect((rect.topleft[0] / tile_size) - 1, (rect.topleft[1] / tile_size), 1, 1))
            if not floor_tile_filled or self.physics_manager.was_collided(self, ImpactSide.LEFT) is not None:
                self.physics_manager.set_velocity_x(self, 0)
                self._horizontal_direction = RIGHT
            else:
                self.physics_manager.set_velocity_x(self, LEFT * ENEMY_SPEED)
        elif self._horizontal_direction == RIGHT:
            rect = self.get_rect()
            floor_tile_filled = self.physics_manager.is_space_filled(pygame.Rect((rect.bottomright[0] / tile_size) + 1, (rect.bottomright[1] / tile_size) + 1, 1, 1))
            #mvmnt_space_filled = self.physics_manager.is_space_filled(pygame.Rect((rect.topright[0] / tile_size), (rect.topright[1] / tile_size), 1, 1))
            if not floor_tile_filled or self.physics_manager.was_collided(self, ImpactSide.RIGHT) is not None:
                self.physics_manager.set_velocity_x(self, 0)
                self._horizontal_direction = LEFT
            else:
                self.physics_manager.set_velocity_x(self, RIGHT * ENEMY_SPEED)

        #kill self if hit on the head by a block
        top_collider = self.physics_manager.was_collided(self, ImpactSide.TOP)
        print top_collider
        if top_collider is not None and isinstance(top_collider, Block):
            self.crush()

    def crush(self):
        self.dissolved = True

    @staticmethod
    def generate(model, physics_manager):
        if model == "basic":
            enemy = Enemy(pygame.image.load(Actor.MAIN_CHARACTER[0]), Actor.MAIN_CHARACTER[1], Actor.MAIN_CHARACTER[2], physics_manager)
            enemy.points_per_tile = 10
            return enemy
