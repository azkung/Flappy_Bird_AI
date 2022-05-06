import random
from neuron import neuron
from bird import bird
import math
import copy


def sigmoid(x):
    try:
        return 1/(1+ (math.e**(-x)))
    except:
        return 1

class ai_bird(object):
    def __init__(self,layersInfo):
        self.layersAmount = len(layersInfo)
        self.network = []
        for i in range(self.layersAmount):
            neurons = []
            for j in range(layersInfo[i]):
                bias = random.randint(-1,1)
                weights = []
                if i != 0:
                    for x in range(layersInfo[i-1]):
                        weight = random.randint(-100,100)/100
                        weights.append(weight)
                    
                n = neuron(weights,bias)
                neurons.append(n)
            self.network.append(neurons)

        self.b = bird(150,350)
        self.fitness = 0

    def update(self,xDistance,yDistance,screen):
        self.network[0][0].activator = xDistance/750
        self.network[0][1].activator = (self.b.rect.centery - yDistance)/350

        for i in range(1,len(self.network)):
            for j in range(len(self.network[i])):
                val = 0
                for x in range(len(self.network[i][j].weights)):
                    val += (self.network[i-1][x].activator)*(self.network[i][j].weights[x])
                val += self.network[i][j].bias
                self.network[i][j].activator = sigmoid(val)

        if self.network[self.layersAmount-1][0].activator > 0.5:
            self.b.velocity = -100
        
        self.b.draw(screen)

        self.fitness += 1

    def mutate(self):
        
        for i in range(len(self.network)):
            for j in range(len(self.network[i])):
                self.network[i][j].mutateWeights()
        
        return 


    def copyBird(self,newAi):
        del self.network[:]
        self.network = copy.deepcopy(newAi.network)
        self.layersAmount = len(newAi.network)
        


            
    def reset(self):
        self.b.reset(150,350)
        self.fitness = 0

        
