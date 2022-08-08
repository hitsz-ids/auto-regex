from opendlp.regex_generation.regex_tree.function_set import Lookaround
from opendlp.regex_generation.config.conf import RegexFlavour
from opendlp.regex_generation.regex_tree import RegexContext

class LookaheadNegative(Lookaround):
    def form(self, string, flavour=RegexFlavour.Python, context=RegexContext()):
        string += "(?!"
        string = self.children[0].form(string, flavour, context)
        string += ")"
        return string

    def build_copy(self):
        return LookaheadNegative()