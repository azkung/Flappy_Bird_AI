import math
import random

def sigmoid(x):
    return 1/(1+ pow(math.e,-x))

class neuron(object):
    def __init__(self,weights,bias):
        if len(weights) == 0:
            self.input = True
        else:
            self.input = False

        self.weights = weights
        self.bias = bias

        self.activator = 0

    def mutateWeights(self):
     
        for i in range(len(self.weights)):
            percent = random.randint(0,200)
            if percent == 43:   
                self.weights[i] = random.randint(-100,100)/100

        percent = random.randint(0,200)
        if percent == 3:   
            self.bias += random.randint(-100,100)/100

        #weights are to previous neurons
        
