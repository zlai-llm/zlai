import unittest
from zlai.documents.load_md import *
from zlai.graph import *

markdown_text = """
# 火锅产业链

## 上游

### 食材供应
- 肉类（牛肉、羊肉、猪肉）
- 海鲜
- 蔬菜水果
- 干货（大米、面粉、香料、罐头等）

### 调味品生产
- 火锅底料
- 火锅蘸料
    - 盐
    - 醋
    - 豆瓣酱
- 调料产品

### 供应链服务
- 原料采购
- 食材加工
- 配送服务

## 中游

### 餐饮服务
- 火锅餐厅
- 火锅外卖
- 方便火锅

### 咨询与管理服务
- 人员培训
- 运营咨询
- 软件管理系统

### 装修与设计服务
- 门店装修
- 品牌设计

## 下游

### 销售渠道
- 家庭消费
- 餐饮渠道
- 商超渠道
- 电商渠道

### 消费场景
- 家庭
- 餐馆
- 酒店
- 外卖及线上渠道

### 品牌文化
- 品牌建设
- 营销模式创新
"""


class TestMarkdown(unittest.TestCase):
    def test_markdown(self):
        """"""
        parse_md = ParseMarkdown(text=markdown_text)
        print(parse_md.to_table())

    def test_graph(self):
        """"""
        parse_md = ParseMarkdown(text=markdown_text)
        df = parse_md.to_table()
        graph_data = GraphData(df)
        c = graph_data.render(
            nodes=graph_data.nodes,
            links=graph_data.links,
            categories=graph_data.categories,
            show_legend=True,
        )
        c.render()

    def test_tree(self):
        """"""
        parse_md = ParseMarkdown(text=markdown_text)
        df = parse_md.to_table()

        tree_data = TreeData(df)
        c = tree_data.render(data=tree_data.chart_data, orient="LR")
        c.render()

    def test_get_source(self):
        """"""
        parse_md = ParseMarkdown(text=markdown_text)
        df = parse_md.to_table()
        data = get_node_source(df=df, node="方便火锅")
        print(data)
