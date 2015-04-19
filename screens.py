import pygame

PAUSE_COLOR = (0,0,0)
PAUSE_ALPHA = 150

class PauseScreen(object):
    def doFrame(self, screen, delta, events):
        surface = pygame.Surface(screen.get_size())
        surface.fill(PAUSE_COLOR)
        surface.set_alpha(PAUSE_ALPHA)
        screen.blit(surface, (0,0))
