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

    def update(self, accelerate, steer, bounds=(0, 0, 800, 600)):
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

        # Collision detection with boundaries
        min_x, min_y, max_x, max_y = bounds
        if not (min_x <= self.x <= max_x and min_y <= self.y <= max_y):
            self.alive = False

        # Age / fitness updates
        self.age += 1
        self.fitness += abs(self.velocity)

        if self.age > self.max_age:
            self.alive = False
    def think(self, bounds=(0, 0, 800, 600)):
        state = np.array(self.get_state(bounds))
        action = self.brain.forward(state)
        return action

    def draw(self, screen):
        rect = pygame.Surface((self.width, self.height))
        rect.fill(self.color)

        rotated = pygame.transform.rotate(rect, -self.angle)
        new_rect = rotated.get_rect(center=(self.x, self.y))
        screen.blit(rotated, new_rect)


    def cast_sensor_rays(self, bounds=(0, 0, 800, 600), num_rays=5, ray_length=150):
        # Returns list of distances to wall for each ray
        angles = np.linspace(-np.pi/4, np.pi/4, num_rays)  # -45° to +45° relative to car
        results = []
        for a in angles:
            ray_angle = math.radians(self.angle) + a
            for d in range(0, ray_length, 5):
                rx = self.x + d * math.cos(ray_angle)
                ry = self.y + d * math.sin(ray_angle)
                min_x, min_y, max_x, max_y = bounds
                if not (min_x <= rx <= max_x and min_y <= ry <= max_y):
                    results.append(d)
                    break
            else:
                results.append(ray_length)
        return results

    def get_state(self, bounds=(0, 0, 800, 600)):
        # State: [sensor1, sensor2, ..., velocity, angle]
        sensors = self.cast_sensor_rays(bounds)
        return np.array(sensors + [self.velocity, self.angle])
