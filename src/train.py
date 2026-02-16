import time
from src.population import Population
from src.storage import init_db, save_generation, save_best_brain


def run_training(pop_size=50):
    init_db()

    population = Population(size=pop_size)

    while True:
        population.update()

        if population.all_dead():
            best_fitness = max(car.fitness for car in population.cars)
            print(f"Generation: {population.generation} | Best Fitness: {best_fitness}")
            save_generation(population.generation, best_fitness)
            # save best brain weights
            save_best_brain(population.generation, population.cars[0].brain)
            population.evolve()

        # Small sleep to avoid busy loop; training is step-based so this is fine headless
        time.sleep(0.001)


if __name__ == "__main__":
    run_training()
from src.environment import Environment
from src.population import Population
import csv

env = Environment()
population = Population(size=100, env=env)

for generation in range(50):

    print(f"\nGeneration {generation}")
    print(f"Cars in population: {len(population.cars)}")

    for car in population.cars:
        env.reset()
        for step in range(500):
            action = car.think()
            env.update(action[0], action[1])
            car.fitness += car.velocity

            if env.done:
                break

    population.evaluate()

    best_fitness = max(car.fitness for car in population.cars)
    avg_fitness = sum(car.fitness for car in population.cars) / len(population.cars)

    print(f"Best fitness: {best_fitness}")
    print(f"Average fitness: {avg_fitness}")

    # Save logs
    with open("results/logs.csv", "a", newline="") as f:
        writer = csv.writer(f)
        writer.writerow([generation, best_fitness, avg_fitness])

    population.reproduce(top_k=10)

