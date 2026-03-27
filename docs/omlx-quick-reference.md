# oMLX 快速参考指南

## CLI 命令（仅2个）

```bash
omlx serve   # 启动 API 服务器（读取配置文件加载模型）
omlx launch  # 交互式启动单个模型
```

⚠️ **注意**：oMLX **没有** `model` 子命令！

---

## 正确的模型加载方式

### 方法1：配置文件（推荐）⭐

#### 步骤1：创建/编辑配置文件

```bash
# 配置文件位置（按优先级）
~/.omlx/config.yaml          # 推荐
~/.config/omlx/config.yaml
~/omlx/config.yaml
```

#### 步骤2：添加模型配置

```yaml
# config.yaml
models:
  # 对话模型
  - repo_id: "Qwen/Qwen3.5-9B-Instruct"
    model_type: "text-generation"
    adapter_path: null

  # 嵌入模型 ⭐ 新增
  - repo_id: "nomic-ai/nomic-embed-text-v2-moe"
    model_type: "embedding"
    adapter_path: null

server:
  host: "0.0.0.0"
  port: 8080

cache:
  enabled: true
  size_mb: 2048

quantization:
  enabled: true
  bits: 4  # 4-bit 量化（节省内存）
```

#### 步骤3：启动服务

```bash
# 使用默认配置
omlx serve

# 或指定配置文件
omlx serve --config ~/.omlx/config.yaml

# 后台运行
nohup omlx serve > omlx.log 2>&1 &
```

#### 步骤4：验证加载

```bash
# 列出所有模型
curl http://localhost:8080/v1/models

# 测试嵌入
curl http://localhost:8080/v1/embeddings \
  -H "Content-Type: application/json" \
  -d '{
    "model": "nomic-ai/nomic-embed-text-v2-moe",
    "input": "测试文本"
  }'
```

---

### 方法2：launch 命令（单模型）

```bash
# 启动单个模型（交互式）
omlx launch nomic-ai/nomic-embed-text-v2-moe

# 查看选项
omlx launch --help
```

⚠️ **限制**：
- 一次只能运行一个模型
- 不适合生产环境
- 适合快速测试

---

## 一键配置脚本

### 使用诊断脚本（推荐先运行）

```bash
# 1. 运行诊断，找到配置文件位置
chmod +x scripts/omlx-diagnose.sh
./scripts/omlx-diagnose.sh

# 输出会显示：
# - oMLX 安装状态
# - 配置文件位置
# - 当前运行状态
# - 已加载的模型
```

### 使用自动配置脚本

```bash
# 2. 运行配置脚本（自动添加嵌入模型）
chmod +x scripts/omlx-add-embedding-model.sh
./scripts/omlx-add-embedding-model.sh

# 脚本会：
# ✅ 查找或创建配置文件
# ✅ 备份原配置
# ✅ 添加嵌入模型配置
# ✅ 显示重启说明
```

---

## 完整工作流程

### 首次部署

```bash
# 步骤1：诊断环境
./scripts/omlx-diagnose.sh

# 步骤2：添加嵌入模型配置
./scripts/omlx-add-embedding-model.sh

# 步骤3：停止旧服务（如果运行中）
pkill -f omlx

# 步骤4：启动服务
omlx serve

# 步骤5：验证
curl http://localhost:8080/v1/models

# 步骤6：测试
python3 scripts/omlx-embedding-client.py
```

---

## 常见错误和解决方案

### ❌ 错误1：`invalid choice: 'model'`

**原因**：尝试使用不存在的 `omlx model` 命令

**解决**：
```bash
# ❌ 错误用法
omlx model add xxx
omlx model load xxx

# ✅ 正确用法
# 编辑配置文件，然后：
omlx serve
```

---

### ❌ 错误2：配置文件格式错误

**症状**：服务启动失败，提示 YAML 解析错误

**检查**：
```bash
# 验证 YAML 语法
python3 -c "import yaml; yaml.safe_load(open('~/.omlx/config.yaml'))"

# 常见问题：
# - 缩进错误（使用空格，不要用 Tab）
# - 引号不匹配
# - 缺少冒号
```

**修复**：
```yaml
# ✅ 正确格式
models:
  - repo_id: "model-name"  # 2个空格缩进
    model_type: "embedding"

# ❌ 错误格式
models:
- repo_id: "model-name"     # 缺少缩进
model_type: "embedding"      # 缩进错误
```

---

### ❌ 错误3：模型未加载

**诊断**：
```bash
# 1. 检查服务日志
omlx serve 2>&1 | tee omlx.log

# 2. 查看错误信息
tail -100 omlx.log | grep -i error

# 3. 检查模型列表
curl http://localhost:8080/v1/models
```

**可能原因**：
1. 网络问题（无法下载模型）
2. 磁盘空间不足
3. 内存不足
4. 模型 ID 错误

**解决**：
```bash
# 手动下载模型
pip install huggingface_hub
huggingface-cli download nomic-ai/nomic-embed-text-v2-moe

# 使用镜像（国内）
export HF_ENDPOINT=https://hf-mirror.com
huggingface-cli download nomic-ai/nomic-embed-text-v2-moe
```

---

### ❌ 错误4：端口已占用

**症状**：`Address already in use: 8080`

**解决**：
```bash
# 方法A：停止占用端口的进程
lsof -ti:8080 | xargs kill -9

# 方法B：使用其他端口
# 修改配置文件：
server:
  port: 8081  # 改为其他端口
```

---

## API 使用示例

### Python 客户端

