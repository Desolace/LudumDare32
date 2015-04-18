import pygame

class Actor(object):
    MAIN_CHARACTER = ("characters/dumb.jpg", 5, 6)

    _hash = None
    surface = None
    widthInTiles, heightInTiles = None, None
    position = (0,0)
    _tileSize = None

    def __init__(self, surface, wTiles, hTiles):
        self._baseSurface = surface
        self._hash = hash(self._baseSurface)
        self.widthInTiles = wTiles
        self.heightInTiles = hTiles

    @staticmethod
    def genMainCharacter():
        return Actor(pygame.image.load(Actor.MAIN_CHARACTER[0]), Actor.MAIN_CHARACTER[1], Actor.MAIN_CHARACTER[2])

    def update(self, delta, tileSize):
        if tileSize != self._tileSize:
            self.surface = pygame.transform.smoothscale(self._baseSurface, (self.widthInTiles*tileSize, self.heightInTiles*tileSize))
            self._tileSize = tileSize

    def __hash__(self):
        return self._hash

    def __eq__(self, other):
        return hash(self) == hash(other)
