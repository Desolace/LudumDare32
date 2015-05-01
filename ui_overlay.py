import pygame

class TextElement(object):
    def __init__(self, position, size, color, value=""):
        self.position, self.size, self.color, self.value = position, size, color, value

class UIOverlay(object):
    def __init__(self):
        self._fonts = {}
        self.text_elements = {}
        self.labels = []

    def _cached_font(self, size):
        if size not in self._fonts:
            self._fonts[size] = pygame.font.Font("/Library/Fonts/Andale Mono.ttf", size)
        return self._fonts[size]

    def update(self, delta):
        self.labels = []
        for text_element in self.text_elements.values():
            if len(text_element.value) > 0:
                label = self._cached_font(text_element.size).render(text_element.value, 1, text_element.color)
                self.labels.append((label, text_element.position, False))

    def get_drawables(self):
        return self.labels
