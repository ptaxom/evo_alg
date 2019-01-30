
import pygame

width, height = 1000, 700
bgcolor = ((120, 220, 230))

bg_speed = 1
spikes_speed = 1

from Models import *
from vector import Vector
import math

def init():
    pygame.init()
    clock = pygame.time.Clock()
    clock.tick(60)
    main_surface = pygame.display.set_mode((width, height))
    main_surface.fill(bgcolor)
    background = Background(width, height)
    background.load("..\\res\\fon.jpg")
    return main_surface, background


def text_gen(text):
    font = pygame.font.SysFont("Courier", 25)
    color = [(255 - x) for x in bgcolor]
    color = (250, 2, 10)
    text = font.render(text, True, color)
    return text


def center_align(surface, offset):
    return [(width - surface.get_width()) // 2  + offset[0], (height - surface.get_height()) // 2 + offset[1]]


def game_over(surface, score):
    surface.fill(bgcolor)
    text1 = text_gen("Игра закончена.")
    text2 = text_gen("Счет: {}".format(score))
    surface.blit(text1, center_align(text1, (0, -20)))
    surface.blit(text2, center_align(text2, (0, 20)))
    pygame.display.flip()
    while True:
        event = pygame.event.poll()
        if event.type in (pygame.QUIT, pygame.MOUSEBUTTONDOWN, pygame.KEYDOWN):
            break


def main():

    surface, back_ground = init()
    tick = 0

    bird = Bird(Vector(50, height/2), Vector(0, 0), Vector(73, 50))
    bird.load("..\\res\\bird_sprite")

    sFactory = SpikeFactory(height)
    sFactory.load("..\\res\\spikes")
    spikes = [sFactory.create_next(50)]
    for i in range(4):
        spikes.append(sFactory.create_next(spikes[-1].position.cords[0]))

    bg_collision = Obstacle(Vector(0, height - 30), Vector(width, 30))
    score = 0

    while True:

        #creating data


        event = pygame.event.poll()
        if event.type == pygame.QUIT:
            break
        elif event.type == pygame.MOUSEBUTTONDOWN:
            bird.speed = Vector(0, -3)

        # Logics
        # bg update
        back_ground.move(bg_speed)
        #spikes update
        if spikes[0].position.cords[0] + spikes[0].width + 7 < 0:
            spikes.append(sFactory.create_next(spikes[-1].position.cords[0]))
            del spikes[0]
            score += 1
        for spike in spikes:
            spike.update(Vector(-spikes_speed, 0))
        #bird update
        if tick % 3 == 0:
            bird.update_model()
        bird.update_physics(Vector(0, 0.1))

        for spike in spikes:
            if bird.position.cords[0]  < spike.position.cords[0] + spike.width:
                spike_to_analize = spike
                break

        ranges = spike_to_analize.ranges
        dy = math.fabs((ranges[0] * 2 + ranges[1]) / 2 - bird.position.cords[1])
        dx = spike.position.cords[0] + spike.width - bird.position.cords[0]


        #collision update
        collids = bird.collision.intesects(bg_collision) or any([spike.intersects(bird.collision) for spike in spikes])
        if collids:
            game_over(surface, score)
            break

        # Drawing
        back_ground.draw_bg(surface)
        for spike in spikes:
            spike.draw(surface)
        bird.draw(surface)
        text = text_gen("Счет: {}".format(score))
        surface.blit(text, (width - text.get_width(), text.get_height() + 10))

        spike_to_analize.draw_col(surface)
        surface.fill(bgcolor, (bird.position.cords[0], bird.position.cords[1], dx, dy))

        # pygame.time.delay(6)
        pygame.display.flip()
        tick += 1








if __name__ == "__main__":
    main()
