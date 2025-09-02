# This file defines the GeneticAlgorithm class, which encapsulates the core
# logic for the optimization process. It is designed to be independent of the
# GUI and the specific benchmark functions, making it reusable.

import numpy as np
import random

class GeneticAlgorithm:
    """
    A class to encapsulate the Genetic Algorithm logic.
    """
    def __init__(self, objective_func, bounds, dimension, pop_size=1000, crossover_rate=0.8, mutation_rate=0.2):
        """
        Initializes the Genetic Algorithm optimizer.
        Args:
            objective_func (function): The function to be minimized.
            bounds (tuple): A tuple (min_val, max_val) for the search space.
            dimension (int): The number of dimensions for the problem.
            pop_size (int): The size of the population.
            crossover_rate (floa`t): The probability of crossover.
            mutation_rate (float): The probability of mutation for each gene.
        """
        self.objective_func = objective_func
        self.bounds = bounds
        self.dimension = dimension
        self.pop_size = pop_size
        self.crossover_rate = crossover_rate
        self.mutation_rate = mutation_rate
        
        # Initialize the population
        self.population = self._initialize_population()
        self.best_solution = None
        self.best_fitness = float('inf')

    def _initialize_population(self):
        """Creates the initial population as a numpy array."""
        min_b, max_b = self.bounds
        return min_b + (max_b - min_b) * np.random.rand(self.pop_size, self.dimension)

    def _evaluate_fitness(self):
        """Calculates the fitness for each individual in the population."""
        return np.array([self.objective_func(ind) for ind in self.population])

    def _selection(self, fitness):
        """
        Selects parents for the next generation using tournament selection.
        This method is generally more efficient and less prone to premature
        convergence than other methods like roulette wheel.
        """
        parents = []
        for _ in range(self.pop_size):
            # Select two random individuals for the tournament
            i, j = np.random.randint(0, self.pop_size, 2)
            # The individual with the better (lower) fitness wins
            if fitness[i] < fitness[j]:
                parents.append(self.population[i])
            else:
                parents.append(self.population[j])
        return np.array(parents)

    def _crossover(self, parents):
        """
        Performs crossover on the selected parents to create offspring.
        Uses a simple one-point crossover.
        """
        offspring = np.empty_like(parents)
        for i in range(0, self.pop_size, 2):
            p1, p2 = parents[i], parents[i+1]
            if random.random() < self.crossover_rate:
                # Perform crossover
                crossover_point = random.randint(1, self.dimension - 1)
                offspring[i] = np.concatenate([p1[:crossover_point], p2[crossover_point:]])
                offspring[i+1] = np.concatenate([p2[:crossover_point], p1[crossover_point:]])
            else:
                # No crossover, parents move to next generation
                offspring[i], offspring[i+1] = p1, p2
        return offspring

    def _mutation(self, offspring):
        """

        Applies mutation to the offspring.
        Adds a small random value from a Gaussian distribution to each gene
        based on the mutation probability.
        """
        for i in range(len(offspring)):
            for j in range(self.dimension):
                if random.random() < self.mutation_rate:
                    # Add a random value from a normal distribution
                    offspring[i][j] += np.random.normal(0, 0.1)
                    # Clip the value to stay within the defined bounds
                    offspring[i][j] = np.clip(offspring[i][j], self.bounds[0], self.bounds[1])
        return offspring

    def run_generation(self):
        """
        Executes one full generation of the Genetic Algorithm.
        This includes evaluation, selection, crossover, and mutation.
        """
        # 1. Evaluate fitness of the current population
        fitness = self._evaluate_fitness()
        
        # 2. Update the best solution found so far
        current_best_idx = np.argmin(fitness)
        if fitness[current_best_idx] < self.best_fitness:
            self.best_fitness = fitness[current_best_idx]
            self.best_solution = self.population[current_best_idx]
            
        # 3. Select parents for the next generation
        parents = self._selection(fitness)
        
        # 4. Create offspring through crossover
        offspring = self._crossover(parents)
        
        # 5. Apply mutation to the offspring
        mutated_offspring = self._mutation(offspring)
        
        # 6. Replace the old population with the new generation
        self.population = mutated_offspring
        
        # Return current bests for UI update
        return self.best_solution, self.best_fitness