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
            prev_pos = actor.ai_knowledge.get('prev_pos', (-1, -1))
            curr_pos = actor.position
            stuck = (prev_pos == curr_pos and actor.physical.velocity[X] != 0) #we assume that the physics manager has been updated since prev_pos was last set

            if direction == LEFT:
                rect = actor.get_rect()
                floor_tile_filled = self.physics_manager.is_space_filled(Rect((rect.bottomleft[0] / tile_size) - 1, (rect.bottomleft[1] / tile_size), 1, 1))
                if not floor_tile_filled \
                 or actor.physical.given_impacts.get(ImpactSide.LEFT, None) is not None \
                 or actor.physical.received_impacts.get(ImpactSide.LEFT, None) is not None \
                 or stuck:
                    actor.physical.velocity[X] = 0
                    actor.ai_knowledge['x_dir'] = RIGHT
                    print "flip right"
                else:
                    actor.physical.velocity[X] = LEFT * speed
            elif direction == RIGHT:
                rect = actor.get_rect()
                floor_tile_filled = self.physics_manager.is_space_filled(Rect((rect.bottomright[0] / tile_size) + 1, (rect.bottomright[1] / tile_size), 1, 1))
                if not floor_tile_filled \
                 or actor.physical.given_impacts.get(ImpactSide.RIGHT, None) is not None \
                 or actor.physical.received_impacts.get(ImpactSide.RIGHT, None) is not None \
                 or stuck:
                    actor.physical.velocity[X] = 0
                    actor.ai_knowledge['x_dir'] = LEFT
                    print "flip left"
                else:
                    actor.physical.velocity[X] = RIGHT * speed

            #now the last position is the one we were in during this frame
            actor.ai_knowledge['prev_pos'] = curr_pos
