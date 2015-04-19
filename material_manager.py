import json
from pygame import Surface

class Material(object):
    def __init__(self, surface, point_value, weight):
        self.surface = surface
        self.point_value = point_value
        self.weight = weight

class MaterialManager(object):
    def __init__(self, definitions_filename):
        with open(definitions_filename, 'r') as handle:
            self._definitions = json.load(handle)

    def get_material(self, key, size):
        definition = self._definitions.get(key)
        if definition is None:
            raise Exception("Material not found: {0}".format(key))
        else:
            surface = Surface(size)
            surface.fill(tuple(definition["color"]))
            return Material(surface, definition["point_value"], definition["weight"])
