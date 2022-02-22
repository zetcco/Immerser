import pygame
import pythoncom 
import pyHook
import time
import threading

isTyping = False
immerseCount = 0

def OnKeyEvent(event):
    global isTyping
    isTyping = True
    return True

# Check every 0.5 seconds where user is typing
def setTypng():
    global isTyping
    while True:
        isTyping = False
        time.sleep(0.5)

# Set immerse count, this is used to intense/mild the immersive music
def checkTyping():
    global sound_main
    global sound_intense
    global immerseCount
    while True:
        if (isTyping == True):
            print("Immerse")
            immerseCount += 1
            # if (sounda.get_volume() != 0.1 and soundb.get_volume() != 1):
            # for i in range(1, 9):
            #     sounda.set_volume(i/10)
            #     soundb.set_volume((10-i)/10)
            #     time.sleep(0.5)
        else:
            print("No immerse")
            immerseCount -= 1
            # if (sounda.get_volume() != 1 and soundb.get_volume() != 0.1):
            # for i in range(1, 9):
            #     sounda.set_volume((10-i)/10)
            #     soundb.set_volume(i/10)
            #     time.sleep(0.5)
        time.sleep(3)


pygame.init()
pygame.mixer.init()
sound_main = pygame.mixer.Sound("main.mp3")
sound_intense = pygame.mixer.Sound("intense.wav")
sound_main.play(-1)
sound_intense.play(-1)

threading.Thread(target=checkTyping).start()
threading.Thread(target=setTypng).start()

hookManager = pyHook.HookManager()
hookManager.KeyAll = OnKeyEvent
hookManager.HookKeyboard()
pythoncom.PumpMessages()