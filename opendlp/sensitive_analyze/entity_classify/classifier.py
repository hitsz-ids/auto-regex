# coding: UTF-8
import numpy as np
import torch
import os
import pickle
from opendlp.sensitive_analyze.entity_classify.utils_infer import build_dataset, build_iterator
from opendlp.sensitive_analyze.entity_classify.model import Model
from opendlp.sensitive_analyze.entity_classify.config import Config, TOP_N


class EntityClassifier():
    def __init__(self):
        self.config = Config()
        self.device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')  # 设备
        self.__load_vocab()
        self.__load_label2id()

        self.config.n_vocab = len(self.vocab)
        self.config.num_classes = len(self.label2id)
        self.__load_model()

    def __load_model(self):
        self.model = Model(self.config).to(self.device)
        if os.path.exists(self.config.model_path):
            self.model.load_state_dict(torch.load(self.config.model_path, map_location=self.device))
        else:
            raise ValueError('Model file {} dose not exist!'.format(self.config.model_path))

    def __load_vocab(self):
        if os.path.exists(self.config.vocab_path):
            self.vocab = pickle.load(open(self.config.vocab_path, 'rb'))
        else:
            raise ValueError('Vocab file {} dose not exist!'.format(self.config.vocab_path))

    def __load_label2id(self):
        if os.path.exists(self.config.label2id_path):
            self.label2id = pickle.load(open(self.config.label2id_path, 'rb'))
            self.id2label = dict([val, key] for key, val in self.label2id.items())
        else:
            raise ValueError('Label2id file {} dose not exist!'.format(self.config.label2id_path))


    def predict(self, texts):
        """

        :param texts: 文本列表。 例如：['张三']
        :return: top_n 类别。例如：{'张三': ['name', 'address', 'email']}
        """
        dataset = build_dataset(texts, self.vocab, self.config.pad_size)
        data_iter = build_iterator(dataset, self.config, self.device)

        class_list = sorted(list(self.label2id.keys()))
        top_n = TOP_N
        self.model.eval()
        logits_all = np.empty((0, len(class_list)), float)
        result_id = []
        with torch.no_grad():
            for text in data_iter:
                outputs = self.model(text, True)
                logits = outputs.data.cpu().numpy()
                logits_all = np.append(logits_all, logits, axis=0)

        # 取预测概率 top 3的下标
        ind = np.argpartition(logits_all, -top_n)[:, -top_n:]
        for i in range(len(logits_all)):
            res = ind[i][np.argsort(logits_all[i][ind[i]])[::-1][:len(logits_all[i][ind[i]])]]
            result_id.append(res.tolist())

        result = {}
        for te, top3_idxs in zip(texts, result_id):
            result[te] = [self.id2label[idx] for idx in top3_idxs]

        return result

    def predict_prob(self, texts):
        dataset = build_dataset(texts, self.vocab, self.config.pad_size)
        data_iter = build_iterator(dataset, self.config, self.device)

        class_list = sorted(list(self.label2id.keys()))
        top_n = TOP_N
        self.model.eval()
        logits_all = np.empty((0, len(class_list)), float)
        with torch.no_grad():
            for text in data_iter:
                outputs = self.model(text, True)
                logits = outputs.data.cpu().numpy()
                logits_all = np.append(logits_all, logits, axis=0)

        # 取预测概率 top 3的下标
        result_prob = []
        ind = np.argpartition(logits_all, -top_n)[:, -top_n:]
        for i in range(len(logits_all)):
            top_n_idxs = ind[i][np.argsort(logits_all[i][ind[i]])[::-1][:len(logits_all[i][ind[i]])]]
            res = []
            for idx in top_n_idxs:
                res.append({self.id2label[idx] : logits_all[i][idx]})
            result_prob.append(res)

        result = {}
        for te, top3_probs in zip(texts, result_prob):
            result[te] = top3_probs

        return result