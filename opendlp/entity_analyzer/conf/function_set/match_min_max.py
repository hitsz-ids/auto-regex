from opendlp.regex_generation.regex_tree.function_set import TernaryOperator
from opendlp.regex_generation.regex_tree.terminal_set import Constant, Anchor
from opendlp.regex_generation.config.conf import RegexFlavour
from opendlp.regex_generation.regex_tree import RegexContext

class MatchMinMax(TernaryOperator):

    def is_valid(self):
        from opendlp.regex_generation.regex_tree.function_set import Concatenator,\
                                        MatchMinMaxGreedy, Lookaround, Quantifier

        first = self.get_first()
        valid_first = not(isinstance(first, Concatenator) or
                          isinstance(first, Quantifier) or
                          isinstance(first, MatchMinMax) or
                          isinstance(first, MatchMinMaxGreedy) or
                          isinstance(first, Anchor) or
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
        from opendlp.regex_generation.regex_tree.function_set import Group, NonCapturingGroup

        child = self.get_first()
        tmp = ''
        _ = context.inc_groups()
        tmp = child.form(tmp, flavour, context)
        l = len(tmp) - 1 if child.is_escaped() else len(tmp)
        group = l > 1 and not child.is_character_class() and \
                not (isinstance(child, Group)) and \
                not (isinstance(child, NonCapturingGroup))
        if group:
            string += "(?:"
            string += tmp
            string += ")"
        else:
            string += tmp
        string += "{"
        string += str(int(self.get_second().value))
        string += ","
        string += str(int(self.get_third().value))
        string +="}"
        return string

    def build_copy(self):
        return MatchMinMax()