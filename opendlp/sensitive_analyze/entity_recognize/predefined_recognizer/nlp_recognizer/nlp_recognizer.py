
import hanlp
from collections import Counter

from opendlp.sensitive_analyze.entity_recognize.entity_recognizer import EntityRecognizer
from opendlp.sensitive_analyze.entity_recognize.conf import config


class NLPRecognizer(EntityRecognizer):
    def __init__(self):
        self.used_entities = ('PERSON', 'LOCATION', 'ORGANIZATION')
        self.entity_map = {'PERSON': config.PERSON,
                           'LOCATION': config.LOCATION,
                           'ORGANIZATION': config.COMPANY_NAME}
        self.supported_entities = (config.PERSON, config.LOCATION, config.COMPANY_NAME)
        self.model = hanlp.load(hanlp.pretrained.mtl.CLOSE_TOK_POS_NER_SRL_DEP_SDP_CON_ELECTRA_SMALL_ZH)

    def __extract_entity(self, pred_list, entity=None):
        """
        提取一个元素的模型预测结果中的实体类型，如有多个，取频率最高的，频率相等的话取第一个。
        :param pred_list: 一个元素的模型预测结果
        :return:
        """
        entities = []
        for tup in pred_list:
            entity = tup[1]
            if entity in self.used_entities:
                entities.append(self.entity_map[entity])
        counter = Counter(entities)
        if len(counter) > 0:
            most_cnt = counter.most_common(1)[0][1]
            most = [e[0] for e in counter.most_common() if e[1] >= most_cnt]
            if len(most) == 1:
                return most[0]
            else:
                if entity is not None and entity in most:
                    return entity
                elif config.COMPANY_NAME in most:
                    return config.COMPANY_NAME
                elif config.LOCATION in most:
                    return config.LOCATION
                else:
                    return most[0]
        else:
            return None

    def analyze(self, text, entity=None):
        if type(text) is list:
            texts = text
        else:
            texts = [text]
        model_outputs = self.model(texts, tasks='ner')
        ner_outputs = model_outputs['ner/msra']
        result_dict = {}
        for i in range(len(texts)):
            result_dict[texts[i]] = self.__extract_entity(ner_outputs[i], entity)
        return result_dict




