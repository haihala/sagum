from threading import Thread
import time
import pygame
from random import random
from pygame.locals import *


class Game(Thread):
    def __init__(self):
        super(Game, self).__init__()
        self.end = False
        pygame.init()
        #pygame.mouse.set_visible(False)
        self.size = self.width, self.height = 480, 320
        self.screen = pygame.display.set_mode(self.size)
        self.clock = pygame.time.Clock()
        self.black = int(random()*255), int(random()*255), int(random()*255)
        print "Game: Hi are you the person who is supposed to poke me for the evening, I will be your game tonight."

    def setup(self):
        print "Game: Setting up is hard work, but I will try to manage it. Thanks for not helping by the way."

    def run(self):
        print "Game: Running like I saw the last bagel at a bakery I want that bagel."
        while 1:
            self.clock.tick(60)
            self.eventhandler()
            pygame.event.clear()
            self.screen.fill(self.black)
            pygame.display.flip()


    def eventhandler(self):
        for e in pygame.event.get():
            print e
            if e.type == pygame.QUIT:
                print "changing self.end"
                pygame.quit()
                self.end = True
                print "self.end is",self.end

    def wololo(self):
        print "wololo"
