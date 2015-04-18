import pygame
import sys
from pygame.locals import *
from custom_exceptions import UserQuitException
import json
from sounds import SoundManager

from game_instance import GameInstance

TILESIZE = 10
FPS = 60
BLOCKSIZE = 5
SETTINGS_FILE = "settings.cfg"

config_handle = open(SETTINGS_FILE, "r")
config = json.load(config_handle)
config_handle.close()

try:
    pygame.init()
    pygame.display.set_caption(config["title"])
    pygame.mixer.init(frequency=44100, size=-16, channels=2, buffer=4096)
    surface = pygame.display.set_mode((config["width"], config["height"]))
    game = GameInstance(config, "first")
    clock = pygame.time.Clock()

    while True:
        clock.tick(config["fps"])
        delta = clock.get_time() / 1000.0
        game.doFrame(surface, delta)
        pygame.display.update()

except UserQuitException:
    pygame.quit()
    sys.exit()
