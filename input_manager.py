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
    STOP_USER_CLICK=9

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

            elif event.type == KEYUP:
                if event.key == K_UP:
                    yield Actions.STOP_USER_UP
                elif event.key == K_DOWN:
                    yield Actions.STOP_USER_DOWN
                elif event.key == K_LEFT:
                    yield Actions.STOP_USER_LEFT
                elif event.key == K_RIGHT:
                    yield Actions.STOP_USER_RIGHT

            elif event.type == MOUSEBUTTONUP:
                if event.button == 1:
                    self.last_click_position = event.pos
                    yield Actions.STOP_USER_CLICK
