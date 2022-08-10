import grpc
from service.grpc_module import sensitive_pb2, sensitive_pb2_grpc
import os


def send_request(train_data_file, regex_name=None):
    request = sensitive_pb2.RegexGenerateRequest()
    request.train_data_file = train_data_file
    request.regex_name = regex_name

    # ip和端口与sensitive_data_analyzer_server.py中设置的一致
    with grpc.insecure_channel('127.0.0.1:40051') as channel:
        stub = sensitive_pb2_grpc.OpenDlpServiceStub(channel)
        response = stub.RegexGenerate(request)
        status = response.status
        result = response.result
    return status, result


data_dir = 'tests/data/regex_generation/test-data/'
regex_names = ['ID_CARD']
for regex_name in regex_names:
    train_data_file = os.path.join(data_dir, regex_name+'.csv')
    status, result = send_request(train_data_file, regex_name)
    print('status.code: ', status.code)
    print('result: ', result)
    print('\n')


