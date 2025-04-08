import pygame
import time

pygame.init()
pygame.mixer.init()

pygame.mixer.music.load("C:/Users/rodri/Music/1 - Cantad alegres al Señor.mp3")
pygame.mixer.music.play()

while pygame.mixer.music.get_busy():
    time.sleep(0.1)

pygame.quit()