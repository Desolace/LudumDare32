import pygame

PAUSE_COLOR = (0,0,0)
PAUSE_ALPHA = 150

class PauseScreen(object):
    def __init__(self):
        self.enabled = False

    def doFrame(self, screen, delta, events):
        if self.enabled:
            surface = pygame.Surface(screen.get_size())
            surface.fill(PAUSE_COLOR)
            surface.set_alpha(PAUSE_ALPHA)
            screen.blit(surface, (0,0))
