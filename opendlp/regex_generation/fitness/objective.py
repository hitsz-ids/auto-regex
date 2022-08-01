import re
import numpy as np

class Objective:
    def __init__(self, dataset):
        self.dataset = dataset

    def cal_fitness(self, tree):
        """
        calculate fitness of a regex tree
        @param tree: a regex tree
        @return: fitness array with three value:[Ps, Pc, Lscore]
        """
        #TODO: 使用cache

        pos_match_spans = self.get_match_span(tree, is_positive=True)
        neg_match_spans = self.get_match_span(tree, is_positive=False)

        # 这里的算法，负样本匹配数相同时，正样本匹配1个与匹配所有算出来的score是一样的。
        # 只用了precision，没用recall，为什么不考虑recall呢？  recall由后面的分治法考虑？
        score_sample = self.cal_sample_score(pos_match_spans, neg_match_spans)  # precision
        score_char = self.cal_char_score(pos_match_spans, neg_match_spans)
        score_length = self.cal_length_score(tree)

        return (score_sample, score_char, score_length)


    def get_match_span(self, tree, is_positive):
        match_spans = []
        if is_positive:
            examples = self.dataset.pos_examples
        else:
            examples = self.dataset.neg_examples

        flags = re.DOTALL | re.MULTILINE
        pattern = tree.form(string='')

        '''
        try:
            re.compile(pattern)
        except re.error:
            print('tree: {} \tpattern: {}'.format(tree, pattern))
        '''

        for example in examples:
            try:
                matches = re.finditer(pattern, example, flags=flags)
                spans = [match.span() for match in matches]
                match_spans.append(spans)
            except re.error:
                match_spans.append([])

        return match_spans

    def cal_sample_score(self, pos_match_spans, neg_match_spans):
        pos_math_count = self.match_sample_count(pos_match_spans, is_positive=True)
        neg_math_count = self.match_sample_count(neg_match_spans, is_positive=False)
        score = 0
        if pos_math_count + neg_math_count != 0:
            score = pos_math_count / (pos_math_count + neg_math_count)
        return score

    def cal_char_score(self, pos_match_spans, neg_match_spans):
        pos_match_char_cnt, pos_unmatch_char_cnt = self.match_char_count(pos_match_spans, is_positive=True)
        neg_match_char_cnt, neg_unmatch_char_cnt = self.match_char_count(neg_match_spans, is_positive=False)
        score = 0
        if pos_match_char_cnt + pos_unmatch_char_cnt != 0:
            score += pos_match_char_cnt / (pos_match_char_cnt + pos_unmatch_char_cnt)
        if neg_match_char_cnt + neg_unmatch_char_cnt != 0:
            score += neg_match_char_cnt / (neg_match_char_cnt + neg_unmatch_char_cnt)
        return score

    def cal_length_score(self, tree):
        pattern = tree.form(string='')
        pos_example_avg_len = np.mean([len(e) for e in self.dataset.pos_examples])
        score = 1 / np.exp(np.abs(len(pattern)-pos_example_avg_len))
        return score

    def match_sample_count(self, match_spans, is_positive):
        if is_positive:
            samples = self.dataset.pos_examples
        else:
            samples = self.dataset.neg_examples

        count = 0
        for i in range(len(samples)):
            sample = samples[i]
            match_span = match_spans[i]
            if len(match_span)==1 and match_span[0][1]-match_span[0][0]==len(sample):
                count += 1
        return count

    def match_char_count(self, match_spans, is_positive):
        if is_positive:
            samples = self.dataset.pos_examples
        else:
            samples = self.dataset.neg_examples

        match_char_count, unmatch_char_count = 0, 0
        for i in range(len(samples)):
            sample = samples[i]
            match_span = match_spans[i]
            if len(match_span) == 1 and match_span[0][1] - match_span[0][0] == len(sample):
                match_char_count += len(sample)
            elif len(match_span) > 0:
                unmatch_char_count += sum([sp[1]-sp[0] for sp in match_span])
        return match_char_count, unmatch_char_count



