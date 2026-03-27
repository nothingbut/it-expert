# oMLX 本地模型使用指南

## 📋 部署信息

**部署日期**: 2026-03-26
**设备**: MacBook Pro M3 Pro (36GB内存)
**oMLX版本**: v0.2.21
**服务地址**: http://localhost:8000

---

## 🎯 已部署模型

| 模型 | 用途 | 大小 | 模型ID | 状态 |
|------|------|------|--------|------|
| **GLM-4V-9B** | OCR识别 | ~19GB | `glm-4v-9b` | ⏳ 下载中 |
| **OmniCoder-9B** | 代码辅助 | ~18GB | `omnicoder-9b` | ⏳ 下载中 |
| **Qwen2.5-0.5B** | 模型微调 | ~1GB | `qwen2.5-0.5b-instruct` | ⏳ 下载中 |

---

## 🚀 快速使用

### 1. 检查服务状态

```bash
# 检查oMLX进程
ps aux | grep oMLX

# 检查API服务
curl http://localhost:8000/v1/models

# 打开管理界面
open http://localhost:8000/admin
```

### 2. 查看已加载模型

```bash
curl http://localhost:8000/v1/models | python3 -m json.tool
```

---

## 💻 使用场景

### 场景 1: OCR图像识别（GLM-4V-9B）

```python
from openai import OpenAI
import base64

client = OpenAI(
    base_url="http://localhost:8000/v1",
    api_key="2348"  # oMLX设置中的api_key
)

# 读取图片
with open("screenshot.png", "rb") as f:
    image_data = base64.b64encode(f.read()).decode()

# OCR识别
response = client.chat.completions.create(
    model="glm-4v-9b",
    messages=[{
        "role": "user",
        "content": [
            {"type": "text", "text": "识别图片中的所有文字"},
            {
                "type": "image_url",
                "image_url": {
                    "url": f"data:image/png;base64,{image_data}"
                }
            }
        ]
    }]
)

print(response.choices[0].message.content)
```

### 场景 2: 代码辅助开发（OmniCoder-9B）

```python
from openai import OpenAI

client = OpenAI(
    base_url="http://localhost:8000/v1",
    api_key="2348"
)

# 代码生成
response = client.chat.completions.create(
    model="omnicoder-9b",
    messages=[
        {"role": "user", "content": "用Python写一个快速排序算法"}
    ],
    temperature=0.2,  # 代码生成建议低温度
    max_tokens=2000
)

print(response.choices[0].message.content)
```

### 场景 3: Claude Code 集成

#### 方式 1: 环境变量（推荐）

创建临时配置脚本 `~/.omlx-env.sh`:

```bash
#!/bin/bash
# oMLX 本地模型环境变量

export OPENAI_API_BASE="http://localhost:8000/v1"
export OPENAI_API_KEY="2348"
export OPENAI_MODEL="omnicoder-9b"

echo "✅ oMLX 环境变量已设置"
echo "   API Base: $OPENAI_API_BASE"
echo "   Model: $OPENAI_MODEL"
```

使用方式：
```bash
# 每次使用前执行
source ~/.omlx-env.sh

# 然后正常使用 Claude Code
claude-code "优化这个函数"
```

#### 方式 2: 直接在代码中配置

```python
# ~/my_project/local_assistant.py
from openai import OpenAI

# 使用本地oMLX
local_client = OpenAI(
    base_url="http://localhost:8000/v1",
    api_key="2348"
)

def code_assistant(prompt, model="omnicoder-9b"):
    response = local_client.chat.completions.create(
        model=model,
        messages=[{"role": "user", "content": prompt}]
    )
    return response.choices[0].message.content

# 使用示例
if __name__ == "__main__":
    result = code_assistant("重构这个函数使用列表推导式")
    print(result)
```

### 场景 4: 模型微调（Qwen2.5-0.5B）

```bash
# 使用MLX进行微调
cd /Users/shichang/models

# 准备训练数据（JSON Lines格式）
cat > train_data.jsonl << 'EOF'
{"messages": [{"role": "user", "content": "你好"}, {"role": "assistant", "content": "你好！我是AI助手"}]}
{"messages": [{"role": "user", "content": "介绍一下Python"}, {"role": "assistant", "content": "Python是一门高级编程语言..."}]}
EOF

# 微调命令（使用mlx-lm）
python -m mlx_lm.lora \
  --model Qwen2.5-0.5B-Instruct \
  --train \
  --data train_data.jsonl \
  --iters 1000 \
  --save-every 100 \
  --adapter-path ./adapters
```

---

## 🔧 配置管理

### 查看当前配置

```bash
cat ~/.omlx/settings.json | python3 -m json.tool
```

### 关键配置项

```json
{
  "server": {
    "port": 8000,
    "host": "127.0.0.1"
  },
  "model": {
    "model_dir": "/Users/shichang/models",
    "max_model_memory": "auto"
  },
  "cache": {
    "enabled": true,
    "ssd_cache_max_size": "auto"
  },
  "auth": {
    "api_key": "2348"
  }
}
```

