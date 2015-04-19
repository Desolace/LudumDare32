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

    TOGGLE_PAUSE=15

class InputManager(object):
    def __init__(self):
        self._paused = False
        self._state = []

    def get_active_events(self):
        actions = []

        for event in pygame.event.get():
            #User quits
            if event.type == QUIT or (event.type == KEYDOWN and (event.key == K_q or event.key == K_ESCAPE)):
                actions.append(Actions.QUIT)
            elif event.type == KEYDOWN and event.key == K_p:
                self._paused = not self._paused
                actions.append(Actions.TOGGLE_PAUSE)
            elif not self._paused:
                if event.type == KEYDOWN:
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

                elif event.type == USEREVENT:
                    actions.append((Actions.USER_BLOW, event.bounds))

        return actions
