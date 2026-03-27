# oMLX 客户端配置指南

> 用于配置 ThinkBook 和铭凡小主机连接 M4 Mac mini 上的 oMLX AI 服务

---

## 📋 配置概览

### 服务器信息（M4 Mac mini）

| 配置项 | 值 |
|--------|-----|
| **服务地址** | http://192.168.x.x:8000 |
| **API 端点** | /v1/chat/completions, /v1/embeddings |
| **API 格式** | OpenAI 兼容 |
| **认证方式** | Bearer Token |
| **API Key** | `2348` |
| **Web 界面** | http://192.168.x.x:8000/admin/chat |

### 可用模型

| 模型 ID | 用途 | 大小 |
|---------|------|------|
| `Qwen3.5-0.8B` | 通用对话 | 1.71GB |
| `OmniCoder-9B` | 代码生成 | 18.40GB |
| `GLM-OCR` | 视觉/OCR | 2.59GB |
| `nomic-embed-4bit` | 文本嵌入 | 0.08GB |

---

## 🖥️ ThinkBook 配置

### 1. Claude Code 配置

**文件位置**: `.claude/settings.json`

```json
{
  "llm": {
    "provider": "openai",
    "baseURL": "http://192.168.x.x:8000/v1",
    "apiKey": "2348",
    "models": {
      "opus": "OmniCoder-9B",
      "sonnet": "Qwen3.5-0.8B",
      "haiku": "Qwen3.5-0.8B"
    }
  },
  "embedding": {
    "provider": "openai",
    "baseURL": "http://192.168.x.x:8000/v1",
    "apiKey": "2348",
    "model": "nomic-embed-4bit"
  }
}
```

**说明**：
- `baseURL`: Mac mini 局域网 IP + 端口
- `apiKey`: 使用 oMLX 的 API Key
- `models`: 映射 Claude 模型到 oMLX 模型
- `embedding`: 配置嵌入模型（用于 RAG、代码搜索）

---

### 2. Python 客户端配置

```python
# config.py
import os

# oMLX 服务器配置
OMLX_BASE_URL = "http://192.168.x.x:8000/v1"
OMLX_API_KEY = "2348"

# 模型配置
MODELS = {
    "chat": "Qwen3.5-0.8B",      # 通用对话
    "code": "OmniCoder-9B",       # 代码生成
    "vision": "GLM-OCR",          # 视觉识别
    "embedding": "nomic-embed-4bit"  # 文本嵌入
}

# 使用示例
import requests

def chat(messages, model="chat"):
    """对话 API"""
    response = requests.post(
        f"{OMLX_BASE_URL}/chat/completions",
        headers={'Authorization': f'Bearer {OMLX_API_KEY}'},
        json={
            'model': MODELS[model],
            'messages': messages
        }
    )
    return response.json()['choices'][0]['message']['content']

def get_embedding(text):
    """嵌入 API"""
    response = requests.post(
        f"{OMLX_BASE_URL}/embeddings",
        headers={'Authorization': f'Bearer {OMLX_API_KEY}'},
        json={
            'model': MODELS['embedding'],
            'input': text
        }
    )
    return response.json()['data'][0]['embedding']

# 测试
if __name__ == "__main__":
    # 测试对话
    reply = chat([{"role": "user", "content": "你好"}])
    print(f"对话: {reply}")

    # 测试嵌入
    embedding = get_embedding("测试文本")
    print(f"嵌入维度: {len(embedding)}")
```

---

### 3. curl 命令测试

```bash
# 设置变量
OMLX_URL="http://192.168.x.x:8000/v1"
API_KEY="2348"

# 测试对话
curl ${OMLX_URL}/chat/completions \
  -H "Authorization: Bearer ${API_KEY}" \
  -H "Content-Type: application/json" \
  -d '{
    "model": "Qwen3.5-0.8B",
    "messages": [
      {"role": "user", "content": "你好，介绍一下你自己"}
    ]
  }'

# 测试嵌入
curl ${OMLX_URL}/embeddings \
  -H "Authorization: Bearer ${API_KEY}" \
  -H "Content-Type: application/json" \
  -d '{
    "model": "nomic-embed-4bit",
    "input": "测试嵌入功能"
  }'
```

---

## 🖥️ 铭凡小主机（WSL2）配置

### 1. OpenClaw 配置

**文件位置**: `~/.openclaw/config.yaml`

