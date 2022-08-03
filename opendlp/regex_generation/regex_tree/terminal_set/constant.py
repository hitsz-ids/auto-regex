from opendlp.regex_generation.regex_tree import Node
from opendlp.regex_generation.config.conf import RegexFlavour
from opendlp.regex_generation.regex_tree import RegexContext

class Constant(Node):
    allowed_classes = {"\\w", "\\d", ".", "\\b", "\\s"}

    def __init__(self, value: str):
        super().__init__()
        self.__value = value
        self.is_char_class = value in Constant.allowed_classes
        self.is_escape = value.startswith('\\')

    @property
    def value(self):
        return self.__value

    def is_character_class(self):
        return self.is_char_class

    def is_escaped(self):
        return self.is_escape

    def get_min_children_count(self):
        return 0

    def get_max_children_count(self):
        return 0

    def clone_tree(self):
        return Constant(self.value)

    def is_valid(self):
        return True

    def form(self, string, flavour=RegexFlavour.Python, context=RegexContext()):
        return string + self.value

    def __eq__(self, other):
        if isinstance(other, Constant):
            return other.value == self.value
        else:
            return False

    def __hash__(self):
        return hash(self.value)

