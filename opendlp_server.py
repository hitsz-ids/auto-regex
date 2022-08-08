import os
import json
from pathlib import Path
import logging
from logging.config import fileConfig
import grpc
from concurrent import futures
from grpc_module import sensitive_pb2, sensitive_pb2_grpc
from opendlp import table_analyzer


LOGGING_CONF_FILE = 'logging.ini'
fileConfig(Path(Path(__file__).parent, LOGGING_CONF_FILE))
LOGGER = logging.getLogger('openDLP')


def check_param(status, to_analyze_file_path, user_define_pattern_file, thresholds):
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


class Analyzer(sensitive_pb2_grpc.SensitiveDataAnalyzerServiceServicer):

    def SensitiveAnalyze(self, request, context):
        LOGGER.info("------ 接收敏感数据识别参数:")
        to_analyze_file_path = request.to_analyze_file_path
        user_define_pattern_file = request.user_define_pattern_file
        thresholds = request.thresholds
        LOGGER.info("   to_analyze_file_path: {}".format(to_analyze_file_path))
        LOGGER.info("   user_define_pattern_file: {}".format(user_define_pattern_file))
        LOGGER.info("   threshold: {}".format(thresholds))

        status = sensitive_pb2.Status()
        status.code = sensitive_pb2.OK
        status = check_param(status, to_analyze_file_path, user_define_pattern_file, thresholds)
        result = {}
        if status.code == sensitive_pb2.OK:
            status, result = table_analyzer.analyze(status, to_analyze_file_path, user_define_pattern_file, thresholds)

        return sensitive_pb2.SensitiveResponse(status=status, result=json.dumps(result))


def main():
    LOGGER.info('启动服务，服务监听端口为:40051')
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    sensitive_pb2_grpc.add_SensitiveDataAnalyzerServiceServicer_to_server(Analyzer(), server)
    server.add_insecure_port('[::]:40051')
    server.start()
    server.wait_for_termination()

if __name__ == '__main__':
    main()