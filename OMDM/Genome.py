"""

"""
from random import random


class Genome:
    """
    Use this class initialize an individual's genome.
    """

    def __init__(self, genome_length=None, input_genes=None):
        """
        Put any declarations of object fields/variables in this method.
        @param genome_size:
        @type genome_size:
        """
        #   If genome length is provided, create new genes.
        if genome_length:
            self.genes = [random() for i in range(genome_length)]
        #   If input genes are provided, make the Genome with the input genes.
        elif input_genes:
            self.genes = input_genes


#   Use this conditional to test the class by running it "standalone".
if __name__ == "__main__":
    pass
