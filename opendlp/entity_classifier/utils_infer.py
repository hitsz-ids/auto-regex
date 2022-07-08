# coding: UTF-8
import torch


UNK, PAD = '<UNK>', '<PAD>'  # 未知字，padding符号
SEPARATE_SYMBOL = ','  # csv文件分隔符

def build_dataset(text, vocab, pad_size):
    tokenizer = lambda x: [y for y in x]  # char-level

    contents = []
    for te in text:
        content = str(te).strip()
        words_line = []
        token = tokenizer(content)
        seq_len = len(token)
        if pad_size:
            if len(token) < pad_size:
                token.extend([PAD] * (pad_size - len(token)))
            else:
                token = token[:pad_size]
                seq_len = pad_size
        # word to id
        for word in token:
            words_line.append(vocab.get(word, vocab.get(UNK)))
        contents.append((words_line, seq_len))
    return contents  # [([...], 0), ([...], 1), ...]


class DatasetIterater(object):
    def __init__(self, batches, batch_size, device):
        self.batch_size = batch_size
        self.batches = batches
        self.n_batches = len(batches) // batch_size
        self.residue = False  # 记录batch数量是否为整数
        if len(batches) % self.batch_size != 0:
            self.residue = True
        self.index = 0
        self.device = device

    def _to_tensor(self, datas):
        x = torch.LongTensor([_[0] for _ in datas]).to(self.device)

        # pad前的长度(超过pad_size的设为pad_size)
        seq_len = torch.LongTensor([_[1] for _ in datas]).to(self.device)
        return (x, seq_len)

    def __next__(self):
        if self.residue and self.index == self.n_batches:
            batches = self.batches[self.index * self.batch_size: len(self.batches)]
            self.index += 1
            batches = self._to_tensor(batches)
            return batches

        elif self.index >= self.n_batches:
            self.index = 0
            raise StopIteration
        else:
            batches = self.batches[self.index * self.batch_size: (self.index + 1) * self.batch_size]
            self.index += 1
            batches = self._to_tensor(batches)
            return batches

    def __iter__(self):
        return self

    def __len__(self):
        if self.residue:
            return self.n_batches + 1
        else:
            return self.n_batches


def build_iterator(dataset, config, device):
    iter = DatasetIterater(dataset, config.batch_size, device)
    return iter