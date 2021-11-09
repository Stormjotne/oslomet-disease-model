"""

"""
from .Genome import Genome


class Individual:
    """
    Use this class initialize model individuals.
    """

    def __init__(self, mutation_probability, genome_length=None, input_genes=None, input_genomes=None,
                 soft_mutation=False):
        """
        Put any declarations of object fields/variables in this method.
        :param genome_length:
        """
        self.mutation_probability = mutation_probability
        self.soft_mutation = soft_mutation
        #   If genome length is provided, create a new genome.
        if genome_length:
            self.genome_length = genome_length
            self.genome = Genome(self.mutation_probability, genome_length=genome_length)
        #   If an input genome is provided, base the new Genome on the input.
        elif input_genes:
            self.genome = self.clone(input_genes)
        #   If two input genomes are provided, base the new Genome on those two inputs.
        elif input_genomes:
            self.genome = self.crossover(input_genomes[0], input_genomes[1])
        #   Declare other fields.
        self.phenotype = None
        self.fitness = None
        self.model = None
        
    def clone(self, parent_genes):
        """
        Create new genome from parent's genome with a chance of mutation.
        :param parent_genes:
        :type parent_genes:
        """
        return Genome(self.mutation_probability,
                      input_genome=parent_genes,
                      soft_mutation=self.soft_mutation)
        
    def crossover(self, parent_genome_one, parent_genome_two):
        """
        Create new genome from two parents' genomes with a chance of mutation.
        :param parent_genome_one:
        :param parent_genome_two:
        """
        return Genome(self.mutation_probability,
                      input_genomes=(parent_genome_one, parent_genome_two),
                      soft_mutation=self.soft_mutation)


#   Use this conditional to test the class by running it "standalone".
if __name__ == "__main__":
    pass
