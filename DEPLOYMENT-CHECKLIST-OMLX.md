# oMLX 完整部署检查清单

> M4 Mac mini AI 服务器部署验收清单

**部署日期**: 2026-03-27
**验收标准**: 所有 ✅ 项目必须完成，⭐ 为关键项

---

## 📦 阶段1：服务器端部署（M4 Mac mini）

### 1.1 系统准备 ⭐

- [ ] 确认系统版本：macOS 15.0+ (Sequoia)
- [ ] 确认芯片：Apple Silicon (M4)
- [ ] 确认内存：32GB 统一内存
- [ ] 确认磁盘空间：至少 50GB 可用
- [ ] 确认网络：连接到局域网

**验证命令**：
```bash
sw_vers
sysctl -n machdep.cpu.brand_string
sysctl hw.memsize
df -h ~
ifconfig | grep "inet "
```

---

### 1.2 oMLX 安装 ⭐⭐⭐

- [ ] 安装 Homebrew（如未安装）
- [ ] 安装 oMLX：`brew install omlx`
- [ ] 验证安装：`which omlx`
- [ ] 检查版本：`omlx --version`
- [ ] 创建模型目录：`mkdir -p ~/models`

**验证标准**：
```bash
which omlx
# 预期输出：/opt/homebrew/bin/omlx

omlx --version
# 预期输出：omlx version 0.2.x
```

---

### 1.3 模型下载 ⭐⭐⭐

#### 对话模型

- [ ] Qwen3.5-0.8B 已下载
- [ ] 文件大小：~1.71GB
- [ ] 包含文件：config.json, model.safetensors, tokenizer.json

**验证**：
```bash
ls -lh ~/models/Qwen3.5-0.8B/
du -sh ~/models/Qwen3.5-0.8B/
```

#### 代码模型

- [ ] OmniCoder-9B 已下载
- [ ] 文件大小：~18.40GB
- [ ] 包含文件：config.json, model.safetensors, tokenizer.json

**验证**：
```bash
ls -lh ~/models/OmniCoder-9B/
du -sh ~/models/OmniCoder-9B/
```

#### 视觉模型

- [ ] GLM-OCR 已下载
- [ ] 文件大小：~2.59GB
- [ ] 包含文件：config.json, model.safetensors, tokenizer.json

**验证**：
```bash
ls -lh ~/models/GLM-OCR/
du -sh ~/models/GLM-OCR/
```

#### 嵌入模型 ⭐

- [ ] nomic-embed-4bit 已下载
- [ ] 文件大小：~80MB
- [ ] 包含文件：config.json, model.safetensors, tokenizer.json

**验证**：
```bash
ls -lh ~/models/nomic-embed-4bit/
du -sh ~/models/nomic-embed-4bit/

# 使用 Python 下载（如未下载）
python3 << 'EOF'
from huggingface_hub import snapshot_download
snapshot_download(
    repo_id="mlx-community/nomicai-modernbert-embed-base-4bit",
    local_dir="~/models/nomic-embed-4bit"
)
EOF
```

---

### 1.4 服务启动 ⭐⭐⭐

- [ ] 启动服务：`omlx serve --model-dir ~/models --host 0.0.0.0 --port 8000 &`
- [ ] 或使用 Homebrew：`brew services start omlx`
- [ ] 验证进程运行：`pgrep -fl omlx`
- [ ] 验证端口监听：`lsof -nP -iTCP:8000 | grep LISTEN`
- [ ] 验证日志无错误：`tail -50 /tmp/omlx.log`

**验证标准**：
```bash
pgrep -fl omlx
# 预期输出：xxxxx /opt/homebrew/bin/omlx serve ...

lsof -nP -iTCP:8000 | grep LISTEN
# 预期输出：omlx xxxxx ... *:8000 (LISTEN)
```

---

### 1.5 API 测试 ⭐⭐⭐

#### 健康检查

- [ ] 健康检查通过：`curl http://localhost:8000/health`

**预期输出**：
```json
{"status": "ok"}
```

#### 模型列表 ⭐

- [ ] 获取模型列表：`curl http://localhost:8000/v1/models -H "Authorization: Bearer 2348"`
- [ ] 确认包含 4 个模型：
  - [ ] Qwen3.5-0.8B
  - [ ] OmniCoder-9B
  - [ ] GLM-OCR
  - [ ] nomic-embed-4bit

