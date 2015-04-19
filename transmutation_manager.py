import pygame
from actor import Actor

"""
Manages the players points and the absorbtion and construction of new actors.
"""
class TransmutationManager(object):
    def __init__(self, material_manager):
        self._sucking = []
        self.current_points = 0
        self._tiles_removed = {}
        self.material_manager = material_manager
        self.blow_key = None

    """
    Determines the number of points required to construct an NxM block of the current blow material
    """
    def get_points_required(self, width_tiles, height_tiles):
        material = self.material_manager.get_material(self.blow_key, (0,0))
        return material.point_value * width_tiles * height_tiles

    """
    Begin destruction of the given actor, the next update after full destruction will finish the job
    """
    def suck(self, actor):
        if actor.points_per_tile > 0:
            actor.start_dissolving()
            self._sucking.append(actor)
            self._tiles_removed[actor] = 0

    """
    Create an object if we have enough points, and return it. The object is not placed into the world here.
    """
    def blow(self, rect, tile_size):
        material = self.material_manager.get_material(self.blow_key, (rect.width, rect.height))
        actor = Actor(material.surface, rect.width / tile_size, rect.height / tile_size)
        actor.points_per_tile = material.point_value

        points_used = material.point_value * actor.widthInTiles * actor.heightInTiles

        if points_used <= self.current_points:
            self.current_points -= points_used
            return (actor, (rect.left / tile_size, rect.top / tile_size), material.weight)

    """
    Finds dissolving actors and absorbs points
    """
    def update(self, delta):
        for actor in self._sucking:
            new_tiles_removed = actor.total_tile_count - len(actor.tiles_to_dissolve)
            delta_tiles_removed = new_tiles_removed - self._tiles_removed[actor]
            self._tiles_removed[actor] = new_tiles_removed
            self.current_points += delta_tiles_removed * actor.points_per_tile
            print "User has {0} points to spend".format(self.current_points)

        done_dissolving = [actor for actor in self._sucking if actor.dissolved]
        for actor in done_dissolving:
            self._sucking.remove(actor)
            print "User has {0} points to spend".format(self.current_points)
