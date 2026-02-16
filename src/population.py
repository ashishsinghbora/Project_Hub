from car import Car


class Population:
    def __init__(self, size, env, spawn_x=None, spawn_y=None):
        self.size = size
        self.env = env
        # default spawn in center of environment if not supplied
        if spawn_x is None:
            spawn_x = env.width // 2 if hasattr(env, "width") else 400
        if spawn_y is None:
            spawn_y = env.height // 2 if hasattr(env, "height") else 300

        self.spawn_x = spawn_x
        self.spawn_y = spawn_y
        self.cars = [Car(self.spawn_x, self.spawn_y) for _ in range(size)]
        self.generation = 1

    def update(self):
        bounds = (0, 0, getattr(self.env, "width", 800), getattr(self.env, "height", 600))
        for car in self.cars:
            if getattr(car, "alive", True):
                throttle, steering = car.think(bounds)
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
            # fallback mutate signature
            try:
                child.brain.mutate(0.2)
            except TypeError:
                child.brain.mutate()
            new_cars.append(child)

        self.cars = new_cars
        self.generation += 1

    # Optional compatibility methods from alternate API
    def evaluate(self):
        for car in self.cars:
            car.fitness = getattr(car, "distance_traveled", car.fitness)

    def select_best(self, top_k=10):
        self.cars.sort(key=lambda c: c.fitness, reverse=True)
        return self.cars[:top_k]

    def reproduce(self, top_k=10):
        best = self.select_best(top_k)
        new_cars = []

        for parent in best:
            new_cars.append(parent)

        import numpy as _np
        while len(new_cars) < self.size:
            parent = _np.random.choice(best)
            child = Car(self.spawn_x, self.spawn_y)
            child.brain = parent.brain.copy()
            try:
                child.brain.mutate()
            except TypeError:
                pass
            new_cars.append(child)

        self.cars = new_cars
        self.generation += 1
