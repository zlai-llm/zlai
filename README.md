# ZLAI

> 适配中文大模型的`Langchain-Agent`

## 简介

- `LLMs`: 提供远程、本地、预训练等大模型服务
- `Embedding`: 提供远程、本地、预训练等向量化模型服务
- `prompt`: 提供prompt组织流程
- `elasticsearch`: 提供elasticsearch工具
- `agent`: 提供agent工具

> Wechat

<center>
<img src="assets/wechat-group.jpg" width="200px">
<h5>微信群</h5>
</center>

> 待增加功能

- [ ] 增加对于多模态模型的支持，图片解读、文生图等
- [ ] 增加复杂任务的动态规划
- [ ] 增加Agent生成知识图谱
- [ ] message prompt 的组织方式中的参数不能与 task completion 中的参数重名
- [ ] 对知识对话增加记忆机制，增加记忆机制在多个Agent之间的共享
  - [X] 完成`ChatAgent/Knowledge`

> 0.3.83

1. 增加了Tools-call
2. 修复了一些内容，增加了几个测试。

> 0.3.76

1. 增加了对于GLM4-API的支持
2. 增加了对Ali-Qwen2-API的支持
3. 增加了`PretrainedEmbedding`，用于提供预训练的向量化模型
4. 修改了其他bug.

-----
@2024/03/27
