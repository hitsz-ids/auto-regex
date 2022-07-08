import pandas as pd
import logging
from collections import Counter
import json
from opendlp.analyzer_engine import AnalyzerEngine
from opendlp.entity_analyzer.utils import get_threshold
from opendlp.entity_analyzer.conf import config
from grpc_module import sensitive_pb2


LOGGER = logging.getLogger('openDLP')


def analyze(status, csv_table_path, regex_pattern_file='', thresholds=''):
    LOGGER.info('start analyzing......')
    try:
        data_table = pd.read_csv(csv_table_path, dtype=str)
    except Exception as error:
        LOGGER.error(error)
        status.code = sensitive_pb2.FILE_READ_ERROR
        status.msg = '待识别数据表文件{}读取失败。'.format(csv_table_path)
        return status, {}

    LOGGER.info('table columns: {}'.format(len(data_table.columns)))
    LOGGER.info('table rows: {}'.format(len(data_table)))
    data_num = min(len(data_table), config.MAX_ROWS)
    data_table = data_table[0:data_num]
    LOGGER.info('after select at most {} rows, table rows: {}'.format(config.MAX_ROWS, len(data_table)))
    data_table = data_table.fillna('')  #空值是nan，取出来后的数据类型是float

    if regex_pattern_file is not None:
        try:
            analyzer = AnalyzerEngine(regex_pattern_file)
        except Exception as error:
            status.code = sensitive_pb2.ANY_COLUMN_RECOGNIZE_ERROR
            status.msg = '敏感数据识别引擎初始化失败'
            LOGGER.error(error)
            return status, {}
    else:
        try:
            analyzer = AnalyzerEngine()
        except Exception as error:
            status.code = sensitive_pb2.ANY_COLUMN_RECOGNIZE_ERROR
            status.msg = '敏感数据识别引擎初始化失败'
            LOGGER.error(error)
            return status, {}

    if thresholds != '':
        thresholds = json.loads(thresholds)

    result_dic = dict()
    success_flag_dic = dict()
    for name in data_table.columns:
        LOGGER.info('analyzing {} ......'.format(name))
        try:
            result_dic[name] = analyzer.analyze(data_table[name], thresholds)
            success_flag_dic[name] = True
        except Exception as error:
            success_flag_dic[name] = False
            status.code = sensitive_pb2.ANY_COLUMN_RECOGNIZE_ERROR
            status.msg = "存在敏感数据识别失败的列。"
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

    LOGGER.info('analyzing finished.')
    if status.code == sensitive_pb2.OK:
        status.msg = '识别成功。'

    return status, result
