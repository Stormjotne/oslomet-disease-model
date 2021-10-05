

class Individual:
    """
    Use this class initialize model individuals.
    """

    def __init__(self, genotype):
        """
        Put any declarations of object fields/variables in this method.
        :param genome:
        """
        self.genotype = genotype
        self.phenotype = None
        self.fitness = None
        self.model = None


#   Use this conditional to test the class by running it "standalone".
if __name__ == "__main__":
    pass
