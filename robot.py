#! /usr/bin/env python
#importng necessary modules

import pygame
from pygame.locals import *
import numpy
import random
import pyaudio
import analyse

# Initialize PyAudio
pyaud = pyaudio.PyAudio()

# Open input stream, 16-bit mono at 44100 Hz
stream = pyaud.open(
    format = pyaudio.paInt16,
    channels = 1,
    rate = 44100,
    input = True)

pygame.init()
screen=pygame.display.set_mode((640,480),FULLSCREEN)
pygame.display.set_caption("roboface")

#inheritance of Sprite class.every Sprite Must Have image and rect property otherwise it wll give you an exception
class Boxes(pygame.sprite.Sprite):
    def __init__(self):   
        pygame.sprite.Sprite.__init__(self)
        self.image=pygame.Surface((360, 24))
        self.image.fill(pygame.color.Color(0, 0, 0))
        self.rect=self.image.get_rect()
        self.rect.center=(320, 380)


def main():
    background=pygame.Surface(screen.get_size())
    background=background.convert()
    background.fill((255, 248, 220))
    screen.blit(background,(0,0))
    boxes=[]

    right_eye = Boxes()
    right_eye.image=pygame.Surface((40, 40))
    right_eye.rect=right_eye.image.get_rect()
    right_eye.rect.center=(140, 100)
    boxes.append(right_eye)

    left_eye = Boxes()
    left_eye.image=pygame.Surface((40, 40))
    left_eye.rect=left_eye.image.get_rect()
    left_eye.rect.center=(500, 100)
    boxes.append(left_eye)

    mouth = Boxes()

    boxes.append(mouth)

    allSprites=pygame.sprite.Group(boxes)
    RESET = allSprites

    running = True
    while running:
        #Python event management
        for event in pygame.event.get ():
            # Quit if x is clicked or escaped is pushed
            if event.type == pygame.QUIT or (event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE):
                stream.close()
                running = False
        
        # Press 't' to talk.
        if (event.type == pygame.KEYDOWN and event.key == pygame.K_t):

            # Read raw microphone data, the try escape fixes an overflow bug.
            try:
                rawsamps = stream.read(1024)

                # Convert raw data to NumPy array
                samps = numpy.fromstring(rawsamps, dtype=numpy.int16)

                # Show the volume and pitch
                num = max(24, (60 + int(analyse.loudness(samps))))
                # print num
                # print analyse.musical_detect_pitch(samps)
                mouth.image=pygame.Surface((360, num))
            except:
                print "overflow"
        if (event.type == pygame.KEYDOWN and event.key == pygame.K_b):
            right_eye.image=pygame.Surface((40, 10))
            left_eye.image=pygame.Surface((40, 10))
        if event.type == pygame.KEYUP:
            right_eye.image=pygame.Surface((40, 40))
            left_eye.image=pygame.Surface((40, 40))
            mouth.image=pygame.Surface((360, 24))

        #following the CUD Rule (Clear,Update,Draw)
        allSprites.clear(screen,background)
        allSprites.update()
        allSprites.draw(screen)
        pygame.display.flip()

if __name__=='__main__':
    main()
