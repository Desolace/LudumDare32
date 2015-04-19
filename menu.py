import pygame
from material_manager import MaterialManager

class InventoryMenu(object):
    def __init__(self, config):
        self.enabled = False
        self.material_manager = MaterialManager(config["material_file"])

    def doFrame(self, screen, delta, events):
        if self.enabled:
            surface = pygame.Surface((screen.get_width() / 2, screen.get_height() / 2))
            surface.fill((255, 0, 0))
            surface.set_alpha(200)

            dirt = self.material_manager.get_material("dirt", (50,50))
            surface.blit(dirt.surface, (10, 10))

            stone = self.material_manager.get_material("stone", (50,50))
            surface.blit(stone.surface, (70, 10))

            screen.blit(surface, ((screen.get_width() / 4), (screen.get_height() / 4)))
