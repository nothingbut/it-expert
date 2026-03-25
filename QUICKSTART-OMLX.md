# M4 Mac mini oMLX 快速部署指南

> **用途**: 在 M4 Mac mini 上快速部署 oMLX AI 服务器
> **预计时间**: 15-30 分钟（不含模型下载）
> **目标**: 为局域网内所有设备提供大模型 API 服务

---

## 📋 部署前检查清单

### 系统要求
```bash
# 1. 检查 macOS 版本（需要 15.0+）
sw_vers
# 应显示: ProductVersion: 15.x.x

# 2. 检查内存（建议 32GB+）
sysctl -n hw.memsize | awk '{print $1/1024/1024/1024 " GB"}'
# 应显示: 32 GB 或更高

# 3. 检查磁盘空间（需要 100GB+）
df -h | grep -E "/$"
# 确保 Available 有 100GB+

# 4. 确认 Apple Silicon
uname -m
# 应显示: arm64

# ✅ 全部通过后继续
```

---

## 🚀 快速部署（5 步完成）

### 第 1 步: 下载并安装 oMLX（2 分钟）

```bash
# 下载最新版 oMLX
curl -L https://github.com/jundot/omlx/releases/latest/download/oMLX.dmg \
  -o ~/Downloads/oMLX.dmg

# 打开 DMG
open ~/Downloads/oMLX.dmg

# 拖拽 oMLX 到 Applications 文件夹
# （在打开的窗口中手动操作）

# 启动 oMLX
open -a oMLX

# 验证服务是否启动
sleep 5
curl http://localhost:8080/v1/models
# 如果返回 JSON，说明启动成功 ✅
```

---

### 第 2 步: 下载推荐模型（5 分钟配置）

```bash
# 打开 Web 管理界面
open http://localhost:8080/admin
```

**在 Web UI 中下载以下模型**：

1. **Qwen/Qwen2.5-9B-Instruct** (18GB)
   - 用途: 通用对话
   - 优先级: ⭐⭐⭐⭐⭐

2. **Tesslate/OmniCoder-9B** (18GB)
   - 用途: 代码生成
   - 优先级: ⭐⭐⭐⭐⭐

3. **THUDM/glm-4v-9b** (19GB)
   - 用途: 视觉/OCR
   - 优先级: ⭐⭐⭐⭐

**下载步骤**：
1. 点击 "Models" 标签
2. 点击 "Download Model" 按钮
3. 输入模型 ID（例如：Qwen/Qwen2.5-9B-Instruct）
4. 点击 "Download & Load"
5. 重复上述步骤下载其他模型

**⚠️ 模型下载需要 30-60 分钟**，可以在后台下载，继续下一步配置。

---

### 第 3 步: 网络配置（3 分钟）

```bash
# 1. 获取 Mac mini IP 地址
IP=$(ipconfig getifaddr en0 || ipconfig getifaddr en1)
echo "Mac mini IP 地址: $IP"
# 记录这个 IP，后续客户端配置需要使用

# 2. 配置防火墙允许局域网访问
# 打开系统设置
open "x-apple.systempreferences:com.apple.preference.security?Firewall"

# 手动操作：
# - 确保 oMLX 在允许列表中
# - 或者直接关闭防火墙（仅限受信任的局域网）

# 3. 测试本地访问
curl http://localhost:8080/v1/models

# 4. 测试局域网访问（从其他设备执行）
# curl http://$IP:8080/v1/models
```

---

### 第 4 步: 配置性能优化（3 分钟）

```bash
# 打开 Web UI 设置页面
open http://localhost:8080/admin#settings
```

**在 Web UI 中配置以下参数**：

#### 模型管理
```
✓ Enable LRU Cache: 开启
✓ Max Models in Memory: 2
✓ Model TTL: 30 分钟
✓ Auto-unload on Idle: 开启
```

#### 缓存设置
```
Hot Tier (RAM): 8 GB
Cold Tier (SSD): 50 GB
Cache Eviction Policy: LRU
✓ Prefix Sharing: 开启
```

#### 性能设置
```
Max Batch Size: 8
Max Wait Time: 50 ms
✓ Continuous Batching: 开启
```

点击 "Save Settings" 保存配置。

---

### 第 5 步: 配置自动启动（2 分钟）

