import numpy as np

def select_parents(population, fitness, num_of_parents):
    """
    Selects a subset of the population to serve as parents using fitness-proportional selection.
    Returns: list of selected parent solutions.
    """
    # Invert fitness values (since lower fitness is better)
    
    adjusted_fitness = [1/f for f in fitness]

    total_adjusted_fitness = sum(adjusted_fitness)
    probabilities = [solution_fitness/total_adjusted_fitness for solution_fitness in adjusted_fitness]

    indices = np.random.choice(len(population), size=num_of_parents, p=probabilities, replace=True)
    parents = [population[i] for i in indices]
    parents_fitness = [fitness[i] for i in indices]
    return parents, parents_fitness