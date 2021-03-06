import pygame

"""
Screens are statically rendered with no interactivity
"""

PAUSE_COLOR = (0,0,0)
PAUSE_ALPHA = 150

class PauseScreen(object):
    def __init__(self, config, enabled=False):
        self.enabled = enabled

    def doFrame(self, screen, delta, events):
        if self.enabled:
            surface = pygame.Surface(screen.get_size())
            surface.fill(PAUSE_COLOR)
            surface.set_alpha(PAUSE_ALPHA)
            screen.blit(surface, (0,0))

COMPLETE_COLOR = (0, 255, 0)
COMPLETE_ALPHA = 150

class CompleteScreen(object):
    def __init__(self, config, enabled=False):
        self.enabled = enabled

    def doFrame(self, screen, delta, events):
        if self.enabled:
            surface = pygame.Surface(screen.get_size())
            surface.fill(COMPLETE_COLOR)
            surface.set_alpha(COMPLETE_ALPHA)
            screen.blit(surface, (0,0))

GAME_OVER_COLOR = (0, 0, 0)
GAME_OVER_ALPHA = 150

class GameOverScreen(object):
    def __init__(self, config, enabled=False):
        self.enabled = enabled

    def doFrame(self, screen, delta, events):
        if self.enabled:
            surface = pygame.Surface(screen.get_size())
            surface.fill(GAME_OVER_COLOR)
            surface.set_alpha(GAME_OVER_ALPHA)
            screen.blit(surface, (0,0))
