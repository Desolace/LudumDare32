import pygame
import sys
from input_manager import Actions

class SoundEffect(object):
    def __init__(self, filename, loops):
        self.filename, self.loops = filename, loops
SoundEffect.Run = SoundEffect(filename='sounds/run.wav', loops=-1)
SoundEffect.Jump = SoundEffect(filename='sounds/jump.wav', loops=0)

"""
Starts and stops sound effects. Sounds may be directly started and stopped with enable_sound and disable_sound.
The actors list contains actors with a 'sounds' dictionary. Every update, any key with a None value is stopped, and any key with a non-None value is played (if it has not started already).
"""
class SoundManager(object):

    def __init__(self):
        self._volume = 1.0
        self._muted = False
        self._sounds = {}
        self.actors = []

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

    def update(self, delta):
        for actor in self.actors:
            for key, sound in actor.sounds.items():
                if sound is None:
                    self.disable_sound(key)
                else:
                    self.enable_sound(key, sound)
