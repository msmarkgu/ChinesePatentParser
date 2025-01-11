# ChinesePatentParser

A Python script that can parse a Chinese patent of invention type to extract named fields, sections, and subsections in it. The parsing result can then be used for various NLP tasks such as patent analysis, claim comparison, and patent infringement evaluation.

Chinese patent of invention type typically has fixed template with named fields, sections and subsections, like below:

![patent image](./example/Alibaba.png)

The parser uses regular expression to extract the named fields, sections and subsections.

# Dependencies

The script uses [PdfPlumber](https://github.com/jsvine/pdfplumber) to extract text in the input PDF.

# Installation

Simply run in command line:

```
pip install ChinesePatentParser
```

# How to Use

To use the script in command line, run it like following:

```
python -m ChinesePatentParser.patent_parser ./example/Alibaba.pdf > ./example/Alibaba.json
```

To use the parser in your script, do something like below:

```
from ChinesePatentParser import patent_parser  # Absolute import

pdf_path = './example/Alibaba.pdf'

parser = patent_parser.PatentParser()

data = parser.parse_pdf_file(pdf_path)

data_json = data.to_json()

print(f"\n{data_json}")
```

# Example Result

The parser will extract all the named fields, sections and subsections to output as in JSON format, like below:

```
{
    "申请公布号": "CN 102890692 A",
    "申请公布日": "2013.01.23 A 296098201 NC (19)中华人民共和国国家知识产权局 *CN102890692A* (12)发明专利申请",
    "申请号": "201110207897.1",
    "申请日": "2011.07.22",
    "申请人": "阿里巴巴集团控股有限公司\n地址 英属开曼群岛大开曼资本大厦一座四\n层847号邮箱",
    "发明人": "孙一鸣 强琦 蔡波洋 金晓军\n吴宗远",
    "代理机构": "北京润泽恒知识产权代理有\n限公司 11319\n代理人 苏培华",
    "国际分类号": "l.\nG06F 17/30(2006.01)\n权利权要利求要书求 书2 页2页 说 说明明书书 121 2页页 附附图图 77 页页",
    "发明名称": "一种网页信息抽取方法及抽取系统",
    "摘要": "本申请提供了一种网页信息抽取方法及抽取系统，...，可以实现大批量网页高度自动化的信息抽取。",
    "权利要求书": [
      "1.一种网页信息抽取方法，其特征在于，包括：\n通过界面交互方式配置网页信息抽取任务，并存入数据库；\n监控数据库，当发现数据库中存入新的网页信息抽取任务后，将所述新的网页信息抽\n取任务发送给调度器；\n调度器解析网页信息抽取任务，并依据解析结果自动执行所述网页信息抽取任务。",
      "2. 根据权利要求 1 所述的方法，其特征在于，..., 对所述点击行为或抽取行为进行细化配置。",
      ...,
      ...,
      ...,
      "11.根据权利要求10所述的系统，其特征在于，...，则依据点击行为的配置调度渲染引擎进行渲染。\n33"
    ],
    "技术领域": [
      "[0001] 本申请涉及网页处理技术，特别是涉及一种网页信息抽取方法及抽取系统。"
    ],
    "背景技术": [
      "[0002] 网页信息抽取就是获取网页的数据，...，另一种就是利用机器学习方法进行抽取。",
      ...,
      ...,
      ...,
      "[0007] 因此，目前还没有一种真正简单、...网应用进行网页信息的自动抽取。"
    ],
    "发明内容": [
      "[0008] 本申请提供了一种网页信息抽取方法及抽取系统，...技术门槛较高的问题。",
      "[0009] 为了解决上述问题，本申请公开了一种网页信息抽取方法，包括：",
      ...,
      ...,
      ...,
      "[0046] 当然，实施本申请的任一产品不一定需要同时达到以上所述的所有优点。"
    ],
    "附图说明": [
      "[0047] 图1是本申请实施例所述一种网页信息抽取方法的流程图；",
      "[0048] 图2是本申请实施例中页面节点的示意图；",
      ...,
      ...,
      ...,
      "[0055] 图9是本申请实施例所述一种网页信息抽取系统的结构图。"
    ],
    "具体实施方式": [
      "[0056] 为使本申请的上述目的、特征和优点...进一步详细的说明。",
      "[0057] 本申请提供了一种网页信息抽取方法及系统，...，可实现针对互联网站点的信息抽取。",
      ...,
      ...,
      ...,
      "[0244] 以上对本申请所提供的一种网页信息抽取方法及抽取系统，..., 本申请的限制。\n1155"
    ]
  }

```

See the [json file](./example/Alibaba.json) in the example folder for complete extraction result of the example.

# Acknowledgement

Thanks to the authors of all the dependencies libraries, the Python and Open Source Community.
