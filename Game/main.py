
import pygame

# width, height = 1000, 700


from Models import *
from vector import Vector
import math
import copy
import json
from BotAlgs import *


def text_gen(text):
    font = pygame.font.SysFont("Courier", 25)
    color = [(255 - x) for x in Scene.bgcolor]
    color = (250, 2, 10)
    text = font.render(text, True, color)
    return text


x = []
y = []

class Scene:
    bgcolor = ((120, 220, 230))
    bg_speed = 1
    spikes_speed = 5

    def __init__(self, width, height):
        self.width = width
        self.height = height
        self.surface = pygame.display.set_mode((width, height))
        self.background = Background(width, height)
        self.background.load("..\\res\\fon.jpg")
        self.bots = []
        self.dead_bots = []
        self.spikes = []
        self.background_offset = 0
        self.other_obstacles = [Obstacle(Vector(0, height - self.background_offset), Vector(width, 10000))]
        self.sFactory = SpikeFactory(height)

    def init(self, bots_AI, spikes_amount):
        pygame.init()
        clock = pygame.time.Clock()
        clock.tick(60)
        #Bots init
        for ai in bots_AI:
            self.bots.append(Bot(Vector(50, self.height / 2), ai))
        #Spikes init
        self.sFactory.load("..\\res\\spikes")
        self.spikes = [self.sFactory.create_next(70)]
        for i in range(spikes_amount - 1):
            self.spikes.append(self.sFactory.create_next(self.spikes[-1].position.cords[0]))

    def main_loop(self):
        tick = 0
        while self.bots:
            event = pygame.event.poll()
            if event.type == pygame.QUIT:
                break

            self.background.move(Scene.bg_speed)

            self.update_spikes()

            self.update_bots()

            self.update_bot_models(tick)

            #draw
            self.draw_scene()

            #display
            pygame.display.flip()
            tick += 1

    def update_spikes(self):
        # Remove first spike, if need
        first_spike = self.spikes[0]
        if first_spike.position.cords[0] + first_spike.width + 7 < 0:
            self.spikes.append(self.sFactory.create_next(self.spikes[-1].position.cords[0]))
            del self.spikes[0]
            self.inc_bots_score()
        # Move other spikes
        for spike in self.spikes:
            spike.update(Vector(-Scene.spikes_speed, 0))

    def inc_bots_score(self):
        for bot in self.bots:
            bot.score += 1

    def draw_score(self):
        text = text_gen("Максимальный счет: {}".format(max([bot.score for bot in self.bots ])))
        self.surface.blit(text, (self.width - text.get_width(), text.get_height() + 10))

    def draw_scene(self):
        self.background.draw_bg(self.surface)

        for spike in self.spikes:
            spike.draw(self.surface)

        for bot in self.bots:
            bot.bird.draw(self.surface)

    def center_align(self, surface_to_draw, offset):
        return [(self.width - surface_to_draw.get_width()) // 2 + offset[0], (self.height - surface_to_draw.get_height()) // 2 + offset[1]]

    def game_over(self):
        self.surface.fill(Scene.bgcolor)
        text1 = text_gen("Игра закончена.")
        # text2 = text_gen("Счет: {}".format(score))
        self.surface.blit(text1, self.center_align(text1, (0, -20)))
        # surface.blit(text2, center_align(text2, (0, 20)))
        pygame.display.flip()
        while True:
            event = pygame.event.poll()
            if event.type in (pygame.QUIT, pygame.MOUSEBUTTONDOWN, pygame.KEYDOWN):
                break

    def bot_collids(self, bot):
        collids_with_other = any([bot.bird.collision.intesects(obstacle) for obstacle in self.other_obstacles])
        collids_with_spike = any([spike.intersects(bot.bird.collision) for spike in self.spikes])
        return collids_with_other or collids_with_spike

    def calc_data(self, bot):
        bird = bot.bird
        for spike in self.spikes:
            if bird.position.cords[0] < spike.position.cords[0] + spike.width:
                spike_to_analize = spike
                break

        ranges = spike_to_analize.ranges
        dy = (math.fabs((ranges[0] * 2 + ranges[1]) / 2 - bird.position.cords[1])) / self.height
        dx = (spike.position.cords[0] + spike.width - bird.position.cords[0]) / self.width
        sw = spike_to_analize.width / 60
        h = (self.height - bird.position.cords[1] - self.background_offset) / self.height
        return [dx, dy, sw, h]

    def update_bots(self):
        for i, bot in enumerate(self.bots):
            data = self.calc_data(bot)
            if self.bot_collids(bot):
                bot.score += 1 - math.fabs(data[1])
                self.dead_bots.append(bot)
                del self.bots[i]
                continue
            if bot.make_decision(data):
                bot.bird.speed = Vector(0, -3)
            bot.bird.update_physics(Vector(0, 0.1))

    def update_bot_models(self, tick):
        if tick % 3 == 0:
            for bot in self.bots:
                bot.bird.update_model()

    def print_scores(self):
        self.dead_bots.sort(key=lambda bot: bot.score, reverse=True)
        avg = 0
        print("ТОП-10 ботов: ")
        for i in range(10):
            print("{} -> Счет: {}".format(i, self.dead_bots[i].score))
            avg += self.dead_bots[i].score
        if not x:
            x.append(1)
        else:
            x.append(x[-1] + 1)
        y.append(avg / 10)

bots_count = 100
top_bots_count = 10

top_bots = []

def prepare_other_scene(scene):
    AI = [(copy.deepcopy(scene.dead_bots[x].gen)) for i in range(bots_count // top_bots_count - 1) for x in range(top_bots_count)]
    for bot in top_bots:
        AI.append(copy.deepcopy(bot.gen))
    for ai in AI:
        ai.mutate_genome(10)
    scene = Scene(1000, 700)
    scene.init(AI, 4)
    scene.main_loop()
    scene.print_scores()

    for i in range(top_bots_count):
        top_bots.append(scene.dead_bots[i])
    top_bots.sort(key=lambda bot: bot.score, reverse=True)
    del top_bots[top_bots_count:]
    return scene


import matplotlib.pyplot as plt

import datetime
import os

def save_bots(**kwargs):
    if "dirname" in kwargs:
        dir_name = "..\\res\\genomes\\" + kwargs["dirname"]
    else:
        dir_name = "..\\res\\genomes\\" + str(datetime.datetime.now()).split(".")[0].replace(" ", "_").replace(":", "_").replace("-", "_")
    if not os.path.exists(dir_name):
        os.mkdir(dir_name)
    dir_name += "\\"
    for i, bot in enumerate(top_bots):
        bot.gen.serialize(dir_name + str(i) + ".txt")
    scores = [bot.score for bot in top_bots]
    file = open(dir_name+"scores.txt", "w")
    file.write(json.dumps(scores))
    file.close()


def load_top_bots(dirname):
    dirname = "..\\res\\genomes\\" + dirname + "\\"
    scores = []
    file = open(dirname + "scores.txt", "r")
    score_str = file.read()
    file.close()
    scores = json.loads(score_str)
    for i in range(len(scores)):
        ai = SingleNeuroNet.load_from_file(dirname + str(i) + ".txt")
        bot = Bot(Vector(), ai)
        bot.score = scores[i]
        top_bots.append(bot)
    top_bots.sort(key=lambda bot: bot.score, reverse=True)


if __name__ == "__main__":
    load_top_bots("test")
    scene = Scene(1000, 700)
    scene.init([SingleNeuroNet((4, 7, 1)) for i in range(bots_count)], 4)
    scene.main_loop()
    scene.print_scores()
    for i in range(1,40):
        print("Итерация {}: ".format(i))
        scene = prepare_other_scene(scene)

    plt.plot(x, y)
    plt.show()
    save_bots(dirname="test")


    # nn = SingleNeuroNet((4, 7, 1))
    # nn.serialize("..\\res\\genomes\\1.txt")
    # print(nn.make_decesion((1, 1, 1, 1)))
    # print(nn.make_decesion((0.2, 0.2, -0.2, 0.7)))
    # print(nn.make_decesion((0, 0, 0.0, 0)))
    # nm = copy.deepcopy(nn)
    # print(nn.genome[1] - nm.genome[1])
    # nn.mutate_genome()
    # print(nn.genome[1] - nm.genome[1])