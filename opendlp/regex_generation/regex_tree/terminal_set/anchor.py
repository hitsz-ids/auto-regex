from opendlp.regex_generation.regex_tree import Node
from opendlp.regex_generation.config.conf import RegexFlavour
from opendlp.regex_generation.regex_tree import RegexContext

class Anchor(Node):
    def __init__(self, value):
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
        return Anchor(self.value)

    def is_valid(self):
        return True

    def form(self, string, flavour=RegexFlavour.Python, context=RegexContext()):
        return string + self.value

    def __eq__(self, other):
        if isinstance(other, Anchor):
            return other.value == self.value
        else:
            return False

    def __hash__(self):
        return hash(self.value)