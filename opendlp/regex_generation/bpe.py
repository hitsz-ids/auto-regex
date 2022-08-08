from typing import List, Set
import collections
import re

def learn_bpe(strings: List[str], pair_percent_threshold: float, char_percent_threshold:float, with_position:bool) -> dict:
    """
    learn byte pair encode tokens from positive examples
    @param strings: raw string list used to learn bpe
    @param percent: proportion threshold
    @return: learned byte pair encode tokens
    """

    vocab = get_vocab(strings)
    percent = 1.0
    # 待改进，这里如果 pair_percent_threshold <=0，则会死循环
    while percent >= pair_percent_threshold:
        pair2freq = pair_freq_stats(vocab, with_position)
        best = max(pair2freq, key=pair2freq.get)
        percent = pair2freq.get(best) / len(strings)
        if percent >= pair_percent_threshold:
            vocab = merge_vocab(best, vocab, with_position)

    bpe_tokens = get_tokens(vocab, pair_percent_threshold, len(strings), char_percent_threshold, with_position)
    if with_position:
        bpe_tokens = sorted(bpe_tokens, key=lambda x: len(x[0]), reverse=True)
    else:
        bpe_tokens = sorted(bpe_tokens, key=len, reverse=True)
    bpe_token_dict = {'with_position':with_position,
                      'tokens': bpe_tokens}
    return bpe_token_dict


def get_vocab(strings: List[str]):
    vocab = collections.defaultdict(int)
    for string in strings:
        words = string.strip().split(' ')
        for word in words:
            vocab[' '.join(list(word)) + ' </w>'] += 1
    return vocab

def pair_freq_stats(vocab, with_position=False):
    pair_freq = collections.defaultdict(int)
    for word, freq in vocab.items():
        symbols = word.split(' ')
        if with_position:
            for i in range(len(symbols) - 1):
                # 仅统计不同的数据中出现的次数，如果freq不为1，则表明有多条训练数据串相同
                pair_freq[(symbols[i], symbols[i + 1]), (i, i + 1)] += 1
        else:
            for i in range(len(symbols) - 1):
                pair_freq[symbols[i], symbols[i+1]] += 1
    return pair_freq

def merge_vocab(pair, v_in, with_position=False):
    v_out = {}

    if with_position:
        pair_tokens = pair[0]
        pair_pos = pair[1]
        for word in v_in:
            symbols = word.split(' ')
            if symbols[pair_pos[0]:pair_pos[1]+1] == list(pair_tokens):
                w_out = ' '.join(symbols[0:pair_pos[0]+1])+' '.join(symbols[pair_pos[1]:])
                v_out[w_out] = v_in[word]
            else:
                v_out[word] = v_in[word]
    else:
        bigram = re.escape(' '.join(pair))
        pattern = re.compile(r'(?<!\S)' + bigram + '(?!\S)')
        for word in v_in:
            w_out = pattern.sub(''.join(pair), word)
            v_out[w_out] = v_in[word]

    return v_out


def get_tokens(vocab, pair_threshold, example_num, char_threshold, with_position=False):
    if with_position:
        tokens = collections.defaultdict(int)
        for word, freq in vocab.items():
            word_tokens = word.split()
            start_pos = 0
            for token in word_tokens:
                tokens[(token, (start_pos, start_pos+len(token)))] += freq
                start_pos += len(token)
    else:
        tokens = collections.defaultdict(int)
        for word, freq in vocab.items():
            word_tokens = set(word.split())  # 同一个字符串中不统计多次
            for token in word_tokens:
                tokens[token] += freq

    result = filter_tokens(tokens, pair_threshold, example_num, char_threshold, with_position)
    return result


def filter_tokens(token_dict, pair_threshold, example_num, char_threshold, with_position):
    result = []
    if not with_position:
        tmp = [{k: v} for k, v in token_dict.items() if v >= int(pair_threshold * example_num) and k!='</w>']
        for dic in tmp:
            for k, v in dic.items():
                if len(k) > 1 or (len(k) == 1 and v >= int(char_threshold * example_num)):
                    result.append(k)
    else:
        tmp = [{k: v} for k, v in token_dict.items() if v>=int(pair_threshold*example_num) and k[0]!='</w>']
        for dic in tmp:
            for k, v in dic.items():
                if len(k[0]) > 1 or (len(k[0]) == 1 and v >= int(char_threshold * example_num)):
                    result.append(k)
    return result