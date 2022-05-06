import pygame

class button(object):
    def __init__(self,x,y,imageName,length,height):
        self.image = pygame.image.load(imageName)
        self.rect = self.image.get_rect()
        self.rect.centerx = x
        self.rect.centery = y
        self.height = height
        self.length = length
        self.clicked = False


    def update(self,mouseX,mouseY,clicked):
        if clicked == True and self.clicked == False:
            if mouseX <= self.rect.centerx + self.length/2 and mouseX >= self.rect.centerx - self.length/2:
                if mouseY <= self.rect.centery + self.height/2 and mouseY >= self.rect.centery - self.height/2:
                    self.clicked = True
                    #print("bonjour")

    def draw(self,win):
        win.blit(self.image,self.rect)

