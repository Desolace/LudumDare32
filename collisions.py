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
        for other_actor in self._actors:
            if actor != other_actor and other_actor.physical.collidable and change_box.colliderect(other_actor.physical.get_scaled_rect(self._precision)):
                yield other_actor

    def handle_collisions_x(self, actor, dx):
        if actor.physical.collidable and dx != 0:
            oldx = actor.physical.position[X]
            actor_box = actor.physical.get_scaled_rect(self._precision)
            change_box = Rect(actor_box.topright[X] if dx > 0 else actor_box.topleft[X] - (abs(dx) * self._precision), actor_box.topright[Y], abs(dx) * self._precision, actor_box.height)
            collisions = [collider for collider in self._get_collisions(actor, change_box)]

            if len(collisions):
                first_collision = max(collisions, key=(lambda x: x.physical.position[X])) if dx > 0 else max(collisions, key=(lambda x: x.physical.position[X] + x.physical.width))
                old_x = actor.physical.position[X]
                if dx > 0:
                    actor.physical.position[X] = first_collision.physical.position[X] - actor.physical.width
                    actual_dx = abs(actor.physical.position[X] - old_x)
                    if actual_dx != 0:
                        actor.physical.given_impacts[ImpactSide.RIGHT] = first_collision
                        first_collision.physical.received_impacts[ImpactSide.LEFT] = actor
                else:
                    actor.physical.position[X] = first_collision.physical.position[X] + first_collision.physical.width
                    actual_dx = abs(actor.physical.position[X] - old_x)
                    if actual_dx != 0:
                        actor.physical.given_impacts[ImpactSide.LEFT] = first_collision
                        first_collision.physical.received_impacts[ImpactSide.RIGHT] = actor
            else:
                actor.physical.position[X] += dx

    def handle_collisions_y(self, actor, dy):
        if actor.physical.collidable and dy != 0:
            actor_box = actor.physical.get_scaled_rect(self._precision)
            change_box = Rect(actor_box.bottomleft[X], actor_box.bottomleft[Y] if dy > 0 else actor_box.topleft[Y] - (abs(dy) * self._precision), actor_box.width, abs(dy) * self._precision)
            collisions = [collider for collider in self._get_collisions(actor, change_box)]

            if len(collisions):
                first_collision = max(collisions, key=(lambda x: x.physical.position[Y])) if dy > 0 else max(collisions, key=(lambda x: x.physical.position[Y] + x.physical.height))
                old_y = actor.physical.position[Y]
                if dy > 0:
                    actor.physical.position[Y] = first_collision.physical.position[Y] - actor.physical.height
                    actual_dy = abs(actor.physical.position[Y] - old_y)
                    if actual_dy != 0:
                        actor.physical.given_impacts[ImpactSide.BOTTOM] = first_collision
                        first_collision.physical.received_impacts[ImpactSide.TOP] = actor
                else:
                    actor.physical.position[Y] = first_collision.physical.position[Y] + first_collision.physical.height
                    actual_dy = abs(actor.physical.position[Y] - old_y)
                    if actual_dy != 0:
                        actor.physical.given_impacts[ImpactSide.TOP] = first_collision
                        first_collision.physical.received_impacts[ImpactSide.BOTTOM] = actor
                actor.physical.velocity[Y] = 0
            else:
                actor.physical.position[Y] += dy
