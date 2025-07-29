# 百炼API配置指南

## 概述

本项目已配置为使用阿里云百炼API的 `qwen-turbo` 模型。百炼API提供了与OpenAI API兼容的接口，可以直接使用 `openai` Python库进行调用。

## 配置步骤

### 1. 获取百炼API密钥

1. 访问 [阿里云百炼控制台](https://dashscope.console.aliyun.com/)
2. 注册/登录阿里云账号
3. 在控制台中创建API密钥
4. 复制API密钥（格式：`sk-xxx`）

### 2. 配置环境变量

创建或编辑 `.env` 文件：

```env
# 百炼API配置
LLM_API_KEY=sk-your-dashscope-api-key-here
MODEL_NAME=qwen-turbo
API_BASE=https://dashscope.aliyuncs.com/compatible-mode/v1
MODEL_CONTEXT_LENGTH=1000000

# 其他配置
MAX_TOKENS_PER_CHUNK=500
TEMPERATURE=0.7
CHUNK_STRATEGY=semantic
MAX_CHUNK_SIZE=2000
OVERLAP_SIZE=200
```

### 3. 测试API配置

运行测试脚本验证配置：

```bash
python test_qwen_api.py
```

## API调用示例

```python
import os
from openai import OpenAI

client = OpenAI(
    api_key=os.getenv("LLM_API_KEY"),
    base_url="https://dashscope.aliyuncs.com/compatible-mode/v1"
)

completion = client.chat.completions.create(
    model="qwen-turbo",
    messages=[
        {'role': 'system', 'content': '你是一个有用的AI助手。'},
        {'role': 'user', 'content': '请分析以下内容...'}
    ],
    max_tokens=500,
    temperature=0.7
)

print(completion.choices[0].message.content)
```

## 模型参数

- **模型名称**: `qwen-turbo`
- **上下文长度**: 1,000,000 tokens (1M)
- **最大Token**: 可配置（默认500）
- **温度**: 可配置（默认0.7）
- **API端点**: `https://dashscope.aliyuncs.com/compatible-mode/v1`
- **智能分片**: 根据上下文长度自动计算最优分片大小

## 注意事项

1. **API密钥安全**: 请妥善保管API密钥，不要提交到版本控制系统
2. **费用控制**: 百炼API按调用次数和Token数量计费，请注意使用量
3. **网络连接**: 确保服务器能够访问阿里云API端点
4. **兼容性**: 百炼API与OpenAI API兼容，但可能存在细微差异

## 故障排除

### 常见错误

1. **API密钥错误**
   ```
   Error: Invalid API key
   ```
   解决：检查API密钥是否正确设置

2. **网络连接问题**
   ```
   Error: Connection timeout
   ```
   解决：检查网络连接和防火墙设置

3. **模型不存在**
   ```
   Error: Model not found
   ```
   解决：确认模型名称正确（qwen-turbo）

### 调试步骤

1. 运行测试脚本：`python test_qwen_api.py`
2. 检查环境变量：`echo $LLM_API_KEY`
3. 查看日志文件：`logs/app.log`
4. 检查网络连接：`ping dashscope.aliyuncs.com`

## 更多信息

- [百炼API官方文档](https://help.aliyun.com/zh/model-studio/)
- [模型列表](https://help.aliyun.com/zh/model-studio/getting-started/models)
- [API参考](https://help.aliyun.com/zh/model-studio/reference/api-overview) 