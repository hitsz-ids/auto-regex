import re
import pandas as pd

class Dataset:
    def __init__(self, data_path):
        self.data_path = data_path

    def clean(self, strings):
        res = []
        tmp = [s.strip().replace(' ', '') for s in strings]
        for s in tmp:
            if s != '':
                res.append(s)
        return res

    def read_csv_data(self):
        df = pd.read_csv(self.data_path, dtype=str)
        df['positive'].dropna(inplace=True)
        df['negative'].dropna(inplace=True)
        pos_examples = self.clean(df['positive'])
        neg_examples = self.clean(df['negative'])
        return pos_examples, neg_examples

    def build(self):
        pos_examples, neg_examples = self.read_csv_data()
        self.__pos_examples = pos_examples
        self.__neg_examples = neg_examples
        self.is_fixed_length = self.same_length()

    def same_length(self):
        for i in range(len(self.pos_examples) - 1):
            if len(self.pos_examples[i + 1]) != len(self.pos_examples[i]):
                return False
        return True

    @property
    def pos_examples(self):
        return self.__pos_examples

    @property
    def neg_examples(self):
        return self.__neg_examples

    def remove_by_regex(self, regex_tree):
        """
        remove positive samples that can be matched by regex_tree
        @param regex_tree: a regex tree
        @return: None
        """
        flags = re.DOTALL | re.MULTILINE
        pattern = regex_tree.form(string='')
        matched_ids = set()
        for i in range(len(self.__pos_examples)):
            example = self.__pos_examples[i]
            matches = re.finditer(pattern, example, flags=flags)
            for match in matches:
                if match.span()[1]-match.span()[0] == len(example):
                    matched_ids.add(i)

        pos_examples = []
        for i in range(len(self.__pos_examples)):
            if i not in matched_ids:
                pos_examples.append(self.__pos_examples[i])
        self.__pos_examples = pos_examples

