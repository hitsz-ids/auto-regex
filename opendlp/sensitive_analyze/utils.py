import re
from opendlp.sensitive_analyze.entity_recognize.conf import config

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
