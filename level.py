import json
import pygame
from actor import Actor

class Level(object):

    def __init__(self, level_name, physics_manager):
        with open(level_name, "r") as levelData:
            self._level_def = json.load(levelData)
            self.width = self._level_def['w']
            self.height = self._level_def['h']
            self.actors = []
            self._tile_size = None
            self.physics_manager = physics_manager

            physics_manager.world_width = self.width
            physics_manager.world_height = self.height

            self.surface = pygame.Surface((self.width, self.height))

            for item in self._level_def['map']:
                material = self._level_def['materials'][item['mat']]
                color = tuple(material['color'])
                subsurface = pygame.Surface((item['w'], item['h']))
                for dx in range(0, item['w']):
                    for dy in range(0, item['h']):
                        subsurface.set_at((dx, dy), color)
                if item.get("bg"): #its a background item, not interactable with the world
                    self.surface.blit(subsurface, (item['x'], item['y']))
                else: #its an actor in the world
                    new_actor = Actor(subsurface, item['w'], item['h'])
                    new_actor.point_value = material["points"]
                    physics_manager.add_actor(new_actor, weight=material["weight"])
                    physics_manager.set_position(new_actor, (item['x'], item['y']))
                    self.actors.append(new_actor)

    def update(self, tile_size):
        if(tile_size != self._tile_size):
            self.surface = pygame.transform.scale(self.surface, (self.width * tile_size, self.height * tile_size))
            self._tile_size = tile_size

        dissolved_actors = [a for a in self.actors if a.dissolved]
        for actor in dissolved_actors:
            self.actors.remove(actor)
            self.physics_manager.remove_actor(actor)
