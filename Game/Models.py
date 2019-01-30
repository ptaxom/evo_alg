import pygame
import os
import re
from scipy.stats import truncnorm
from vector import Vector


draw_col = False

class Obstacle:
    def __init__(self, point, border):
        self.point = point
        self.border = border

    def __contains__(self, item):
        if (self.point[0] <= item[0] <= self.point[0] + self.border[0] and
           self.point[1] <= item[1] <= self.point[1] + self.border[1]):
            return True
        else:
            return False

    def intesects(self, other):
        return any([(lambda i, j: Vector(self.point[0] + self.border[0] * i, self.point[1] + self.border[1] * j) in other)(i,j) for i in range(2) for j in range(2)])

    def draw(self, surface):
        rect = [*self.point.cords, *self.border.cords]
        color = (255, 0, 0)
        surface.fill(color, rect)

class SpikeFactory:

    @staticmethod
    def get_truncated_normal(mean=60, sd=20, low=40, upp=80):
        return truncnorm(
            (low - mean) / sd, (upp - mean) / sd, loc=mean, scale=sd)

    @staticmethod
    def get_truncated_mean(mean):
        sd, low, upp = mean / 3, mean * 0.66, mean * 1.33
        return SpikeFactory.get_truncated_normal(mean, sd, low, upp)

    def __init__(self, height, mean_width = 50, mean_dx = 300, mean_spike_height_top = 230, mean_spike_pass = 200):
        self.height = height
        self.dist_gen = SpikeFactory.get_truncated_mean(mean_dx)
        self.width_gen = SpikeFactory.get_truncated_mean(mean_width)
        self.height_gen = SpikeFactory.get_truncated_mean(mean_spike_height_top)
        self.pass_gen = SpikeFactory.get_truncated_mean(mean_spike_pass)

    def load(self, dirname):
        self.spike_bottom_image = pygame.image.load(dirname + os.sep + "0.png")
        self.base_image = pygame.image.load(dirname + os.sep + "1.png")
        self.spike_top_image = pygame.image.load(dirname + os.sep + "2.png")

    def create_next(self, last_x):
        ranges = [int(self.height_gen.rvs()), int(self.pass_gen.rvs())]
        ranges.append(self.height - sum(ranges))
        spike_width = int(self.width_gen.rvs())
        # spike_width = 50
        spike_height = self.spike_top_image.get_height()
        base = pygame.transform.scale(self.base_image, (spike_width, ranges[0]-spike_height))

        top_sprite = pygame.Surface((spike_width, ranges[0]), pygame.SRCALPHA, 32).convert_alpha()
        top_sprite.blit(base, (0, 0))
        top_sprite.blit(self.spike_top_image, (0, ranges[0] - spike_height))

        bottom_sprite = pygame.Surface((spike_width, ranges[2]), pygame.SRCALPHA, 32).convert_alpha()
        base = pygame.transform.scale(self.base_image, (spike_width, ranges[2] - spike_height))
        bottom_sprite.blit(base, (0, spike_height))
        bottom_sprite.blit(self.spike_bottom_image, (0, 0))

        sprites = [top_sprite, bottom_sprite]
        spike_x = int(self.dist_gen.rvs())
        return Spike(ranges, spike_width, Vector(last_x+spike_x, 0), sprites)


class Spike:
    def __init__(self, ranges, width, position, sprites):
        self.ranges = ranges
        self.width = width
        self.position = position
        self.sprites = sprites
        self.collision = self.create_collision()

    def create_collision(self):
        return [Obstacle(self.position, Vector(self.width, self.ranges[0])),
                Obstacle(self.position + Vector(0, self.ranges[0]+self.ranges[1]), Vector(self.width, self.ranges[2]))]

    def update(self, delta_pos):
        self.position = self.position + delta_pos
        self.collision = self.create_collision()

    def intersects(self, obstacle):
        return any(obstacle.intesects(x) for x in self.collision)

    def draw(self, surface):
        # draw_rects = (self.position.cords, (self.position + Vector(0, self.ranges[0] + self.ranges[1])).cords)
        surface.blit(self.sprites[0], self.position.cords)
        surface.blit(self.sprites[1], (self.position + Vector(0, self.ranges[0] + self.ranges[1])).cords)
        if draw_col:
            self.draw_col(surface)

    def draw_col(self, surface):
        for x in self.collision:
            x.draw(surface)

class Background:

    def __init__(self, width, height):
        self.width = width
        self.height = height
        self.background_image = None
        self.offset_x = 0

    def load(self, filename):
        buffer_image = pygame.image.load(filename)
        self.background_image = pygame.transform.scale(buffer_image, (self.width, self.height))

    def move(self, offset_dx):
        self.offset_x += offset_dx
        if self.offset_x % self.width == 0:
            self.offset_x = 0

    def draw_bg(self, surface):
        surface.blit(self.background_image, (-self.offset_x, 0))
        surface.blit(self.background_image, (self.width - self.offset_x, 0))


class Bird:
    def __init__(self, startpos, speed, size):
        self.position = startpos
        self.sprites = []
        self.current_sprite = 0
        self.speed = speed
        self.size = size
        self.collision = Obstacle(startpos, size)

    def load(self, dir_name):
        files = os.listdir(dir_name)
        for file in files:
            if re.match(r"[0-9]+\.png$", file):
                image = pygame.image.load(dir_name + os.sep + file)
                self.sprites.append(pygame.transform.scale(image, self.size.cords))

    def update_physics(self, delta_speed):
        self.speed = self.speed + delta_speed
        self.position = self.position + self.speed
        self.collision = Obstacle(self.position, self.size)

    def update_model(self):
        self.current_sprite += 1
        if self.current_sprite == len(self.sprites):
            self.current_sprite = 0

    def draw(self, surface):
        surface.blit(self.sprites[self.current_sprite], self.position.cords)
        if draw_col:
            self.collision.draw(surface)



