from opendlp.regex_generation.regex_tree.function_set import BinaryOperator, Quantifier
from opendlp.regex_generation.config.conf import RegexFlavour
from opendlp.regex_generation.regex_tree import RegexContext

class Or(BinaryOperator):

    def is_valid(self):
        if isinstance(self.get_left(), Quantifier) or \
            isinstance(self.get_right(), Quantifier):
            return False
        return self.get_left().is_valid() and self.get_right().is_valid()

    def form(self, string, flavour=RegexFlavour.Python, context=RegexContext()):
        if isinstance(self.parent, Quantifier):
            string += "(?:"
        string = self.get_left().form(string, flavour, context)
        string += '|'
        string = self.get_right().form(string, flavour, context)
        if isinstance(self.parent, Quantifier):
            string += ")"
        return string

    def build_copy(self):
        return Or()