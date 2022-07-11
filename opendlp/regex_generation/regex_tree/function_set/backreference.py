from opendlp.regex_generation.regex_tree import Node
from opendlp.regex_generation.config.conf import RegexFlavour
from opendlp.regex_generation.regex_tree import RegexContext

class Backreference(Node):
    def __init__(self, value:int):
        super().__init__()
        self.__value = value

    @property
    def value(self):
        return self.__value

    def get_min_children_count(self):
        return 0

    def get_max_children_count(self):
        return 0

    def clone_tree(self):
        return Backreference(self.value)

    def is_valid(self):
        return True

    def form(self, string, flavour=RegexFlavour.Python, context=RegexContext()):
        string += str(int(self.value))
        return string

    def __eq__(self, other):
        if isinstance(other, Backreference):
            return other.value == self.value
        else:
            return False

    def __hash__(self):
        return hash(self.value)