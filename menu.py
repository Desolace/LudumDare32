import pygame

class InventoryMenu(object):
    def __init__(self):
        self.enabled = False

    def doFrame(self, screen, delta, events):
        if self.enabled:
            surface = pygame.Surface((screen.get_width() / 2, screen.get_height() / 2))
            surface.fill((255, 0, 0))
            surface.set_alpha(200)
            screen.blit(surface, ((screen.get_width() / 4), (screen.get_height() / 4)))
