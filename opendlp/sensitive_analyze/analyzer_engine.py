
from collections import Counter
from itertools import compress
from typing import Optional, List

from opendlp.sensitive_analyze.entity_classify.classifier import EntityClassifier
from opendlp.sensitive_analyze.entity_recognize import RecognizerEngine
from opendlp.sensitive_analyze.entity_recognize import RecognizerRegistry
from opendlp.sensitive_analyze.entity_recognize.utils import get_threshold
from opendlp.sensitive_analyze.utils import filter_entities


class AnalyzerEngine:
    """
    敏感数据分析引擎
    """
    def __init__(self, pattern_file: Optional[str] = ''):
        """敏感数据分析引擎构造函数
        Args:
            pattern_file: 自定义类型的识别正则表达式文件，json文件
        """
        self.pattern_file = pattern_file
        self.entity_classifier = EntityClassifier()
        self.registry = RecognizerRegistry(pattern_file)
        self.recognizer_engine = RecognizerEngine()

    def analyze(self, texts: List[str], thresholds):
        """对字符串列表中的数据进行敏感数据分析

        Args:
            texts: 字符串列表
            thresholds: 敏感数据识别判断阈值，一列中某个敏感数据类型的占比达到阈值后则认为是此列数据是该敏感数据类型

        Returns:
            字符串列表中每一个字符串的敏感数据类型
        """

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
        """对字符串列表中的数据用内置敏感数据类型进行敏感数据分析

        Args:
            texts: 字符串列表

        Returns:
            字符串列表中每一个字符串的敏感数据类型，未识别出敏感数据类型的为None
        """
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
        """对字符串列表中的数据用用户自定义敏感数据类型进行敏感数据分析

        Args:
            texts: 字符串列表
            result_predefined: 字符串列表中各个字符串用内置敏感数据类型的分析结果，没有识别出敏感数据类型的为None

        Returns:
            字符串列表中每一个字符串经过内置类型和自定义类型识别后的敏感数据类型
        """
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


