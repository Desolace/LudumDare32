import pygame
from collisions import CollisionDetector, ImpactSide

class PhysicsAttributes:
    def __init__(self, width=0, height=0, position=[0.0,0.0], velocity=[0.0,0.0], acceleration=[0.0, 0.0], collidable=True, weight=0):
        self.width = width
        self.height = height
        self.position = list(position)
        self.velocity = list(velocity)
        self.acceleration = list(acceleration)
        self.collidable = collidable
        self.weight = weight
        self.received_impacts = {}
        self.given_impacts = {}

    def get_rect(self):
        return pygame.Rect(self.position[0], self.position[1], self.width, self.height)
    def get_scaled_rect(self, scale):
        return pygame.Rect(self.position[0] * scale, self.position[1] * scale, self.width * scale, self.height * scale)

X = 0
Y = 1
GRAVITY = 9.8

class PhysicsManager(object):
    FLOOR = 12318423 #unique identifier for the floor

    _actors = []
    world_width, world_height = None, None
    _collision_precision = 100

    UNITS_PER_TILE = 10

    def add_actor(self, actor):
        self._actors.append(actor)

    def remove_actor(self, actor):
        self._actors.remove(actor)

    def update(self, delta, tileSize):
        collision_detector = CollisionDetector(self._actors, self._collision_precision)

        #clear collisions
        for actor in self._actors:
            actor.physical.received_impacts = {}
            actor.physical.given_impacts = {}

        for actor in self._actors:
            if actor.physical.weight != 0:
                actor.physical.acceleration[Y] = GRAVITY
            actor.physical.velocity[X] += delta * actor.physical.acceleration[X] #every frame, we update the velocity based on how fast it is changing
            actor.physical.velocity[Y] += delta * actor.physical.acceleration[Y]

            dx = delta * actor.physical.velocity[X] * self.UNITS_PER_TILE
            collision_detector.handle_collisions_x(actor, dx)
            dy = delta * actor.physical.velocity[Y] * self.UNITS_PER_TILE
            collision_detector.handle_collisions_y(actor, dy)

        #set real screen positions
        for actor in self._actors:
            actor.position = (actor.physical.position[X] * tileSize, actor.physical.position[Y] * tileSize)

    def is_space_filled(self, space):
        for actor in self._actors:
            if actor.physical.get_rect().colliderect(space):
                return True
        return False
