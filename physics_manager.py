import pygame
from collisions import CollisionDetector

class PhysicsAttributes:
    def __init__(self):
        self.width = 0
        self.height = 0
        self.position = [0.0,0.0]
        self.velocity = [0.0, 0.0]
        self.acceleration = [0.0, 0.0]
        self.weight = 0

    def get_rect(self):
        return pygame.Rect(self.position[0], self.position[1], self.width, self.height)
    def get_scaled_rect(self, scale):
        return pygame.Rect(self.position[0] * scale, self.position[1] * scale, self.width * scale, self.height * scale)

X = 0
Y = 1
GRAVITY = 9.8

class PhysicsManager(object):
    _actors = {}
    world_width, world_height = None, None
    _collision_precision = 100

    UNITS_PER_TILE = 10

    def add_actor(self, actor, weight=False):
        self._actors[actor] = PhysicsAttributes()
        self._actors[actor].width = actor.widthInTiles
        self._actors[actor].height = actor.heightInTiles
        self._actors[actor].weight = weight

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
    def set_position(self, actor, (positionX, positionY)):
        self._actors[actor].position = [positionX, positionY]

    def update(self, delta, tileSize):
        collision_detector = CollisionDetector(self._actors, self._collision_precision)

        for actor, attributes in self._actors.iteritems():
            if attributes.weight != 0:
                attributes.acceleration[Y] = GRAVITY
            attributes.velocity[X] += delta * attributes.acceleration[X] #every frame, we update the velocity based on how fast it is changing
            attributes.velocity[Y] += delta * attributes.acceleration[Y]

            attributes.position[Y] += delta * attributes.velocity[Y] * self.UNITS_PER_TILE
            if(attributes.position[Y] < 0):
                attributes.position[Y] = 0
                attributes.velocity[Y] = 0
            elif(attributes.position[Y] > self.world_height - attributes.height):
                attributes.position[Y] = self.world_height - attributes.height
                attributes.velocity[Y] = 0
            if attributes.velocity[Y] != 0:
                collision_detector.handle_collisions_y(actor)

            attributes.position[X] += delta * attributes.velocity[X] * self.UNITS_PER_TILE
            if(attributes.position[X] < 0):
                attributes.position[X] = 0
            elif(attributes.position[X] > self.world_width - attributes.width):
                attributes.position[X] = self.world_width - attributes.width
            if attributes.velocity[X] != 0:
                collision_detector.handle_collisions_x(actor)

        #set real screen positions
        for actor, attributes in self._actors.iteritems():
            actor.position = (attributes.position[X] * tileSize, attributes.position[1] * tileSize)
