import numpy as np
import time

# Import the necessary components from your other project files
from genetic_algorithm import GeneticAlgorithm
from benchmark_functions import FUNCTIONS

# Experiment Configuration 
NUM_RUNS = 10  # Number of times to run the GA for each function to get an average.
MAX_GENERATIONS = 500
POPULATION_SIZE = 100
DIMENSIONS_TO_TEST = [5, 10]

def run_experiment(func_name, dimension):
    """
    Runs the Genetic Algorithm for a given function and dimension for NUM_RUNS times.
    
    Args:
        func_name (str): The name of the benchmark function.
        dimension (int): The dimension (5 or 10).
        
    Returns:
        tuple: A tuple containing (best_fitness, worst_fitness, mean_fitness, std_dev).
    """
    results = []
    function_info = FUNCTIONS[func_name]
    
    print(f"  Running {func_name} in {dimension}D ({NUM_RUNS} times)...")
    
    for i in range(NUM_RUNS):
        # Initialize the GA instance
        ga = GeneticAlgorithm(
            objective_func=function_info["func"],
            bounds=function_info["bounds"],
            dimension=dimension,
            pop_size=POPULATION_SIZE
        )
        
        # Run the GA for the specified number of generations
        for _ in range(MAX_GENERATIONS):
            ga.run_generation()
            
        # Store the best fitness found in this run
        results.append(ga.best_fitness)
        print(f"    Run {i+1}/{NUM_RUNS} complete. Best Fitness: {ga.best_fitness:.4f}")

    # Calculate statistics over all the runs
    best_fitness = np.min(results)
    worst_fitness = np.max(results)
    mean_fitness = np.mean(results)
    std_dev = np.std(results)
    
    return best_fitness, worst_fitness, mean_fitness, std_dev

def main():
    """
    Main function to run all experiments and print the results table.
    """
    print("Starting experiment to generate results table...")
    start_time = time.time()
    
    # Print Table Header 
    print("\n" + "="*85)
    print("### Genetic Algorithm Performance Results")
    print(f"*(Based on {NUM_RUNS} runs per experiment, {MAX_GENERATIONS} generations, {POPULATION_SIZE} population size)*")
    print("| Function      | Dim | Best Fitness      | Worst Fitness     | Mean Fitness      | Std Deviation     |")
    print("|---------------|-----|-------------------|-------------------|-------------------|-------------------|")

    # Run Experiments and Print Table Rows 
    for func_name in FUNCTIONS.keys():
        for dim in DIMENSIONS_TO_TEST:
            best, worst, mean, std = run_experiment(func_name, dim)
            
            # Print the formatted row for the Markdown table
            print(f"| {func_name:<13} | {dim:<3} | {best:<17.6f} | {worst:<17.6f} | {mean:<17.6f} | {std:<17.6f} |")

    end_time = time.time()
    print("="*85)
    print(f"\nAll experiments completed in {end_time - start_time:.2f} seconds.")

if __name__ == "__main__":
    main()