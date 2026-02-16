try:
    import pygame
except Exception:
    pygame = None

import math
import numpy as np
from .brain import Brain


class Car:
    def __init__(self, x, y):
        # Position
        self.x = x
        self.y = y
        self.start_x = x
        self.start_y = y

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
        self.max_age = 2000  # Increased max age for longer episodes
        self.distance_traveled = 0
        self.wall_collisions = 0

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
        prev_x, prev_y = self.x, self.y
        self.x += self.velocity * math.cos(rad)
        self.y += self.velocity * math.sin(rad)
        
        # Track distance traveled
        dx = self.x - prev_x
        dy = self.y - prev_y
        self.distance_traveled += math.sqrt(dx**2 + dy**2)

        # Collision detection with boundaries
        min_x, min_y, max_x, max_y = bounds
        if not (min_x <= self.x <= max_x and min_y <= self.y <= max_y):
            self.wall_collisions += 1
            self.alive = False

        # Age / fitness updates
        self.age += 1
        
        # Get sensor readings to reward smart navigation
        ray_length = 150
        sensors = self.cast_sensor_rays(bounds, num_rays=5, ray_length=ray_length)
        # Reward: cars that navigate (use steering) to avoid obstacles
        min_sensor = min(sensors) if sensors else ray_length
        sensor_reward = (min_sensor / (ray_length or 1)) * 10  # Bonus for staying away from walls
        
        # Fitness: distance + age + smart navigation - collision penalty
        self.fitness = (self.distance_traveled + 
                       (self.age * 0.3) + 
                       sensor_reward -
                       (self.wall_collisions * 100))

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
