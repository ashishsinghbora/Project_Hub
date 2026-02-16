"""
Headless training demo—runs a few generations and shows fitness progress.
"""
import time
from src.population import Population


class SimpleEnv:
    """Minimal environment for headless training."""
    def __init__(self, width=1600, height=1200):
        self.width = width
        self.height = height


def run_demo(pop_size=10, num_gens=5, steps_per_gen=200):
    """Run headless training for demo purposes."""
    env = SimpleEnv(width=800, height=600)
    population = Population(size=pop_size, env=env)
    
    print(f"Starting demo: {pop_size} cars, {num_gens} generations, {steps_per_gen} steps/gen\n")
    
    for gen in range(num_gens):
        # Run population for a fixed number of steps
        for step in range(steps_per_gen):
            population.update()
            
            # Check if all dead and evolve
            if population.all_dead():
                break
        
        # Report fitness
        fitnesses = [car.fitness for car in population.cars]
        best_fitness = max(fitnesses) if fitnesses else 0
        avg_fitness = sum(fitnesses) / len(fitnesses) if fitnesses else 0
        
        print(f"Generation {population.generation:3d} | Best: {best_fitness:8.2f} | Avg: {avg_fitness:8.2f}")
        
        # Evolve for next generation
        population.evolve()
    
    print("\nDemo complete!")


if __name__ == "__main__":
    run_demo(pop_size=25, num_gens=40, steps_per_gen=400)
