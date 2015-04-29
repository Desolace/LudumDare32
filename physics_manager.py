import pygame
from collisions import CollisionDetector, ImpactSide

class PhysicsAttributes:
    def __init__(self):
        self.width = 0
        self.height = 0
        self.position = [0.0,0.0]
        self.velocity = [0.0,0.0]
        self.acceleration = [0.0,0.0]
        self.collidable = True
        self.weight = 0
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

    _actors = {}
    world_width, world_height = None, None
    _collision_precision = 100

    UNITS_PER_TILE = 10

    def add_actor(self, actor, weight=False, collidable=True):
        self._actors[actor] = PhysicsAttributes()
        self._actors[actor].width = actor.widthInTiles
        self._actors[actor].height = actor.heightInTiles
        self._actors[actor].weight = weight
        self._actors[actor].collidable = collidable

    def remove_actor(self, actor):
        del self._actors[actor]

    def set_velocity(self, actor, velocity):
        self._actors[actor].velocity = velocity
    def set_velocity_x(self, actor, velocity_x):
        self._actors[actor].velocity[X] = velocity_x
    def set_velocity_y(self, actor, velocity_y):
        self._actors[actor].velocity[Y] = velocity_y
    def add_velocity_x(self, actor, velocity_dx):
        self._actors[actor].velocity[X] += velocity_dx
    def add_velocity_y(self, actor, velocity_dy):
        self._actors[actor].velocity[Y] += velocity_dy
    def get_velocity(self, actor):
        return self._actors[actor].velocity
    def get_velocity_x(self, actor):
        return self._actors[actor].velocity[X]
    def get_velocity_y(self, actor):
        return self._actors[actor].velocity[Y]
    def set_position(self, actor, position):
        self._actors[actor].position = list(position)

    def update(self, delta, tileSize):
        collision_detector = CollisionDetector(self._actors, self._collision_precision)

        #clear collisions
        for actor, attributes in self._actors.items():
            attributes.received_impacts = {}
            attributes.given_impacts = {}

        for actor, attributes in self._actors.items():
            if attributes.weight != 0:
                attributes.acceleration[Y] = GRAVITY
            attributes.velocity[X] += delta * attributes.acceleration[X] #every frame, we update the velocity based on how fast it is changing
            attributes.velocity[Y] += delta * attributes.acceleration[Y]

            dx = delta * attributes.velocity[X] * self.UNITS_PER_TILE
            collision_detector.handle_collisions_x(actor, dx)
            dy = delta * attributes.velocity[Y] * self.UNITS_PER_TILE
            collision_detector.handle_collisions_y(actor, dy)

        #set real screen positions
        for actor, attributes in self._actors.items():
            actor.position = (attributes.position[X] * tileSize, attributes.position[Y] * tileSize)

    def is_space_filled(self, space):
        for actor, attributes in self._actors.items():
            if attributes.get_rect().colliderect(space):
                return True
        return False

    def received_impact(self, actor, side):
        return self._actors[actor].received_impacts.get(side, None)
    def gave_impact(self, actor, side):
        return self._actors[actor].given_impacts.get(side, None)
