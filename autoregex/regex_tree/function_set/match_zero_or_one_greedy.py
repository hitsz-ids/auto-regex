from autoregex.regex_tree.function_set import Quantifier
from autoregex.config.conf import RegexFlavour
from autoregex.regex_tree import RegexContext

class MatchZeroOrOneGreedy(Quantifier):

    def form(self, string, flavour=RegexFlavour.Python, context=RegexContext()):
        string = self.children[0].form(string, flavour, context)
        string += "?"
        return string

    def build_copy(self):
        return MatchZeroOrOneGreedy()