import pygame
from material_manager import MaterialManager
from actor import Actor
from input_manager import Actions, CustomEvents

"""
Menus are like screens, but interactive!
"""
MAIN_MENU_BG_COLOR = (0, 0, 0)

class MainMenu(object):
    def __init__(self, config, enabled=False):
        self.enabled = enabled
        self._go_button = pygame.Surface((100, 100))
        pygame.draw.circle(self._go_button, (0, 255, 0), (50, 50), 50)

    def _handle_events(self, events):
        for event in events:
            event_name = event if isinstance(event, int) else event[0]
            if event_name == Actions.USER_MENU_CLICK:
                go_rect = self._go_button.get_rect().move(self._go_button_position)
                if go_rect.collidepoint(event[1]):
                    pygame.event.post(pygame.event.Event(CustomEvents.STARTBUTTONCLICK))

    def doFrame(self, screen, delta, events):
        if self.enabled:
            self._go_button_position = ((screen.get_width() / 2 - 50), (screen.get_height() / 2 - 50))
            self._handle_events(events)

            screen.fill(MAIN_MENU_BG_COLOR)

            screen.blit(self._go_button, self._go_button_position)

INV_HIGHLIGHT_COLOR = (0,0,0)

class InventoryMenu(object):
    def __init__(self, config, enabled=False):
        self.enabled = enabled
        self.material_manager = MaterialManager(config["material_file"])

        dirt = self.material_manager.get_material("dirt", (50,50))
        stone = self.material_manager.get_material("stone", (50,50))

        dirt_actor = Actor(dirt.surface, 5, 5)
        dirt_actor.position = (10, 10)
        dirt_actor.mat_name = "dirt"
        stone_actor = Actor(stone.surface, 5, 5)
        stone_actor.position = (70, 10)
        stone_actor.mat_name = "stone"

        self.actors = [dirt_actor, stone_actor]

    def _handle_events(self, events):
        for event in events:
            event_name = event if isinstance(event, int) else event[0]

            if event_name == Actions.USER_MENU_CLICK:
                for actor in self.actors:
                    rect = actor.get_rect()
                    rect.move_ip(self.surface_position)
                    if rect.collidepoint(event[1]):
                        pygame.event.post(pygame.event.Event(CustomEvents.CLOSEINV))
                        pygame.event.post(pygame.event.Event(CustomEvents.CHOOSEMAT, name=actor.mat_name))

    def doFrame(self, screen, delta, events):
        if self.enabled:
            self.surface_position = ((screen.get_width() / 4), (screen.get_height() / 4))
            self.surface = pygame.Surface((screen.get_width() / 2, screen.get_height() / 2))
            self.surface.fill((255, 0, 0))
            self.surface.set_alpha(200)

            self._handle_events(events)

            mouse_pos = pygame.mouse.get_pos()

            for actor in self.actors:
                actor.update(delta, 10)
                self.surface.blit(actor.surface, actor.position)

                #highlight it if the mouse is on top
                rect = actor.get_rect()
                rect.move_ip(self.surface_position)
                if rect.collidepoint(mouse_pos):
                    pygame.draw.rect(self.surface, INV_HIGHLIGHT_COLOR, actor.get_rect(), 2)

            screen.blit(self.surface, self.surface_position)
