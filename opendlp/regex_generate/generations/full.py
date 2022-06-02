
class Full:
    def __init__(self, max_depth, node_factory):
        self.max_depth = max_depth
        self.node_factory = node_factory

    def generate(self, population_size):
        """
        generate regex trees with fixed depth.
        @param population_size: tree nums to be generate
        @return:
        """
        raise NotImplementedError
