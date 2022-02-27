import pygame
import pythoncom 
import pyHook
import time
import threading

class Immerser:
    typeCount = 0
    switching = False
    keysPer = 0
    oldCount = 0
    prevCount = 0

    def __init__(self, main_music_loc, intense_music_loc, fadeInTime = 0.5, fadeOutTime = 0.2, minKeyCount = 2):
        self.main_music_loc = main_music_loc
        self.intense_music_loc = intense_music_loc
        self.fadeInTime = fadeInTime
        self.fadeOutTime = fadeOutTime
        self.minKeyCount = minKeyCount

    def OnKeyEvent(self, event):
        self.typeCount += 1
        return True

    def isTyping(self):
        self.keysPer = self.typeCount - self.oldCount
        self.oldCount = self.typeCount
        return self.keysPer

    # Play switch between immersive and normal music
    def adaptMusic(self):
        while True:
            self.keysPer = self.isTyping()
            if ( ((self.prevCount <= self.minKeyCount and self.prevCount >= 0 and self.keysPer > self.minKeyCount) or (self.keysPer <= self.minKeyCount and self.keysPer >= 0 and self.prevCount > self.minKeyCount)) and self.switching == False ):
                # print("Switching")
                self.switching = True
                self.switchMusic()
                self.switching = False
            else:
                # print("Normal")
                pass

            self.prevCount = self.keysPer
            time.sleep(1)

    def switchMusic(self):
        if (round(self.sound_intense.get_volume(),1) == 0 and self.sound_main.get_volume() == 1):
            # print("Intense: %f -> %f | Main: %f -> %f" % (round(self.sound_intense.get_volume(),1), 1, round(self.sound_main.get_volume(),1), 0))
            for i in range(0,11):
                self.sound_intense.set_volume(i/10)
                self.sound_main.set_volume((10-i)/10)
                # print("\tIntense: %f | Main: %f" % (round(self.sound_intense.get_volume(),1), round(self.sound_main.get_volume(),1)))
                time.sleep(self.fadeInTime)
        elif (self.sound_intense.get_volume() == 1 and round(self.sound_main.get_volume(),1) == 0):
            # print("Intense: %f -> %f | Main: %f -> %f" % (round(self.sound_intense.get_volume(),1), 0, round(self.sound_main.get_volume(),1), 1))
            for i in range(0,11):
                self.sound_intense.set_volume((10-i)/10)
                self.sound_main.set_volume(i/10)
                # print("\tIntense: %f | Main: %f" % (round(self.sound_intense.get_volume(),1), round(self.sound_main.get_volume(),1)))
                time.sleep(self.fadeOutTime)
    
    def play(self):
        pygame.init()
        pygame.mixer.init()
        self.sound_main = pygame.mixer.Sound(self.main_music_loc)           # Setup the main audio clip
        self.sound_intense = pygame.mixer.Sound(self.intense_music_loc)     # Setup the intense audio clip
        self.sound_intense.set_volume(0)                                    # Set insense audio volume to zero

        # Play both audios
        self.sound_main.play(-1)                                            
        self.sound_intense.play(-1)

        # Start music mixer thread
        threading.Thread(target=self.adaptMusic).start()

        # Start keyboard listener thread
        hookManager = pyHook.HookManager()
        hookManager.KeyUp = self.OnKeyEvent
        hookManager.HookKeyboard()
        pythoncom.PumpMessages()