class Drawable(object):
  def __init__(self, surface, position, should_reposition):
    self.surface = surface
    self.position = position
    self.should_reposition = should_reposition
