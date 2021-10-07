"""

"""
from random import random, uniform, choice, shuffle


class Genome:
    """
    Use this class initialize an individual's genome.
    """

    def __init__(self, mutation_probability, genome_length=None, input_genes=None, input_genomes=None):
        """
        Put any declarations of object fields/variables in this method.
        :param mutation_probability:
        :type mutation_probability:
        :param genome_length:
        :type genome_length:
        :param input_genes:
        :type input_genes:
        :param input_genomes:
        :type input_genomes:
        """
        self.mutation_probability = mutation_probability
        #   If genome length is provided, create new genes.
        if genome_length:
            self.genome_length = genome_length
            self.genes = self.normalized_genes()
        #   If input genes are provided, make the Genome with the input genes.
        elif input_genes:
            self.genes = self.copy_genes(input_genes, )
        elif input_genomes:
            self.genes = self.uniform_zip_genes(input_genomes[0], input_genomes[1])
            
    def normalized_genes(self):
        """
        Create a list of random values between 0 and 1.
        :return:
        :rtype:
        """
        return [random() for i in range(self.genome_length)]
    
    def uniform_zip_genes(self, input_genes_one, input_genes_two):
        """
        Uniform combination of two parent genomes with chance of mutation.
        :param input_genes_one:
        :type input_genes_one:
        :param input_genes_two:
        :type input_genes_two:
        :return:
        :rtype:
        """
        genes = []
        for gene_one, gene_two in zip(input_genes_one, input_genes_two):
            genes.append(self.normalized_medium_mutation() if random() < self.mutation_probability else choice((gene_one, gene_two)))
        return genes
        
    def copy_genes(self, input_genes):
        """
        Copy genes with chance of mutation.
        :param input_genes:
        :type input_genes:
        :return:
        :rtype:
        """
        genes = []
        for gene in input_genes:
            genes.append(self.normalized_medium_mutation() if random() < self.mutation_probability else gene)
        return genes
        
    @staticmethod
    def normalized_medium_mutation():
        """
        Replace existing gene with a new one entirely.
        :return:
        :rtype:
        """
        return random()
        
    @staticmethod
    def normalized_soft_mutation(input_gene):
        """
        Update the existing gene within a limit.
        [0,0.25], <0.25, 0.75>, [0.75, 1.0>
        :param input_gene:
        :type input_gene:
        :return:
        :rtype:
        """
        if input_gene <= 0.25:
            return uniform(0, 0.5)
        elif 0.25 < input_gene < 0.75:
            return uniform(0.25, 0.75)
        elif input_gene >= 0.75:
            return uniform(0.5, 1)


#   Use this conditional to test the class by running it "standalone".
if __name__ == "__main__":
    pass
