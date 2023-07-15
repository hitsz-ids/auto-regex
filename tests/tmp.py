from auto_regex.dataset import Dataset
import os
from auto_regex.utils import get_final_metric


if __name__ == '__main__':
    data_dir = './data/'
    regex_name = 'ID_CARD'
    train_data_file = os.path.join(data_dir, regex_name + '.csv')

    regex_0 = '\d\d\d\d\d\d19\d\d\d\d\d\d\d\d\d\w'
    regex_1 = '\d{6,6}20\d{9,9}\w'
    regex_2 = '\d\d\d\d\d\d19\d\d\d\d\d\d\d\d\d\w|\d{6,6}20\d{9,9}\w'

    dataset = Dataset(train_data_file)
    dataset.build()

    regexs = [regex_0, regex_1, regex_2]
    for regex in regexs:
        precision, recall = get_final_metric(dataset.pos_examples, dataset.neg_examples, regex)
        print(f'pattern: {regex} precision: {precision}, recall: {recall}')
