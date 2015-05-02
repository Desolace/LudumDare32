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
from viewport import Viewport
from ui_overlay import UIOverlay, TextElement

"""
Manages all state for a given run of a level
"""
class GameInstance(object):

    def __init__(self, config, level_name):
        self.config = config
        self.physics_manager = PhysicsManager()
        self.sound_manager = SoundManager()
        self.material_manager = MaterialManager(config["material_file"])
        self.transmutation_manager = TransmutationManager(self.material_manager)
        self.transmutation_manager.blow_key = "stone"
        self.level = Level("{0}/{1}.lvl".format(config["levels_dir"], level_name), self.physics_manager, self.material_manager)

        self.main_char = Player.genMainCharacter(self.physics_manager, self.sound_manager)
        self.level.actors.append(self.main_char)

        self.viewport = Viewport(config["width"], config["height"], self.main_char, self.level, 100)
        self.picking_handler = PickingHandler(self.viewport, self.transmutation_manager, self.physics_manager)

        self.ui_overlay = UIOverlay(config["font_file"])
        self.ui_overlay.text_elements["score"] = TextElement((20, 20), 20, (0, 0, 0), "0 pts")

        self.physics_manager.add_actor(self.main_char, weight=3)
        self.physics_manager.set_position(self.main_char, (25, 10))
        self._highlight_actors = False

    """
    Internally sets and returns the tilesize required to display on the given screen
    """
    def _recalc_tilesize(self, screen):
        self.tile_size = screen.get_width() / self.config["width_tiles"]
        return self.tile_size

    """
    Clears the event queue and performs associated actions for the existing events
    """
    def _handle_events(self, events):
        for event in events:

            event_name = event if isinstance(event, int) else event[0]

            if event_name == Actions.START_USER_LEFT:
                self.physics_manager.add_velocity_x(self.main_char, -self.config["user_motion_speed"])
            elif event_name == Actions.START_USER_RIGHT:
                self.physics_manager.add_velocity_x(self.main_char, self.config["user_motion_speed"])
            elif event_name == Actions.START_USER_UP:
                if self.physics_manager.get_velocity_y(self.main_char) == 0:
                    self.physics_manager.add_velocity_y(self.main_char, -self.config["user_jump_speed"])
            elif event_name == Actions.STOP_USER_LEFT:
                self.physics_manager.add_velocity_x(self.main_char, self.config["user_motion_speed"])
            elif event_name == Actions.STOP_USER_RIGHT:
                self.physics_manager.add_velocity_x(self.main_char, -self.config["user_motion_speed"])
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
        self.ui_overlay.text_elements["score"].value = "{0} pts".format(self.transmutation_manager.current_points)
        self.ui_overlay.update(delta)

        self.level.update(delta, self.tile_size)
        self.viewport.update(delta)

    """
    Renders all game objects to the screen
    """
    def _render(self, screen):
        additional_drawables = []

        mouse_position = pygame.mouse.get_pos()
        for actor in self.level.actors:
            if self._highlight_actors and self.picking_handler.is_picked(actor, mouse_position) and actor.dissolvable:
                picker = (pygame.Surface(actor.surface.get_size()), actor.position, True)
                picker[0].set_colorkey((0,0,0))
                pygame.draw.rect(picker[0], tuple(self.config["picking_color"]), picker[0].get_rect(), 2)
                additional_drawables.append(picker)

        additional_drawables.append((self.picking_handler.surface, self.picking_handler.position, True))

        additional_drawables += self.ui_overlay.get_drawables()

        screen.blit(self.viewport.render(additional_drawables), (0,0))

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
