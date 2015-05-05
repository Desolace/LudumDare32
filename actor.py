import pygame
import random
import math

from physics_manager import PhysicsManager
from collisions import ImpactSide
from input_manager import CustomEvents
from sound_manager import SoundEffect

class Actor(object):
    _hash = None
    surface = None
    widthInTiles, heightInTiles = None, None
    position = (0,0)
    _tile_size = None
    DISSOLVE_DURATION_SECONDS = 1

    def __init__(self, surface, width_tiles, height_tiles):
        self._base_surface = surface
        self._base_surface.set_colorkey((1,1,1))
        self._hash = hash(self._base_surface)
        self.widthInTiles = width_tiles
        self.heightInTiles = height_tiles
        self.points_per_tile = 0
        self._is_dissolving = False
        self.dissolved = False
        self.dissolvable = False

    def start_dissolving(self):
        if not self._is_dissolving:
            self._is_dissolving = True
            self.tiles_to_dissolve = []

            for i in range(0, self.widthInTiles):
                for j in range(0, self.heightInTiles):
                    self.tiles_to_dissolve.append((i, j))

            self.total_tile_count = len(self.tiles_to_dissolve)

    def update(self, delta, tile_size):
        if tile_size != self._tile_size:
            self.surface = pygame.transform.smoothscale(self._base_surface, (int(self.widthInTiles*tile_size), int(self.heightInTiles*tile_size)))
            self._tile_size = tile_size
        if self._is_dissolving:
            if len(self.tiles_to_dissolve) > 0:
                percent_to_dissolve = delta / Actor.DISSOLVE_DURATION_SECONDS
                num_tiles_to_dissolve = min(int(math.ceil(self.total_tile_count * percent_to_dissolve)), len(self.tiles_to_dissolve))

                to_dissolve = random.sample(self.tiles_to_dissolve, num_tiles_to_dissolve)
                for tile in to_dissolve:
                    self.tiles_to_dissolve.remove(tile)
                    self.surface.fill((1,1,1,0), pygame.Rect(tile[0] * tile_size, tile[1] * tile_size, tile_size, tile_size))
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
    def __init__(self, surface, width_tiles, height_tiles):
        Actor.__init__(self, surface, width_tiles, height_tiles)

class AnimatedActor(Actor):
    def __init__(self, left_surface, right_surface, width_tiles, height_tiles, physics_manager):
        assert left_surface.get_size() == right_surface.get_size()
        Actor.__init__(self, right_surface, width_tiles, height_tiles)
        self._base_left_surface = left_surface
        self._base_right_surface = right_surface

    def update(self, delta, tile_size):
        if tile_size != self._tile_size:
            size = (int(self.widthInTiles*tile_size), int(self.heightInTiles*tile_size))
            self._left_surface = pygame.transform.smoothscale(self._base_left_surface, size)
            self._right_surface = pygame.transform.smoothscale(self._base_right_surface, size)
            self._tile_size = tile_size

        previous_surface = self.surface
        self.surface = self._left_surface
        Actor.update(self, delta, tile_size)
        self.surface = self._right_surface
        Actor.update(self, delta, tile_size)

        velocity = self.physics_manager.get_velocity_x(self)
        if velocity > 0: #going right
            self.surface = self._right_surface
        elif velocity < 0: #going left
            self.surface = self._left_surface
        elif previous_surface is not None:
            self.surface = previous_surface
        else:
            self.surface = self._right_surface

