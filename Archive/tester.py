if __name__ == "__main__":
    from OMDM.Individual import Individual
    from OMDM.Fitness import population_spread_fitness
    from OMDM.Model import Model
    new_individual = Individual(0.2, genome_length=7)
    new_model = Model(new_individual.genome.genome,100,visualize=True)
    new_individual.phenotype = new_model.simulate()
    print(new_individual.phenotype)
    new_individual.fitness = population_spread_fitness(new_individual.phenotype, 5000, 1, 1)
    print(new_individual.fitness)