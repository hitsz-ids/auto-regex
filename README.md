# openDLP

openDLP（open data loss prevention）是一个敏感数据识别工具，支持对结构化数据表进行敏感数据识别，可以帮助企业进行数据资产分类分级，保护数据安全。

openDLP根据不同的敏感数据的特点，采用正则表达式、人工智能算法等不同方法进行敏感数据识别，内置支持了多种敏感数据类型，同时支持自定义敏感数据类型识别。

openDLP的正则表达式生成功能能够基于提供的正、负训练样本数据，自动学习生成正则表达式。

| 重要链接                                                     |                                                              |
| ------------------------------------------------------------ | ------------------------------------------------------------ |
| :book:  [文档](https://opendlp.readthedocs.io/ )             | 项目文档                                                     |
| :octocat:  [项目仓库](https://github.com/hitsz-ids/openDLP)  | 项目Github仓库                                               |
| :scroll: [License](https://github.com/hitsz-ids/openDLP/blob/main/LICENSE) | Apache-2.0 license                                           |
| <img src="docs/imgs/AI靶场logo.png" style="zoom:10%;" /> 示例 | 在[AI靶场](https://datai.pcl.ac.cn/)上运行opendlp示例（敬请期待） |

[文档]: https://opendlp.readthedocs.io/
[项目仓库]: https://github.com/hitsz-ids/openDLP
[License]: https://github.com/hitsz-ids/openDLP/blob/main/LICENSE
[AI靶场]: https://datai.pcl.ac.cn/

## 特性

+ 表格数据敏感数据识别：
  + 目前支持身份证号、人名等17中常见敏感数据类型识别，详见：
  + 对于不在内置类型中的类别，支持用户传入正则表达式，对自定义敏感数据类型进行识别；
  + 采用神经网络分类模型、实体识别、正则表达式、数据校验规则等技术进行敏感数据识别。
+ 正则表达式生成：
  + 基于正、负样本数据，自动学习生成正则表达式；
  + 考虑了样本数据串中的频繁子字符串，能够捕获到数据中的细节特征。



## 安装

可通过如下命令进行安装：

```bash
pip install opendlp
```



## 快速开始

### 表格敏感数据识别

#### 下载资源文件（可选）

本项目中的命名实体识别使用了HanLP开源项目中的模型，使用前需先下载相关模型文件并解压到指定目录，如未手动下载，第一次运行时会自动下载。

+ [close_tok_pos_ner_srl_dep_sdp_con_electra_small_20210111_124159.zip](https://file.hankcs.com/hanlp/mtl/close_tok_pos_ner_srl_dep_sdp_con_electra_small_20210111_124159.zip) 下载解压到HANLP_HOME/mtl，其中HANLP_HOME默认为/root/.hanlp，可修改。
+ [electra_zh_small_20210706_125427.zip](https://file.hankcs.com/hanlp/transformers/electra_zh_small_20210706_125427.zip) 下载解压到HANLP_HOME/transformers。
+ [char_table.json.zip](https://file.hankcs.com/corpus/char_table.json.zip) 下载解压到HANLP_HOME/thirdparty/file.hankcs.com/corpus。

#### 内置敏感数据类型识别

```python
from opendlp.sensitive_analyze import table_analyzer
# openDLP github项目中的数据，根据实际情况修改路径
csv_table_path = 'openDLP/tests/data/dataset-test.csv'   
result = table_analyzer.analyze(csv_table_path)
print(result)
```

输出如下：

```
{'PERSON': {'success': True, 'type': 'PERSON', 'fraction': '969/1000'},
 'ID_CARD': {'success': True, 'type': 'ID_CARD', 'fraction': '1000/1000'},
 'TELEPHONE': {'success': True, 'type': 'TELEPHONE', 'fraction': '1000/1000'},
 'MOBILE_PHONE': {'success': True,
  'type': 'MOBILE_PHONE',
  'fraction': '1000/1000'},
 'EMAIL': {'success': True, 'type': 'EMAIL', 'fraction': '971/1000'},
 'LICENSE_PLATE': {'success': True,
  'type': 'LICENSE_PLATE',
  'fraction': '1000/1000'},
 'BANK_CARD': {'success': True, 'type': 'BANK_CARD', 'fraction': '1000/1000'},
 'PASSPORT': {'success': True, 'type': 'PASSPORT', 'fraction': '1000/1000'},
 'COMPANY_NAME': {'success': True,
  'type': 'COMPANY_NAME',
  'fraction': '789/1000'},
 'SOCIAL_CREDIT_CODE': {'success': True,
  'type': 'SOCIAL_CREDIT_CODE',
  'fraction': '1000/1000'},
 'IPV4': {'success': True, 'type': 'IPV4', 'fraction': '1000/1000'},
 'IPV6': {'success': True, 'type': 'IPV6', 'fraction': '1000/1000'},
 'MAC': {'success': True, 'type': 'MAC', 'fraction': '1000/1000'},
 'DOMAIN_NAME': {'success': True,
  'type': 'DOMAIN_NAME',
  'fraction': '965/1000'},
 'LOCATION': {'success': True, 'type': 'LOCATION', 'fraction': '997/1000'},
 'POSTCODE': {'success': True, 'type': 'POSTCODE', 'fraction': '993/1000'},
 'DATE': {'success': True, 'type': 'DATE', 'fraction': '1000/1000'}}
```

#### 用户自定义敏感数据类型识别

```python
csv_table_path = 'openDLP/tests/data/data-udf.csv'
regex_pattern_file = 'openDLP/tests/data/pattern.json'
threshold = {'QQ':1}

result = table_analyzer.analyze(csv_table_path, regex_pattern_file, threshold)
```

输出如下：

```
{'QQ': {'success': True, 'type': 'OTHER', 'fraction': '9/10'},
 'PASSWORD': {'success': True, 'type': 'PASSWORD', 'fraction': '10/10'}}
```

“QQ”为数据表中的列名，“success”标识该列是否识别成功，“type”为识别成的敏感数据类型，OTHER表示不是敏感数据类型，“fraction”为该列中识别比例最高的类型的占比，这里的"9/10"的含义是该列有10个元素，有9个识别为了QQ，但QQ的判断阈值设置的是1，大于0.9，所以其类型被判断为了OTHER。



### 正则表达式生成

```python
from opendlp.regex_generation import generator
regex_name = 'id_card'
train_data_file = '../openDLP/tests/data/regex_generation/test-data/ID_CARD.csv'

result = generator.generate(regex_name, train_data_file, init_population_size=500, max_iterations=100)
```

会输出类似下面这样的信息：

```
id_card: \d{6,6}19\d{9,9}\w|\d{6,6}20\d{9,9}\w
```



## 合作伙伴

<img src="docs/imgs/奇安信.png" style="zoom:100%;" />  <img src="docs/imgs/昂楷.png" style="zoom:80%;" />    <img src="docs/imgs/傲天.png" style="zoom:125%;" />