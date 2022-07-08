import re
from collections import Counter
from itertools import compress
from typing import Optional, List

from opendlp.entity_classifier.classifier import EntityClassifier
from opendlp.entity_analyzer import RecognizerEngine
from opendlp.entity_analyzer import RecognizerRegistry
from opendlp.entity_analyzer.conf import config
from opendlp.entity_analyzer.utils import get_threshold


class AnalyzerEngine:
    def __init__(self, pattern_file: Optional[str] = ''):
        self.pattern_file = pattern_file
        self.entity_classifier = EntityClassifier()
        self.registry = RecognizerRegistry(pattern_file)
        self.recognizer_engine = RecognizerEngine()

    def analyze(self, texts: List[str], thresholds):

        result_predefined = self.analyze_predefined(texts)

        if self.pattern_file == '':
            return result_predefined

        counter = Counter(result_predefined)
        most_entity = None
        if len(counter) > 0:
            most_common = counter.most_common(1)
            # most entity 可能是 None，result_predefined 中None可能最多
            most_entity = most_common[0][0]
            most_cnt = most_common[0][1]
        else:
            most_cnt = 0

        if most_cnt == 0 or most_entity is None or most_cnt / len(result_predefined) \
                < get_threshold(thresholds, most_entity):
            result = self.analyze_userdefined(texts, result_predefined)
            return result
        else:
            return result_predefined

    def analyze_predefined(self, texts: List[str]):
        candi_entities = self.entity_classifier.predict(texts)
        candi_entities = filter_entities(candi_entities)

        result = [None] * len(texts)
        tried_entities = []

        text_analyze_flag = [True] * len(texts)
        for i in range(len(result)):
            if result[i] is not None:
                text_analyze_flag[i] = False

        while any(text_analyze_flag):
            text_list = list(compress(texts, text_analyze_flag))
            entities = []
            for t in text_list:
                entities.extend(candi_entities[t])

            if len(entities) == 0:
                break

            counter = Counter(entities)
            entities_count_sorted = counter.most_common()
            finish_flag = True
            for tup in entities_count_sorted:
                entity = tup[0]
                if entity in tried_entities:
                    continue
                tried_entities.append(entity)
                recognizer = self.registry.load_predefined_recognizers(
                    entities=[entity])[0]
                res = self.recognizer_engine.analyze(texts=text_list,
                                                     entity=entity,
                                                     recognizer=recognizer)
                # res 不全为None
                if any(res):
                    res_i = 0
                    for i in range(len(text_analyze_flag)):
                        if text_analyze_flag[i]:
                            result[i] = res[res_i]
                            res_i += 1

                            if result[i] is not None:
                                text_analyze_flag[i] = False
                    # 本次有识别出结果，则重新生成待匹配的实体类型
                    finish_flag = False
                    break
            if finish_flag:
                break

        return result

    def analyze_userdefined(self, texts: List[str], result_predefined: List):
        result = result_predefined

        recognizers = self.registry.load_user_defined_recognizers()

        text_analyze_flag = [True] * len(texts)
        for i in range(len(result)):
            if result[i] is not None:
                text_analyze_flag[i] = False

        for recognizer in recognizers:
            if any(text_analyze_flag):
                text_list = list(compress(texts, text_analyze_flag))

                res = self.recognizer_engine.analyze(texts=text_list,
                                                     entity=None,
                                                     recognizer=recognizer)
                # res 不全为None
                if any(res):
                    res_i = 0
                    for i in range(len(text_analyze_flag)):
                        if text_analyze_flag[i]:
                            result[i] = res[res_i]
                            res_i += 1

                            if result[i] is not None:
                                text_analyze_flag[i] = False
            # 全都识别出来了，结束
            else:
                break

        return result


def filter_entities(candi_entities):
    """
    筛选掉不合理的实体类型，如非汉字文本中的PERSON实体。主要是为了减少调用NLP模型的次数。
    Args:
        candi_entities: 文本对应的候选实体词典

    Returns: dict
    """
    chinese_pattern = r'[\u4e00-\u9fa5]'
    for text, entity_list in candi_entities.items():
        if config.PERSON in entity_list or config.LOCATION in entity_list \
                or config.COMPANY_NAME in entity_list:
            match = re.search(chinese_pattern, text, re.MULTILINE)
            if match is None:
                left = [x for x in entity_list if x not in
                        (config.PERSON, config.LOCATION, config.COMPANY_NAME)]
                candi_entities[text] = left
    return candi_entities
