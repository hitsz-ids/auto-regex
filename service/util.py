import os
import json
import logging
import pandas as pd
from service.grpc_module import autoregex_pb2

LOGGER = logging.getLogger('AutoRegex')


def check_param_regex_generate(status, regex_name, train_data_file):
    if regex_name == '':
        status.code = autoregex_pb2.PARAMETER_ERROR
        status.msg = '正则表达式名称参数 regex_name 不能为空。'
        return status
    if train_data_file == '':
        status.code = autoregex_pb2.PARAMETER_ERROR
        status.msg = '正则表达式生成训练数据文件参数 train_data_file 不能为空。'
        return status
    if not os.path.isfile(train_data_file):
        status.code = autoregex_pb2.PARAMETER_ERROR
        status.msg = '{}文件不存在，或不是文件。请检查参数。'.format(train_data_file)
        return status
    if not train_data_file.endswith('.csv'):
        status.code = autoregex_pb2.PARAMETER_ERROR
        status.msg = '正则表达式生成训练数据文件{}不是csv文件，目前仅支持csv文件。'.format(train_data_file)
        return status
    try:
        df = pd.read_csv(train_data_file, nrows=3)
    except:
        status.code = autoregex_pb2.FILE_READ_ERROR
        status.msg = '训练样例数据文件{}读取失败。'.format(train_data_file)
        return status
    if not ('positive' in df.columns and 'negative' in df.columns):
        status.code = autoregex_pb2.FILE_READ_ERROR
        status.msg = '训练样例数据中需包含{}和{}列名'.format('positive', 'negative')
        return status

    status.code = autoregex_pb2.OK
    return status