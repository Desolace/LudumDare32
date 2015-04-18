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
            backgroundMusix.play(loops = -1)
        except:
            print "error"
            
    def play_one_sound_effect(s,effect):
        effectFilename = ''
        if effect == "jump":
            effectFilename = 'sounds/jump.wav'
        try:
            soundEffect = pygame.mixer.Sound(effectFilename)
            soundEffect.play(loops = 0)
        except:
            e = sys.exc_info()[0]
            print e

    def start_cont_effect(s,effect):
        contFilename = ''
        if effect == "run":
            contFilename = 'sounds/run.wav'
        try:
            s.contEffect = pygame.mixer.Sound(contFilename)
            s.contEffect.play(loops = -1)
        except:
            e = sys.exc_info()[0]
            print e

    def stop_cont_effect(s):
        try:
            s.contEffect.stop()
        except:
            e = sys.exc_info()[0]
            print e
