import pygame
import random

pipeImageUpper = pygame.image.load("pipeUpper.png")
pipeImageLower = pygame.image.load("pipeLower.png")

class pipePart(object):
    def __init__(self,x,y,img):
        self.rect = img.get_rect()
        self.rect.centerx = x
        self.rect.centery = y
        self.image = img
        self.velocity = -3
        self.DX = 100
        self.DY = 700

    def draw(self,win,update):
        win.blit(self.image, self.rect)
        if update == True:
            self.rect.centerx += self.velocity



class pipe(object):
    def __init__(self,x):
        r = random.randint(100,600)
        pos1 = r-(410)
        pos2 = r+(410)
        self.y = r
        self.x = x
        self.topPipe = pipePart(x,pos1,pipeImageUpper)
        self.bottomPipe = pipePart(x,pos2,pipeImageLower)
        self.passed = False
        #self.previousPosition = x

    def draw(self,win,update = True):
        self.topPipe.draw(win,update)
        self.bottomPipe.draw(win,update)
        self.x = self.topPipe.rect.centerx

    def reset(self,x):
        self.passed = False
        self.x = x
        self.topPipe.rect.centerx = self.x
        self.bottomPipe.rect.centerx = self.x
        r = random.randint(100,600)
        pos1 = r-(410)
        pos2 = r+(410)
        self.y = r
        self.topPipe.rect.centery = pos1
        self.bottomPipe.rect.centery = pos2
        
