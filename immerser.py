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

    def __init__(self, main_music_loc, intense_music_loc):
        self.main_music_loc = main_music_loc
        self.intense_music_loc = intense_music_loc

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
            if ( ((self.prevCount <= 2 and self.prevCount >= 0 and self.keysPer > 2) or (self.keysPer <= 2 and self.keysPer >= 0 and self.prevCount > 2)) and self.switching == False ):
                self.switching = True
                self.switchMusic()
                self.switching = False

            self.prevCount = self.keysPer
            time.sleep(1)

    def switchMusic(self):
        if (round(self.sound_intense.get_volume(),1) == 0 and self.sound_main.get_volume() == 1):
            # print("Intense: %f -> %f | Main: %f -> %f" % (round(sound_intense.get_volume(),1), 1, round(sound_main.get_volume(),1), 0))
            for i in range(0,11):
                self.sound_intense.set_volume(i/10)
                self.sound_main.set_volume((10-i)/10)
                # print("\tIntense: %f | Main: %f" % (round(sound_intense.get_volume(),1), round(sound_main.get_volume(),1)))
                time.sleep(0.5)
        elif (self.sound_intense.get_volume() == 1 and round(self.sound_main.get_volume(),1) == 0):
            # print("Intense: %f -> %f | Main: %f -> %f" % (round(sound_intense.get_volume(),1), 0, round(sound_main.get_volume(),1), 1))
            for i in range(0,11):
                self.sound_intense.set_volume((10-i)/10)
                self.sound_main.set_volume(i/10)
                # print("\tIntense: %f | Main: %f" % (round(sound_intense.get_volume(),1), round(sound_main.get_volume(),1)))
                time.sleep(0.2)
    
    def play(self):
        pygame.init()
        pygame.mixer.init()
        self.sound_main = pygame.mixer.Sound(self.main_music_loc)
        self.sound_intense = pygame.mixer.Sound(self.intense_music_loc)
        self.sound_intense.set_volume(0)
        self.sound_main.play(-1)
        self.sound_intense.play(-1)

        threading.Thread(target=self.adaptMusic).start()

        hookManager = pyHook.HookManager()
        hookManager.KeyUp = self.OnKeyEvent
        hookManager.HookKeyboard()
        pythoncom.PumpMessages()