import pygame

"""
A view into a larger level, of a given size and position.
"""
class Viewport(object):
    def __init__(self, width, height, target_actor, level, scroll_buffer=50):
        self.surface = pygame.Surface((width, height))
        self.target_actor = target_actor
        self.level = level
        self._scroll_buffer = scroll_buffer
        self._view = pygame.Rect(0, 0, width, height)
        self._buffer_view = pygame.Rect(scroll_buffer, scroll_buffer, width - scroll_buffer*2, height - scroll_buffer*2)

    def _reposition_view_x(self):
        target_box = self.target_actor.get_rect()
        diff_x_right = target_box.right - self._buffer_view.right
        diff_x_left = target_box.left - self._buffer_view.left

        assert diff_x_right < 0 or diff_x_left > 0

        if diff_x_right > 0:
            self._buffer_view.move_ip(diff_x_right, 0)
            self._view.move_ip(diff_x_right, 0)
        elif diff_x_left < 0:
            self._buffer_view.move_ip(diff_x_left, 0)
            self._view.move_ip(diff_x_left, 0)

    def _reposition_view_y(self):
        target_box = self.target_actor.get_rect()
        diff_x_top = target_box.top - self._buffer_view.top
        diff_x_bottom = target_box.bottom - self._buffer_view.bottom

        assert diff_x_top > 0 or diff_x_bottom < 0

        if diff_x_top < 0:
            self._buffer_view.move_ip(0, diff_x_top)
            self._view.move_ip(0, diff_x_top)
        elif diff_x_bottom > 0:
            self._buffer_view.move_ip(0, diff_x_bottom)
            self._view.move_ip(0, diff_x_bottom)

    def _clamp_view(self):
        self._view.clamp_ip(self.level.get_rect())
        self._buffer_view.clamp_ip(self.level.get_rect())

    def update(self, delta):
        self._reposition_view_x()
        self._reposition_view_y()
        self._clamp_view()

    def render(self, additional_drawables):
        self.surface.blit(self.level.surface, (-self._view.x, -self._view.y))
        for actor in self.level.actors:
            self.surface.blit(actor.surface, (actor.position[0] - self._view.x, actor.position[1] - self._view.y))
        for (d_surface, position) in additional_drawables:
            self.surface.blit(d_surface, (position[0] - self._view.x, position[1] - self._view.y))
        return self.surface

    def convert_position(self, position):
        return (position[0] + self._view.x, position[1] + self._view.y)
