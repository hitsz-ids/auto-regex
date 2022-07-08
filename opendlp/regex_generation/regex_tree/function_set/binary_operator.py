from abc import abstractmethod
from opendlp.regex_generation.regex_tree import Node

class BinaryOperator(Node):

    def get_min_children_count(self) -> int:
        return 2

    def get_max_children_count(self) -> int:
        return 2

    def get_left(self):
        return self.children[0]

    def get_right(self):
        return self.children[1]

    def clone_tree(self):
        clone = self.build_copy()
        for child in self.children:
            new_child = child.clone_tree()
            new_child.set_parent(clone)
            clone.children.append(new_child)
        return clone

    @abstractmethod
    def build_copy(self):
        raise NotImplementedError