```yaml
# OpenClaw 配置
llm:
  provider: openai
  api_base: http://192.168.x.x:8000/v1
  api_key: "2348"
  model: Qwen3.5-0.8B

  # 代码生成专用
  code_model: OmniCoder-9B

  # 视觉识别
  vision_model: GLM-OCR

# 嵌入模型（RAG）
embedding:
  provider: openai
  api_base: http://192.168.x.x:8000/v1
  api_key: "2348"
  model: nomic-embed-4bit

# 其他配置
server:
  port: 18789
  host: 0.0.0.0
```

**说明**：
- OpenClaw 支持 OpenAI 格式 API
- `api_base`: 指向 oMLX 服务器
- `code_model`: 专门用于代码生成的模型
- `embedding`: 用于代码搜索、文档检索

---

### 2. WSL2 网络配置

```bash
# 在 WSL2 中测试连接
curl http://192.168.x.x:8000/v1/models \
  -H "Authorization: Bearer 2348"

# 如果无法访问，检查防火墙
# Windows 防火墙需要允许端口 8000
```

**Windows 防火墙配置**（在铭凡小主机上）：

```powershell
# 以管理员身份运行 PowerShell

# 允许 WSL2 访问局域网（入站规则）
New-NetFirewallRule -DisplayName "Allow WSL2 LAN Access" `
  -Direction Inbound `
  -Action Allow `
  -Protocol TCP `
  -LocalPort 8000

# 如果还需要出站规则
New-NetFirewallRule -DisplayName "Allow WSL2 LAN Access Out" `
  -Direction Outbound `
  -Action Allow `
  -Protocol TCP `
  -RemotePort 8000
```

---

### 3. Node.js 客户端配置

```javascript
// omlx-client.js
const axios = require('axios');

const OMLX_BASE_URL = 'http://192.168.x.x:8000/v1';
const API_KEY = '2348';

// 对话 API
async function chat(messages, model = 'Qwen3.5-0.8B') {
  const response = await axios.post(
    `${OMLX_BASE_URL}/chat/completions`,
    {
      model: model,
      messages: messages
    },
    {
      headers: {
        'Authorization': `Bearer ${API_KEY}`,
        'Content-Type': 'application/json'
      }
    }
  );
  return response.data.choices[0].message.content;
}

// 嵌入 API
async function getEmbedding(text) {
  const response = await axios.post(
    `${OMLX_BASE_URL}/embeddings`,
    {
      model: 'nomic-embed-4bit',
      input: text
    },
    {
      headers: {
        'Authorization': `Bearer ${API_KEY}`,
        'Content-Type': 'application/json'
      }
    }
  );
  return response.data.data[0].embedding;
}

// 测试
async function test() {
  try {
    // 测试对话
    const reply = await chat([
      { role: 'user', content: '你好' }
    ]);
    console.log('对话:', reply);

    // 测试嵌入
    const embedding = await getEmbedding('测试');
    console.log('嵌入维度:', embedding.length);
  } catch (error) {
    console.error('错误:', error.message);
  }
}

test();
```

---

## 🌐 网络配置

### Mac mini 网络检查

```bash
# 查看 Mac mini 局域网 IP
ifconfig en0 | grep "inet " | awk '{print $2}'

# 或者
ipconfig getifaddr en0

# 确认 oMLX 监听状态
lsof -nP -iTCP:8000 | grep LISTEN
```

**预期输出**：
```
omlx    xxxxx user   *:8000 (LISTEN)
```

说明 oMLX 正在监听所有接口（`0.0.0.0:8000`）。

---

### 客户端网络测试

#### 在 ThinkBook 上

```powershell
# 测试网络连通性
Test-NetConnection -ComputerName 192.168.x.x -Port 8000

# 预期输出：
# TcpTestSucceeded : True
```

```bash
# 测试 API
curl http://192.168.x.x:8000/v1/models \
  -H "Authorization: Bearer 2348"
```

#### 在铭凡小主机（WSL2）上

```bash
# 在 WSL2 中测试
curl http://192.168.x.x:8000/v1/models \
  -H "Authorization: Bearer 2348"
```

---

## 🔧 故障排除

### 问题1：无法连接到服务器

**症状**：`Connection refused` 或 `Connection timeout`

**排查步骤**：

1. **检查 Mac mini IP 地址**
   ```bash
   # 在 Mac mini 上
   ipconfig getifaddr en0
   ```

2. **检查 oMLX 服务状态**
   ```bash
   # 在 Mac mini 上
   pgrep -fl omlx
   ```

