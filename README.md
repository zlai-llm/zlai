<div align="center">

# ZLAI

[![Python package](https://img.shields.io/pypi/v/zlai)](https://pypi.org/project/zlai/)
[![Python](https://img.shields.io/pypi/pyversions/zlai.svg)](https://pypi.python.org/pypi/zlai/)
[![PyPI - Downloads](https://img.shields.io/pypi/dm/zlai)](https://pypi.org/project/zlai/)
[![GitHub star chart](https://img.shields.io/github/stars/zlai-llm/zlai?style=flat-square)](https://star-history.com/#zlai-llm/zlai)
[![GitHub Forks](https://img.shields.io/github/forks/zlai-llm/zlai.svg)](https://star-history.com/#zlai-llm/zlai)
[![Doc](https://img.shields.io/badge/Doc-online-green)](https://zlai-llm.github.io/zlai-doc/)
[![Issue](https://img.shields.io/github/issues/zlai-llm/zlai)](https://github.com/zlai-llm/zlai/issues/new/choose)
[![Discussions](https://img.shields.io/github/discussions/zlai-llm/zlai)](https://github.com/zlai-llm/zlai/issues/new/choose)
[![CONTRIBUTING](https://img.shields.io/badge/Contributing-8A2BE2)](https://github.com/zlai-llm/zlai/blob/main/CONTRIBUTING.md)
[![License: MIT](https://img.shields.io/github/license/zlai-llm/zlai)](https://github.com/zlai-llm/zlai/blob/main/LICENSE)

> 适配中文大模型的`Langchain-Agent`

</div>

## 简介

1. `LLM`: 调用大模型的便捷方法，包括本地大模型与线上大模型，其中包括主流大模型`API`，`GLM/Qwen/Yi/MoonShot`等100多种大模型。采用了统一的调用风格与方式，使得大模型调用更加便捷。
2. `Message`: 消息管理机制，方便管理`System/User/Assistant Message`，并进行大模型对话的记忆管理。
3. `Embedding`: 提供一系列向量化方法，包括本地与API向量化模型的调用，以及文本的各类向量化匹配、与向数据库对接等功能。
4. `RAG`: 提供一系列文档知识库问答方法。
5. `AgentTask`: 提供Agent任务流的调度，实现Agent任务的各种自动化流转。
6. `AgentTools`: 提供一系列Agent工具函数，实现更方便的Agent使用，如让大模型实现股票期货数据查询问答、数据分析作图等。
7. `Other`: 其他便捷方法。

[详细文档](https://zlai-llm.github.io/zlai-doc/#/)

-----

## 如何安装？

```bash
# [推荐] 安装最新版本ZLAI的所有模块
pip install zlai[all] -U
# [推荐] 最轻量化安装
pip install zlai[tiny] -U
# [推荐] 安装全部大模型API依赖
pip install zlai[api] -U
```

您也可以在[GitHub](https://github.com/zlai-llm/zlai.git)/[PyPi](https://pypi.org/project/zlai/)查看最新代码与最新发行版本。

[Quick Start](https://zlai-llm.github.io/zlai-doc/#/quick_start)

[版本计划](https://zlai-llm.github.io/zlai-doc/#/version/version)

## Star History

[![Star History Chart](https://api.star-history.com/svg?repos=zlai-llm/zlai&type=Date)](https://star-history.com/#zlai-llm/zlai&Date)

-----

<div align="center">

> Wechat

<center>
<img src="https://raw.githubusercontent.com/zlai-llm/zlai/master/assets/wechat.jpg" width="160px">
<h5>微信群</h5>
</center>

</div>

-----
@2024/03/27
