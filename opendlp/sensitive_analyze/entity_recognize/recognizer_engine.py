import re

from opendlp.sensitive_analyze.entity_recognize.conf import config


class RecognizerEngine:
    def __init__(self):
        pass

    def analyze(self, texts, entity, recognizer):
        # 用预定义敏感数据类型匹配

        if entity in [config.PERSON, config.COMPANY_NAME, config.LOCATION]:
            nlp_results = recognizer.analyze(text=texts, entity=entity)
            results = [None]*len(texts)
            for i in range(len(texts)):
                results[i] = nlp_results[texts[i]]  # 先不check是不是entity类型把
        else:
            texts = [re.sub(r'\s+', '', text) for text in texts]
            text = ' '+' '.join(texts)
            re_results = recognizer.analyze(text=text)

            re_result_dic = {}
            for match in re_results:
                start = match.start  # 匹配里有空格
                end = match.end
                match_text = text[start:end]
                re_result_dic[match_text] = entity or recognizer.supported_entity

            results = [None]*len(texts)
            for i in range(len(texts)):
                if texts[i] in re_result_dic.keys():
                    results[i] = re_result_dic[texts[i]]

        return results
