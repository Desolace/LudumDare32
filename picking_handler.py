class PickingHandler(object):
    def is_picked(self, actor, position):
        return actor.get_rect().collidepoint(position)
