
from opendlp.regex_generation.regex_tree.function_set import UnaryOperator
from opendlp.regex_generation.regex_tree.terminal_set import Anchor


class Quantifier(UnaryOperator):
    def is_valid(self):
        # 不能放在外面，不然有循环引用
        from opendlp.regex_generation.regex_tree.function_set import MatchMinMax, MatchMinMaxGreedy, Lookaround

        child = self.children[0]
        return child.is_valid() and not(isinstance(child, Quantifier) or
                                        isinstance(child, MatchMinMax) or
                                        isinstance(child, MatchMinMaxGreedy) or
                                        isinstance(child, Anchor) or
                                        isinstance(child, Lookaround))