```python
import requests

# 基本调用
def get_embedding(text, model="nomic-ai/nomic-embed-text-v2-moe"):
    response = requests.post(
        'http://localhost:8080/v1/embeddings',
        json={'model': model, 'input': text}
    )
    return response.json()['data'][0]['embedding']

# 批量调用
def get_embeddings(texts, model="nomic-ai/nomic-embed-text-v2-moe"):
    response = requests.post(
        'http://localhost:8080/v1/embeddings',
        json={'model': model, 'input': texts}
    )
    return [item['embedding'] for item in response.json()['data']]

# 使用
embedding = get_embedding("人工智能")
print(f"维度: {len(embedding)}")  # 768

embeddings = get_embeddings(["文本1", "文本2", "文本3"])
print(f"数量: {len(embeddings)}")  # 3
```

### curl 命令

```bash
# 单文本
curl http://localhost:8080/v1/embeddings \
  -H "Content-Type: application/json" \
  -d '{
    "model": "nomic-ai/nomic-embed-text-v2-moe",
    "input": "你的文本"
  }'

# 批量
curl http://localhost:8080/v1/embeddings \
  -H "Content-Type: application/json" \
  -d '{
    "model": "nomic-ai/nomic-embed-text-v2-moe",
    "input": ["文本1", "文本2", "文本3"]
  }'
```

---

## 服务管理

### 启动服务

```bash
# 前台运行（适合调试）
omlx serve

# 后台运行
nohup omlx serve > omlx.log 2>&1 &

# 指定配置
omlx serve --config /path/to/config.yaml
```

### 停止服务

```bash
# 方法1：找到进程并结束
pkill -f omlx

# 方法2：查找PID后结束
ps aux | grep omlx
kill <PID>

# 方法3：强制结束
pkill -9 -f omlx
```

### 重启服务

```bash
# 一行命令
pkill -f omlx && sleep 2 && omlx serve &
```

### 查看日志

```bash
# 实时查看
tail -f omlx.log

# 查看错误
grep -i error omlx.log

# 查看特定模型
grep "nomic-embed" omlx.log
```

---

## 配置文件完整示例

```yaml
# ~/.omlx/config.yaml

# 模型配置
models:
  # 对话模型
  - repo_id: "Qwen/Qwen3.5-9B-Instruct"
    model_type: "text-generation"
    adapter_path: null

  # 代码模型
  - repo_id: "deepseek-ai/OmniCoder-9B"
    model_type: "text-generation"
    adapter_path: null

  # 视觉模型
  - repo_id: "THUDM/GLM-4V-9B"
    model_type: "vision"
    adapter_path: null

  # 嵌入模型
  - repo_id: "nomic-ai/nomic-embed-text-v2-moe"
    model_type: "embedding"
    adapter_path: null

# 服务器配置
server:
  host: "0.0.0.0"        # 监听所有接口（局域网可访问）
  port: 8080             # API 端口
  workers: 1             # 工作进程数
  timeout: 300           # 请求超时（秒）

# 缓存配置
cache:
  enabled: true          # 启用缓存
  size_mb: 2048          # 缓存大小（MB）
  ttl: 3600              # 缓存过期时间（秒）

# 量化配置
quantization:
  enabled: true          # 启用量化
  bits: 4                # 量化位数（4/8）
  calibration: false     # 校准量化（更精确但更慢）

# 日志配置
logging:
  level: "INFO"          # 日志级别：DEBUG/INFO/WARNING/ERROR
  file: "~/.omlx/logs/server.log"
  max_size_mb: 100
  backup_count: 5

# 性能配置
performance:
  max_batch_size: 32     # 最大批处理大小
  prefill_chunk_size: 512
  max_concurrent_requests: 4
```

---

## 性能优化建议

### 内存优化

```yaml
# 低内存配置（16GB）
quantization:
  bits: 4                # 4-bit 量化
cache:
  size_mb: 1024          # 减少缓存

# 高内存配置（32GB+）
quantization:
  bits: 8                # 8-bit 量化（更精确）
cache:
  size_mb: 4096          # 增加缓存
```

### 吞吐量优化

```yaml
performance:
  max_batch_size: 64          # 增加批处理
  max_concurrent_requests: 8  # 增加并发
```

### 延迟优化

```yaml
cache:
  enabled: true
  size_mb: 4096          # 大缓存
quantization:
  enabled: false         # 禁用量化（如果内存足够）
```

---

## 监控和调试

### 健康检查

```bash
# 检查服务状态
curl http://localhost:8080/health

# 列出模型
curl http://localhost:8080/v1/models

# 查看模型详情
curl http://localhost:8080/v1/models/<model-id>
```

### 性能测试

```bash
# 测试延迟
time curl http://localhost:8080/v1/embeddings \
  -H "Content-Type: application/json" \
  -d '{"model": "nomic-ai/nomic-embed-text-v2-moe", "input": "test"}'

# 压力测试（需要 ab 工具）
ab -n 100 -c 10 -p test.json -T application/json \
  http://localhost:8080/v1/embeddings
```

---

## 相关文档

- [omlx-embedding-models.md](./omlx-embedding-models.md) - 完整部署指南
- [QUICKSTART-OMLX.md](../QUICKSTART-OMLX.md) - 快速开始
- [mac-omlx-deployment-plan.md](../mac-omlx-deployment-plan.md) - 部署计划
- [BASELINE.md](../BASELINE.md) - 系统基线

---

## 获取帮助

```bash
# oMLX 帮助
omlx --help
omlx serve --help
omlx launch --help

# 查看版本
omlx --version

# 官方文档
# https://github.com/jundot/omlx
```

---

## 更新记录

| 日期 | 版本 | 说明 |
|------|------|------|
| 2026-03-27 | 1.0 | 初始版本 - 修正 CLI 命令错误 |
