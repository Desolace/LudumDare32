from pygame import Rect
from physics_manager import ImpactSide

LEFT, RIGHT = -1, 1
DEFAULT_SPEED = 3
X, Y = 0, 1

class AIManager(object):
    def __init__(self, physics_manager):
        self.actors = []
        self.physics_manager = physics_manager

    def update(self, delta, tile_size):
        for actor in self.actors:
            direction = actor.ai_knowledge.get('x_dir', LEFT)
            speed = actor.ai_knowledge.get('speed', DEFAULT_SPEED)

            if direction == LEFT:
                rect = actor.get_rect()
                floor_tile_filled = self.physics_manager.is_space_filled(Rect((rect.bottomleft[0] / tile_size) - 1, (rect.bottomleft[1] / tile_size), 1, 1))
                if not floor_tile_filled or actor.physical.given_impacts.get(ImpactSide.LEFT, None) is not None or actor.physical.received_impacts.get(ImpactSide.LEFT, None) is not None:
                    actor.physical.velocity[X] = 0
                    actor.ai_knowledge['x_dir'] = RIGHT
                else:
                    actor.physical.velocity[X] = LEFT * speed
            elif direction == RIGHT:
                rect = actor.get_rect()
                floor_tile_filled = self.physics_manager.is_space_filled(Rect((rect.bottomright[0] / tile_size) + 1, (rect.bottomright[1] / tile_size), 1, 1))
                if not floor_tile_filled or actor.physical.given_impacts.get(ImpactSide.RIGHT, None) is not None or actor.physical.received_impacts.get(ImpactSide.RIGHT, None) is not None:
                    actor.physical.velocity[X] = 0
                    actor.ai_knowledge['x_dir'] = LEFT
                else:
                    actor.physical.velocity[X] = RIGHT * speed
