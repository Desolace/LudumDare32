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

class InputManager(object):
    def __init__(self):
        pass

    def eventQueue(self):
        for event in pygame.event.get():
            #User quits
            if event.type == QUIT or (event.type == KEYDOWN and (event.key == K_q or event.key == K_ESCAPE)):
                yield Actions.QUIT

            elif event.type == KEYDOWN:
                if event.key == K_UP:
                    yield Actions.START_USER_UP
                elif event.key == K_DOWN:
                    yield Actions.START_USER_DOWN
                elif event.key == K_LEFT:
                    yield Actions.START_USER_LEFT
                elif event.key == K_RIGHT:
                    yield Actions.START_USER_RIGHT
                elif event.key == K_LCTRL or event.key == K_RCTRL:
                    yield Actions.START_DISSOLVE_SELECTION

            elif event.type == KEYUP:
                if event.key == K_UP:
                    yield Actions.STOP_USER_UP
                elif event.key == K_DOWN:
                    yield Actions.STOP_USER_DOWN
                elif event.key == K_LEFT:
                    yield Actions.STOP_USER_LEFT
                elif event.key == K_RIGHT:
                    yield Actions.STOP_USER_RIGHT
                elif event.key == K_LCTRL or event.key == K_RCTRL:
                    yield Actions.STOP_DISSOLVE_SELECTION

            elif event.type == MOUSEBUTTONDOWN:
                if event.button == 1:
                    self.last_click_position = event.pos
                    if not (pygame.key.get_mods() & KMOD_CTRL):
                        yield Actions.START_BLOW_SELECTION
            elif event.type == MOUSEBUTTONUP:
                if event.button == 1: #left click
                    self.last_click_position = event.pos
                    if pygame.key.get_mods() & KMOD_CTRL:
                        yield Actions.USER_SUCK
                    else:
                        yield Actions.STOP_BLOW_SELECTION

            elif event.type == USEREVENT:
                self.last_user_selection = event.bounds
                yield Actions.USER_BLOW
