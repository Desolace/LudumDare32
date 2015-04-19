import pygame
from pygame.locals import *
from custom_exceptions import *

from level import Level
from actor import Actor
from input_manager import InputManager, Actions
from physics_manager import PhysicsManager
from picking_handler import PickingHandler
from sounds import SoundManager
from transmutation_manager import TransmutationManager
from material_manager import MaterialManager

class GameInstance(object):

    def __init__(self, config, level_name):
        self.config = config
        self.input_manager = InputManager()
        self.physics_manager = PhysicsManager()
        self.material_manager = MaterialManager(config["material_file"])
        self.transmutation_manager = TransmutationManager(self.material_manager)
        self.blow_key = "stone"
        self.picking_handler = PickingHandler(self.transmutation_manager)
        self.level = Level("{0}/{1}.lvl".format(config["levels_dir"], level_name), self.physics_manager, self.material_manager)

        self.main_char = Actor.genMainCharacter()

        self.physics_manager.add_actor(self.main_char, weight=3)
        self._highlight_actors = False
        self.userSounds = SoundManager()


    def _handle_events(self):
        for event in self.input_manager.eventQueue():
            if event == Actions.QUIT:
                raise UserQuitException()
            elif event == Actions.START_USER_LEFT:
                self.physics_manager.add_velocity_x(self.main_char, -self.config["user_motion_speed"])
                self.userSounds.start_cont_effect('run')
            elif event == Actions.START_USER_RIGHT:
                self.physics_manager.add_velocity_x(self.main_char, self.config["user_motion_speed"])
                self.userSounds.start_cont_effect('run')
            elif event == Actions.START_USER_UP:
                if self.physics_manager.get_velocity_y(self.main_char) == 0:
                    self.physics_manager.add_velocity_y(self.main_char, -self.config["user_jump_speed"])
                    self.userSounds.play_one_sound_effect('jump')
            elif event == Actions.STOP_USER_LEFT:
                self.physics_manager.add_velocity_x(self.main_char, self.config["user_motion_speed"])
                self.userSounds.stop_cont_effect('run')
            elif event == Actions.STOP_USER_RIGHT:
                self.physics_manager.add_velocity_x(self.main_char, -self.config["user_motion_speed"])
                self.userSounds.stop_cont_effect('run')
            elif event == Actions.USER_SUCK:
                [self.transmutation_manager.suck(actor) for actor in self.level.actors if self.picking_handler.is_picked(actor, self.input_manager.last_click_position)]
            elif event == Actions.USER_BLOW:
                (new_actor, tile_pos, weight) = self.transmutation_manager.blow(self.blow_key, self.input_manager.last_user_selection, self.tile_size)
                self.level.actors.append(new_actor)
                self.physics_manager.add_actor(new_actor, weight=weight)
                self.physics_manager.set_position(new_actor, tile_pos)
            elif event == Actions.START_BLOW_SELECTION:
                self.picking_handler.start_user_selection(self.input_manager.last_click_position, self.tile_size)
            elif event == Actions.STOP_BLOW_SELECTION:
                self.picking_handler.stop_user_selection()
            elif event == Actions.START_DISSOLVE_SELECTION:
                self._highlight_actors = True
            elif event == Actions.STOP_DISSOLVE_SELECTION:
                self._highlight_actors = False

    def _recalc_tilesize(self, screen):
        self.tile_size = screen.get_width() / self.level.width

    def _handle_updates(self, delta):
        self.physics_manager.update(delta, self.tile_size)
        self.picking_handler.update(delta, self.tile_size)
        self.transmutation_manager.update(delta)

        self.main_char.update(delta, self.tile_size)
        for actor in self.level.actors:
            actor.update(delta, self.tile_size)

        self.level.update(self.tile_size)

    def _render(self, screen):
        mouse_position = pygame.mouse.get_pos()
        screen.blit(self.level.surface, (0,0))
        screen.blit(self.main_char.surface, self.main_char.position)
        for actor in self.level.actors:
            screen.blit(actor.surface, actor.position)
            if self._highlight_actors and self.picking_handler.is_picked(actor, mouse_position):
                pygame.draw.rect(screen, tuple(self.config["picking_color"]), actor.get_rect(), 2)

        screen.blit(self.picking_handler.surface, self.picking_handler.position)

    def doFrame(self, screen, delta):
        self._recalc_tilesize(screen)
        self._handle_events()
        self._handle_updates(delta)
        self._render(screen)
