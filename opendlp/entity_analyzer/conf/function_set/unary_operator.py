from abc import abstractmethod
from opendlp.regex_generation.regex_tree import Node

class UnaryOperator(Node):

    def get_min_children_count(self) -> int:
        return 1

    def get_max_children_count(self) -> int:
        return 1

    def clone_tree(self):
        clone = self.build_copy()
        if len(self.children) > 0:
            child = self.children[0].clone_tree()
            child.set_parent(clone)
            clone.children.append(child)
        return clone

    @abstractmethod
    def build_copy(self):
        raise NotImplementedError
