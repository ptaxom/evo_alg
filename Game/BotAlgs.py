
from Models import Bird
from vector import *
import random
import numpy as np
import json
import math


def vectorize(f):
    return np.vectorize(f)

@vectorize
def sigmoid(x):
    return 1.0 / (1 + math.exp(-x))


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
    def __init__(self, layer_cfg):
        self.layer_cfg = layer_cfg
        self.genome = []
        for i in range(1, len(layer_cfg)):
            self.genome.append(SingleNeuroNet.random_init(layer_cfg[i-1], layer_cfg[i]))
        self.treshold = random.random()

    @staticmethod
    def random_init(n, m):
        mat_arr = [[(random.random() * (-1 if random.random() < 0.5 else 1)) for i in range(m)] for j in range(n)]
        return np.array(mat_arr)

    def mutate_genome(self, koef = 10.0):
        for i in range(len(self.layer_cfg) - 1):
            self.genome[i] += SingleNeuroNet.random_init(self.layer_cfg[i], self.layer_cfg[i+1]) / koef
        self.treshold  += (random.random() - 0.5) / koef
        if self.treshold < 0:
            self.treshold *= -1

    def make_decesion(self, input_data):
        val = np.array(input_data)
        for layer in self.genome:
            val = sigmoid(np.dot(val, layer))
        if val < self.treshold:
            return False
        else:
            return True

    def serialize(self, filename):
        json_repres = dict()
        json_repres["layer_cfg"] = self.layer_cfg
        json_repres["treshold"] = self.treshold
        genome = []
        for layer in self.genome:
            genome.append(layer.tolist())
        json_repres["genome"] = genome
        json_str = json.dumps(json_repres)
        file = open(filename, "w")
        file.write(json_str)
        file.close()


    @staticmethod
    def load_from_file(filename):
        file = open(filename, "r")
        str = file.read()
        file.close()
        obj_dict = json.loads(str)
        net = SingleNeuroNet(obj_dict["layer_cfg"])
        net.treshold = obj_dict["treshold"]
        genome = []
        for layer in obj_dict["genome"]:
            genome.append(np.array(layer))
        net.genome = genome
        return net

