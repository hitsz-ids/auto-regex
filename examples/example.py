import grpc
from grpc_module import sensitive_pb2, sensitive_pb2_grpc
from pprint import pprint

def send_request(to_analyze_file_path, user_define_pattern_file=None, thresholds=None):
    request = sensitive_pb2.SensitiveRequest()
    request.to_analyze_file_path = to_analyze_file_path
    if user_define_pattern_file is not None:
        request.user_define_pattern_file = user_define_pattern_file
    if thresholds is not None:
        request.thresholds = thresholds

    # ip和端口与sensitive_data_analyzer_server.py中设置的一致
    with grpc.insecure_channel('127.0.0.1:40051') as channel:
        stub = sensitive_pb2_grpc.SensitiveDataAnalyzerServiceStub(channel)
        response = stub.SensitiveAnalyze(request)
        status = response.status
        result = response.result
    return status, result


to_analyze_file_path = 'tests/data/data-udf.csv'
user_define_pattern_file = 'tests/data/pattern.json'
thresholds = '{"QQ":1}'
status, result = send_request(to_analyze_file_path, user_define_pattern_file, thresholds)
print('status.code: ', status.code)
print('status.msg: ', status.msg)
print('result: ', result)