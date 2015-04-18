import pygame
import random
import math

class Actor(object):
    MAIN_CHARACTER = ("characters/dumb.jpg", 5, 6)

    _hash = None
    surface = None
    widthInTiles, heightInTiles = None, None
    position = (0,0)
    _tileSize = None
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

    def update(self, delta, tileSize):
        if tileSize != self._tileSize:
            self.surface = pygame.transform.smoothscale(self._baseSurface, (self.widthInTiles*tileSize, self.heightInTiles*tileSize))
            self._tileSize = tileSize

        if self._is_dissolving:
            if len(self.tiles_to_dissolve) > 0:
                percent_to_dissolve = delta / Actor.DISSOLVE_DURATION_SECONDS
                num_tiles_to_dissolve = int(math.ceil(self.total_tile_count * percent_to_dissolve))

                to_dissolve = random.sample(self.tiles_to_dissolve, num_tiles_to_dissolve)
                for tile in to_dissolve:
                    self.tiles_to_dissolve.remove(tile)
                    self.surface.fill((1,1,1), pygame.Rect(tile[0] * tileSize, tile[1] * tileSize, tileSize, tileSize))
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
