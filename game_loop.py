import pygame
from pygame.locals import *
from input_manager import InputManager, Actions
import screens, menu

from game_instance import GameInstance
from ui_overlay import UIOverlay, TextElement

class Game(object):
    def __init__(self, config):
        self.max_fps = config.get("max_fps", 60)

        pygame.init()
        pygame.display.set_caption(config["title"])
        pygame.mixer.init(frequency=44100, size=-16, channels=2, buffer=4096)
        self.display = pygame.display.set_mode((config["width"], config["height"]))
        self.game_instance = GameInstance(config, "first")
        self.clock = pygame.time.Clock()
        self.input_manager = InputManager()
        self.ui_overlay = UIOverlay(config["font_file"])
        self.ui_overlay.text_elements["framerate"] = TextElement((20, 50), 20, (0, 0, 0), "0 fps")

        self.screens = {
            "pause":screens.PauseScreen(config),
            "inventory":menu.InventoryMenu(config),
            "complete":screens.CompleteScreen(config),
            "gameover":screens.GameOverScreen(config)
        }

        self.main_menu = menu.MainMenu(config, enabled=True)
        self.paused = False
        self.show_fps = config.get("show_fps", False)
        self.run_loop = self.debug_loop
        self.is_running = True

    def debug_loop(self):
        events = self.input_manager.get_active_events()

        #user closes the game
        if Actions.QUIT in events:
            pygame.quit()
            self.is_running = False
            return
        elif Actions.START_GAME in events:
            self.run_loop = self.in_game_loop

        delta = self.clock.tick(self.max_fps) / 1000.0

        self.main_menu.doFrame(self.display, delta, events)
        pygame.display.update()

    def in_game_loop(self):
        events = self.input_manager.get_active_events()

        #user closes the game
        if Actions.QUIT in events:
            pygame.quit()
            self.is_running = False
            return
        elif Actions.GAME_WON in events:
            self.paused = True
            self.screens["complete"].enabled = True
        elif Actions.GAME_OVER in events:
            self.paused = True
            self.screens["gameover"].enabled = True
        #toggle relevent ui screens
        elif Actions.TOGGLE_PAUSE in events:
            self.paused = not self.paused
            self.screens["pause"].enabled = not self.screens["pause"].enabled
        elif Actions.TOGGLE_INVENTORY in events:
            self.paused = not self.paused
            self.screens["pause"].enabled = not self.screens["pause"].enabled
            self.screens["inventory"].enabled = not self.screens["inventory"].enabled
        elif Actions.TOGGLE_SHOW_FPS in events:
            self.show_fps = not self.show_fps

        delta = self.clock.tick(self.max_fps) / 1000.0
        if self.show_fps:
            self.ui_overlay.text_elements["framerate"].value = "{0} fps".format(int(self.clock.get_fps()))
        else:
            self.ui_overlay.text_elements["framerate"].value = ""
        self.ui_overlay.update(delta)

        #render the game field, a delta of 0 means don't do any physics updates, events of [] means dont perform any inputs
        if self.paused:
            self.game_instance.doFrame(self.display, 0, [])
        else:
            self.game_instance.doFrame(self.display, delta, events)

        #display any active ui screens
        for screen in self.screens.values():
            screen.doFrame(self.display, delta, events)

        #render the app-scope UI
        for (label, position, _) in self.ui_overlay.get_drawables():
            self.display.blit(label, position)

        #give it to the user
        pygame.display.update()
