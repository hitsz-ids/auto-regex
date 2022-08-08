from opendlp.regex_generation.regex_tree.function_set import Quantifier
from opendlp.regex_generation.config.conf import RegexFlavour
from opendlp.regex_generation.regex_tree import RegexContext

class MatchZeroOrOne(Quantifier):

    def form(self, string, flavour=RegexFlavour.Python, context=RegexContext()):
        from opendlp.regex_generation.regex_tree.function_set import Group, NonCapturingGroup

        child = self.children[0]
        tmp = ''
        _ = context.inc_groups()
        tmp = child.form(tmp, flavour, context)
        l = len(tmp)-1 if child.is_escaped() else len(tmp)
        group = l>1 and not child.is_character_class() and \
                not(isinstance(child, Group)) and \
                not(isinstance(child, NonCapturingGroup))

        # TODO:这块之后得研究一下
        if group:
            string += "(?:"
            string += tmp
            string += ")"
        else:
            string += tmp
        string += "?"
        return string

    def build_copy(self):
        return MatchZeroOrOne()