```bash
# 将 oMLX 添加到登录项
osascript -e 'tell application "System Events" to make login item at end with properties {path:"/Applications/oMLX.app", hidden:false}'

# 验证是否添加成功
osascript -e 'tell application "System Events" to get the name of every login item'
# 应该看到 "oMLX" 在列表中

# ✅ 现在每次开机自动启动 oMLX
```

---

## 🖥️ 客户端配置

### 配置 1: 联想 ThinkBook+ (Claude Code)

```powershell
# 在 Windows 上执行
notepad %USERPROFILE%\.claude\settings.json
```

**添加以下内容**（替换 `192.168.x.x` 为实际 IP）：

```json
{
  "apiBaseUrl": "http://192.168.x.x:8080/v1",
  "apiKey": "dummy",
  "model": "qwen2.5-9b",

  "providers": {
    "omlx-qwen": {
      "baseUrl": "http://192.168.x.x:8080/v1",
      "apiKey": "dummy",
      "models": {
        "qwen": "qwen2.5-9b"
      }
    },
    "omlx-coder": {
      "baseUrl": "http://192.168.x.x:8080/v1",
      "apiKey": "dummy",
      "models": {
        "coder": "omnicoder-9b"
      }
    }
  }
}
```

**验证连接**：
```powershell
# 使用 Python 测试
python -c "from openai import OpenAI; client = OpenAI(base_url='http://192.168.x.x:8080/v1', api_key='dummy'); response = client.chat.completions.create(model='qwen2.5-9b', messages=[{'role': 'user', 'content': '你好'}]); print(response.choices[0].message.content)"
```

---

### 配置 2: 铭凡UM773 (OpenClaw WSL2)

```bash
# 在 WSL2 Ubuntu 中执行
nano ~/.openclaw/config.json
```

**添加以下内容**（替换 `192.168.x.x` 为实际 IP）：

```json
{
  "providers": {
    "omlx-qwen": {
      "type": "openai-completions",
      "baseUrl": "http://192.168.x.x:8080/v1",
      "apiKey": "dummy",
      "models": {
        "qwen": {
          "id": "qwen2.5-9b",
          "name": "Qwen3.5-9B (本地)"
        }
      }
    },
    "omlx-coder": {
      "type": "openai-completions",
      "baseUrl": "http://192.168.x.x:8080/v1",
      "apiKey": "dummy",
      "models": {
        "coder": {
          "id": "omnicoder-9b",
          "name": "OmniCoder-9B (本地)"
        }
      }
    },
    "omlx-vlm": {
      "type": "openai-completions",
      "baseUrl": "http://192.168.x.x:8080/v1",
      "apiKey": "dummy",
      "models": {
        "ocr": {
          "id": "glm-4v-9b",
          "name": "GLM-4V-9B (视觉)"
        }
      }
    }
  },
  "defaultProvider": "omlx-qwen"
}
```

**验证连接**：
```bash
# 重启 OpenClaw
openclaw restart

# 测试连接
curl http://192.168.x.x:8080/v1/models

# 测试对话
openclaw "你好，介绍一下你自己"
```

---

## ✅ 验证部署成功

### 检查服务状态

```bash
# 方法 1: Web UI
open http://localhost:8080/admin

# 方法 2: 命令行（如果安装了 CLI）
omlx status

# 方法 3: API 检查
curl http://localhost:8080/v1/models | jq
```

### 运行性能测试

```bash
# 如果安装了 CLI
omlx benchmark --model qwen2.5-9b --requests 10

# 或通过 Web UI
# 访问 http://localhost:8080/admin#benchmark
# 点击 "Run Benchmark"
```

### 测试基本功能

```bash
# 测试通用对话
curl http://localhost:8080/v1/chat/completions \
  -H "Content-Type: application/json" \
  -d '{
    "model": "qwen2.5-9b",
    "messages": [{"role": "user", "content": "你好"}]
  }' | jq

# 测试代码生成
curl http://localhost:8080/v1/chat/completions \
  -H "Content-Type: application/json" \
  -d '{
    "model": "omnicoder-9b",
    "messages": [{"role": "user", "content": "写一个快速排序"}]
  }' | jq
```

---

## 📊 预期性能

### Mac Mini M4 (32GB)

