import pygame
from pygame.locals import *
from custom_exceptions import *

from level import Level
from actor import Actor
from input_manager import InputManager, Actions
from physics_manager import PhysicsManager

class GameInstance(object):
    def __init__(self, config, level_name):
        self.config = config
        self.input_manager = InputManager()
        self.physics_manager = PhysicsManager()
        self.level = Level("{0}/{1}.lvl".format(config["levels_dir"], level_name), self.physics_manager)

        self.main_char = Actor.genMainCharacter()

        self.physics_manager.add_actor(self.main_char, weight=3)

    def _handle_dissolving(self, position):
        for actor in self.level.actors:
            if actor.get_rect().collidepoint(position):
                actor.start_dissolving()

    def doFrame(self, screen, delta):
        tile_size = screen.get_width() / self.level.width

        for event in self.input_manager.eventQueue():
            if event == Actions.QUIT:
                raise UserQuitException()
            elif event == Actions.START_USER_LEFT:
                self.physics_manager.add_velocity_x(self.main_char, -self.config["user_motion_speed"])
            elif event == Actions.START_USER_RIGHT:
                self.physics_manager.add_velocity_x(self.main_char, self.config["user_motion_speed"])
            elif event == Actions.START_USER_UP:
                if self.physics_manager.get_velocity_y(self.main_char) == 0:
                    self.physics_manager.add_velocity_y(self.main_char, -self.config["user_jump_speed"])
            elif event == Actions.STOP_USER_LEFT:
                self.physics_manager.add_velocity_x(self.main_char, self.config["user_motion_speed"])
            elif event == Actions.STOP_USER_RIGHT:
                self.physics_manager.add_velocity_x(self.main_char, -self.config["user_motion_speed"])
            elif event == Actions.STOP_USER_CLICK:
                self._handle_dissolving(self.input_manager.last_click_position)

        self.physics_manager.update(delta, tile_size)

        self.main_char.update(delta, tile_size)
        for actor in self.level.actors:
            actor.update(delta, tile_size)

        self.level.update(tile_size)

        screen.blit(self.level.surface, (0,0))
        screen.blit(self.main_char.surface, self.main_char.position)
        for actor in self.level.actors:
            screen.blit(actor.surface, actor.position)
