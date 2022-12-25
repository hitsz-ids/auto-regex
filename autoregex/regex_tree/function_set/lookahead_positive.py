from autoregex.regex_tree.function_set import Lookaround
from autoregex.config.conf import RegexFlavour
from autoregex.regex_tree import RegexContext

class LookaheadPositive(Lookaround):
    def form(self, string, flavour=RegexFlavour.Python, context=RegexContext()):
        string += "(?="
        string = self.children[0].form(string, flavour, context)
        string += ")"
        return string

    def build_copy(self):
        return LookaheadPositive()