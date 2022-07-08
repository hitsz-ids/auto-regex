import os
import pandas as pd

from opendlp_server import LOGGER

class Dataset:
    def __init__(self, data_path):
        self.data_path = data_path


    def clean(self, strings):
        res = []
        tmp = [s.strip() for s in strings]
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

    @property
    def pos_examples(self):
        return self.__pos_examples

    @property
    def neg_examples(self):
        return self.__neg_examples

    def remove_by_regex(self, regex_tree):
        """
        remove positive samples that can be mathced by regex_tree
        @param regex_tree: a regex tree
        @return: None
        """
        raise NotImplementedError