import grpc
from grpc_module import sensitive_pb2, sensitive_pb2_grpc
import unittest
import os

BASE_PATH = os.path.dirname(__file__)

def send_request(to_analyze_file_path, user_define_pattern_file=None, thresholds=None):
    request = sensitive_pb2.SensitiveRequest()
    request.to_analyze_file_path = to_analyze_file_path
    if user_define_pattern_file is not None:
        request.user_define_pattern_file = user_define_pattern_file
    if thresholds is not None:
        request.thresholds = thresholds

    with grpc.insecure_channel('127.0.0.1:40051') as channel:
        stub = sensitive_pb2_grpc.SensitiveDataAnalyzerServiceStub(channel)
        response = stub.SensitiveAnalyze(request)
        status = response.status
        result = response.result
    return status, result


class TestSensitiveServiceErrors(unittest.TestCase):
    def test_param_error_empty_param(self):
        # to_analyze_file_path参数为空
        to_analyze_file_path = ''
        status, result = send_request(to_analyze_file_path)
        self.assertEqual(status.code, 10000)
        self.assertEqual(status.msg, '待识别数据表文件参数 to_analyze_file_path 不能为空。')
        self.assertEqual(result, '{}')

    def test_param_error_file_not_exist_analyze(self):
        # analyze文件不存在
        to_analyze_file_path = os.path.join(BASE_PATH, 'data/data-not-exist.csv')
        status, result = send_request(to_analyze_file_path)
        self.assertEqual(status.code, 10000)
        self.assertEqual(status.msg, '{}文件不存在，或不是文件。请检查参数。'.format(to_analyze_file_path))
        self.assertEqual(result, '{}')

    def test_param_error_file_not_exist_pattern(self):
        # pattern文件不存在
        to_analyze_file_path = os.path.join(BASE_PATH, 'data/data1.csv')
        user_define_pattern_file = os.path.join(BASE_PATH, 'data/pattern-not-exist.json')
        status, result = send_request(to_analyze_file_path, user_define_pattern_file)
        self.assertEqual(status.code, 10000)
        self.assertEqual(status.msg, '{}文件不存在，或不是文件。请检查参数。'.format(user_define_pattern_file))
        self.assertEqual(result, '{}')

    def test_param_error_file_type_error_analyze(self):
        # analyze文件后缀不是csv
        to_analyze_file_path = os.path.join(BASE_PATH, 'data/pattern.json')
        status, result = send_request(to_analyze_file_path)

        self.assertEqual(status.code, 10000)
        self.assertEqual(status.msg, '待识别数据文件{}不是csv文件，目前仅支持csv文件。'.format(to_analyze_file_path))
        self.assertEqual(result, '{}')

    def test_param_error_file_type_error_pattern(self):
        # pattern文件后缀不是json
        to_analyze_file_path = os.path.join(BASE_PATH, 'data/data1.csv')
        user_define_pattern_file = os.path.join(BASE_PATH, 'data/data1.csv')
        status, result = send_request(to_analyze_file_path, user_define_pattern_file)
        self.assertEqual(status.code, 10000)
        self.assertEqual(status.msg, '用户自定义正则文件{}不是json文件。'.format(user_define_pattern_file))
        self.assertEqual(result, '{}')

    def test_param_error_thresholds_not_json(self):
        # thresholds参数无法转换为json
        to_analyze_file_path = os.path.join(BASE_PATH, 'data/data1.csv')
        user_define_pattern_file = os.path.join(BASE_PATH, 'data/pattern.json')
        thresholds = '{"hello worlds"}'
        status, result = send_request(to_analyze_file_path, user_define_pattern_file, thresholds)
        self.assertEqual(status.code, 10000)
        self.assertEqual(status.msg, 'threshold参数: {}无法转换为json'.format(thresholds))
        self.assertEqual(result, '{}')

    def test_param_error_thresholds_bad_value(self):
        # threshold参数中存在无法转换为浮点数的值！
        to_analyze_file_path = os.path.join(BASE_PATH, 'data/data1.csv')
        user_define_pattern_file = os.path.join(BASE_PATH, 'data/pattern.json')
        thresholds = '{"NAME":0.8, "ADDRESS":"0.7", "MAIL":"a"}'
        status, result = send_request(to_analyze_file_path, user_define_pattern_file, thresholds)
        self.assertEqual(status.code, 10000)
        'thresholds参数: {}中存在无法转换为浮点数的值！'.format(thresholds)
        self.assertEqual(result, '{}')

    def test_file_read_error(self):
        # 读取文件错误
        to_analyze_file_path = os.path.join(BASE_PATH, 'data/error-test/data-gbk.csv')
        status, result = send_request(to_analyze_file_path)
        self.assertEqual(status.code, 10001)
        self.assertEqual(status.msg, '待识别数据表文件{}读取失败。'.format(to_analyze_file_path))
        self.assertEqual(result, '{}')

        to_analyze_file_path = os.path.join(BASE_PATH, 'data/error-test/empty.csv')
        status, result = send_request(to_analyze_file_path)
        self.assertEqual(status.code, 10001)
        self.assertEqual(status.msg, '待识别数据表文件{}读取失败。'.format(to_analyze_file_path))
        self.assertEqual(result, '{}')

    def test_json_file_parse_error(self):
        # json文件解析失败
        to_analyze_file_path = os.path.join(BASE_PATH, 'data/data1.csv')
        user_define_pattern_file = os.path.join(BASE_PATH, 'data/error-test/json-error.json')
        status, result = send_request(to_analyze_file_path, user_define_pattern_file)
        self.assertEqual(status.code, 10002)
        self.assertEqual(status.msg, '用户自定义正则文件{}解析失败。'.format(user_define_pattern_file))
        self.assertEqual(result, '{}')


