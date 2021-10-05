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
        @param genome_length:
        @type genome_length:
        @param input_genes:
        @type input_genes:
        """
        self.genome_length = genome_length
        #   If genome length is provided, create new genes.
        if genome_length:
            self.genes = self.normalized_genome()
        #   If input genes are provided, make the Genome with the input genes.
        elif input_genes:
            self.genes = input_genes
            
    def normalized_genome(self):
        """
        Create a list of random values between 0 and 1.
        @return:
        @rtype:
        """
        genes = [random() for i in range(self.genome_length)]
        return genes


#   Use this conditional to test the class by running it "standalone".
if __name__ == "__main__":
    pass
