import random
from pygame import Rect

X, Y = 0, 1

class ImpactSide(object):
    TOP, RIGHT, BOTTOM, LEFT = 0, 1, 2, 3

class CollisionDetector(object):
    def __init__(self, allActors, precision):
        self._actors = allActors
        self._precision = precision

    def _get_collisions(self, actor, change_box):
        for other_actor, other_attributes in self._actors.iteritems():
            if actor != other_actor and other_attributes.collidable and change_box.colliderect(other_attributes.get_scaled_rect(self._precision)):
                yield other_actor
                
    def handle_collisions_x(self, actor, dx):
        if self._actors[actor].collidable and dx != 0:
            oldx = self._actors[actor].position[X]
            actor_box = self._actors[actor].get_scaled_rect(self._precision)
            change_box = Rect(actor_box.topright[X] if dx > 0 else actor_box.topleft[X] - (abs(dx) * self._precision), actor_box.topright[Y], abs(dx) * self._precision, actor_box.height)
            collisions = [collider for collider in self._get_collisions(actor, change_box)]

            if len(collisions):
                first_collision = max(collisions, key=(lambda x: self._actors[x].position[X])) if dx > 0 else max(collisions, key=(lambda x: self._actors[x].position[X] + self._actors[x].width))
                if dx > 0:
                    self._actors[actor].position[X] = self._actors[first_collision].position[X] - self._actors[actor].width
                    self._actors[actor].given_impacts[ImpactSide.RIGHT] = first_collision
                    self._actors[first_collision].received_impacts[ImpactSide.LEFT] = actor
                else:
                    self._actors[actor].position[X] = self._actors[first_collision].position[X] + self._actors[first_collision].width
                    self._actors[actor].given_impacts[ImpactSide.LEFT] = first_collision
                    self._actors[first_collision].received_impacts[ImpactSide.RIGHT] = actor
            else:
                self._actors[actor].position[X] += dx

    def handle_collisions_y(self, actor, dy):
        if self._actors[actor].collidable and dy != 0:
            actor_box = self._actors[actor].get_scaled_rect(self._precision)
            change_box = Rect(actor_box.bottomleft[X], actor_box.bottomleft[Y] if dy > 0 else actor_box.topleft[Y] - (abs(dy) * self._precision), actor_box.width, abs(dy) * self._precision)
            collisions = [collider for collider in self._get_collisions(actor, change_box)]

            if len(collisions):
                first_collision = max(collisions, key=(lambda x: self._actors[x].position[Y])) if dy > 0 else max(collisions, key=(lambda x: self._actors[x].position[Y] + self._actors[x].height))
                if dy > 0:
                    self._actors[actor].position[Y] = self._actors[first_collision].position[Y] - self._actors[actor].height
                    self._actors[actor].given_impacts[ImpactSide.BOTTOM] = first_collision
                    self._actors[first_collision].received_impacts[ImpactSide.TOP] = actor
                else:
                    self._actors[actor].position[Y] = self._actors[first_collision].position[Y] + self._actors[first_collision].height
                    self._actors[actor].given_impacts[ImpactSide.TOP] = first_collision
                    self._actors[first_collision].received_impacts[ImpactSide.BOTTOM] = actor
                self._actors[actor].velocity[Y] = 0
            else:
                self._actors[actor].position[Y] += dy
