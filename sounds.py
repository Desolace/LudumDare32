import pygame
import sys

class SoundManager(object):
    def __init__(self,contEffect=None):
        self.contEffect = contEffect

    def set_background_music(level):
        backgroundMusic.stop()
        backFilename = ""
        if level == 1:
            backFilename = ""
        try:
            backgroundMusic = pygame.mixer.Sound(backFilename)
            backgroundMusic.play(loops = -1)
        except Exception as e:
            print e

    def play_one_sound_effect(self,effect):
        print "a"
        effectFilename = ''
        if effect == "jump":
            effectFilename = 'sounds/jump.wav'
        try:
            soundEffect = pygame.mixer.Sound(effectFilename)
            soundEffect.play(loops = 0)
        except Exception as e:
            print e

    def start_cont_effect(self,effect):
        print self
        contFilename = ''
        if effect == "run":
            contFilename = 'sounds/run.wav'
        try:
            self.contEffect = pygame.mixer.Sound(contFilename)
            self.contEffect.play(loops = -1)
        except Exception as e:
            print e

    def stop_cont_effect(self):
        print self
        try:
            self.contEffect.stop()
        except Exception as e:
            print e
