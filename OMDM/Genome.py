"""

"""
from random import random, uniform, choice, shuffle


class Genome:
    """
    Use this class initialize an individual's genome.
    Genome is the dictionary wrapper around the gene values.
    """

    def __init__(self, mutation_probability, genome_length=None, input_genome=None, input_genomes=None):
        """
        Put any declarations of object fields/variables in this method.
        :param mutation_probability:
        :type mutation_probability:
        :param genome_length:
        :type genome_length:
        :param input_genome:
        :type input_genome:
        :param input_genomes:
        :type input_genomes:
        """
        self.genome_labels = ["number_of_agents", "social_distancing", "hand_hygiene", "respiratory_hygiene",
            "face_masks", "face_shields", "key_object_disinfection", "surface_disinfection",
            "ventilation_of_indoor_spaces", "face_touching_avoidance", "test_based_screening",
            "vaccination", "cohort_size", "electives"]
        self.mutation_probability = mutation_probability
        #   If genome length is provided, create new genes.
        if genome_length:
            self.genome_length = genome_length
            normalized_genes = self.normalized_genes()
            self.genome = self.genes_to_genome(normalized_genes)
        #   If input genes are provided, make the Genome with the input genes.
        elif input_genome:
            copied_genes = self.copy_genes(input_genome)
            self.genome = self.genes_to_genome(copied_genes)
        elif input_genomes:
            uniform_zipped_genes = self.uniform_zip_genes(input_genomes[0], input_genomes[1])
            self.genome = self.genes_to_genome(uniform_zipped_genes)
            
    def genes_to_attributes(self, genes):
        """
        Create object attributes of genes with labels as field names.
        :param genes:
        :type genes:
        :return:
        :rtype:
        """
        pass
    
    def genes_to_genome(self, genes):
        """
        Create an ordered dictionary of genes with labels as keys.
        :param genes:
        :type genes:
        :return:
        :rtype:
        """
        return dict(zip(self.genome_labels, genes))

    @staticmethod
    def genome_to_genes(genome):
        """
        Unpack dictionary to manipulate gene values.
        :param genome:
        :type genome:
        :return:
        :rtype:
        """
        return list(genome.values())
        
    def normalized_genes(self):
        """
        Create a list of random values between 0 and 1.
        :return:
        :rtype:
        """
        return [random() for i in range(self.genome_length)]
        
    def copy_genes(self, input_genome):
        """
        Copy genes with chance of mutation.
        :param input_genome:
        :type input_genome:
        :return:
        :rtype:
        """
        genes = []
        #   Unpack dictionary to manipulate gene values.
        extracted_genes = self.genome_to_genes(input_genome)
        for gene in extracted_genes:
            genes.append(self.normalized_medium_mutation() if random() < self.mutation_probability else gene)
        return genes
    
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
        #   Unpack dictionary to manipulate gene values.
        extracted_genes_one = self.genome_to_genes(input_genes_one)
        extracted_genes_two = self.genome_to_genes(input_genes_two)
        for gene_one, gene_two in zip(extracted_genes_one, extracted_genes_two):
            genes.append(self.normalized_medium_mutation() if random() < self.mutation_probability else choice((gene_one, gene_two)))
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
    new_genome = Genome(0.20, genome_length=9)
    print(new_genome.genome)
    copied_genome = Genome(0.20, input_genome=new_genome.genome)
    print(copied_genome.genome)
    uniform_zipped_genome = Genome(0.20, input_genomes=(new_genome.genome, copied_genome.genome))
    print(uniform_zipped_genome.genome)
