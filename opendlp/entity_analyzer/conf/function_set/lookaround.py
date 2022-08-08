from opendlp.regex_generation.regex_tree.function_set import UnaryOperator
from opendlp.regex_generation.regex_tree.terminal_set import RegexRange, Anchor

class Lookaround(UnaryOperator):
    def __init__(self):
        super().__init__()
        self.num_quantifier = 0
        self.has_only_min_max = True

    def is_valid(self):
        from opendlp.regex_generation.regex_tree.function_set import Backreference

        child = self.children[0]
        return not(isinstance(child, RegexRange) or
                   isinstance(child, Anchor) or
                   isinstance(child, Backreference)) and child.is_valid()

    def check_quantifiers(self, root):
        from opendlp.regex_generation.regex_tree.function_set import Quantifier, \
                                                    MatchMinMax, MatchMinMaxGreedy

        if isinstance(root, Quantifier):
            self.num_quantifier += 1
            self.has_only_min_max = False
        elif isinstance(root, MatchMinMax) or isinstance(root, MatchMinMaxGreedy):
            self.num_quantifier += 1

        for child in root.children:
            self.check_quantifiers(child)


    def is_look_behind_valid(self):
        self.check_quantifiers(self)
        return self.has_only_min_max or (self.num_quantifier < 1)