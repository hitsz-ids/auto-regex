from opendlp.regex_generation.regex_tree import Node
from opendlp.regex_generation.config.conf import RegexFlavour
from opendlp.regex_generation.regex_tree import RegexContext

class RegexRange(Node):
    def __init__(self, value:str):
        super().__init__()
        self.__value = value

    @property
    def value(self):
        return self.__value

    def is_character_class(self):
        return True

    def get_min_children_count(self):
        return 0

    def get_max_children_count(self):
        return 0

    def clone_tree(self):
        return RegexRange(self.value)

    def is_valid(self):
        # 只有在ListMatch或ListNotMatch中才有效。
        return False

    def form(self, string, flavour=RegexFlavour.Python, context=RegexContext()):
        return string + self.value

    def __eq__(self, other):
        if isinstance(other, RegexRange):
            return other.value == self.value
        else:
            return False

    def __hash__(self):
        return hash(self.value)