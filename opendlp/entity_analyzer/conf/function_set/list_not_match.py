from opendlp.regex_generation.regex_tree.function_set import UnaryOperator
from opendlp.regex_generation.regex_tree.terminal_set import Constant, RegexRange
from opendlp.regex_generation.config.conf import RegexFlavour
from opendlp.regex_generation.regex_tree import RegexContext


class ListNotMatch(UnaryOperator):
    def is_valid(self):
        check_valid(self.children[0])

    def form(self, string, flavour=RegexFlavour.Python, context=RegexContext()):
        string += "[^"
        string = self.children[0].form(string, flavour, context)
        string += "]"
        return string

    def build_copy(self):
        return ListNotMatch()

    def is_character_class(self):
        return True


def check_valid(root):
    from opendlp.regex_generation.regex_tree.function_set import Concatenator

    if not (isinstance(root, Constant) or
            isinstance(root, RegexRange) or
            isinstance(root, Concatenator)):
        return False

    for child in root.children:
        if not check_valid(child):
            return False
    return True