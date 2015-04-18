class TransmutationManager(object):
    def __init__(self):
        self._sucking = []
        self._points = 0

    def suck(self, actor):
        actor.start_dissolving()
        self._sucking.append(actor)
    def blow(self):
        pass

    def update(self, delta):
        done_dissolving = [actor for actor in self._sucking if actor.dissolved]
        for actor in done_dissolving:
            self._sucking.remove(actor)
            self._points += actor.point_value
            print "User has {0} points to spend".format(self._points)
