import pygame
import random
import math

from physics_manager import PhysicsAttributes
from collisions import ImpactSide
from input_manager import CustomEvents
from sound_manager import SoundEffect

class Actor(object):

    DISSOLVE_DURATION_SECONDS = 1

    def __init__(self, surface, width_tiles, height_tiles, weight=3, collidable=True):
        self.physical = PhysicsAttributes(width=width_tiles, height=height_tiles, weight=weight, collidable=collidable)

        self._tile_size = None
        self.surface = None
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
    def __init__(self, surface, width_tiles, height_tiles, weight, collidable):
        Actor.__init__(self, surface, width_tiles, height_tiles, weight, collidable)

class AnimatedActor(Actor):
    def __init__(self, left_surface, right_surface, width_tiles, height_tiles, weight, collidable):
        assert left_surface.get_size() == right_surface.get_size()
        Actor.__init__(self, right_surface, width_tiles, height_tiles, weight, collidable)
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

        velocity = self.physical.velocity[0]
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

    def __init__(self, left_surface, right_surface, width_tiles, height_tiles, weight, collidable):
        self.sounds = {Player.RUN: None, Player.JUMP: None}
        AnimatedActor.__init__(self, left_surface, right_surface, width_tiles, height_tiles, weight, collidable)
        self.name ="player"

    def update(self, delta, tile_size):
        if isinstance(self.physical.received_impacts.get(ImpactSide.TOP, None), Block):
            self.die()
        AnimatedActor.update(self, delta, tile_size)

        if self.physical.velocity[0] != 0:
            self.sounds[Player.RUN] = SoundEffect.Run
        else:
            self.sounds[Player.RUN] = None
        if self.physical.velocity[1] < 0:
            self.sounds[Player.JUMP] = SoundEffect.Jump
        else:
            self.sounds[Player.JUMP] = None

    def die(self):
        pygame.event.post(pygame.event.Event(CustomEvents.PLAYERDEAD))

    @staticmethod
    def genMainCharacter():
        return Player(pygame.image.load(Player.MAIN_CHARACTER[0]), pygame.image.load(Player.MAIN_CHARACTER[1]), Player.MAIN_CHARACTER[2], Player.MAIN_CHARACTER[3], 3, True)


class Enemy(AnimatedActor):
    ROCKY = ("characters/rocky.png", 4, 4)
    SPIKEY = ("characters/spikey.png", 5, 4)

    def __init__(self, left_surface, right_surface, width_tiles, height_tiles, weight, collidable):
        self.ai_knowledge = {'speed':1}
        AnimatedActor.__init__(self, left_surface, right_surface, width_tiles, height_tiles, weight, collidable)

    def update(self, delta, tile_size):
        AnimatedActor.update(self, delta, tile_size)

        #kill self if hit on the head by a block
        #also kill self if it hits the floor
        if isinstance(self.physical.received_impacts.get(ImpactSide.TOP, None), Block):
            self.crush()

    def crush(self):
        self.dissolved = True

    @staticmethod
    def generate(model):
        if model == "rocky":
            left = pygame.image.load(Enemy.ROCKY[0])
            right = pygame.transform.flip(left, True, False)
            enemy = Enemy(left, right, Enemy.ROCKY[1], Enemy.ROCKY[2], 3, True)
            enemy.points_per_tile = 10
            return enemy
        elif model == "spikey":
            left = pygame.image.load(Enemy.SPIKEY[0])
            right = pygame.transform.flip(left, True, False)
            enemy = Enemy(left, right, Enemy.SPIKEY[1], Enemy.SPIKEY[2], 3, True)
            enemy.points_per_tile = 10
            return enemy
