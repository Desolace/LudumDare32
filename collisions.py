import random
from pygame import Rect

X, Y = 0, 1

class ImpactSide(object):
    TOP, RIGHT, BOTTOM, LEFT = 0, 1, 2, 3

class CollisionDetector(object):
    def __init__(self, allActors, precision):
        self._actors = allActors
        self._precision = precision

    def _get_collisions(self, actor):
        actorRect = self._actors[actor].get_scaled_rect(self._precision)

        for otherActor, otherAttributes in self._actors.iteritems():
            if actor != otherActor and otherAttributes.collidable and actorRect.colliderect(otherAttributes.get_scaled_rect(self._precision)):
                yield otherActor

    def _clips_top(self, rect, top_edge):
        return rect.top < top_edge and rect.bottom > top_edge
    def _clips_bottom(self, rect, bottom_edge):
        return rect.bottom < bottom_edge and rect.top > bottom_edge
    def _clips_left(self, rect, left_edge):
        return rect.left < left_edge and rect.right > left_edge
    def _clips_right(self, rect, right_edge):
        return rect.left < right_edge and rect.right > right_edge
    def _clips_vertically(self, rect, other_rect):
        abstract_rect = Rect(-10000, rect.top, 1000000, rect.height)
        other_abstract_rect = Rect(-10000, other_rect.top, 1000000, other_rect.height)
        return abstract_rect.colliderect(other_abstract_rect)
    def _clips_horizontally(self, rect, other_rect):
        abstract_rect = Rect(rect.left, -10000, rect.width, 1000000)
        other_abstract_rect = Rect(other_rect.left, -10000, other_rect.width, 1000000)
        return abstract_rect.colliderect(other_abstract_rect)

    def _snap_x(self, movingActor, blockingActor):
        movingRect = self._actors[movingActor].get_scaled_rect(self._precision)
        blockingRect = self._actors[blockingActor].get_scaled_rect(self._precision)
        if self._clips_vertically(movingRect, blockingRect):
            if self._clips_left(movingRect, blockingRect.left):
                self._actors[movingActor].recent_impact_sides[ImpactSide.RIGHT] = blockingActor
                self._actors[blockingActor].recent_impact_sides[ImpactSide.LEFT] = movingActor
                self._actors[movingActor].position[X] = (blockingRect.left / self._precision) - self._actors[movingActor].width
            elif self._clips_right(movingRect, blockingRect.right):
                self._actors[movingActor].recent_impact_sides[ImpactSide.LEFT] = blockingActor
                self._actors[blockingActor].recent_impact_sides[ImpactSide.RIGHT] = movingActor
                self._actors[movingActor].position[X] = (blockingRect.right / self._precision)

    def _snap_y(self, movingActor, blockingActor):
        movingRect = self._actors[movingActor].get_scaled_rect(self._precision)
        blockingRect = self._actors[blockingActor].get_scaled_rect(self._precision)

        if self._clips_horizontally(movingRect, blockingRect):
            if self._clips_top(movingRect, blockingRect.top):
                self._actors[movingActor].recent_impact_sides[ImpactSide.BOTTOM] = blockingActor
                self._actors[blockingActor].recent_impact_sides[ImpactSide.TOP] = movingActor
                self._actors[movingActor].velocity[Y] = 0
                self._actors[movingActor].position[Y] = (blockingRect.top / self._precision) - self._actors[movingActor].height
            elif self._clips_bottom(movingRect, blockingRect.bottom):
                self._actors[movingActor].recent_impact_sides[ImpactSide.TOP] = blockingActor
                self._actors[blockingActor].recent_impact_sides[ImpactSide.BOTTOM] = movingActor
                self._actors[movingActor].velocity[Y] = 0
                self._actors[movingActor].position[Y] = (blockingRect.bottom / self._precision)

    def handle_collisions_x(self, actor):
        if self._actors[actor].collidable:
            for collision in self._get_collisions(actor):
                self._snap_x(actor, collision)

    def handle_collisions_y(self, actor):
        if self._actors[actor].collidable:
            for collision in self._get_collisions(actor):
                self._snap_y(actor, collision)
