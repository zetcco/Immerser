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
    keysPer = typeCount - isTyping.oldCount
    isTyping.oldCount = typeCount
    return keysPer

# Play switch between immersive and normal music
def adaptMusic():
    global switching

    while True:
        # print(round(sound_intense.get_volume(),1), round(sound_main.get_volume(),1))
        keysPer = isTyping()
        # print(adaptMusic.prevCount, keysPer)
        if ( ((adaptMusic.prevCount <= 2 and adaptMusic.prevCount >= 0 and keysPer > 2) or (keysPer <= 2 and keysPer >= 0 and adaptMusic.prevCount > 2)) and switching == False ):
            # print("Switch")
            switching = True
            switchMusic()
            switching = False
        else:
            a = 0
            # print("Normal")

        adaptMusic.prevCount = keysPer
        time.sleep(1)

def switchMusic():
    global sound_intense
    global sound_main

    if (round(sound_intense.get_volume(),1) == 0 and sound_main.get_volume() == 1):
        # print("Intense: %f -> %f | Main: %f -> %f" % (round(sound_intense.get_volume(),1), 1, round(sound_main.get_volume(),1), 0))
        for i in range(0,11):
            sound_intense.set_volume(i/10)
            sound_main.set_volume((10-i)/10)
            # print("\tIntense: %f | Main: %f" % (round(sound_intense.get_volume(),1), round(sound_main.get_volume(),1)))
            time.sleep(0.5)
    elif (sound_intense.get_volume() == 1 and round(sound_main.get_volume(),1) == 0):
        # print("Intense: %f -> %f | Main: %f -> %f" % (round(sound_intense.get_volume(),1), 0, round(sound_main.get_volume(),1), 1))
        for i in range(0,11):
            sound_intense.set_volume((10-i)/10)
            sound_main.set_volume(i/10)
            # print("\tIntense: %f | Main: %f" % (round(sound_intense.get_volume(),1), round(sound_main.get_volume(),1)))
            time.sleep(0.2)

typeCount = 0
switching = False
keysPer = 0
adaptMusic.prevCount = 0
isTyping.oldCount = 0

pygame.init()
pygame.mixer.init()
sound_main = pygame.mixer.Sound("Mixing\opgx\main.mp3")
sound_intense = pygame.mixer.Sound("Mixing\opgx\intense.wav")
sound_intense.set_volume(0)
sound_main.play(-1)
sound_intense.play(-1)

threading.Thread(target=adaptMusic).start()

hookManager = pyHook.HookManager()
hookManager.KeyUp = OnKeyEvent
hookManager.HookKeyboard()
pythoncom.PumpMessages()