import pygame
import sys


class SoundManager(object):
    
    def __init__(self,contEffect=None):
        self.contEffect = contEffect
        self.soundList = {'run' : 0}        

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
        contFilename = ''
        if effect == 'run':
            self.soundList[effect] += 1
            if self.soundList[effect] == 1:
                contFilename = 'sounds/run.wav'
                try:
                    self.contEffect = pygame.mixer.Sound(contFilename)
                    self.contEffect.play(loops = -1)
                except Exception as e:
                    print e

    def stop_cont_effect(self,effect):
        try:
            self.soundList[effect] -= 1
            if self.soundList[effect] == 0:
                self.contEffect.stop()
        except Exception as e:
            print e
