import random

def crossover(parent1, parent2, fitness1, fitness2, crossover_point, max_ports_per_station):
    """
    Combines two parent solutions to generate an offspring using partial crossover. 
    To generate better offspring, if the crossover point is not equal to 0.5, 
    when combining the genes of the parents, a larger number of genes are taken from the parent with better fitness score.
    Returns: dict (a new solution formed by combining parts of both parents)
    """
    cs_list_1, cs_list_2 = list(parent1.keys()), list(parent2.keys())

    if fitness1 < fitness2:
        num_of_genes1 = int(len(cs_list_1)*max(crossover_point, 1-crossover_point))
        num_of_genes2 = int(len(cs_list_2)*min(crossover_point, 1-crossover_point))
    else:
        num_of_genes1 = int(len(cs_list_1)*min(crossover_point, 1-crossover_point))
        num_of_genes2 = int(len(cs_list_2)*max(crossover_point, 1-crossover_point))

    genes_from_parent1 = random.sample(cs_list_1, k=num_of_genes1)
    genes_from_parent2 = random.sample(cs_list_2, k=num_of_genes2)

    child = {}

    # Genes from parent1
    for cs in genes_from_parent1:
        child[cs] = parent1[cs]

    # Genes from parent2 (merging genes)
    for cs in genes_from_parent2:
        if cs in child:
            child[cs] = min(max_ports_per_station, child[cs] + parent2[cs])
        else:
            child[cs] = parent2[cs]

    return child
