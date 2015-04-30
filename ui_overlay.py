import pygame
from font_manager import FontManager

class TextElement(object):
    def __init__(self, position, size, color, value=""):
        self.position, self.size, self.color, self.value = position, size, color, value

class UIOverlay(object):
    def __init__(self):
        self.text_elements = {}
        self.labels = []
        self.font_manager = FontManager()

    def update(self, delta):
        self.labels = []
        for text_element in self.text_elements.values():
            label = self.font_manager._get_font(text_element.size).render(text_element.value, 1, text_element.color)
            self.labels.append((label, text_element.position, False))

    def get_drawables(self):
        return self.labels
