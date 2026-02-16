import pygame
from car import Car


class Environment:
    def __init__(self, width=800, height=600):
        self.width = width
        self.height = height
        self.car = Car(width // 2, height // 2)
        self.done = False

    def update(self, accelerate, steer):
        self.car.update(accelerate, steer)
        self.check_collision()

    def check_collision(self):
        if (
            self.car.x < 0
            or self.car.x > self.width
            or self.car.y < 0
            or self.car.y > self.height
        ):
            self.done = True

    def draw(self, screen):
        screen.fill((30, 30, 30))
        self.car.draw(screen)

    def reset(self):
        self.car = Car(self.width // 2, self.height // 2)
        self.done = False

