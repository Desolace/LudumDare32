import json
import pygame
from actor import Actor

"""
An instance of the given level. Handles creation of all static actors in the level.
"""
class Level(object):

    def __init__(self, level_name, physics_manager, material_manager):
        self.goal = None

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
            self.surface.fill((255,255,255))

            for item in self._level_def['map']:
                material = material_manager.get_material(item['mat'], (item['w'], item['h']))

                if item.get("bg"): #its a background item, not interactable with the world
                    self.surface.blit(material.surface, (item['x'], item['y']))
                else: #its an actor in the world
                    new_actor = Actor(material.surface, item['w'], item['h'])
                    new_actor.points_per_tile = material.point_value
                    physics_manager.add_actor(new_actor, weight=material.weight, collidable=material.collidable)
                    physics_manager.set_position(new_actor, (item['x'], item['y']))
                    self.actors.append(new_actor)

                    if item.get("goal"): #this is the level end goal point
                        self.goal = new_actor

        if self.goal is None:
            raise Exception("LvlError: A goal is required for each level.")

    def is_player_at_goal(self, player):
        return self.goal.get_rect().contains(player.get_rect())

    """
    Updates all internal actors and handles removing dissolved ones.
    """
    def update(self, delta, tile_size):
        if(tile_size != self._tile_size):
            self.surface = pygame.transform.scale(self.surface, (self.width * tile_size, self.height * tile_size))
            self._tile_size = tile_size

        dissolved_actors = [a for a in self.actors if a.dissolved]
        for actor in dissolved_actors:
            self.actors.remove(actor)
            self.physics_manager.remove_actor(actor)

        for actor in self.actors:
            actor.update(delta, tile_size)
