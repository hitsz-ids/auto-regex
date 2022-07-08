import os

TOP_N = 3

class Config(object):

    """配置参数"""
    def __init__(self,):
        curr_path = os.path.dirname(__file__)
        self.vocab_path = os.path.join(curr_path + '/trained-model/vocab.pkl')         # 词表
        self.label2id_path = os.path.join(curr_path + '/trained-model/label2id.pkl')  # 标签
        self.model_path = os.path.join(curr_path + '/trained-model/model.pt')         # 模型训练结果

        self.batch_size = 512                                           # mini-batch大小   256
        self.pad_size = 64                                              # 每句话处理成的长度(短填长切)
        self.embed =  100                                               # 字向量维度
        self.filter_sizes = (2, 3, 5)                                   # 卷积核尺寸
        self.num_filters = 64                                           # 卷积核数量(channels数)
        self.dropout = 0.3
        self.num_classes = None                                         # 类别数，在运行时赋值
        self.n_vocab = None                                             # 词表大小，在运行时赋值


