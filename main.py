import pygame
import sys
from pygame.locals import *
import json
from sounds import SoundManager
from input_manager import InputManager, Actions
import screens, menu

from game_instance import GameInstance

TILESIZE = 10
FPS = 60
BLOCKSIZE = 5
SETTINGS_FILE = "settings.cfg"

config_handle = open(SETTINGS_FILE, "r")
config = json.load(config_handle)
config_handle.close()

pygame.init()
pygame.display.set_caption(config["title"])
pygame.mixer.init(frequency=44100, size=-16, channels=2, buffer=4096)
surface = pygame.display.set_mode((config["width"], config["height"]))
game = GameInstance(config, "first")
clock = pygame.time.Clock()
input_manager = InputManager()

screens = {
    "pause":screens.PauseScreen(config),
    "inventory":menu.InventoryMenu(config),
    "complete":screens.CompleteScreen(config),
    "gameover":screens.GameOverScreen(config)
}

main_menu = menu.MainMenu(config, enabled=True)

while True:
    events = input_manager.get_active_events()

    #user closes the game
    if Actions.QUIT in events:
        pygame.quit()
        sys.exit()
    elif Actions.START_GAME in events:
        break

    clock.tick(config["fps"])
    delta = clock.get_time() / 1000.0

    main_menu.doFrame(surface, delta, events)
    pygame.display.update()

paused = False

while True:
    events = input_manager.get_active_events()

    #user closes the game
    if Actions.QUIT in events:
        pygame.quit()
        sys.exit()
    elif Actions.GAME_WON in events:
        paused = True
        screens["complete"].enabled = True
    elif Actions.GAME_OVER in events:
        paused = True
        screens["gameover"].enabled = True
    #toggle relevent ui screens
    elif Actions.TOGGLE_PAUSE in events:
        paused = not paused
        screens["pause"].enabled = not screens["pause"].enabled
    elif Actions.TOGGLE_INVENTORY in events:
        paused = not paused
        screens["pause"].enabled = not screens["pause"].enabled
        screens["inventory"].enabled = not screens["inventory"].enabled

    clock.tick(config["fps"])
    delta = clock.get_time() / 1000.0

    #render the game field, a delta of 0 means don't do any physics updates, events of [] means dont perform any inputs
    if paused:
        game.doFrame(surface, 0, [])
    else:
        game.doFrame(surface, delta, events)

    #display any active ui screens
    for screen in screens.itervalues():
        screen.doFrame(surface, delta, events)

    #give it to the user
    pygame.display.update()
