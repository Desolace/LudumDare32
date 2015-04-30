from pygame import font as _font
from sys import platform as _platform

class FontManager(object):
    def __init__(self):
        self._fonts = {}
        if _platform == "darwin":
           self.defont = "/Library/Fonts/Andale Mono.ttf"
        elif ((_platform == "linux") or (_platform == "linux2")):
           self.defont = "/usr/share/fonts/truetype/ubuntu-font-family/UbuntuMono-R.ttf"
        elif _platform == "win32":
            self.defont = "C:\Windows\Fonts\lucon.ttf"

    def _get_font(self, size):
        if size not in self._fonts:
            self._fonts[size] = _font.Font(self.defont, size)
        return self._fonts[size]
