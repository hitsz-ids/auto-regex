
from pathlib import Path
import logging
from logging.config import fileConfig
import grpc
from concurrent import futures
from service.grpc_module import autoregex_pb2, autoregex_pb2_grpc
from service.util import check_param_regex_generate
from autoregex import generator


LOGGING_CONF_FILE = 'logging.ini'
fileConfig(Path(Path(__file__).parent, LOGGING_CONF_FILE))
LOGGER = logging.getLogger('AuoRegex')


class Server(autoregex_pb2_grpc.AutoRegexServiceServicer):

    def RegexGenerate(self, request, context):
        '''
        正则表达式生成接口
        '''
        LOGGER.info("------ 接收正则表达式生成参数:")
        regex_name = request.regex_name
        train_data_file = request.train_data_file
        LOGGER.info("   regex_name: {}".format(regex_name))
        LOGGER.info("   train_data_file: {}".format(train_data_file))

        status = autoregex_pb2.Status()
        status.code = autoregex_pb2.OK
        status = check_param_regex_generate(status, regex_name, train_data_file)
        result = autoregex_pb2.Result()
        if status.code == autoregex_pb2.OK:
            try:
                res = generator.generate(regex_name, train_data_file)
            except Exception as error:
                LOGGER.error(error)
                status.code = autoregex_pb2.REGEX_GENERATE_ERROR
                status.msg = '正则表达式生成失败。'
            else:
                result.regex_name = res['regex_name']
                result.regex_pattern = res['regex_pattern']

        return autoregex_pb2.Response(status=status, result=result)


def main():
    LOGGER.info('启动服务，服务监听端口为:40051')
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    autoregex_pb2_grpc.add_AutoRegexServiceServicer_to_server(Server(), server)
    server.add_insecure_port('[::]:40051')
    server.start()
    server.wait_for_termination()

if __name__ == '__main__':
    main()