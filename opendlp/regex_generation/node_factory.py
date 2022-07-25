from opendlp.regex_generation.utils import escape
from opendlp.regex_generation.regex_tree.terminal_set import Constant, RegexRange
from opendlp.regex_generation.regex_tree.function_set import (
    Concatenator,
    Group,
    NonCapturingGroup,
    ListMatch,
    ListNotMatch,
    MatchZeroOrOne,
    MatchZeroOrMore,
    MatchOneOrMore,
    MatchMinMax
)


class NodeFactory:
    def __init__(self):
        self.terminal_set = []
        self.function_set = []

    def build_terminal_set(self):
        """
        load default terminal set
        @return:
        """
        self.alphabet = [chr(i) for i in range(97, 123)] + [chr(i) for i in range(65, 123)]
        self.digit = [chr(i) for i in range(48, 58)]
        self.symbols = [":", ",", ";", "_", "-", "=", "\\", "’", "/", "?", "!",
                        "}", "{", "(", ")", "[", "]", "<", ">", "@", "#", "%"]
        self.wildcard = ["."]
        self.character_class = ["\\w", "\\d"]
        self.range_alphabet = ["a-z", "A-Z"]
        self.range_digit = ["0-9"]
        self.range_chinese = [r"\u4e00-\u9fa5"]

        self.constant = self.alphabet + self.digit + self.symbols + \
                        self.character_class + self.wildcard
        self.range = self.range_alphabet + self.range_digit + self.range_chinese

        for c in self.constant:
            self.terminal_set.append(Constant(escape(c)))
        for r in self.range:
            self.terminal_set.append(RegexRange(r))

    def build_function_set(self):
        """
        load default terminal set
        @return:
        """
        self.operators = [Concatenator,
                            Group,
                            NonCapturingGroup,
                            ListMatch,
                            ListNotMatch,
                            MatchZeroOrOne,
                            MatchZeroOrMore,
                            MatchOneOrMore,
                            MatchMinMax]
        self.function_set = [f() for f in self.operators]


    def build(self):
        self.build_terminal_set()
        self.build_function_set()