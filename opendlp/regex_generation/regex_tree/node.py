from abc import abstractmethod

from opendlp.regex_generation.config.conf import RegexFlavour
from opendlp.regex_generation.regex_tree.id_factory import IDFactory
from opendlp.regex_generation.regex_tree.regex_context import RegexContext


class Node:
    def __init__(self):
        self.__id = IDFactory.next_id()
        self.children = []
        self.parent = None

    @property
    def id(self):
        return self.__id

    def set_parent(self, node):
        self.parent = node

    def is_character_class(self):
        return False

    def is_escaped(self):
        return False


    @abstractmethod
    def get_min_children_count(self) -> int:
        """
        @return: min children count of node
        """

    @abstractmethod
    def get_max_children_count(self) -> int:
        """
        @return: max children count of node
        """

    @abstractmethod
    def clone_tree(self):
        """
        clone current node and it's children
        @return:
        """

    @abstractmethod
    def is_valid(self):
        """
        check whether the tree with current node as root is a valid regex pattern
        @return: bool
        """

    @abstractmethod
    def form(self, string, flavour=RegexFlavour.Python, context=RegexContext()):
        """
        form regex string
        @param string: regex string before current node
        @param flavour: regex grammar related with language
        @param context:
        @return: new string
        """

    def __eq__(self, other):
        if isinstance(other, Node):
            return other.form('') == self.form('')
        else:
            return False

    def __hash__(self):
        return hash(self.form(''))
