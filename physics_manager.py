import pygame
from random import *

class PhysicsAttributes:
    def __init__(self):
        self.width = 0
        self.height = 0
        self.position = [0.0,0.0]
        self.velocity = [0.0, 0.0]
        self.acceleration = [0.0, 0.0]

    def get_rect(self):
        return pygame.Rect(self.position[0], self.position[1], self.position[0] + self.width, self.position[1] + self.height)

X = 0
Y = 1

class PhysicsManager(object):
    _actors = {}
    _worldWidth, _worldHeight = None, None

    UNITS_PER_TILE = 10

    def __init__(self, worldWidth, worldHeight):
        self._worldWidth = worldWidth
        self._worldHeight = worldHeight

    def add_actor(self, actor, has_gravity=False):
        self._actors[actor] = PhysicsAttributes()
        self._actors[actor].width = actor.widthInTiles
        self._actors[actor].height = actor.heightInTiles
        if has_gravity:
            self._actors[actor].acceleration[Y] = 9.8 #units/second

    def remove_actor(self, actor):
        self._actors[actor] = None

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

    def _handleCollisionsX(self, actor):
        collisionX = self._isColliding(actor)
        while collisionX is not None:
            #self._snapBackX(actor, collisionX)
            print collisionX
            print random()
            return
            collisionX = self._isColliding(actor)

    """
    Determines if a given actor is currently in collision with any other actor
    """
    def _isColliding(self, actor):
        actorRect = self._actors[actor].get_rect()
        for otherActor, otherAttributes in self._actors.iteritems():
            if actor != otherActor and actorRect.colliderect(otherAttributes.get_rect()):
                return otherActor
        return None

    def _snapBackX(self, movingActor, blockingActor):
        movingRect = self._actors[movingActor].get_rect()
        blockingRect = self._actors[blockingActor].get_rect()

        if movingRect.right > blockingRect.left and movingRect.left < blockingRect.left: #borders on the left edge
            self._actors[movingActor].position[X] = blockingRect.left - self._actors[movingActor].width - 1
        elif movingRect.left < blockingRect.right and movingRect.right > blockingRect.right: #borders on the right edge
            self._actors[movingActor].position[X] = blockingRect.right + 1

    def update(self, delta, tileSize):
        for actor, attributes in self._actors.iteritems():
            attributes.velocity[0] += delta * attributes.acceleration[0] #every frame, we update the velocity based on how fast it is changing
            attributes.velocity[1] += delta * attributes.acceleration[1]

            attributes.position[0] += delta * attributes.velocity[0] * self.UNITS_PER_TILE
            if(attributes.position[0] < 0):
                attributes.position[0] = 0
                attributes.velocity[0] = 0
            elif(attributes.position[0] > self._worldWidth - attributes.width):
                attributes.position[0] = self._worldWidth - attributes.width
                attributes.velocity[0] = 0 #the object has stopped moving

            #self._handleCollisionsX(actor)

            attributes.position[1] += delta * attributes.velocity[1] * self.UNITS_PER_TILE
            if(attributes.position[1] < 0):
                attributes.position[1] = 0
                attributes.velocity[1] = 0
            elif(attributes.position[1] > self._worldHeight - attributes.height):
                attributes.position[1] = self._worldHeight - attributes.height
                attributes.velocity[1] = 0

        #set screen positions
        for actor, attributes in self._actors.iteritems():
            actor.position = (attributes.position[0] * tileSize, attributes.position[1] * tileSize)