3. **检查防火墙**
   ```bash
   # 在 Mac mini 上检查防火墙
   sudo /usr/libexec/ApplicationFirewall/socketfilterfw --getglobalstate

   # 如果开启，添加 oMLX 例外
   sudo /usr/libexec/ApplicationFirewall/socketfilterfw --add /opt/homebrew/bin/omlx
   ```

4. **测试端口可达性**
   ```bash
   # 从客户端测试
   nc -zv 192.168.x.x 8000
   ```

---

### 问题2：API 返回 401 认证错误

**症状**：`{"error": {"message": "API key required"}}`

**解决**：

1. **检查 API Key**
   ```bash
   # 在 Mac mini 上
   cat ~/.omlx/settings.json | grep api_key
   ```

2. **在请求中添加正确的 Header**
   ```bash
   # 正确格式
   -H "Authorization: Bearer 2348"

   # ❌ 错误格式
   -H "Authorization: 2348"
   -H "api-key: 2348"
   ```

---

### 问题3：模型不存在

**症状**：`{"error": {"message": "Model not found"}}`

**解决**：

1. **检查可用模型**
   ```bash
   curl http://192.168.x.x:8000/v1/models \
     -H "Authorization: Bearer 2348"
   ```

2. **使用正确的模型 ID**
   ```bash
   # ✅ 正确（区分大小写）
   "model": "Qwen3.5-0.8B"
   "model": "nomic-embed-4bit"

   # ❌ 错误
   "model": "qwen3.5-0.8b"
   "model": "nomic-embed"
   ```

---

### 问题4：WSL2 无法访问 Mac mini

**症状**：WSL2 中 curl 超时

**解决**：

1. **检查 WSL2 网络模式**
   ```powershell
   # 在 Windows 上查看 .wslconfig
   type %USERPROFILE%\.wslconfig
   ```

2. **可能需要使用 Windows 主机 IP**
   ```bash
   # 在 WSL2 中获取 Windows 主机 IP
   cat /etc/resolv.conf | grep nameserver | awk '{print $2}'

   # 如果 Mac mini 和 Windows 在同一局域网，应该能直接访问
   ```

3. **检查 Windows 防火墙**（见上面的防火墙配置）

---

## 📊 性能优化建议

### 1. 批量请求

```python
# ❌ 不推荐：逐个请求
for text in texts:
    embedding = get_embedding(text)

# ✅ 推荐：批量请求（5-10x 更快）
embeddings = get_embeddings(texts)
```

### 2. 连接池

```python
# 使用 requests Session 复用连接
import requests

session = requests.Session()
session.headers.update({'Authorization': f'Bearer {API_KEY}'})

def chat_with_session(messages):
    return session.post(
        f"{OMLX_BASE_URL}/chat/completions",
        json={'model': 'Qwen3.5-0.8B', 'messages': messages}
    ).json()
```

### 3. 超时设置

```python
# 设置合理的超时
response = requests.post(
    url,
    json=data,
    timeout=(3.0, 30.0)  # (连接超时, 读取超时)
)
```

---

## 📝 配置检查清单

### Mac mini（服务器端）

- [ ] oMLX 服务运行中（`pgrep -fl omlx`）
- [ ] 监听 0.0.0.0:8000（`lsof -nP -iTCP:8000`）
- [ ] 防火墙允许端口 8000
- [ ] API Key 已设置（`~/.omlx/settings.json`）
- [ ] 4 个模型已加载
- [ ] 局域网 IP 已确认

### ThinkBook（客户端）

- [ ] 能 ping 通 Mac mini
- [ ] 端口 8000 可达（`Test-NetConnection`）
- [ ] Claude Code 配置已更新
- [ ] Python 客户端测试通过
- [ ] curl 测试成功

### 铭凡小主机（客户端）

- [ ] WSL2 已安装
- [ ] 能访问局域网（从 WSL2 ping Mac mini）
- [ ] Windows 防火墙已配置
- [ ] OpenClaw 配置已更新
- [ ] Node.js 客户端测试通过

---

## 🔗 相关文档

- [BASELINE.md](../BASELINE.md) - 系统基线
- [omlx-embedding-quickstart.md](./omlx-embedding-quickstart.md) - 嵌入模型部署
- [omlx-quick-reference.md](./omlx-quick-reference.md) - oMLX 参考
- [openclaw-installation-plan.md](../openclaw-installation-plan.md) - OpenClaw 部署

---

**更新日期**: 2026-03-27
**状态**: ✅ 验证通过（MacBook Pro 测试）
**待验证**: ThinkBook + 铭凡小主机实际部署
