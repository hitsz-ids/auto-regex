# openDLP

openDLP(open Data Loss Prevention)是一个敏感数据识别工具，使用正则表达式、人工智能算法、数据校验规则等多种技术对结构化数据表和Json之类的半结构化数据进行字段级敏感数据识别，可以帮助企业和组织进行数据资产分类分级，保障数据安全。

正则表达式是敏感数据识别的常用技术手段，openDLP的正则表达式智能生成功能能够基于提供的正、负训练样本数据，自动学习生成正则表达式，帮助提高正则表达式编写效率。

| 重要链接                                                     |                                                              |
| ------------------------------------------------------------ | ------------------------------------------------------------ |
| :book:  [文档](https://opendlp.readthedocs.io)               | 项目API文档                                                  |
| :octocat:  [项目仓库](https://github.com/hitsz-ids/openDLP)  | 项目Github仓库                                               |
| :scroll: [License](https://github.com/hitsz-ids/openDLP/blob/main/LICENSE) | Apache-2.0 license                                           |
| <img src="docs/imgs/AI靶场logo.png" style="zoom:100%;" /> 示例 | 在[AI靶场](https://datai.pcl.ac.cn/)上运行opendlp示例（敬请期待） |

[文档]: https://opendlp.readthedocs.io
[项目仓库]: https://github.com/hitsz-ids/openDLP
[License]: https://github.com/hitsz-ids/openDLP/blob/main/LICENSE
[AI靶场]: https://datai.pcl.ac.cn/



## 主要特性

+ 表格数据敏感数据识别：
  + 目前支持身份证号、人名等17中常见敏感数据类型识别，详见：[文档](https://opendlp.readthedocs.io)
  + 对于不在内置类型中的类别，支持用户传入正则表达式，对自定义敏感数据类型进行识别；
  + 采用神经网络分类模型、实体识别、正则表达式、数据校验规则等技术进行敏感数据识别。
+ 正则表达式生成：
  + 基于正、负样本数据，自动学习生成正则表达式；
  + 考虑了样本数据串中的频繁子字符串，能够捕获到数据中的细节特征。



## 如何安装

推荐使用 pip 命令进行安装：

```bash
pip install opendlp
```

将从[PyPI](https://pypi.org/)获取并安装最新的稳定版本。



## 快速开始

### 结构化数据表敏感字段识别

#### 示例1：使用内置敏感数据类型识别

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

#### 示例2：使用用户自定义敏感数据类型识别

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

更多使用示例见：[文档](https://opendlp.readthedocs.io/en/latest/README.html)



## 关于API

openDLP提供了表格敏感数据识别和正则表达式生成接口，具体接口参数请参考 [API文档](https://opendlp.readthedocs.io/en/latest/api/index.html)。



## 代码贡献

openDLP开源项目由**哈尔滨工业大学（深圳）数据安全研究院**发起，若您对openDLP项目感兴趣并愿意一起完善它，欢迎加入我们的开源社区。

### Owner

+ Longice(zekuncao@gmail.com) 

### Maintainer

+ Longice(zekuncao@gmail.com) 

您可以联系项目Owner，若您通过审核便可成为openDLP的Maintainer成员之一。



## 关于授权

openDLP开源项目使用 Apache-2.0 license，有关协议请参考[LICENSE](https://github.com/hitsz-ids/openDLP/blob/main/LICENSE)。



## Used by

###组织

<img src="docs/imgs/组织.png" alt="组织" style="zoom:50%;" />

###开源项目

+ [eoapi](https://github.com/eolinker/eoapi)：一个可拓展的 API 工具，简单（Easy） & 开源（OpenSource）的 API 生态系统