### 修改端口（如果需要）

```bash
# 编辑配置
nano ~/.omlx/settings.json

# 修改端口：
"server": {
  "port": 8080  # 改为8080
}

# 重启oMLX
pkill -9 oMLX
open -a oMLX
```

---

## 📊 性能监控

### 查看模型加载状态

```bash
curl http://localhost:8000/v1/models | python3 -m json.tool
```

### 查看日志

```bash
# 实时日志
tail -f ~/.omlx/logs/server.log

# 错误日志
grep ERROR ~/.omlx/logs/server.log
```

### 内存使用

```bash
# 查看oMLX进程内存
ps aux | grep oMLX | awk '{print $4 "%", $11}'

# 查看Metal GPU内存
# 通过 Activity Monitor.app → Window → GPU History
```

---

## 🛠️ 故障排除

### 问题 1: 端口被占用

```bash
# 查看8000端口占用
lsof -i :8000

# 解决：杀死占用进程或修改oMLX配置端口
```

### 问题 2: 模型未加载

```bash
# 检查模型目录
ls -lh /Users/shichang/models/

# 检查日志
tail -50 ~/.omlx/logs/server.log | grep -i error

# 手动加载模型（通过Web UI）
open http://localhost:8000/admin
```

### 问题 3: 内存不足

```bash
# 查看可用内存
sysctl hw.memsize
vm_stat

# 解决：
# 1. 卸载未使用的模型
# 2. 减少 max_model_memory
# 3. 禁用缓存
```

### 问题 4: 下载速度慢

```bash
# 使用HuggingFace镜像
export HF_ENDPOINT=https://hf-mirror.com

# 重新下载
cd /Users/shichang/models
huggingface-cli download --resume-download <model-id>
```

---

## 📚 API参考

### 端点列表

| 端点 | 方法 | 说明 |
|------|------|------|
| `/v1/models` | GET | 列出所有可用模型 |
| `/v1/chat/completions` | POST | 对话补全（OpenAI格式） |
| `/v1/completions` | POST | 文本补全 |
| `/v1/embeddings` | POST | 文本嵌入 |
| `/admin` | GET | Web管理界面 |

### 请求示例

```bash
# 对话补全
curl http://localhost:8000/v1/chat/completions \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer 2348" \
  -d '{
    "model": "omnicoder-9b",
    "messages": [
      {"role": "user", "content": "Hello!"}
    ],
    "temperature": 0.7,
    "max_tokens": 1000
  }'
```

---

## 🔄 日常维护

### 启动oMLX

```bash
# 方式1: 应用程序
open -a oMLX

# 方式2: 已配置自动启动
# 每次开机自动运行
```

### 停止oMLX

```bash
pkill -9 oMLX
```

### 更新oMLX

```bash
# 查看当前版本
open http://localhost:8000/admin

# 下载最新版本
curl -L https://github.com/jundot/omlx/releases/latest/download/oMLX-*.dmg \
  -o ~/Downloads/oMLX-latest.dmg

# 覆盖安装
```

### 清理缓存

```bash
# 清理SSD缓存
rm -rf ~/.omlx/cache/*

# 清理日志
rm -rf ~/.omlx/logs/*.log
```

---

## 🌐 局域网访问

如果需要从其他设备访问（如ThinkBook+、铭凡UM773）：

### 1. 修改oMLX配置

```bash
# 编辑配置
nano ~/.omlx/settings.json

# 修改host：
"server": {
  "host": "0.0.0.0",  # 监听所有网络接口
  "port": 8000
}

# 重启oMLX
pkill -9 oMLX && open -a oMLX
```

### 2. 配置防火墙

```bash
# 允许8000端口
sudo /usr/libexec/ApplicationFirewall/socketfilterfw --add /Applications/oMLX.app
sudo /usr/libexec/ApplicationFirewall/socketfilterfw --unblockapp /Applications/oMLX.app
```

### 3. 获取局域网IP

```bash
# 获取IP地址
ipconfig getifaddr en0  # 以太网
# 或
ipconfig getifaddr en1  # Wi-Fi

# 示例: 192.168.1.160
```

### 4. 从其他设备访问

```bash
# 在其他设备上测试
curl http://192.168.1.160:8000/v1/models
```

---

## 📝 备注

- **API Key**: `2348` （在 `~/.omlx/settings.json` 中配置）
- **模型目录**: `/Users/shichang/models`
- **配置目录**: `~/.omlx/`
- **日志目录**: `~/.omlx/logs/`
- **缓存目录**: `~/.omlx/cache/`

---

## 🔗 相关文档

- [oMLX GitHub](https://github.com/jundot/omlx)
- [快速部署指南](./QUICKSTART-OMLX.md)
- [完整部署方案](./mac-omlx-deployment-plan.md)
- [MLX vs oMLX 对比](./docs/mlx-vs-omlx-comparison.md)

---

**创建日期**: 2026-03-26
**最后更新**: 2026-03-26
**设备**: MacBook Pro M3 Pro (36GB)