class Player(AnimatedActor):
    MAIN_CHARACTER = ("characters/guyL.png", "characters/guyR.png", 4, 8)
    RUN = 'player_run'
    JUMP = 'player_jump'

    def __init__(self, left_surface, right_surface, width_tiles, height_tiles, physics_manager, sound_manager):
        self.physics_manager = physics_manager
        self.sound_manager = sound_manager
        AnimatedActor.__init__(self, left_surface, right_surface, width_tiles, height_tiles, physics_manager)

    def update(self, delta, tile_size):
        if isinstance(self.physics_manager.received_impact(self, ImpactSide.TOP), Block):
            self.die()
        AnimatedActor.update(self, delta, tile_size)

        if self.sound_manager is not None: #play needed sounds
            if self.physics_manager.get_velocity_x(self) != 0:
                self.sound_manager.enable_sound(Player.RUN, SoundEffect.Run)
            else:
                self.sound_manager.disable_sound(Player.RUN)
            if self.physics_manager.get_velocity_y(self) < 0:
                self.sound_manager.enable_sound(Player.JUMP, SoundEffect.Jump)
            else:
                self.sound_manager.disable_sound(Player.JUMP)

    def die(self):
        pygame.event.post(pygame.event.Event(CustomEvents.PLAYERDEAD))

    @staticmethod
    def genMainCharacter(physics_manager, sound_manager):
        return Player(pygame.image.load(Player.MAIN_CHARACTER[0]), pygame.image.load(Player.MAIN_CHARACTER[1]), Player.MAIN_CHARACTER[2], Player.MAIN_CHARACTER[3], physics_manager, sound_manager)

LEFT, RIGHT = -1, 1
ENEMY_SPEED = 1

class Enemy(AnimatedActor):
    ROCKY = ("characters/rocky.png", 4, 4)
    SPIKEY = ("characters/spikey.png", 5, 4)

    def __init__(self, left_surface, right_surface, width_tiles, height_tiles, physics_manager):
        self.physics_manager = physics_manager
        self._horizontal_direction = LEFT
        AnimatedActor.__init__(self, left_surface, right_surface, width_tiles, height_tiles, physics_manager)

    def update(self, delta, tile_size):
        AnimatedActor.update(self, delta, tile_size)

        if self._horizontal_direction == LEFT:
            rect = self.get_rect()
            floor_tile_filled = self.physics_manager.is_space_filled(pygame.Rect((rect.bottomleft[0] / tile_size) - 1, (rect.bottomleft[1] / tile_size), 1, 1))
            if not floor_tile_filled or self.physics_manager.gave_impact(self, ImpactSide.LEFT) is not None or self.physics_manager.received_impact(self, ImpactSide.LEFT) is not None:
                self.physics_manager.set_velocity_x(self, 0)
                self._horizontal_direction = RIGHT
            else:
                self.physics_manager.set_velocity_x(self, LEFT * ENEMY_SPEED)
        elif self._horizontal_direction == RIGHT:
            rect = self.get_rect()
            floor_tile_filled = self.physics_manager.is_space_filled(pygame.Rect((rect.bottomright[0] / tile_size) + 1, (rect.bottomright[1] / tile_size), 1, 1))
            if not floor_tile_filled or self.physics_manager.gave_impact(self, ImpactSide.RIGHT) is not None or self.physics_manager.received_impact(self, ImpactSide.RIGHT) is not None:
                self.physics_manager.set_velocity_x(self, 0)
                self._horizontal_direction = LEFT
            else:
                self.physics_manager.set_velocity_x(self, RIGHT * ENEMY_SPEED)

        #kill self if hit on the head by a block
        #also kill self if it hits the floor
        if isinstance(self.physics_manager.received_impact(self, ImpactSide.TOP), Block):
            self.crush()

    def crush(self):
        self.dissolved = True

    @staticmethod
    def generate(model, physics_manager):
        if model == "rocky":
            left = pygame.image.load(Enemy.ROCKY[0])
            right = pygame.transform.flip(left, True, False)
            enemy = Enemy(left, right, Enemy.ROCKY[1], Enemy.ROCKY[2], physics_manager)
            enemy.points_per_tile = 10
            return enemy
        elif model == "spikey":
            left = pygame.image.load(Enemy.SPIKEY[0])
            right = pygame.transform.flip(left, True, False)
            enemy = Enemy(left, right, Enemy.SPIKEY[1], Enemy.SPIKEY[2], physics_manager)
            enemy.points_per_tile = 10
            return enemy
