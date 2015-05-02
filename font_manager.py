from pygame import font as _font
from sys import platform as _platform

class FontManager(object):
    def __init__(self, font_file):
        self._fonts = {}
        self.font_file = font_file

    def _get_font(self, size):
        if size not in self._fonts:
            self._fonts[size] = _font.Font(self.font_file, size)
        return self._fonts[size]
