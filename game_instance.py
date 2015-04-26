import pygame
from pygame.locals import *

from level import Level
from actor import Actor, Player
from input_manager import Actions, CustomEvents
from physics_manager import PhysicsManager
from picking_handler import PickingHandler
from sound_manager import SoundManager
from transmutation_manager import TransmutationManager
from material_manager import MaterialManager

"""
Manages all state for a given run of a level
"""
class GameInstance(object):

    def __init__(self, config, level_name):
        self.config = config
        self.physics_manager = PhysicsManager()
        self.material_manager = MaterialManager(config["material_file"])
        self.transmutation_manager = TransmutationManager(self.material_manager)
        self.transmutation_manager.blow_key = "stone"
        self.picking_handler = PickingHandler(self.transmutation_manager, self.physics_manager)
        self.level = Level("{0}/{1}.lvl".format(config["levels_dir"], level_name), self.physics_manager, self.material_manager)

        self.main_char = Player.genMainCharacter(self.physics_manager)

        self.physics_manager.add_actor(self.main_char, weight=3)
        self.physics_manager.set_position(self.main_char, (25, 10))
        self._highlight_actors = False
        self.sound_manager = SoundManager()

    """
    Internally sets and returns the tilesize required to display on the given screen
    """
    def _recalc_tilesize(self, screen):
        self.tile_size = screen.get_width() / self.level.width
        return self.tile_size

    """
    Clears the event queue and performs associated actions for the existing events
    """
    def _handle_events(self, events):
        for event in events:

            event_name = event if isinstance(event, int) else event[0]

            if event_name == Actions.START_USER_LEFT:
                self.physics_manager.add_velocity_x(self.main_char, -self.config["user_motion_speed"])
                self.sound_manager.start_cont_effect('run')
            elif event_name == Actions.START_USER_RIGHT:
                self.physics_manager.add_velocity_x(self.main_char, self.config["user_motion_speed"])
                self.sound_manager.start_cont_effect('run')
            elif event_name == Actions.START_USER_UP:
                if self.physics_manager.get_velocity_y(self.main_char) == 0:
                    self.physics_manager.add_velocity_y(self.main_char, -self.config["user_jump_speed"])
                    self.sound_manager.play_one_sound_effect('jump')
            elif event_name == Actions.STOP_USER_LEFT:
                self.physics_manager.add_velocity_x(self.main_char, self.config["user_motion_speed"])
                self.sound_manager.stop_cont_effect('run')
            elif event_name == Actions.STOP_USER_RIGHT:
                self.physics_manager.add_velocity_x(self.main_char, -self.config["user_motion_speed"])
                self.sound_manager.stop_cont_effect('run')
            elif event_name == Actions.USER_SUCK:
                [self.transmutation_manager.suck(actor) for actor in self.level.actors if self.picking_handler.is_picked(actor, event[1])]
            elif event_name == Actions.USER_BLOW:
                (new_actor, tile_pos, weight) = self.transmutation_manager.blow(event[1], self.tile_size)
                self.level.actors.append(new_actor)
                self.physics_manager.add_actor(new_actor, weight=weight)
                self.physics_manager.set_position(new_actor, tile_pos)
            elif event_name == Actions.START_BLOW_SELECTION:
                self.picking_handler.start_user_selection(event[1], self.tile_size)
            elif event_name == Actions.STOP_BLOW_SELECTION:
                self.picking_handler.stop_user_selection()
            elif event_name == Actions.START_DISSOLVE_SELECTION:
                self._highlight_actors = True
            elif event_name == Actions.STOP_DISSOLVE_SELECTION:
                self._highlight_actors = False
            elif event_name == Actions.CHOOSE_MATERIAL:
                self.transmutation_manager.blow_key = event[1]
            elif event_name == Actions.MUTE:
                self.sound_manager.mute()
            elif event_name == Actions.UNMUTE:
                self.sound_manager.unmute()

    """
    Updates all game objects and manager systems based on the frame time delta
    """
    def _handle_updates(self, delta):
        self.physics_manager.update(delta, self.tile_size)
        self.picking_handler.update(delta, self.tile_size)
        self.transmutation_manager.update(delta)

        self.main_char.update(delta, self.tile_size)
        self.level.update(delta, self.tile_size)

    """
    Renders all game objects to the screen
    """
    def _render(self, screen):
        mouse_position = pygame.mouse.get_pos()
        screen.blit(self.level.surface, (0,0))
        screen.blit(self.main_char.surface, self.main_char.position)
        for actor in self.level.actors:
            screen.blit(actor.surface, actor.position)
            if self._highlight_actors and self.picking_handler.is_picked(actor, mouse_position) and actor.dissolvable:
                pygame.draw.rect(screen, tuple(self.config["picking_color"]), actor.get_rect(), 2)

        screen.blit(self.picking_handler.surface, self.picking_handler.position)

    """
    Handle events, update game state, and render to the given screen
    """
    def doFrame(self, screen, delta, events):
        self._recalc_tilesize(screen)
        self._handle_events(events)
        self._handle_updates(delta)

        if self.level.is_player_at_goal(self.main_char):
            pygame.event.post(pygame.event.Event(CustomEvents.USERWINS))

        self._render(screen)
