from auto_regex.regex_tree.function_set.quantifier import Quantifier
from auto_regex.config.conf import RegexFlavour
from auto_regex.regex_tree import RegexContext

class MatchZeroOrMoreGreedy(Quantifier):

    def form(self, string, flavour=RegexFlavour.Python, context=RegexContext()):
        child = self.children[0]
        string = child.form(string, flavour, context)
        string += "*"
        return string

    def build_copy(self):
        return MatchZeroOrMoreGreedy()