import pygame
from pygame.locals import *

class Actions(object):
    QUIT=0
    START_USER_LEFT=1
    START_USER_RIGHT=2
    START_USER_UP=3
    START_USER_DOWN=4
    STOP_USER_LEFT=5
    STOP_USER_RIGHT=6
    STOP_USER_UP=7
    STOP_USER_DOWN=8
    USER_SUCK=9
    START_BLOW_SELECTION=13
    STOP_BLOW_SELECTION=14
    USER_BLOW=10
    START_DISSOLVE_SELECTION=11
    STOP_DISSOLVE_SELECTION=12

    TOGGLE_SHOW_FPS=24
    TOGGLE_PAUSE=15
    TOGGLE_INVENTORY=16

    USER_MENU_CLICK=17

    CHOOSE_MATERIAL=18
    GAME_WON=19
    GAME_OVER=21
    START_GAME=20
    MUTE=22
    UNMUTE=23

    SHOW_CONSOLE=25

class CustomEvents:
    CHOOSEMAT=USEREVENT+1
    CLOSEINV=USEREVENT+2
    USERWINS=USEREVENT+3
    STARTBUTTONCLICK=USEREVENT+4
    PLAYERDEAD=USEREVENT+5

class InputManager(object):
    def __init__(self):
        self._paused = False
        self._in_game = False
        self._state = []

    def get_active_events(self):
        actions = []

        for event in pygame.event.get():
            """
            Global actions, can happen at any time
            """
            if event.type == QUIT or (event.type == KEYDOWN and (event.key == K_q or event.key == K_ESCAPE)):
                actions.append(Actions.QUIT)
            elif event.type == KEYDOWN and event.key == K_m:
                if Actions.MUTE in self._state:
                    self._state.remove(Actions.MUTE)
                    actions.append(Actions.UNMUTE)
                else:
                    self._state.append(Actions.MUTE)
                    actions.append(Actions.MUTE)
            elif event.type == KEYDOWN and event.key == K_f:
                actions.append(Actions.TOGGLE_SHOW_FPS)
            elif event.type == KEYDOWN and event.key == K_w:
                if pygame.key.get_mods() & KMOD_CTRL:
                    actions.append(Actions.SHOW_CONSOLE)
            elif self._in_game:
                """
                Game is in session
                User is playing the game
                """
                if not self._paused:
                    if event.type == CustomEvents.CHOOSEMAT:
                        actions.append((Actions.CHOOSE_MATERIAL, event.name))
                    elif event.type == CustomEvents.USERWINS:
                        actions.append((Actions.GAME_WON))

                    elif event.type == KEYDOWN:
                        if event.key == K_UP:
                            self._state.append(Actions.START_USER_UP)
                            actions.append(Actions.START_USER_UP)
                        elif event.key == K_DOWN:
                            self._state.append(Actions.START_USER_DOWN)
                            actions.append(Actions.START_USER_DOWN)
                        elif event.key == K_LEFT:
                            self._state.append(Actions.START_USER_LEFT)
                            actions.append(Actions.START_USER_LEFT)
                        elif event.key == K_RIGHT:
                            self._state.append(Actions.START_USER_RIGHT)
                            actions.append(Actions.START_USER_RIGHT)
                        elif event.key == K_LCTRL or event.key == K_RCTRL:
                            self._state.append(Actions.START_DISSOLVE_SELECTION)
                            actions.append(Actions.START_DISSOLVE_SELECTION)
                        elif event.key == K_i: #show inventory
                            self._state.append(Actions.TOGGLE_INVENTORY)
                            actions.append(Actions.TOGGLE_INVENTORY)
                            self._paused = True
                        elif event.key == K_p: #pause the game
                            self._state.append(Actions.TOGGLE_PAUSE)
                            actions.append(Actions.TOGGLE_PAUSE)
                            self._paused = True

                    elif event.type == KEYUP:
                        if event.key == K_UP:
                            if Actions.START_USER_UP in self._state:
                                self._state.remove(Actions.START_USER_UP)
                                actions.append(Actions.STOP_USER_UP)
                        elif event.key == K_DOWN:
                            if Actions.START_USER_DOWN in self._state:
                                self._state.remove(Actions.START_USER_DOWN)
                                actions.append(Actions.STOP_USER_DOWN)
                        elif event.key == K_LEFT:
                            if Actions.START_USER_LEFT in self._state:
                                self._state.remove(Actions.START_USER_LEFT)
                                actions.append(Actions.STOP_USER_LEFT)
                        elif event.key == K_RIGHT:
                            if Actions.START_USER_RIGHT in self._state:
                                self._state.remove(Actions.START_USER_RIGHT)
                                actions.append(Actions.STOP_USER_RIGHT)
                        elif event.key == K_LCTRL or event.key == K_RCTRL:
                            if Actions.START_DISSOLVE_SELECTION in self._state:
                                self._state.remove(Actions.START_DISSOLVE_SELECTION)
                                actions.append(Actions.STOP_DISSOLVE_SELECTION)

                    elif event.type == MOUSEBUTTONDOWN:
                        if event.button == 1:
                            if not (pygame.key.get_mods() & KMOD_CTRL):
                                self._state.append(Actions.START_BLOW_SELECTION)
                                actions.append((Actions.START_BLOW_SELECTION, event.pos))
                    elif event.type == MOUSEBUTTONUP:
                        if event.button == 1: #left click
                            if pygame.key.get_mods() & KMOD_CTRL:
                                if Actions.START_DISSOLVE_SELECTION in self._state:
                                    actions.append((Actions.USER_SUCK, event.pos))
                            else:
                                if Actions.START_BLOW_SELECTION in self._state:
                                    self._state.remove(Actions.START_BLOW_SELECTION)
                                    actions.append((Actions.STOP_BLOW_SELECTION, event.pos))
                    elif event.type == CustomEvents.PLAYERDEAD:
                        actions.append(Actions.GAME_OVER)

                    elif event.type == USEREVENT:
                        actions.append((Actions.USER_BLOW, event.bounds))
                elif self._paused:
                    """
                    Game is running, but is paused
                    """
                    if event.type == CustomEvents.CLOSEINV and Actions.TOGGLE_INVENTORY in self._state:
                        self._state.remove(Actions.TOGGLE_INVENTORY)
                        actions.append(Actions.TOGGLE_INVENTORY)
                        self._paused = False
                    if event.type == KEYDOWN:
                        if event.key == K_i and Actions.TOGGLE_INVENTORY in self._state:
                            self._state.remove(Actions.TOGGLE_INVENTORY)
                            actions.append(Actions.TOGGLE_INVENTORY)
                            self._paused = False
                        elif event.key == K_p and Actions.TOGGLE_PAUSE in self._state:
                            self._state.remove(Actions.TOGGLE_PAUSE)
                            actions.append(Actions.TOGGLE_PAUSE)
                            self._paused = False
                    elif event.type == MOUSEBUTTONUP:
                        if event.button == 1:
                            actions.append((Actions.USER_MENU_CLICK, event.pos))
            else:
                """
                Not in game, probably at a menu
                """
                if event.type == MOUSEBUTTONUP:
                    if event.button == 1:
                        actions.append((Actions.USER_MENU_CLICK, event.pos))
                elif event.type == CustomEvents.STARTBUTTONCLICK:
                    self._in_game = True
                    actions.append(Actions.START_GAME)
                elif event.type == KEYDOWN and event.key == K_SPACE:
                    self._in_game = True
                    actions.append(Actions.START_GAME)

        return actions
