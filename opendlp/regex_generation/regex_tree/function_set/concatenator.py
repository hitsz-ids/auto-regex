from opendlp.regex_generation.config.conf import RegexFlavour
from opendlp.regex_generation.regex_tree import RegexContext
from opendlp.regex_generation.regex_tree.function_set import BinaryOperator


class Concatenator(BinaryOperator):

    def is_valid(self):
        from opendlp.regex_generation.regex_tree.function_set import Or

        if isinstance(self.get_left(), Or) or isinstance(self.get_right(), Or):
            return False
        return self.get_left().is_valid() and self.get_right().is_valid()

    def form(self, string, flavour=RegexFlavour.Python, context=RegexContext()):
        string = self.get_left().form(string, flavour, context)
        string = self.get_right().form(string, flavour, context)
        return string

    def build_copy(self):
        return Concatenator()
