from src.car import Car


class Population:
    def __init__(self, size, spawn_x=400, spawn_y=300):
        self.size = size
        self.spawn_x = spawn_x
        self.spawn_y = spawn_y
        self.cars = [Car(spawn_x, spawn_y) for _ in range(size)]
        self.generation = 1

    def update(self, bounds=(0, 0, 800, 600)):
        for car in self.cars:
            if getattr(car, "alive", True):
                throttle, steering = car.think()
                car.update(throttle, steering, bounds)

    def all_dead(self):
        return all(not getattr(car, "alive", False) for car in self.cars)

    def evolve(self):
        # Sort by fitness descending
        self.cars.sort(key=lambda c: c.fitness, reverse=True)

        best = self.cars[0]

        new_cars = []

        # Elitism: keep exact copy of best
        child = Car(self.spawn_x, self.spawn_y)
        child.brain = best.brain.copy()
        new_cars.append(child)

        # Fill rest with mutated copies
        for _ in range(self.size - 1):
            child = Car(self.spawn_x, self.spawn_y)
            child.brain = best.brain.copy()
            child.brain.mutate(0.2)
            new_cars.append(child)

        self.cars = new_cars
        self.generation += 1
from src.car import Car
import numpy as np

class Population:
    def __init__(self, size, env):
        self.size = size
        self.env = env
        self.cars = [Car(env.start_x, env.start_y) for _ in range(size)]
        self.generation = 1

    def evaluate(self):
        for car in self.cars:
            car.fitness = car.distance_traveled

    def select_best(self, top_k=10):
        self.cars.sort(key=lambda c: c.fitness, reverse=True)
        return self.cars[:top_k]

    def reproduce(self, top_k=10):
        best = self.select_best(top_k)
        new_cars = []

        for parent in best:
            new_cars.append(parent)

        while len(new_cars) < self.size:
            parent = np.random.choice(best)
            child = Car(self.env.start_x, self.env.start_y)
            child.brain = parent.brain.copy()
            child.brain.mutate()
            new_cars.append(child)

        self.cars = new_cars
        self.generation += 1
