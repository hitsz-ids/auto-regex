
class NodeFactory:
    def __init__(self):
        self.terminal_set = []
        self.function_set = []

    def build_terminal_set(self, bpe_tokens):
        """
        load default terminal set
        @return:
        """
        raise NotImplementedError

    def build_function_set(self):
        """
        load default terminal set
        @return:
        """
        raise NotImplementedError

    def build(self, bpe_tokens=None):
        self.build_terminal_set(bpe_tokens)
        self.build_function_set()