**预期输出包含**：
```json
{
  "data": [
    {"id": "Qwen3.5-0.8B", ...},
    {"id": "OmniCoder-9B", ...},
    {"id": "GLM-OCR", ...},
    {"id": "nomic-embed-4bit", ...}
  ]
}
```

#### 对话 API 测试 ⭐

- [ ] 对话测试通过：
```bash
curl http://localhost:8000/v1/chat/completions \
  -H "Authorization: Bearer 2348" \
  -H "Content-Type: application/json" \
  -d '{
    "model": "Qwen3.5-0.8B",
    "messages": [{"role": "user", "content": "你好，介绍一下你自己"}]
  }'
```

**预期**：返回有效的对话响应

#### 嵌入 API 测试 ⭐

- [ ] 嵌入测试通过：
```bash
curl http://localhost:8000/v1/embeddings \
  -H "Authorization: Bearer 2348" \
  -H "Content-Type: application/json" \
  -d '{
    "model": "nomic-embed-4bit",
    "input": "测试嵌入模型"
  }'
```

**预期**：返回 768 维向量

---

### 1.6 配置验证 ⭐

- [ ] 配置文件存在：`~/.omlx/settings.json`
- [ ] API Key 正确：`2348`
- [ ] 监听地址：`0.0.0.0`
- [ ] 端口：`8000`
- [ ] 模型目录：`~/models`
- [ ] 缓存启用：`true`

**验证命令**：
```bash
cat ~/.omlx/settings.json | grep -E "api_key|host|port|model_dir"
```

---

### 1.7 Web 界面测试

- [ ] 访问 Web 界面：http://localhost:8000/admin/chat
- [ ] 可以登录（使用 API Key: 2348）
- [ ] 可以查看模型列表
- [ ] 可以进行对话测试
- [ ] 可以查看服务状态

---

### 1.8 网络配置 ⭐⭐

- [ ] 获取 Mac mini 局域网 IP：`ipconfig getifaddr en0`
- [ ] 记录 IP 地址：`192.168.___.___ `（填写实际 IP）
- [ ] 防火墙允许端口 8000（如启用）
- [ ] 从其他设备可以访问（见阶段2）

**验证命令**：
```bash
# 获取 IP
ipconfig getifaddr en0

# 检查防火墙
sudo /usr/libexec/ApplicationFirewall/socketfilterfw --getglobalstate

# 如果防火墙开启，添加例外
sudo /usr/libexec/ApplicationFirewall/socketfilterfw --add /opt/homebrew/bin/omlx
```

---

## 🖥️ 阶段2：客户端配置（ThinkBook）

### 2.1 网络连通性测试 ⭐

- [ ] 能 ping 通 Mac mini：`ping 192.168.x.x`
- [ ] 端口 8000 可达：`Test-NetConnection -ComputerName 192.168.x.x -Port 8000`
- [ ] 预期：`TcpTestSucceeded : True`

---

### 2.2 curl 测试

- [ ] 测试健康检查：
```bash
curl http://192.168.x.x:8000/health
```

- [ ] 测试模型列表：
```bash
curl http://192.168.x.x:8000/v1/models \
  -H "Authorization: Bearer 2348"
```

- [ ] 测试对话 API：
```bash
curl http://192.168.x.x:8000/v1/chat/completions \
  -H "Authorization: Bearer 2348" \
  -H "Content-Type: application/json" \
  -d '{
    "model": "Qwen3.5-0.8B",
    "messages": [{"role": "user", "content": "你好"}]
  }'
```

- [ ] 测试嵌入 API：
```bash
curl http://192.168.x.x:8000/v1/embeddings \
  -H "Authorization: Bearer 2348" \
  -H "Content-Type: application/json" \
  -d '{
    "model": "nomic-embed-4bit",
    "input": "测试"
  }'
```

---

### 2.3 Claude Code 配置 ⭐

- [ ] 编辑配置文件：`.claude/settings.json`
- [ ] 添加 oMLX 配置：
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

- [ ] 重启 Claude Code
- [ ] 测试对话功能
- [ ] 测试代码生成功能

---

