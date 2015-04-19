import pygame
from actor import Actor

class TransmutationManager(object):
    def __init__(self):
        self._sucking = []
        self._points = 0
        self._tiles_removed = {}

    def suck(self, actor):
        actor.start_dissolving()
        self._sucking.append(actor)
        self._tiles_removed[actor] = 0
    def blow(self, material, rect, tile_size):
        surface = pygame.Surface((rect.width, rect.height))
        surface.fill(material["color"])
        actor = Actor(surface, rect.width / tile_size, rect.height / tile_size)
        actor.point_value = material["points"]
        return (actor, (rect.left / tile_size, rect.top / tile_size), material["weight"])

    def get_points(self):
        return self._points

    def update(self, delta):
        for actor in self._sucking:
            new_tiles_removed = actor.total_tile_count - len(actor.tiles_to_dissolve)
            delta_tiles_removed = new_tiles_removed - self._tiles_removed[actor]
            self._tiles_removed[actor] = new_tiles_removed
            self._points += delta_tiles_removed * actor.points_per_tile
            print "User has {0} points to spend".format(self._points)

        done_dissolving = [actor for actor in self._sucking if actor.dissolved]
        for actor in done_dissolving:
            self._sucking.remove(actor)
            print "User has {0} points to spend".format(self._points)
