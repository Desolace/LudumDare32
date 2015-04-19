import pygame
from material_manager import MaterialManager
from actor import Actor
from input_manager import Actions, CustomEvents

class InventoryMenu(object):
    def __init__(self, config):
        self.enabled = False
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

            for actor in self.actors:
                actor.update(delta, 10)
                self.surface.blit(actor.surface, actor.position)

            screen.blit(self.surface, self.surface_position)
