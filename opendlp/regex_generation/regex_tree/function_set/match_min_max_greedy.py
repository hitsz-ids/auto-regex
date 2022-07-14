from opendlp.regex_generation.regex_tree.function_set import TernaryOperator
from opendlp.regex_generation.regex_tree.terminal_set import Constant
from opendlp.regex_generation.config.conf import RegexFlavour
from opendlp.regex_generation.regex_tree import RegexContext

class MatchMinMaxGreedy(TernaryOperator):

    def is_valid(self):
        from opendlp.regex_generation.regex_tree.function_set import Concatenator, \
                                                Lookaround, Quantifier, MatchMinMax

        first = self.get_first()
        valid_first = not(isinstance(first, Concatenator) or
                          isinstance(first, Quantifier) or
                          isinstance(first, MatchMinMax) or
                          isinstance(first, MatchMinMaxGreedy) or
                          isinstance(first, Lookaround)) and first.is_valid()

        second, third = self.get_second(), self.get_third()
        if isinstance(second, Constant) and isinstance(third, Constant):
            try:
                left_value = int(self.get_second().value)
                right_value = int(self.get_third().value)
            except ValueError:
                return False
            if left_value<0 or right_value<0:
                return False
            if left_value>right_value:
                return False
            return valid_first
        else:
            return False

    def form(self, string, flavour=RegexFlavour.Python, context=RegexContext()):
        string = self.get_first().form(string, flavour, context)
        string += "{"
        string += str(int(self.get_second().value))
        string += ","
        string += str(int(self.get_third().value))
        string += "}"
        return string

    def build_copy(self):
        return MatchMinMaxGreedy()