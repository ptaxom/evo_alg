
from Models import Bird
from vector import *
import random
import numpy as np
from numpy import ndarray

def rand_choose():
    return True if random.random() > 0.98 else False

class BotAlg:
    def __init__(self, alg):
        self.alg = alg

    def make_decision(self, *args, **kwargs):
        return self.alg(*args, **kwargs)


class Bot:
    def __init__(self, start_pos, AI): # start_pos = Vector(50, height / 2)
        self.bird = Bird(start_pos, Vector(0, 0), Vector(73, 50))
        self.bird.load("..\\res\\bird_sprite")
        self.gen = AI
        self.score = 0

    def make_decision(self, data):
        return self.gen.make_decesion(data)


class SingleNeuroNet:
    def __init__(self, input_amount, hidden_layer, output_amount):
        self.input_amount = input_amount
        self.hidden_layer = hidden_layer
        self.output_amount = output_amount
        self.genome = [SingleNeuroNet.random_init(input_amount, hidden_layer), SingleNeuroNet.random_init(hidden_layer, output_amount)]
        self.treshold = random.random()

    @staticmethod
    def random_init(n, m):
        mat_arr = [[(random.random() * (-1 if random.random() < 0.5 else 1)) for i in range(m)] for j in range(n)]
        return np.array(mat_arr)

    def mutate_genome(self, koef = 10.0):
        self.genome[0] += SingleNeuroNet.random_init(self.input_amount, self.hidden_layer)  / koef
        self.genome[1] += SingleNeuroNet.random_init(self.hidden_layer, self.output_amount) / koef
        self.treshold  += (random.random() - 0.5) / koef

    def make_decesion(self, input):
        val = np.dot(np.array(input), self.genome[0])
        val2 = np.dot(val, self.genome[1])
        if val2 < self.treshold:
            return False
        else:
            return True

    def deep_copy(self):
        another = type(self)(self.input_amount, self.hidden_layer, self.output_amount)
        another.treshold = self.treshold
        gen0 = [[self.genome[0][i][j] for j in range(self.hidden_layer)] for i in range(self.input_amount)]
        gen1 = [[self.genome[1][i][j] for j in range(self.output_amount)] for i in range(self.hidden_layer)]
        another.genome = [np.array(gen0), np.array(gen1)]
        return another
