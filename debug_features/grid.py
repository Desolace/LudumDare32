import pygame
from drawable import Drawable

class DebugGrid(Drawable):
    def __init__(self, width_tiles, height_tiles):
        self._width_tiles, self._height_tiles = width_tiles, height_tiles
        self._base = pygame.Surface((width_tiles, height_tiles)).convert_alpha()
        current_grid_color = (0, 0, 0, 100)
        other_grid_color = (0, 0, 0, 0)

        for x in range(width_tiles):
            for y in range(height_tiles):
                self._base.set_at((x, y), current_grid_color)
                current_grid_color, other_grid_color = other_grid_color, current_grid_color
            current_grid_color, other_grid_color = other_grid_color, current_grid_color

        self.surface = self._base.copy()
        self.position = (0,0)
        self.should_reposition = True

    def rescale(self, tile_size):
        self.surface = pygame.transform.scale(self._base, (tile_size * self._width_tiles, tile_size * self._height_tiles))