### 2.4 Python 客户端测试

- [ ] 创建测试脚本：`test-omlx.py`
- [ ] 测试对话 API
- [ ] 测试嵌入 API
- [ ] 测试批量请求
- [ ] 验证性能（延迟 < 500ms）

**测试脚本**：
```python
import requests

API_URL = "http://192.168.x.x:8000/v1"
API_KEY = "2348"

# 测试对话
response = requests.post(
    f"{API_URL}/chat/completions",
    headers={'Authorization': f'Bearer {API_KEY}'},
    json={
        'model': 'Qwen3.5-0.8B',
        'messages': [{'role': 'user', 'content': '你好'}]
    }
)
print("对话:", response.json()['choices'][0]['message']['content'])

# 测试嵌入
response = requests.post(
    f"{API_URL}/embeddings",
    headers={'Authorization': f'Bearer {API_KEY}'},
    json={
        'model': 'nomic-embed-4bit',
        'input': '测试'
    }
)
print("嵌入维度:", len(response.json()['data'][0]['embedding']))
```

---

## 🖥️ 阶段3：客户端配置（铭凡小主机 WSL2）

### 3.1 WSL2 网络测试 ⭐

- [ ] WSL2 已安装并运行
- [ ] 从 WSL2 可以 ping 通 Mac mini：`ping 192.168.x.x`
- [ ] 从 WSL2 可以访问 API：
```bash
curl http://192.168.x.x:8000/v1/models \
  -H "Authorization: Bearer 2348"
```

---

### 3.2 Windows 防火墙配置

- [ ] 允许 WSL2 访问局域网（如需要）：
```powershell
# 以管理员身份运行
New-NetFirewallRule -DisplayName "Allow WSL2 LAN Access" `
  -Direction Inbound `
  -Action Allow `
  -Protocol TCP `
  -LocalPort 8000
```

---

### 3.3 OpenClaw 配置 ⭐

- [ ] 编辑配置：`~/.openclaw/config.yaml`
- [ ] 添加 oMLX 配置：
```yaml
llm:
  provider: openai
  api_base: http://192.168.x.x:8000/v1
  api_key: "2348"
  model: Qwen3.5-0.8B
  code_model: OmniCoder-9B

embedding:
  provider: openai
  api_base: http://192.168.x.x:8000/v1
  api_key: "2348"
  model: nomic-embed-4bit
```

- [ ] 重启 OpenClaw
- [ ] 测试连接
- [ ] 测试代码生成

---

### 3.4 Node.js 客户端测试

- [ ] Node.js 24+ 已安装
- [ ] 创建测试脚本：`test-omlx.js`
- [ ] 测试对话 API
- [ ] 测试嵌入 API
- [ ] 验证性能

---

## 📊 阶段4：性能验证

### 4.1 延迟测试 ⭐

- [ ] 对话 API 延迟 < 200ms（首次）
- [ ] 对话 API 延迟 < 100ms（缓存后）
- [ ] 嵌入 API 延迟 < 100ms
- [ ] 批量嵌入（10条）< 200ms

**测试命令**：
```bash
# 测试延迟
time curl http://192.168.x.x:8000/v1/embeddings \
  -H "Authorization: Bearer 2348" \
  -d '{"model": "nomic-embed-4bit", "input": "测试"}'
```

---

### 4.2 并发测试

- [ ] 支持 2 个并发请求（不同模型）
- [ ] 支持 4 个并发请求（同一模型）
- [ ] 无错误或超时

---

### 4.3 内存监控 ⭐

- [ ] 空载内存：< 5GB
- [ ] 4 模型加载：~23GB
- [ ] 推理时内存峰值：< 28GB
- [ ] 无内存泄漏（长时间运行）

**监控命令**：
```bash
# 查看 oMLX 内存占用
ps aux | grep omlx | awk '{print $11, $6/1024 "MB"}'

# 或使用 Activity Monitor（GUI）
```

---

### 4.4 长时间稳定性测试

- [ ] 运行 24 小时无崩溃
- [ ] 处理 1000+ 请求无错误
- [ ] 内存占用稳定（无增长）
- [ ] 日志无异常错误

---

## 📝 阶段5：文档和备份

### 5.1 文档完整性 ⭐

