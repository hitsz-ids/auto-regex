
import json
from pathlib import Path
import logging
from logging.config import fileConfig
import grpc
from concurrent import futures
from service.grpc_module import sensitive_pb2, sensitive_pb2_grpc
from service.util import check_param_sensitive, check_param_regex_generate
from opendlp.sensitive_analyze import table_analyzer, exceptions
from opendlp.regex_generation import generator


LOGGING_CONF_FILE = 'logging.ini'
fileConfig(Path(Path(__file__).parent, LOGGING_CONF_FILE))
LOGGER = logging.getLogger('openDLP')


class DLPServer(sensitive_pb2_grpc.OpenDlpServiceServicer):

    def SensitiveAnalyze(self, request, context):
        '''
        敏感数据识别接口
        '''
        LOGGER.info("------ 接收敏感数据识别参数:")
        to_analyze_file_path = request.to_analyze_file_path
        user_define_pattern_file = request.user_define_pattern_file
        thresholds = request.thresholds
        LOGGER.info("   to_analyze_file_path: {}".format(to_analyze_file_path))
        LOGGER.info("   user_define_pattern_file: {}".format(user_define_pattern_file))
        LOGGER.info("   threshold: {}".format(thresholds))

        status = sensitive_pb2.Status()
        status.code = sensitive_pb2.OK
        status = check_param_sensitive(status, to_analyze_file_path, user_define_pattern_file, thresholds)

        result = {}
        if status.code == sensitive_pb2.OK:
            if thresholds != '':
                thresholds = json.loads(thresholds)
            else:
                thresholds = dict()

            try:
                result = table_analyzer.analyze(to_analyze_file_path, user_define_pattern_file, thresholds)
            except exceptions.FILE_READ_ERROR as error:
                LOGGER.error(error)
                status.code = sensitive_pb2.FILE_READ_ERROR
                status.msg = '待识别数据表文件{}读取失败。'.format(to_analyze_file_path)
                result = {}
            except Exception as error:
                LOGGER.error(error)
                status.code = sensitive_pb2.SENSITIVE_ANALYZE_ERROR
                status.msg = '敏感数据识别失败。'
                result = {}
            else:
                status.msg = '敏感数据识别成功。'

        LOGGER.info('------ 敏感数据识别完成。')
        return sensitive_pb2.SensitiveResponse(status=status, result=json.dumps(result))

    def RegexGenerate(self, request, context):
        '''
        正则表达式生成接口
        '''
        LOGGER.info("------ 接收正则表达式生成参数:")
        regex_name = request.regex_name
        train_data_file = request.train_data_file
        LOGGER.info("   regex_name: {}".format(regex_name))
        LOGGER.info("   train_data_file: {}".format(train_data_file))

        status = sensitive_pb2.Status()
        status.code = sensitive_pb2.OK
        status = check_param_regex_generate(status, regex_name, train_data_file)
        result = sensitive_pb2.Result()
        if status.code == sensitive_pb2.OK:
            try:
                res = generator.generate(regex_name, train_data_file)
            except exceptions as error:
                LOGGER.error(error)
                status.code = sensitive_pb2.REGEX_GENERATE_ERROR
                status.msg = '正则表达式生成失败。'
            else:
                result.regex_name = res['regex_name']
                result.regex_pattern = res['regex_pattern']

        return sensitive_pb2.RegexGenerateResponse(status=status, result=result)


def main():
    LOGGER.info('启动服务，服务监听端口为:40051')
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    sensitive_pb2_grpc.add_OpenDlpServiceServicer_to_server(DLPServer(), server)
    server.add_insecure_port('[::]:40051')
    server.start()
    server.wait_for_termination()

if __name__ == '__main__':
    main()