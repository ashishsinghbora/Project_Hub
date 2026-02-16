from src.car import Car
import numpy as np


class Population:
    """Population manager used by training.

    Expected to be constructed with `Population(size, env)` where `env` is an
    `Environment` instance exposing `width` and `height`.
    """

    def __init__(self, size, env):
        self.size = size
        self.env = env
        spawn_x = env.width // 2
        spawn_y = env.height // 2
        self.cars = [Car(spawn_x, spawn_y) for _ in range(size)]
        self.generation = 1
        self.best_fitness_history = [0]  # Track best fitness per generation
        self.stale_gens = 0  # Count generations without improvement

    def update(self):
        bounds = (0, 0, self.env.width, self.env.height)
        for car in self.cars:
            if getattr(car, "alive", True):
                throttle, steering = car.think(bounds)
                car.update(throttle, steering, bounds)

    def all_dead(self):
        return all(not getattr(car, "alive", False) for car in self.cars)

    def evolve(self):
        # Sort by fitness descending
        self.cars.sort(key=lambda c: c.fitness, reverse=True)

        best_fitness = self.cars[0].fitness
        self.best_fitness_history.append(best_fitness)
        
        # Track stale generations (no improvement)
        if best_fitness <= self.best_fitness_history[-2]:
            self.stale_gens += 1
        else:
            self.stale_gens = 0
        
        # Adaptive mutation rate: increase if no improvement
        base_mutation = 0.3
        stale_boost = min(0.4, self.stale_gens * 0.05)  # Up to +0.4 mutation rate
        
        # Tournament selection: select top 30% to breed
        elite_count = max(2, self.size // 3)
        elite = self.cars[:elite_count]

        new_cars = []

        # Elitism: keep best 2 unchanged
        for i in range(min(2, elite_count)):
            child = Car(self.env.width // 2, self.env.height // 2)
            child.brain = elite[i].brain.copy()
            new_cars.append(child)

        # Fill rest with tournament-selected crosses + adaptive mutations
        while len(new_cars) < self.size:
            # Tournament: randomly pick 2 from elite
            parent1 = elite[np.random.randint(0, len(elite))]
            parent2 = elite[np.random.randint(0, len(elite))]
            
            child = Car(self.env.width // 2, self.env.height // 2)
            
            # Crossover: blend weights
            if np.random.rand() < 0.5:
                child.brain = parent1.brain.copy()
            else:
                child.brain = parent2.brain.copy()
            
            # Adaptive mutation: higher when stale
            mutation_rate = base_mutation + stale_boost + np.random.rand() * 0.2
            child.brain.mutate(mutation_rate)
            
            new_cars.append(child)

        self.cars = new_cars
        self.generation += 1
