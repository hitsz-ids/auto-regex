from opendlp.regex_generation.regex_tree.terminal_set import Constant, RegexRange
from opendlp.regex_generation.regex_tree.function_set import Concatenator, ListMatch, MatchOneOrMore, MatchMinMax
from opendlp.regex_generation.utils import escape
from collections import deque
import functools
import random
import re
from enum import Enum

class PositionType(Enum):
    DIGIT = 1
    ALPHA = 2
    CHINESE = 3
    ALPHA_DIGIT = 4
    BPE = 5
    OTHER = 6


class DatasetPopulationGenerator:
    def __init__(self, dataset, bpe_token_dict):
        self.pos_examples = dataset.pos_examples
        self.is_fixed_length = dataset.is_fixed_length
        self.bpe_token_dict = bpe_token_dict

    def generate(self, n_pop):
        population = set()

        examples = self.pos_examples.copy()
        random.shuffle(examples)

        if self.is_fixed_length:
            position_type = {}
            for i in range(len(self.pos_examples[0])):
                position_type[i] = self.get_fixed_position_type(i)

            for example in examples:
                individual = self.create_individual_from_example_fixed(example, position_type,
                                                                       compat=False, use_min_max=False)
                population.add(individual)
                individual = self.create_individual_from_example_fixed(example, position_type,
                                                                       compat=True, use_min_max=True)
                population.add(individual)
                # 样本等长情况下，use_min_max=True或False的结果一样
                #individual = self.create_individual_from_example_fixed(example, position_type,
                #                                                       compat=True, use_min_max=False)
                #population.append(individual)
                if len(population) >= n_pop:
                    break
        else:
            for example in examples:
                individual = self.create_individual_from_example_unfixed(example, compat=False, use_min_max=False)
                population.add(individual)
                individual = self.create_individual_from_example_unfixed(example, compat=True, use_min_max=True)
                population.add(individual)
                individual = self.create_individual_from_example_unfixed(example, compat=True, use_min_max=False)
                population.add(individual)
                if len(population) >= n_pop:
                    break

        return list(population)

    def create_individual_from_example_unfixed(self, example:str, compat:bool, use_min_max=False):
        '''
        非等长正样本生成个体
        @param example: 一个正样本字符串
        @return: 生成的个体
        '''
        chinese = ListMatch()
        chinese.children.append(RegexRange('\\u4e00-\\u9fff'))

        nodes = deque()
        example_tokens = self.tokenize_with_bpe(example)
        for token in example_tokens:
            if token in self.bpe_token_dict['tokens']:
                nodes.append(Constant(escape(token)))
            elif token.isdigit():
                nodes.append(Constant('\\d'))
            elif token.encode('utf-8').isalpha():
                nodes.append(Constant('\\w'))
            elif u'\u4e00' <= token <= u'\u9fff':
                nodes.append(chinese.clone_tree())
            else:
                nodes.append(Constant(escape(token)))

        if compat:
            nodes = compact_to_quantifier(nodes, use_min_max, False)
        tree = functools.reduce(concate, nodes)
        return tree

    def create_individual_from_example_fixed(self,  example:str, position_type_dict:dict,
                                             compat:bool, use_min_max=False):
        '''
        等长正样本生成个体
        @param example: 一个正样本字符串
        @return: 生成的个体
        '''
        chinese = ListMatch()
        chinese.children.append(RegexRange('\\u4e00-\\u9fff'))
        letters = ListMatch()
        letters.children.append(RegexRange('A-Za-z'))
        bpe_match_ranges = [tup[1] for tup in self.bpe_token_dict['tokens']]

        string = example
        nodes = deque()
        for i in range(len(string)):
            p_type = position_type_dict[i]
            if p_type == PositionType.DIGIT:
                nodes.append(Constant('\\d'))
            elif p_type == PositionType.ALPHA:
                nodes.append(letters.clone_tree())
            elif p_type == PositionType.CHINESE:
                nodes.append(chinese.clone_tree())
            elif p_type == PositionType.ALPHA_DIGIT:
                nodes.append(Constant('\\w'))
            elif p_type == PositionType.BPE:
                start, end = find_range(bpe_match_ranges, i)
                if i == start:
                    nodes.append(Constant(escape(string[start:end])))
            else:
                nodes.append(Constant(escape(string[i])))

        if compat:
            nodes = compact_to_quantifier(nodes, use_min_max, True)
        tree = functools.reduce(concate, nodes)
        return tree

    def tokenize_with_bpe(self, string):
        bpe_match_ranges = []
        for bpe_token in self.bpe_token_dict['tokens']:
            ranges = [(m.start(), m.end())for m in re.finditer(escape(bpe_token), string)]
            bpe_match_ranges.extend(ranges)

        # bpe_match_ranges中的区间不重叠，按区间的左边界排序即可
        bpe_match_ranges = sorted(bpe_match_ranges)
        string_tokens = []
        i = 0
        while i<len(string):
            start, end = find_range(bpe_match_ranges, i)
            if start==-1:
                string_tokens.append(string[i])
                i += 1
            else:
                string_tokens.append(string[start:end])
                i += end-start
        return string_tokens

    def get_fixed_position_type(self, idx):
        bpe_match_ranges = [tup[1] for tup in self.bpe_token_dict['tokens']]
        if find_range(bpe_match_ranges, idx)[0] != -1:
            return PositionType.BPE

        types = set()
        for example in self.pos_examples:
            ch = example[idx]
            if ch.isdigit():
                types.add(PositionType.DIGIT)
            elif ch.isalpha():
                types.add(PositionType.ALPHA)
            elif u'\u4e00' <= ch <= u'\u9fff':
                types.add(PositionType.CHINESE)
            else:
                types.add(PositionType.OTHER)

            if len(types) > 2:
                break

        if len(types)==1:
            return list(types)[0]
        elif types=={PositionType.ALPHA, PositionType.DIGIT}:
            return PositionType.ALPHA_DIGIT
        else:
            return PositionType.OTHER

