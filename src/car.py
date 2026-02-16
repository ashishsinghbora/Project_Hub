import pygame
import math
import numpy as np
from src.brain import Brain


class Car:
    def __init__(self, x, y):
        # Position
        self.x = x
        self.y = y

        # Motion
        self.velocity = 0
        self.angle = 0

        # Physics constants
        self.acceleration_rate = 0.3
        self.max_speed = 10
        self.friction = 0.03
        self.steering_rate = 4

        # Visual
        self.width = 60
        self.height = 30
        self.color = (200, 0, 0)

        # AI
        self.brain = Brain()
        self.fitness = 0
        self.alive = True
        self.age = 0
        self.max_age = 1000

    def update(self, accelerate, steer):
        # Acceleration
        self.velocity += accelerate * self.acceleration_rate

        # Friction
        self.velocity -= self.friction * self.velocity

        # Clamp speed
        if self.velocity > self.max_speed:
            self.velocity = self.max_speed
        if self.velocity < -self.max_speed / 2:
            self.velocity = -self.max_speed / 2

        # Steering (only if moving)
        if abs(self.velocity) > 0.1:
            self.angle += steer * self.steering_rate * (self.velocity / self.max_speed)

        # Convert to radians
        rad = math.radians(self.angle)

        # Update position
        self.x += self.velocity * math.cos(rad)
        self.y += self.velocity * math.sin(rad)
        # Age / fitness updates
        self.age += 1
        self.fitness += abs(self.velocity)

        if self.age > self.max_age:
            self.alive = False
    def think(self):
        state = np.array(self.get_state())
        action = self.brain.forward(state)
        return action

    def draw(self, screen):
        rect = pygame.Surface((self.width, self.height))
        rect.fill(self.color)

        rotated = pygame.transform.rotate(rect, -self.angle)
        new_rect = rotated.get_rect(center=(self.x, self.y))
        screen.blit(rotated, new_rect)

    def get_state(self):
        return np.array([self.x, self.y, self.velocity, self.angle])
