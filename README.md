# auto-regex

auto-regex是一个正则表达式智能生成工具，可以基于用户提供的少量某个类型的样本数据，学习该类数据的模式特征，自动生成识别该类型数据的正则表达式，帮助提高在数据类型识别场景中的正则表达式编写效率。



## 目录

- [应用场景](#应用场景)
- [主要特性](#主要特性)
- [安装](#安装)
- [快速开始](#快速开始)
- [API](#API)
- [维护者](#维护者)
- [如何贡献](#如何贡献)
- [许可证](#许可证)
- [Used by](#Used-by)



## 应用场景

- 数据分类分级

  数据分类分级场景中，数据库中有大量数据表和字段，人工一个个查看分析标注敏感类型，效率低。通过正则表达式智能生成工具，对每一个敏感类型，只需人工查看少量表，找到一列该类型数据，提供给正则表达式智能生成工具，生成正则表达式，对数据库中其他大量的表字段进行敏感类型识别。

- 数据流动过程中的敏感数据识别

  数据库中的数据在应用程序间流动时在数据分类分级阶段标注的敏感标签一般不会被保留，通过正则表达式智能生成工具生成的正则表达式可以在数据流动的关键节点上进行敏感数据识别，掌握敏感数据的流向。

  

## 主要特性

+ 基于正、负样本数据，自动学习生成正则表达式；
+ 考虑了样本数据串中的频繁子字符串，能够捕获到数据中的细节特征。



## 安装

推荐使用 pip 命令进行安装：

```bash
pip install auto-regex
```

将从[PyPI](https://pypi.org/)获取并安装最新的稳定版本。



## 快速开始

```python
from auto_regex.generator import generate
regex_name = 'id_card'
train_data_file = 'tests/data/ID_CARD.csv'  # 本项目下tests目录中的数据文件

result = generate(regex_name, train_data_file, init_population_size=500, max_iterations=100)
```

会输出多个正则表达式及其在示例数据上的评估指标，供选择使用：

```bash
name: id_card, pattern: \d{6,6}19\d{9,9}\w|\d{6,6}20\d{9,9}\w, precision: 1.0, recall: 1.0
name: \d\d\d\d\d\d19\d\d\d\d\d\d\d\d\d\w precision: 1.0, recall: 0.6144
name: \d{6,6}20\d{9,9}\w precision: 1.0, recall: 0.3856
```

train_data_file文件中有两列，第一列列名为'positive'，表示正样本，第二列列名为'negative'，表示负样本。对于身份证号码类型，正样本为身份证号码，负样本为非身份证号码数据，如电话号码。



## API

auto-regex提供了正则表达式生成接口，具体接口参数请参考 [API文档](https://hitsz-ids.github.io/auto-regex/docs/zh/generate)。



## 实现原理

主要原理基于以下论文：

[Revisiting Regex Generation for Modeling Industrial Applications by Incorporating Byte Pair Encoder](https://arxiv.org/abs/2005.02558)



## 测试效果

使用身份证号、统一社会信用代码等数据生成的正则表达式，在新的测试数据上的评估指标如下：

```
                   precision    recall  f1-score   support
                   
           ID_CARD     0.9997    1.0000    0.9999     10000
SOCIAL_CREDIT_CODE     0.4784    1.0000    0.6472     10000
      MOBILE_PHONE     0.9890    0.0898    0.1646     10000
              DATE     1.0000    1.0000    1.0000     10000
         BANK_CARD     0.3204    0.7423    0.4476     10000
       DOMAIN_NAME     1.0000    0.8446    0.9158     10000
             EMAIL     1.0000    0.0229    0.0448     10000
         TELEPHONE     0.8938    0.6079    0.7236     10000
              IPV4     1.0000    0.0414    0.0795     10000
          POSTCODE     1.0000    1.0000    1.0000     10000
          PASSPORT     1.0000    1.0000    1.0000     10000
               MAC     1.0000    1.0000    1.0000     10000
     LICENSE_PLATE     1.0000    0.9494    0.9740     10000

         micro avg     0.7725    0.7153    0.7428    130000
         macro avg     0.8986    0.7153    0.6921    130000
```



##与类似工具的区别

其他的如[Regex-generator](https://github.com/maojui/Regex-Generator)之类的正则表达式生成工具目标是学习一个字符串集合中的特征，不考虑同类型的集合外的新数据的识别问题。



## 维护者

auto-regex开源项目由**哈尔滨工业大学（深圳）数据安全研究院**发起，若您对auto-regex项目感兴趣并愿意一起完善它，欢迎加入我们的开源社区。

### Owner

+ Longice(zekuncao@gmail.com) 

### Maintainer

+ Longice(zekuncao@gmail.com) 

您可以联系项目Owner，若您通过审核便可成为auto-regex的Maintainer成员之一。



## 如何贡献

非常欢迎你的加入！[提一个 Issue](https://github.com/hitsz-ids/auto-regex/issues/new) 或者提交一个 Pull Request。



## 许可证

auto-regex开源项目使用 Apache-2.0 license，有关协议请参考[LICENSE](https://github.com/hitsz-ids/auto-regex/blob/main/LICENSE)。



## Used by

<img src="docs/imgs/组织.png" alt="组织" style="zoom:50%;" />

