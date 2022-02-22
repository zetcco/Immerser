import pygame
import pythoncom 
import pyHook
import time
import threading

def OnKeyEvent(event):
    global typeCount
    typeCount += 1
    return True

def isTyping():
    global keysPer
    while True:
        keysPer = typeCount - isTyping.oldCount
        isTyping.oldCount = typeCount
        time.sleep(1)

# Play switch between immersive and normal music
def adaptMusic():
    global switching

    while True:
        print(round(sound_intense.get_volume(),1), round(sound_main.get_volume(),1))
        if ( ((adaptMusic.prevCount == 0 and keysPer > 3) or (keysPer == 0 and adaptMusic.prevCount > 0)) and switching == False ):
            print("Switch")
            switching = True
            # switchMusic()
            time.sleep(2)
            switching = False
        else:
            print("Normal")

        adaptMusic.prevCount = keysPer
        time.sleep(1)

def switchMusic():
    global sound_intense
    global sound_main

    if (round(sound_intense.get_volume(),1) == 0.1 and sound_main.get_volume() == 1):
        for i in range(1,10):
            sound_intense.set_volume(i/10)
            sound_main.set_volume((10-i)/10)
    elif (sound_intense.get_volume() == 1 and round(sound_main.get_volume(),1) == 0.1):
        for i in range(0,10):
            sound_intense.set_volume((10-i)/10)
            sound_main.set_volume(i/10)

isTyping.oldCount = 0
typeCount = 0
switching = False
keysPer = 0
adaptMusic.prevCount = 0

pygame.init()
pygame.mixer.init()
sound_main = pygame.mixer.Sound("main.mp3")
sound_intense = pygame.mixer.Sound("intense.wav")
sound_intense.set_volume(0.1)
sound_main.play(-1)
sound_intense.play(-1)

threading.Thread(target=isTyping).start()
threading.Thread(target=adaptMusic).start()

hookManager = pyHook.HookManager()
hookManager.KeyUp = OnKeyEvent
hookManager.HookKeyboard()
pythoncom.PumpMessages()