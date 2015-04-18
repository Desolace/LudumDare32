import pygame
from pygame.locals import *
from custom_exceptions import *

from level import Level
from character import Character
from input_manager import InputManager, Actions
from physics_manager import PhysicsManager

class GameInstance(object):
    def __init__(self, config, levelName):
        self.config = config
        self.input_manager = InputManager()
        self.level = Level("{0}/{1}.lvl".format(config["levels_dir"], levelName))

        self.main_char = Character.genMainCharacter()
        otherChar = Character.genMainCharacter()

        self.characters = [self.main_char, otherChar]
        self.physics_manager = PhysicsManager(self.level.width, self.level.height)
        self.physics_manager.add_actor(self.main_char, has_gravity=True)
        self.physics_manager.add_actor(otherChar, has_gravity=True)
        self.physics_manager.set_position(otherChar, (20, 5))

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

        self.physics_manager.update(delta, tile_size)

        for character in self.characters:
            character.update(delta, tile_size)

        self.level.update(tile_size)

        screen.blit(self.level.surface, (0,0))
        for character in self.characters:
            screen.blit(character.surface, character.position)
