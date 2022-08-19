# Service

service中是对opendlp sdk进行grpc封装的服务。

## 环境安装

下载项目：

```
git clone https://github.com/hitsz-ids/openDLP.git
```

安装opendlp：

```
pip install opendlp 
```

也可不执行 pip install opendlp，用pip install -r requirements.txt安装依赖包，然后源码执行，pycharm会正常，在终端中可能需要配置一下PYTHONPATH。

安装service相关依赖包：

```
pip install -r requirements_service.txt
```

## 使用方法

### 敏感数据识别模块

#### 下载资源文件（可选）

本项目中的命名实体识别使用了HanLP开源项目中的模型，使用前需先下载相关模型文件并解压到指定目录，如未手动下载，第一次运行时会自动下载。

+ [close_tok_pos_ner_srl_dep_sdp_con_electra_small_20210111_124159.zip](https://file.hankcs.com/hanlp/mtl/close_tok_pos_ner_srl_dep_sdp_con_electra_small_20210111_124159.zip) 下载解压到HANLP_HOME/mtl，其中HANLP_HOME默认为/root/.hanlp，可修改。
+ [electra_zh_small_20210706_125427.zip](https://file.hankcs.com/hanlp/transformers/electra_zh_small_20210706_125427.zip) 下载解压到HANLP_HOME/transformers。
+ [char_table.json.zip](https://file.hankcs.com/corpus/char_table.json.zip) 下载解压到HANLP_HOME/thirdparty/file.hankcs.com/corpus。

#### 启动服务

执行 opendlp_server.py 文件启动敏感数据识别服务。

#### 请求服务

敏感数据识别服务模块主要接收三个参数：

+ to_analyze_file_path：待进行敏感数据识别的表格文件的路径（必需参数），目前仅支持csv文件，且需要有表头。

+ user_define_pattern_file：用户自定义正则表达式json文件（可选参数），例如：

  ```json
  {
      "QQ": ["\\b[1-9][0-9]{4,}\\b"],
      "PASSWORD": ["\\b\\w{6,18}\\b"]
  }
  ```

+ thresholds：判断阈值json串，内容为各个敏感数据类型的判断阈值（可选参数，如不设置则使用默认配置）。例如，某一列中有90%的元素识别为人名，人名类型的阈值为0.8的话，该列类型会被判断为人名，如果人名类型的阈值设置为0.95的话，则不会被判断为人名，会被判断为OTHER。

接口请求调用示例如下（更多示例见tests/test_client.py）：

```python
import grpc
from service.grpc_module import sensitive_pb2, sensitive_pb2_grpc

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
print(result)
```

其输出为：

```shell
{"QQ": {"success": true, "type": "OTHER", "fraction": "9/10"}, "PASSWORD": {"success": true, "type": "PASSWORD", "fraction": "10/10"}}
```

“QQ”为数据表中的列名，“success”标识该列是否识别成功，“type”为识别成的敏感数据类型，OTHER表示不是敏感数据类型，“fraction”为该列中识别比例最高的类型的占比，这里的"9/10"的含义是该列有10个元素，有9个识别为了QQ，但QQ的判断阈值设置的是1，大于0.9，所以其类型被判断为了OTHER。



### 正则表达式生成

#### 启动服务

执行 opendlp_server.py 文件启动敏感数据识别服务。

#### 请求服务

正则表达式生成服务模块主要接收两个参数：

+ regex_name: 正则表达式识别的数据类型名称
+ train_data_file: 训练数据，csv格式，包含“positive”和“negative”列名，分别表示正样本和负样本。

接口请求调用示例如下：

```python
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
regex_names = 'ID_CARD'
train_data_file = os.path.join(data_dir, regex_name+'.csv')
status, result = send_request(train_data_file, regex_name)
print(result)
```

会输出类似如下信息：

```
regex_name: "ID_CARD"
regex_pattern: "\\d{9,9}20\\d{6,6}\\w"
```

