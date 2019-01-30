
from Models import Bird
from vector import *
import random

def rand_choose():
    return True if random.random() > 0.98 else False

class BotAlg:
    def __init__(self, alg):
        self.alg = alg

    def make_decision(self, *args, **kwargs):
        return self.alg(*args, **kwargs)


class Bot:
    def __init__(self, start_pos): # start_pos = Vector(50, height / 2)
        self.bird = Bird(start_pos, Vector(0, 0), Vector(73, 50))
        self.bird.load("..\\res\\bird_sprite")
        self.alg = BotAlg(rand_choose)
        self.score = 0
