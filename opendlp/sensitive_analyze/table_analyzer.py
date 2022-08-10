import pandas as pd
import logging
from collections import Counter
from opendlp.sensitive_analyze.analyzer_engine import AnalyzerEngine
from opendlp.sensitive_analyze.entity_recognize.utils import get_threshold
from opendlp.sensitive_analyze.entity_recognize.conf import config
from opendlp.sensitive_analyze.exceptions import FILE_READ_ERROR

LOGGER = logging.getLogger('openDLP')


def analyze(csv_table_path, regex_pattern_file=None, thresholds=None):
    """表格敏感数据分析，识别出每一列数据所属敏感数据类型，如果不是敏感数据则为"OTHER"

    Args:
        csv_table_path: 数据表文件路径，csv文件
        regex_pattern_file: 自定义类型的识别正则表达式文件，json文件
        thresholds: 敏感数据识别判断阈值，一列中某个敏感数据类型的占比达到阈值后则认为是此列数据是该敏感数据类型

    Returns:
        敏感数据识别结果字典，键为列名，值为字典。值字典中"success"是否识别成功，"type"表示敏感数据类型，"fraction"表示该列中type类型的占比。
        eg: {"qq": {"success": True, "type": "OTHER", "fraction": "9/10"},
        "pwd": {"success": True, "type": "PASSWORD", "fraction": "10/10"}}

    """
    LOGGER.info('start analyzing......')
    try:
        data_table = pd.read_csv(csv_table_path, dtype=str)
    except Exception as error:
        raise FILE_READ_ERROR(error) from error

    LOGGER.info('table columns: {}'.format(len(data_table.columns)))
    LOGGER.info('table rows: {}'.format(len(data_table)))
    data_num = min(len(data_table), config.MAX_ROWS)
    data_table = data_table[0:data_num]
    LOGGER.info('after select at most {} rows, table rows: {}'.format(config.MAX_ROWS, len(data_table)))
    data_table = data_table.fillna('')  #空值是nan，取出来后的数据类型是float

    if regex_pattern_file is not None:
        analyzer = AnalyzerEngine(regex_pattern_file)
    else:
        analyzer = AnalyzerEngine()

    result_dic = dict()
    success_flag_dic = dict()
    for name in data_table.columns:
        LOGGER.info('analyzing {} ......'.format(name))
        try:
            result_dic[name] = analyzer.analyze(data_table[name], thresholds)
            success_flag_dic[name] = True
        except Exception as error:
            success_flag_dic[name] = False
            LOGGER.error(error)

    result = {}
    for key in success_flag_dic.keys():
        if key not in result_dic.keys():
            result[key] = {'success': success_flag_dic[key]}
            continue

        values = result_dic.get(key)
        most_cnt = 0
        most_entity = None
        counter = Counter(values)
        if len(counter) > 0:
            most_common = counter.most_common(1)
            # most entity 可能是 None，result_predefined 中None可能最多
            most_entity = most_common[0][0]
            most_cnt = most_common[0][1]

        threshold = get_threshold(thresholds, most_entity)
        if most_entity is not None and most_cnt / len(values) >= threshold:
            entity = most_entity
        else:
            entity = config.OTHER
        result[key] = {'success': success_flag_dic[key],
                       'type': entity,
                       'fraction': str(most_cnt)+'/'+str(len(values))}
    return result