# 用Concatenator操作符连接两个节点
def concate(first_node, second_node):
    conc = Concatenator()
    conc.children.append(first_node)
    conc.children.append(second_node)
    first_node.parent = conc
    second_node.parent = conc
    return conc

def compact_to_quantifier(nodes:deque, use_min_max:bool, fix_length:bool):
    '''
    当两个相邻节点相等时，用量词压缩。\w\w\w 转换成 \w+
    @param nodes: 节点队列
    @param use_min_max: 是否使用MatchMinMax操作符
    @return: 压缩处理后的节点队列
    '''
    new_nodes = deque()
    while len(nodes)>0:
        node = nodes.popleft()
        repeat_num = 1
        while len(nodes)>0:
            next_node = nodes[0]
            value = node.children[0].value if isinstance(node, ListMatch) else node.value
            next_value = next_node.children[0].value if isinstance(next_node, ListMatch) else next_node.value

            if next_value == value:
                repeat_num += 1
                nodes.popleft()
            else:
                break

        if repeat_num > 1:
            if fix_length:
                new_node = MatchMinMax()
                new_node.children.append(node)
                # MatchMinMax是三元运算符，不能写成{3},得写{3,3}
                new_node.children.append(Constant(str(repeat_num)))
                new_node.children.append(Constant(str(repeat_num)))
            elif use_min_max:
                new_node = MatchMinMax()
                new_node.children.append(node)
                new_node.children.append(Constant('1'))
                new_node.children.append(Constant(str(repeat_num)))
            else:
                new_node = MatchOneOrMore()
                new_node.children.append(node)
            node = new_node
        new_nodes.append(node)
    return new_nodes

def find_range(ranges, index):
    """
    有序区间查找
    @param ranges: 排序后的bpe token在字符串中的位置区间列表，区间不重叠
    @param index: 字符串中的位置索引
    @return: index所在区间的边界，如果不在任何一个区间中，则返回-1,-1。
    """
    for range in ranges:
        start, end = range[0], range[1]
        if index>=start and index<end:
            return start, end
    return -1, -1


