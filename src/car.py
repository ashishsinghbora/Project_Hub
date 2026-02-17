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
        self.steering_angle = 0  # Current steering angle (for smoothing)

        # Physics constants - realistic RC car behavior
        self.acceleration_rate = 0.5  # Progressive acceleration
        self.max_speed = 12  # Realistic top speed
        self.max_reverse_speed = 5  # Reverse is much slower
        self.friction = 0.08  # Tire rolling resistance
        self.air_resistance = 0.02  # Aerodynamic drag
        self.braking_force = 0.25  # Strong braking
        self.steering_limit = 35  # Max steering angle in degrees
        self.steering_smoothing = 0.8  # Faster servo response (80% per frame = very responsive)

        # Visual
        self.width = 60
        self.height = 30
        self.color = (200, 0, 0)

        # Physical dimensions
        self.wheelbase = 35  # Distance between front and rear axles
        self.weight = 1.0  # For momentum calculations
        
        # Traction circle limits - can't do full acceleration AND full steering
        self.max_traction = 1.0  # Total available grip
        
        # AI
        self.brain = Brain()
        self.fitness = 0
        self.alive = True
        self.age = 0
        self.max_age = 2000
        self.distance_traveled = 0
        self.wall_collisions = 0

    def update(self, accelerate, steer, bounds=(0, 0, 800, 600)):
        # ===== ACCELERATION & BRAKING =====
        if accelerate > 0:
            throttle_force = accelerate * self.acceleration_rate
            speed_factor = 1.0 - (abs(self.velocity) / self.max_speed) * 0.4
            self.velocity += throttle_force * speed_factor
        elif accelerate < 0:
            self.velocity += accelerate * self.braking_force
        
        # Friction and air resistance
        friction_force = self.friction + (self.air_resistance * abs(self.velocity))
        self.velocity *= (1 - friction_force)

        # Clamp speeds
        self.velocity = max(-self.max_reverse_speed, min(self.velocity, self.max_speed))

        # ===== STEERING - SIMPLE AND EFFECTIVE =====
        # Smooth steering input (servo response)
        target_steering_angle = steer * self.steering_limit
        self.steering_angle += (target_steering_angle - self.steering_angle) * self.steering_smoothing

        # Apply steering rotation - works at all speeds including stopped
        # Direct proportional turning: steering_angle drives rotation rate
        steering_fraction = self.steering_angle / self.steering_limit  # -1.0 to 1.0
        
        if abs(self.velocity) > 0.05:
            # Moving: turn proportional to velocity and steering
            turn_rate = steering_fraction * self.velocity * 0.25
            self.angle += turn_rate
        else:
            # Standing still: can still turn in place at reduced rate
            turn_rate = steering_fraction * 1.5
            self.angle += turn_rate
        
        # ===== POSITION UPDATE =====
        rad = math.radians(self.angle)
        
        prev_x, prev_y = self.x, self.y
        self.x += self.velocity * math.cos(rad)
        self.y += self.velocity * math.sin(rad)
        
        # Distance tracking
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
