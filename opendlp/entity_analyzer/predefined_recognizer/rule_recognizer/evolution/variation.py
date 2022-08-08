import random

from opendlp.regex_generation.config import conf

class Variation:
    def __init__(self, evolve_param, bpe_token_dict, random_popu_gen):
        self.param = evolve_param
        self.bpe_token_dict = bpe_token_dict
        self.random_popu_gen = random_popu_gen

    def crossover(self, individual1, individual2, tries):
        new_individual1 = individual1.clone_tree()
        new_individual2 = individual2.clone_tree()

        for i in range(tries):
            random_node1 = self.pick_random_node(new_individual1)
            random_node2 = self.pick_random_node(new_individual2)
            if random_node1 is not None and random_node2 is not None:
                self.swap_nodes(random_node1, random_node2)

                if self.check_max_depth(new_individual1, 1, conf.MAX_DEPTH) and \
                    self.check_max_depth(new_individual2, 1, conf.MAX_DEPTH) and \
                    new_individual1.is_valid() and new_individual2.is_valid():
                    break
                new_individual1 = individual1.clone_tree()
                new_individual2 = individual2.clone_tree()

        return new_individual1, new_individual1

    def mutate(self, individual, tries):
        trees = self.random_popu_gen.growth_generate(tries)
        new_individual = individual.clone_tree()

        for i in range(tries):
            random_node = self.pick_random_node(new_individual)
            if random_node is not None:
                self.replace_node(random_node, trees[i])
                if self.check_max_depth(new_individual, 1, conf.MAX_DEPTH) and \
                    new_individual.is_valid():
                    break
                new_individual = individual.clone_tree()

        return new_individual

    def pick_random_node(self, individual):
        sub_trees = []
        rand = random.random()
        if rand <= self.param.pick_node_proba:
            self.get_sub_trees(individual, sub_trees, is_leaf=False)
        else:
            self.get_sub_trees(individual, sub_trees, is_leaf=True)

        # 如果sub_trees为空，则表明individual是一个只有根节点和叶节点的2层树，且走的是leaf=False分支
        # 此时取其叶节点子树
        if len(sub_trees) == 0 and self.check_max_depth(individual, 1, 2):
            self.get_sub_trees(individual, sub_trees, is_leaf=True)

        if len(sub_trees) == 0:
            return None

        return random.choice(sub_trees)

    def get_sub_trees(self, root, sub_trees, is_leaf):
        if self.is_node_pickable(root, is_leaf):
            sub_trees.append(root)
        for child in root.children:
            self.get_sub_trees(child, sub_trees, is_leaf)

    def is_node_pickable(self, root, is_leaf):
        flag1 = not(len(root.children)==0 ^ is_leaf) and root.parent!=None
        if flag1:
            return not self.contain_bpe_tokens(root)
        else:
            return False

    def contain_bpe_tokens(self, root):
        if len(root.children) == 0:
            string = root.form('')
            if not self.bpe_token_dict['with_position']:
                bpe_tokens = set(self.bpe_token_dict['tokens'])
            else:
                bpe_tokens = set([k[0] for k in self.bpe_token_dict['tokens']])
            if string in bpe_tokens:
                return True
            else:
                return False

        flag = False
        for child in root.children:
            flag = flag or self.contain_bpe_tokens(child)
            if flag:
                break
        return flag

    def swap_nodes(self, node1, node2):
        parent1 = node1.parent
        index1 = parent1.children.index(node1)
        parent2 = node2.parent
        index2 = parent2.children.index(node2)
        node1.parent = parent2
        node2.parent = parent1
        parent1.children[index1] = node2
        parent2.children[index2] = node1

    def replace_node(self, node, new_node):
        parent = node.parent
        idx = parent.children.index(node)
        parent.children[idx] = new_node
        new_node.set_parent(parent)
        node.set_parent(None)

    def check_max_depth(self, root, depth, max_depth):
        if depth > max_depth:
            return False
        flag = True
        for child in root.children:
            flag &= self.check_max_depth(child, depth+1, max_depth)
            if not flag:
                return False
        return flag