def strip_white_space(str):
   return str.replace(" ", "").replace("\t", "").replace("\n", "")


class TestSensitiveServiceNormal(unittest.TestCase):

    def test_dataset_test_cleaner(self):
        to_analyze_file_path = os.path.join(BASE_PATH, 'data/dataset-test.csv')
        status, result = send_request(to_analyze_file_path)
        print(result)
        self.assertEqual(status.code, 0)
        self.assertEqual(status.msg, '识别成功。')
        self.assertEqual(strip_white_space(result), strip_white_space(
            '''{"PERSON": {"success": true, "type": "PERSON", "fraction": "969/1000"},
         "ID_CARD": {"success": true, "type": "ID_CARD", "fraction": "1000/1000"},
         "TELEPHONE": {"success": true, "type": "TELEPHONE", "fraction": "1000/1000"},
         "MOBILE_PHONE": {"success": true, "type": "MOBILE_PHONE", "fraction": "1000/1000"},
         "EMAIL": {"success": true, "type": "EMAIL", "fraction": "971/1000"},
         "LICENSE_PLATE": {"success": true, "type": "LICENSE_PLATE", "fraction": "1000/1000"},
         "BANK_CARD": {"success": true, "type": "BANK_CARD", "fraction": "1000/1000"},
         "PASSPORT": {"success": true, "type": "PASSPORT", "fraction": "1000/1000"},
         "COMPANY_NAME": {"success": true, "type": "COMPANY_NAME", "fraction": "789/1000"},
         "SOCIAL_CREDIT_CODE": {"success": true, "type": "SOCIAL_CREDIT_CODE", "fraction": "1000/1000"},
         "IPV4": {"success": true, "type": "IPV4", "fraction": "1000/1000"},
         "IPV6": {"success": true, "type": "IPV6", "fraction": "1000/1000"},
         "MAC": {"success": true, "type": "MAC", "fraction": "1000/1000"},
         "DOMAIN_NAME": {"success": true, "type": "DOMAIN_NAME", "fraction": "965/1000"},
         "LOCATION": {"success": true, "type": "LOCATION", "fraction": "997/1000"},
         "POSTCODE": {"success": true, "type": "POSTCODE", "fraction": "993/1000"},
         "DATE": {"success": true, "type": "DATE", "fraction": "1000/1000"}}'''))

    def test_data1(self):
        to_analyze_file_path = os.path.join(BASE_PATH, 'data/data1.csv')
        status, result = send_request(to_analyze_file_path)
        print(result)
        self.assertEqual(status.code, 0)
        # 把table_analyzer中的data_table = data_table.fillna('')注释掉，此测试函数可以测试到 10003，经测试是正常的。

    def test_data2(self):
        to_analyze_file_path = os.path.join(BASE_PATH, 'data/data2.csv')
        status, result = send_request(to_analyze_file_path)
        print(result)
        self.assertEqual(status.code, 0)

    def test_data3(self):
        to_analyze_file_path = os.path.join(BASE_PATH, 'data/data3.csv')
        status, result = send_request(to_analyze_file_path)
        print(result)
        self.assertEqual(status.code, 0)

    def test_data4(self):
        to_analyze_file_path = os.path.join(BASE_PATH, 'data/data4.csv')
        status, result = send_request(to_analyze_file_path)
        print(result)
        self.assertEqual(status.code, 0)

    def test_data_empty(self):
        to_analyze_file_path = os.path.join(BASE_PATH, 'data/data-empty.csv')
        status, result = send_request(to_analyze_file_path)
        print(result)
        self.assertEqual(status.code, 0)

    def test_data_udf(self):
        to_analyze_file_path = os.path.join(BASE_PATH, 'data/data-udf.csv')
        user_define_pattern_file = os.path.join(BASE_PATH, 'data/pattern.json')
        status, result = send_request(to_analyze_file_path, user_define_pattern_file)
        print(result)
        self.assertEqual(status.code, 0)
        self.assertEqual(strip_white_space(result), strip_white_space(
            '{"QQ": {"success": true, "type": "QQ", "fraction": "9/10"}, '
            '"PASSWORD": {"success": true, "type": "PASSWORD", "fraction": "10/10"}}'))

    def test_thresholds(self):
        to_analyze_file_path = os.path.join(BASE_PATH, 'data/data-udf.csv')
        user_define_pattern_file = os.path.join(BASE_PATH, 'data/pattern.json')
        thresholds = '{"QQ":1}'
        status, result = send_request(to_analyze_file_path, user_define_pattern_file, thresholds)
        print(result)
        self.assertEqual(status.code, 0)
        self.assertEqual(strip_white_space(result), strip_white_space(
            '{"QQ": {"success": true, "type": "OTHER", "fraction": "9/10"}, '
            '"PASSWORD": {"success": true, "type": "PASSWORD", "fraction": "10/10"}}'))
