import pygame

birdImage = pygame.image.load("bird.png")
birdImage2 = pygame.image.load("bird2.png")
birdImage3 = pygame.image.load("bird3.png")

class bird(object):
    def __init__(self,x,y):
        self.rect = birdImage.get_rect()
        self.rect.centerx = x
        self.rect.centery = y
        self.image = birdImage
        self.velocity = 0
        self.acceleration = 10
        self.dead = False
        self.DX = 30
        self.DY = 30
        self.score = 0
        self.prevState = 0

    def draw(self,win,update = True):
        if self.velocity < 0 and self.dead == False:
            if self.prevState == 0:
                self.image = birdImage2
                self.prevState = 1
            elif self.prevState == 1:
                self.image = birdImage3
                self.prevState = 2
            elif self.prevState == 2:
                self.image = birdImage2
                self.prevState = 3
            elif self.prevState == 3:
                self.image = birdImage
                self.prevState = 0
            
        else:
            self.image = birdImage
            self.prevState = 0

        win.blit(self.image, self.rect)
        if update == True:
            self.rect.centery += self.velocity*0.1
            self.velocity += self.acceleration




    def reset(self,x,y):
        self.dead = False
        self.rect.centerx = x
        self.rect.centery = y
        self.velocity = 0
        
