import pygame
import sys
from input_manager import Actions

class SoundEffect(object):
    def __init__(self, filename, loops):
        self.filename, self.loops = filename, loops
SoundEffect.Run = SoundEffect(filename='sounds/run.wav', loops=-1)
SoundEffect.Jump = SoundEffect(filename='sounds/jump.wav', loops=0)

class SoundManager(object):

    def __init__(self):
        self._volume = 1.0
        self._muted = False
        self._sounds = {}

    def mute(self):
        self._muted = True
        for sound in self._sounds.itervalues():
            if sound is not None:
                sound.set_volume(0)
    def unmute(self):
        self._muted = False
        for sound in self._sounds.itervalues():
            if sound is not None:
                sound.set_volume(self._volume)

    def enable_sound(self, key, definition):
        if key not in self._sounds:
            sound = pygame.mixer.Sound(definition.filename)
            if self._muted:
                sound.set_volume(0)
            sound.play(loops = definition.loops)
            self._sounds[key] = sound

    def disable_sound(self, key):
        if key in self._sounds:
            self._sounds[key].stop()
            del self._sounds[key]
