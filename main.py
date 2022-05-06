'''
Flappy Bird
Authors: Alex Kung
Main game loops and logic
'''

import pygame
import sys
from pygame.locals import *
import random
import os
import copy

from bird import bird
from pipe import pipe

from ai_bird import ai_bird

from button import button
from textBox import InputBox

GREEN = (0, 255, 0)
GREY = (210, 210 ,210)
WHITE = (255, 255, 255)
RED = (190, 34, 34)
PURPLE = (255, 0, 255)
BLACK = (0,0,0)

FRAME_RATE = 60.0
SCREEN_SIZE = (900,700)

global bestScore
bestScore = 0

global bestAIScore
bestAIScore = 0

global attempts
attempts = 0

def pygame_modules_have_loaded():
    '''
    Checks if pygame is working before launching the game
    '''
    success = True

    if not pygame.display.get_init:
        success = False
    if not pygame.font.get_init():
        success = False
    if not pygame.mixer.get_init():
        success = False

    return success

pygame.mixer.pre_init(44100, -16, 2, 512)
pygame.init()
pygame.font.init()

if pygame_modules_have_loaded():
    
    game_screen = pygame.display.set_mode(SCREEN_SIZE)
    pygame.display.set_caption('Bird Flappy')
    clock = pygame.time.Clock()

    def collision(x1,y1,length1,width1,x2,y2,length2,width2):
        '''
        Collision detection function
        Uses AABB collision (Axis-Aligned Bounding Box collision)
        '''
        deltaX = x2-x1
        deltaY = y2-y1

        if deltaX < 0:
            deltaX = -deltaX
        if deltaY < 0:
            deltaY = -deltaY

        if deltaX-((length1/2)+(length2/2)) < 0 and deltaY-((width1/2)+(width2/2)) < 0:
            return True
        else:
            return False

    def declare_globals():
        global b
        b = bird(150,350)

        global pipes
        pipes = []
        
        pass


    def handle_input(key_name):
        if key_name == "space":
            b.velocity = -100
        pass


    def text_objects(text, font, color):
        '''
        Returns values needed for text
        '''
        textSurface = font.render(text, True, color)
        return textSurface, textSurface.get_rect()
        

    def update(screen, time, againstAi):
        global attempts
        largeText = pygame.font.Font('arial.ttf',40)   
        smallText = pygame.font.Font('arial.ttf',20)        

        for i in pipes:
            if i.passed == False and i.x < b.rect.centerx:
                b.score += 1
                i.passed = True

            if collision(b.rect.centerx,b.rect.centery,b.DX,b.DY,i.topPipe.rect.centerx,i.topPipe.rect.centery,i.topPipe.DX,i.topPipe.DY):
                b.dead = True
            if collision(b.rect.centerx,b.rect.centery,b.DX,b.DY,i.bottomPipe.rect.centerx,i.bottomPipe.rect.centery,i.bottomPipe.DX,i.bottomPipe.DY):
                b.dead = True
                
        screen.fill((66,170,244))
        
        b.draw(screen)
        for i in pipes:
            i.draw(screen)

        TextSurf, TextRect = text_objects(str(b.score), largeText, BLACK)
        TextRect.x = 450
        TextRect.y = 10
        screen.blit(TextSurf, TextRect)

        if againstAi == True:
            TextSurf, TextRect = text_objects("Attempt: " + str(attempts), smallText, RED)
            TextRect.x = 5
            TextRect.y = 5
            screen.blit(TextSurf, TextRect)
                
        
        pygame.display.flip()
        pygame.display.update()
        if b.rect.centery < 15 or b.rect.centery >= 685:
            b.dead = True
    
    def main(againstAi = False):
        '''
        The main overall in game loop
        Handles user input
        '''
        declare_globals()
        pipeCounter = 100

        if againstAi == False:
            global attempts
            attempts = 0
        

        #main loop
        while True:
            #polls events
            for event in pygame.event.get():
                if event.type == QUIT:
                    #handles quit event
                    pygame.quit()
                    sys.exit()
                if event.type == KEYDOWN:
                    #handles key input
                    key_name = pygame.key.name(event.key)
                    handle_input(key_name)
                                            
            
            #limits loops per second
            milliseconds = clock.tick(FRAME_RATE)
            seconds = milliseconds/1000
            
            update(game_screen, seconds, againstAi)

            sleep_time = (1000.0 / FRAME_RATE) - milliseconds
            
            if sleep_time > 0.0:
                pygame.time.wait(int(sleep_time))
            else:
                pygame.time.wait(1)

            pipeCounter += 1
            if pipeCounter >= 100:
                if len(pipes) < 7:
                    p = pipe(950)
                    pipes.append(p)
                else:
                    lowestIndex = 0
                    lowestX = 0
                    for i in range(len(pipes)):
                        if pipes[i].x < lowestX:
                            lowestIndex = i
                            
                    pipes[lowestIndex].topPipe.rect.centerx = 950
                    pipes[lowestIndex].bottomPipe.rect.centerx = 950
                    pipes[lowestIndex].passed = False
                pipeCounter = 0

            if b.dead == True:
                break

        end(b.score,againstAi)
        return
        

    def ai(againstAI = False, playerScore = 0, maxGenerations = 0, popuationSize = 100):

        global bestAIScore

        popSize = popuationSize
        pipes = []
        population = []
        pipeCounter = 100
        generations = 1
        largeText = pygame.font.Font('arial.ttf',20)

        if againstAI == False:
            bestAIScore = 0
            box = InputBox(350,350,100,32,"")
            pollingPop = True
            while pollingPop:
                for event in pygame.event.get():
                    if event.type == QUIT:
                        pygame.quit()
                        sys.exit()
                    if event.type == KEYDOWN:
                        key_name = pygame.key.name(event.key)
                        if key_name == "escape" and againstAI == False:
                            return
                        if key_name == "return":
                            #print("hi")
                            try:
                                popSize = int(box.text)
                                pollingPop = False
                                break
                            except:
                                print(box.text)
                                pass
                    box.handle_event(event)

                box.update()

                game_screen.fill((0,0,0))
                box.draw(game_screen)

                TextSurf, TextRect = text_objects("Enter Population Size:", largeText, WHITE)
                TextRect.centerx = 450
                TextRect.centery = 300
                game_screen.blit(TextSurf, TextRect)
                pygame.display.flip()

                

        for i in range(popSize):
            aib = ai_bird((2,8,1))
            population.append(aib)

        while True:

            for event in pygame.event.get():
                if event.type == QUIT:
                    #handles quit event
                    pygame.quit()
                    sys.exit()
                if event.type == KEYDOWN:
                    key_name = pygame.key.name(event.key)
                    if key_name == "escape" and againstAI == False:
                        return

            pipeCounter += 1
            if pipeCounter >= 100:
                if len(pipes) < 5:
                    p = pipe(950)
                    pipes.append(p)
                else:
                    lowestIndex = 0
                    lowestX = 0
                    for i in range(len(pipes)):
                        if pipes[i].x < lowestX:
                            lowestIndex = i
                            lowestX = pipes[i].x

                    pipes[lowestIndex].reset(950)
                            
                pipeCounter = 0
            

            milliseconds = clock.tick(FRAME_RATE)
            seconds = milliseconds/1000

            xDistance = 1000001
            yDistance = 1000001
            for i in range(len(pipes)):
                if pipes[i].x < xDistance and pipes[i].passed == False:
                    xDistance = pipes[i].x
                    yDistance = pipes[i].y

            if xDistance == 1000001:
                for i in pipes:
                    print(i.passed)

            for i in pipes:
                for j in population:
                    if i.passed == False and j.b.dead == False and i.x + 60 < j.b.rect.centerx:
                        i.passed = True
                        j.b.score += 1

                    if j.b.dead == False:
                        if collision(j.b.rect.centerx,j.b.rect.centery,j.b.DX,j.b.DY,i.topPipe.rect.centerx,i.topPipe.rect.centery,i.topPipe.DX,i.topPipe.DY):
                            j.b.dead = True
                        if collision(j.b.rect.centerx,j.b.rect.centery,j.b.DX,j.b.DY,i.bottomPipe.rect.centerx,i.bottomPipe.rect.centery,i.bottomPipe.DX,i.bottomPipe.DY):
                            j.b.dead = True

                        if j.b.rect.centery < 15 or j.b.rect.centery >= 685:
                            j.b.dead = True

            
            game_screen.fill((66,170,244))
            
            for i in pipes:
                i.draw(game_screen)

            for i in range(len(population)):
                if population[i].b.dead == False:
                    population[i].update(xDistance + 60,yDistance,game_screen)

            TextSurf, TextRect = text_objects("Generation: " + str(generations), largeText, RED)
            TextRect.x = 5
            TextRect.y = 5
            game_screen.blit(TextSurf, TextRect)

            TextSurf, TextRect = text_objects("Top AI Score: " + str(bestAIScore), largeText, (0,0,255))
            TextRect.x = 5
            TextRect.y = 25
            game_screen.blit(TextSurf, TextRect)
                    
            pygame.display.flip()
            pygame.display.update()

        

            sleep_time = (1000.0 / FRAME_RATE) - milliseconds
            
            if sleep_time > 0.0:
                pygame.time.wait(int(sleep_time))
            else:
                pygame.time.wait(1)

            allDead = True

            for i in population:
                if i.b.dead == False:
                    allDead = False
                    break

            for i in population:
                if i.b.score > bestAIScore:
                    bestAIScore = i.b.score

            if againstAI == True:
                if bestAIScore > playerScore:
                    return True
                if generations >= maxGenerations:
                    return False

            if allDead == True:                    

                newPop = []
                topFitness = 0
                index = 0
                totalFitness = 0
                for i in range(len(population)):
                    if population[i].fitness > topFitness:
                        topFitness = population[i].fitness
                        index = i
                    totalFitness += population[i].fitness
                    
                a = ai_bird((2,8,1))
                a.copyBird(population[index])
                newPop.append(a)
                    
                for i in range(len(population) - 1):
                    val = random.randint(0,totalFitness)
                    fitnessAddition = 0
                    ind = 0
                    while True:
                        fitnessAddition += population[index].fitness
                        if fitnessAddition >= val:
                            break
                        else:
                            ind += 1
                            
                    a = ai_bird((1,1,1))
                    a.copyBird(population[ind])
                    a.mutate()
                    newPop.append(a)

                for i in range(len(newPop)):
                    newPop[i].reset()

                del population[:]
                population = newPop[:]


                del pipes[:]
                pipeCounter = 100
                generations += 1

    
    def vsAI():
        global bestScore
        bestScore = 0
        global bestAIScore
        bestAIScore = 0
        global attempts
        attempts = 0



        b1 = button(450,350,"button4.png",300,75)
        b2 = button(450,450,"button5.png",300,75)
        b3 = button(450,550,"button6.png",300,75)

        p = 0

        while True:
            for event in pygame.event.get():
                if event.type == QUIT:
                    pygame.quit()
                    sys.exit()

                if event.type == MOUSEBUTTONUP:
                    b1.update(pygame.mouse.get_pos()[0],pygame.mouse.get_pos()[1], True)
                    b2.update(pygame.mouse.get_pos()[0],pygame.mouse.get_pos()[1], True)
                    b3.update(pygame.mouse.get_pos()[0],pygame.mouse.get_pos()[1], True)

                if event.type == KEYDOWN:
                    key_name = pygame.key.name(event.key)
                    if key_name == "escape":
                        return
            
            game_screen.fill((0,0,0))
            b1.draw(game_screen)
            b2.draw(game_screen)
            b3.draw(game_screen)
            pygame.display.flip()

            if b1.clicked == True:
                b1.clicked = False
                p = 10
                break
            elif b2.clicked == True:
                b2.clicked = False
                p = 100
                break
            elif b3.clicked == True:
                b3.clicked = False
                p = 1000
                break
            
            
        for i in range(10):
            attempts += 1
            main(True)


        aiWins = ai(True,bestScore,40,p)

        while True:
            for event in pygame.event.get():
                if event.type == QUIT:
                    pygame.quit()
                    sys.exit()
                if event.type == KEYDOWN:
                    key_name = pygame.key.name(event.key)
                    if key_name == "escape" or key_name == "return":
                        return
            
            game_screen.fill((0,0,0))
            largeText = pygame.font.Font('arial.ttf',40)
            TextSurf, TextRect = text_objects("Your score was: " + str(bestScore), largeText, GREEN)
            TextRect.centerx = 450
            TextRect.centery = 200
            game_screen.blit(TextSurf, TextRect)

            TextSurf, TextRect = text_objects("The AI score was: " + str(bestAIScore), largeText, RED)
            TextRect.centerx = 450
            TextRect.centery = 300
            game_screen.blit(TextSurf, TextRect)

            result = ""
            if aiWins == True:
                result = "YOU LOSE"
            else:
                result = "YOU WIN"

            TextSurf, TextRect = text_objects(result, largeText, WHITE)
            TextRect.centerx = 450
            TextRect.centery = 400
            game_screen.blit(TextSurf, TextRect)

            pygame.display.flip()
        
            
    def intro():
        '''
        Intro Screen
        '''

        b1 = button(450,350,"button1.png",300,75)
        b2 = button(450,450,"button2.png",300,75)
        b3 = button(450,550,"button3.png",300,75)

        global attempts
        attempts = 0



        while True:
            for event in pygame.event.get():
                if event.type == QUIT:
                    pygame.quit()
                    sys.exit()
                if event.type == KEYDOWN:
                    key_name = pygame.key.name(event.key)
                    if key_name == "return":
                        vsAI()

                if event.type == MOUSEBUTTONUP:
                    b1.update(pygame.mouse.get_pos()[0],pygame.mouse.get_pos()[1], True)
                    b2.update(pygame.mouse.get_pos()[0],pygame.mouse.get_pos()[1], True)
                    b3.update(pygame.mouse.get_pos()[0],pygame.mouse.get_pos()[1], True)
                    
            game_screen.fill((0,0,0))
            b1.draw(game_screen)
            b2.draw(game_screen)
            b3.draw(game_screen)
            pygame.display.flip()

            if b1.clicked == True:
                b1.clicked = False
                main()
            elif b2.clicked == True:
                b2.clicked = False
                ai()
            elif b3.clicked == True:
                b3.clicked = False
                vsAI()

    def end(score, againstAI = False):
        ''' 
        End Screen
        '''
        while True:
            for event in pygame.event.get():
                if event.type == QUIT:
                    pygame.quit()
                    sys.exit()
                if event.type == KEYDOWN:
                    key_name = pygame.key.name(event.key)
                    if key_name == "return":
                        if againstAI == True:
                            global bestScore
                            if score > bestScore:
                                bestScore = score
                            return
                        else:
                            main()
                            return
                    if key_name == "escape":
                        return

            #prints end screen
            game_screen.fill((66,170,244))
            b.draw(game_screen,False)
            for i in pipes:
                i.draw(game_screen,False)
            largeText = pygame.font.Font('arial.ttf',40)
            TextSurf, TextRect = text_objects("Your score was: " + str(score), largeText, RED)
            TextRect.centerx = 450
            TextRect.centery = 350
            game_screen.blit(TextSurf, TextRect)
            pygame.display.flip()

    #starts at intro screen
    intro()
