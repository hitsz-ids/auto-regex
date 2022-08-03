import grpc
from grpc_module import sensitive_pb2, sensitive_pb2_grpc
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

'''
train_data_file = 'tests/data/regex_generation/regex_gen_test_1000.csv'
regex_name = 'ID_CARD'
status, result = send_request(train_data_file, regex_name)
print('status.code: ', status.code)
print('status.msg: ', status.msg)
print('result: ', result)
'''

data_dir = 'tests/data/regex_generation/debug-data/'
regex_names = ['ID_CARD', 'TELEPHONE', 'MOBILE_PHONE', 'EMAIL', 'LICENSE_PLATE',
               'BANK_CARD', 'PASSPORT', 'SOCIAL_CREDIT_CODE', 'IPV4', 'IPV6', 'MAC',
               'DOMAIN_NAME', 'POSTCODE', 'DATE']
for regex_name in regex_names:
    train_data_file = os.path.join(data_dir, regex_name+'.csv')
    status, result = send_request(train_data_file, regex_name)
    print('status.code: ', status.code)
    print('result: ', result)
    print('\n')