| 模型 | 内存占用 | 推理速度 | 并发支持 | 缓存加速 |
|------|---------|---------|---------|---------|
| Qwen2.5-9B | 12GB | 60-93 t/s | 4-8 用户 | 40-100x |
| OmniCoder-9B | 12GB | 60-93 t/s | 4-8 用户 | 40-100x |
| GLM-4V-9B | 14GB | 40-60 t/s | 2-4 用户 | 30-80x |

### 实际场景

```
单次对话（冷启动）: 2000ms
单次对话（缓存命中）: 50ms（40x 加速）

并发 5 个请求:
- 传统顺序: 25s
- oMLX 批处理: 4s（6x 吞吐量）

长对话（10 轮）:
- 无缓存: 21s
- oMLX 缓存: 8s（2.6x 加速）
```

---

## 🔧 常见问题

### 1. 无法启动 oMLX

```bash
# 检查是否已经运行
ps aux | grep omlx

# 查看日志
tail -n 100 ~/.omlx/logs/server.log

# 常见原因：
# - 端口 8080 被占用
lsof -i :8080
# 解决：修改端口或停止占用进程
```

### 2. 模型下载失败

```bash
# 使用 HuggingFace 镜像
export HF_ENDPOINT=https://hf-mirror.com

# 或在 Web UI 中配置镜像
# Settings → Download → Mirror: hf-mirror.com
```

### 3. 局域网无法访问

```bash
# 检查防火墙
sudo /usr/libexec/ApplicationFirewall/socketfilterfw --getglobalstate

# 检查端口监听
lsof -i :8080 | grep LISTEN

# 从客户端检查连通性
ping <Mac-mini-IP>
telnet <Mac-mini-IP> 8080
```

### 4. 内存不足

```bash
# 查看内存使用
omlx status --memory

# 优化建议：
# 1. 减少同时加载的模型
#    Web UI → Settings → Max Models: 1
#
# 2. 减少缓存大小
#    Web UI → Settings → Hot Tier: 4GB
#
# 3. 启用自动卸载
#    Web UI → Settings → Auto-unload: 开启
```

---

## 📝 部署检查清单

部署完成后，确认以下项目：

- [ ] macOS 版本 15.0+
- [ ] 内存 32GB+
- [ ] 磁盘空间 100GB+
- [ ] oMLX 已安装并运行
- [ ] 至少 1 个模型已下载并加载
- [ ] 本地 API 访问正常 (http://localhost:8080)
- [ ] 局域网 API 访问正常 (http://192.168.x.x:8080)
- [ ] 联想 ThinkBook+ Claude Code 已配置
- [ ] 铭凡UM773 OpenClaw 已配置
- [ ] 性能优化已配置（LRU 缓存、批处理）
- [ ] 自动启动已配置

---

## 🔗 相关文档

### 详细部署指南
- **[Mac Mini oMLX 部署方案](./mac-omlx-deployment-plan.md)** - 完整部署流程
- **[MLX vs oMLX 对比](./docs/mlx-vs-omlx-comparison.md)** - 方案选型依据
- **[MLX 灵活性分析](./docs/mlx-flexibility-deep-dive.md)** - MLX 深度定制

### 项目管理
- **[BASELINE.md](./BASELINE.md)** - 环境基线文档
- **[进度跟踪](./BASELINE.md#项目进度)** - 部署进度更新

---

## 🎉 部署完成

恭喜！现在你的 M4 Mac mini 已经成为强大的局域网 AI 服务器：

```
✅ 服务地址: http://192.168.x.x:8080
✅ 管理界面: http://192.168.x.x:8080/admin
✅ API 兼容: OpenAI + Anthropic 格式
✅ 模型支持: 通用对话 + 代码生成 + 视觉/OCR
✅ 性能优化: 持久化缓存 + 连续批处理
✅ 客户端: Claude Code + OpenClaw + Python SDK
```

### 下一步

1. **更新 BASELINE.md 进度**
   - 标记已完成的任务为 ✅
   - 更新完成日期和备注

2. **测试实际使用**
   - 在 Claude Code 中测试对话
   - 在 OpenClaw 中测试代码生成

3. **监控性能**
   - 定期查看 Web UI 监控面板
   - 关注内存和缓存使用情况

---

**文档版本**: v1.0
**创建日期**: 2026-03-25
**预计部署时间**: 15-30 分钟（不含模型下载）
**支持**: 查看详细文档或提交 Issues