- [ ] BASELINE.md 已更新（Mac mini 配置）
- [ ] BASELINE.md 已更新（模型列表）
- [ ] BASELINE.md 已更新（变更历史）
- [ ] README-OMLX.md 索引完整
- [ ] 所有配置文件已记录

---

### 5.2 配置备份

- [ ] 备份 oMLX 配置：`~/.omlx/settings.json`
- [ ] 备份模型列表：`ls -la ~/models/ > model-list.txt`
- [ ] 备份客户端配置（Claude Code、OpenClaw）
- [ ] 记录所有 IP 地址和端口

**备份命令**：
```bash
# 创建备份目录
mkdir -p ~/omlx-backup

# 备份配置
cp ~/.omlx/settings.json ~/omlx-backup/
ls -la ~/models/ > ~/omlx-backup/model-list.txt
date > ~/omlx-backup/backup-date.txt
```

---

### 5.3 Git 提交 ⭐

- [ ] 所有文档变更已提交
- [ ] 提交信息清晰
- [ ] 推送到远程仓库
- [ ] 备份到其他位置（可选）

---

## 🎯 验收标准总结

### 必须通过（⭐⭐⭐）

- [x] oMLX 服务运行中
- [x] 4 个模型已加载
- [x] 对话 API 正常工作
- [x] 嵌入 API 正常工作
- [ ] ThinkBook 可以访问（待测试）
- [ ] 铭凡小主机 WSL2 可以访问（待测试）

### 推荐完成（⭐⭐）

- [x] Web 界面可访问
- [ ] Claude Code 配置完成
- [ ] OpenClaw 配置完成
- [ ] 性能测试通过
- [x] 文档完整

### 可选项（⭐）

- [ ] 长时间稳定性测试
- [ ] 监控和日志系统
- [ ] 自动启动配置
- [ ] 备份和恢复流程

---

## 📋 快速检查命令集合

```bash
# === Mac mini 服务器端 ===

# 1. 检查服务状态
pgrep -fl omlx
lsof -nP -iTCP:8000 | grep LISTEN

# 2. 检查模型
ls -la ~/models/
du -sh ~/models/*

# 3. 测试 API
curl http://localhost:8000/health
curl http://localhost:8000/v1/models -H "Authorization: Bearer 2348"

# 4. 检查配置
cat ~/.omlx/settings.json | grep -E "api_key|host|port"

# 5. 查看日志
tail -50 /tmp/omlx.log

# 6. 获取 IP
ipconfig getifaddr en0

# === 客户端（ThinkBook/铭凡） ===

# 1. 测试网络
ping 192.168.x.x
curl http://192.168.x.x:8000/health

# 2. 测试 API
curl http://192.168.x.x:8000/v1/models \
  -H "Authorization: Bearer 2348"

# 3. 测试对话
curl http://192.168.x.x:8000/v1/chat/completions \
  -H "Authorization: Bearer 2348" \
  -d '{"model": "Qwen3.5-0.8B", "messages": [{"role": "user", "content": "你好"}]}'

# 4. 测试嵌入
curl http://192.168.x.x:8000/v1/embeddings \
  -H "Authorization: Bearer 2348" \
  -d '{"model": "nomic-embed-4bit", "input": "测试"}'
```

---

## 🔴 关键问题清单

如果以下任一项失败，必须解决后才能继续：

1. [ ] oMLX 服务无法启动 → 检查日志，重新安装
2. [ ] 模型未加载 → 检查模型文件，重启服务
3. [ ] API 返回 401 错误 → 检查 API Key 配置
4. [ ] 客户端无法访问 → 检查网络、防火墙、IP 地址
5. [ ] 性能严重下降 → 检查内存、磁盘、网络

---

## 📞 获取帮助

遇到问题时：

1. **查看日志**：`tail -100 /tmp/omlx.log`
2. **运行诊断**：`scripts/omlx-diagnose.sh`
3. **查阅文档**：`docs/README-OMLX.md`
4. **故障排除**：`docs/omlx-quick-reference.md`

---

**创建日期**: 2026-03-27
**最后更新**: 2026-03-27
**状态**: ✅ 阶段1（服务器端）已完成，待验证阶段2-3（客户端）
**验收人**: ___________
**验收日期**: ___________
