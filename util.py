import os
import json
import logging
from grpc_module import sensitive_pb2

LOGGER = logging.getLogger('openDLP')

def check_param_sensitive(status, to_analyze_file_path, user_define_pattern_file, thresholds):
    if to_analyze_file_path == '':
        status.code = sensitive_pb2.PARAMETER_ERROR
        status.msg = '待识别数据表文件参数 to_analyze_file_path 不能为空。'
        return status
    if not os.path.isfile(to_analyze_file_path):
        status.code = sensitive_pb2.PARAMETER_ERROR
        status.msg = '{}文件不存在，或不是文件。请检查参数。'.format(to_analyze_file_path)
        return status
    if user_define_pattern_file !='' and not os.path.isfile(user_define_pattern_file):
        status.code = sensitive_pb2.PARAMETER_ERROR
        status.msg = '{}文件不存在，或不是文件。请检查参数。'.format(user_define_pattern_file)
        return status

    if not to_analyze_file_path.endswith('.csv'):
        status.code = sensitive_pb2.PARAMETER_ERROR
        status.msg = '待识别数据文件{}不是csv文件，目前仅支持csv文件。'.format(to_analyze_file_path)
        return status
    if user_define_pattern_file != '' and not user_define_pattern_file.endswith('json'):
        status.code = sensitive_pb2.PARAMETER_ERROR
        status.msg = '用户自定义正则文件{}不是json文件。'.format(user_define_pattern_file)
        return status

    if thresholds != '':
        try:
            thresholds = json.loads(thresholds)
        except Exception as error:
            status.code = sensitive_pb2.PARAMETER_ERROR
            status.msg = 'threshold参数: {}无法转换为json'.format(thresholds)
            LOGGER.error(error)
            return status

        for k, v in thresholds.items():
            try:
                _ = float(v)
            except Exception as error:
                status.code = sensitive_pb2.PARAMETER_ERROR
                status.msg = 'thresholds参数: {}中存在无法转换为浮点数的值！'.format(thresholds)
                LOGGER.error(error)
                return status

    if user_define_pattern_file !='':
        try:
            _ = json.load(open(user_define_pattern_file, 'r', encoding='utf-8'))
        except Exception as error:
            status.code = sensitive_pb2.JSON_FILE_PARSE_ERROR
            status.msg = '用户自定义正则文件{}解析失败。'.format(user_define_pattern_file)
            LOGGER.error(error)
            return status

    status.code = sensitive_pb2.OK
    return status


def check_param_regex_generate(status, regex_name, train_data_file):
    if regex_name == '':
        status.code = sensitive_pb2.PARAMETER_ERROR
        status.msg = '正则表达式名称参数 regex_name 不能为空。'
        return status
    if train_data_file == '':
        status.code = sensitive_pb2.PARAMETER_ERROR
        status.msg = '正则表达式生成训练数据文件参数 train_data_file 不能为空。'
        return status
    if not os.path.isfile(train_data_file):
        status.code = sensitive_pb2.PARAMETER_ERROR
        status.msg = '{}文件不存在，或不是文件。请检查参数。'.format(train_data_file)
        return status
    if not train_data_file.endswith('.csv'):
        status.code = sensitive_pb2.PARAMETER_ERROR
        status.msg = '正则表达式生成训练数据文件{}不是csv文件，目前仅支持csv文件。'.format(train_data_file)
        return status

    status.code = sensitive_pb2.OK
    return status