import time
from src.environment import Environment
from src.population import Population
from src.storage import init_db, save_generation, save_best_brain


def run_training(pop_size=50):
    init_db()

    env = Environment()
    population = Population(size=pop_size, env=env)

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

