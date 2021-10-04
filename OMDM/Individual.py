"""

"""
from .Genome import Genome


class Individual:
    """
    Use this class initialize model individuals.
    """

    def __init__(self, genome_length=None, input_genome=None):
        """
        Put any declarations of object fields/variables in this method.
        :param genome_length:
        """
        #   If genome length is provided, create a new genome.
        if genome_length:
            self.genome = Genome(genome_length)
        #   If an input genome is provided, base the new Genome on the input.
        elif input_genome:
            self.genome = Genome(input_genes=input_genome)
        #   Declare other fields.
        self.phenotype = None
        self.fitness = None
        self.model = None


#   Use this conditional to test the class by running it "standalone".
if __name__ == "__main__":
    pass
