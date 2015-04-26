import pygame
import sys


class SoundManager(object):

    _volume = 1.0
    _muted = False
    _sounds = []

    def __init__(self,contEffect=None):
        self.contEffect = contEffect
        self._sounds = [contEffect]
        self.soundList = {'run' : 0}

    def mute(self):
        self._muted = True
        for sound in self._sounds:
            if sound is not None:
                sound.set_volume(0)
    def unmute(self):
        self._muted = False
        for sound in self._sounds:
            if sound is not None:
                sound.set_volume(self._volume)

    def set_background_music(level):
        backgroundMusic.stop()
        backFilename = ""
        if level == 1:
            backFilename = ""
        try:
            backgroundMusic = pygame.mixer.Sound(backFilename)
            backgroundMusic.play(loops = -1)
        except:
            print "error"

    def play_one_sound_effect(self,effect):
        effectFilename = ''
        if effect == "jump":
            effectFilename = 'sounds/jump.wav'
        try:
            soundEffect = pygame.mixer.Sound(effectFilename)
            if self._muted:
                soundEffect.set_volume(0)
            soundEffect.play(loops = 0)
            self._sounds.append(soundEffect)
        except Exception as e:
            print e

    def start_cont_effect(self,effect):
        contFilename = ''
        if effect == 'run':
            self.soundList[effect] += 1
            if self.soundList[effect] == 1:
                contFilename = 'sounds/run.wav'
                try:
                    self.contEffect = pygame.mixer.Sound(contFilename)
                    self.contEffect.play(loops = -1)
                    self._sounds.append(self.contEffect)
                except Exception as e:
                    print e

    def stop_cont_effect(self,effect):
        try:
            self.soundList[effect] -= 1
            if self.soundList[effect] == 0:
                self.contEffect.stop()
                self._sounds.remove(self._contEffect)
        except Exception as e:
            print e
