# Mac Mini 纯 MLX AI 服务器部署方案

> **创建日期**: 2026-03-24
> **目标设备**: Mac Mini (Apple Silicon)
> **部署模型**: Qwen3.5-9B, OmniCoder-9B, GLM-OCR
> **架构**: 纯 MLX，无 Ollama 依赖

---

## 📋 方案概述

### 设计目标

- ✅ **零 Ollama 依赖** - 完全使用 MLX 生态系统
- ✅ **多模型支持** - 同时部署 3 个模型服务
- ✅ **OpenAI 兼容** - 局域网内无缝替换 OpenAI API
- ✅ **高性能** - 使用 vllm-mlx 获取最佳性能
- ✅ **易维护** - 自动化启动和监控脚本

### 架构设计

```
[Mac Mini - M2 Pro 32GB]
    |
    +── MLX API Server 1 (Port 8000)
    |   └── Qwen3.5-9B (通用对话)
    |
    +── MLX API Server 2 (Port 8001)
    |   └── OmniCoder-9B (代码生成)
    |
    +── MLX-VLM Server (Port 8002)
    |   └── GLM-4V-9B (OCR/视觉)
    |
    +── Nginx Proxy (Port 80, 可选)
        └── 统一入口 + 负载均衡

[局域网客户端]
    ├── 铭凡UM773 (游戏前端) → 通用对话
    ├── 联想 ThinkBook+ (开发) → 代码生成
    └── 其他设备 → OCR/视觉任务
```

---

## 🚀 第一阶段：环境准备

### 1.1 系统要求检查

```bash
# 检查 macOS 版本（需要 12.0+）
sw_vers

# 检查可用内存（建议 32GB+）
htop -m  # 或使用 Activity Monitor

# 检查磁盘空间（需要至少 100GB 可用）
df -h

# 检查网络连接
ping -c 3 192.168.1.1
```

### 1.2 安装 Python 环境

```bash
# 安装 Homebrew（如果未安装）
/bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"

# 安装 Python 3.11+
brew install python@3.11

# 验证安装
python3 --version  # 应该是 3.11 或更高
```

### 1.3 创建项目目录

```bash
# 创建 MLX 项目根目录
mkdir -p ~/mlx-ai-server
cd ~/mlx-ai-server

# 创建子目录
mkdir -p {models,logs,scripts,config}

# 目录结构
# ~/mlx-ai-server/
# ├── models/          # 模型文件存储（软链接）
# ├── logs/            # 服务器日志
# ├── scripts/         # 启动/管理脚本
# └── config/          # 配置文件
```

---

## 📦 第二阶段：依赖安装

### 2.1 安装 MLX 核心库

```bash
cd ~/mlx-ai-server

# 创建虚拟环境（推荐）
python3 -m venv venv
source venv/bin/activate

# 升级 pip
pip install --upgrade pip

# 安装核心依赖
pip install mlx mlx-lm

# 安装高性能服务器（推荐）
pip install vllm-mlx

# 安装视觉模型支持
pip install mlx-vlm

# 安装模型管理工具
pip install huggingface_hub

# 验证安装
python -c "import mlx; print(f'MLX version: {mlx.__version__}')"
python -c "import mlx_lm; print('MLX-LM installed')"
python -c "import mlx_vlm; print('MLX-VLM installed')"
```

### 2.2 配置 Hugging Face 缓存

```bash
# 设置环境变量（添加到 ~/.zshrc）
cat >> ~/.zshrc << 'EOF'

# MLX & Hugging Face 配置
export HF_HOME="$HOME/.cache/huggingface"
export MLX_MODELS="$HOME/mlx-ai-server/models"
export TRANSFORMERS_CACHE="$HF_HOME/hub"
EOF

# 重新加载配置
source ~/.zshrc

# 创建缓存目录
mkdir -p ~/.cache/huggingface/hub
```

---

## 🎯 第三阶段：模型下载

### 3.1 下载 Qwen3.5-9B（通用对话）

```bash
cd ~/mlx-ai-server

# 方法 1: 使用 Hugging Face CLI（推荐）
huggingface-cli download Qwen/Qwen2.5-9B-Instruct \
  --local-dir ~/.cache/huggingface/hub/models--Qwen--Qwen2.5-9B-Instruct/snapshots/main \
  --local-dir-use-symlinks False

# 方法 2: 使用 Python 脚本（带进度条）
python3 << 'EOF'
from huggingface_hub import snapshot_download
import os

model_id = "Qwen/Qwen2.5-9B-Instruct"
cache_dir = os.path.expanduser("~/.cache/huggingface")

print(f"下载 {model_id}...")
snapshot_download(
    repo_id=model_id,
    cache_dir=cache_dir,
    local_dir=os.path.join(cache_dir, "hub", f"models--{model_id.replace('/', '--')}", "snapshots", "main"),
    local_dir_use_symlinks=False
)
print("下载完成！")
EOF

# 验证下载
ls -lh ~/.cache/huggingface/hub/models--Qwen--Qwen2.5-9B-Instruct/snapshots/*/model.safetensors
# 应该显示约 18GB 的文件
```

### 3.2 下载 OmniCoder-9B（代码生成）

```bash
# 使用 Hugging Face CLI
huggingface-cli download Tesslate/OmniCoder-9B \
  --local-dir ~/.cache/huggingface/hub/models--Tesslate--OmniCoder-9B/snapshots/main \
  --local-dir-use-symlinks False

# 验证
ls -lh ~/.cache/huggingface/hub/models--Tesslate--OmniCoder-9B/snapshots/*/model.safetensors
```

### 3.3 下载 GLM-4V-9B（OCR/视觉）

```bash
# GLM-4V 模型（GLM-OCR 的开源版本）
huggingface-cli download THUDM/glm-4v-9b \
  --local-dir ~/.cache/huggingface/hub/models--THUDM--glm-4v-9b/snapshots/main \
  --local-dir-use-symlinks False

# 验证
ls -lh ~/.cache/huggingface/hub/models--THUDM--glm-4v-9b/snapshots/main/
```

### 3.4 创建模型软链接（方便管理）

```bash
cd ~/mlx-ai-server/models

# 创建软链接指向实际模型
ln -s ~/.cache/huggingface/hub/models--Qwen--Qwen2.5-9B-Instruct/snapshots/*/ qwen2.5-9b
ln -s ~/.cache/huggingface/hub/models--Tesslate--OmniCoder-9B/snapshots/*/ omnicoder-9b
ln -s ~/.cache/huggingface/hub/models--THUDM--glm-4v-9b/snapshots/*/ glm-4v-9b

# 验证
ls -la
# 应该看到：
# qwen2.5-9b -> ~/.cache/...
# omnicoder-9b -> ~/.cache/...
# glm-4v-9b -> ~/.cache/...
```

---

## ⚙️ 第四阶段：服务部署

### 4.1 创建启动脚本

#### 主服务器启动脚本

```bash
# ~/mlx-ai-server/scripts/start-all.sh
#!/bin/bash

set -e

PROJECT_ROOT="$HOME/mlx-ai-server"
LOG_DIR="$PROJECT_ROOT/logs"
PID_DIR="$PROJECT_ROOT/pids"
MODELS_DIR="$PROJECT_ROOT/models"

# 创建必要目录
mkdir -p "$LOG_DIR" "$PID_DIR"

# 激活虚拟环境
source "$PROJECT_ROOT/venv/bin/activate"

# 配置
QWEN_PORT=8000
CODER_PORT=8001
VLM_PORT=8002

echo "=== MLX AI 服务器启动脚本 ==="
echo "日期: $(date)"
echo ""

# 函数：启动服务器
start_server() {
    local name=$1
    local model_path=$2
    local port=$3
    local type=$4  # 'text' 或 'vlm'

    local pid_file="$PID_DIR/${name}.pid"
    local log_file="$LOG_DIR/${name}.log"

    # 检查是否已运行
    if [ -f "$pid_file" ]; then
        local pid=$(cat "$pid_file")
        if ps -p $pid > /dev/null 2>&1; then
            echo "✓ $name 已在运行（PID: $pid, Port: $port）"
            return 0
        else
            echo "✗ $name PID 文件存在但进程未运行，清理..."
            rm -f "$pid_file"
        fi
    fi

    echo "→ 启动 $name 服务器（Port: $port）..."

    if [ "$type" = "vlm" ]; then
        # 视觉模型服务器
        nohup python -m mlx_vlm.server \
            --model-path "$model_path" \
            --host 0.0.0.0 \
            --port $port \
            >> "$log_file" 2>&1 &
    else
        # 文本模型服务器（使用 vllm-mlx 获得更好性能）
        nohup python -m vllm_mlx.openai_server \
            --model-path "$model_path" \
            --host 0.0.0.0 \
            --port $port \
            --max-model-len 4096 \
            >> "$log_file" 2>&1 &
    fi

    local pid=$!
    echo $pid > "$pid_file"

    # 等待服务器启动
    sleep 5

    # 验证服务器是否启动成功
    if ps -p $pid > /dev/null 2>&1; then
        echo "✓ $name 启动成功（PID: $pid, Port: $port）"
    else
        echo "✗ $name 启动失败，查看日志: $log_file"
        return 1
    fi
}

# 启动所有服务器
start_server "qwen2.5-9b" "$MODELS_DIR/qwen2.5-9b" $QWEN_PORT "text"
start_server "omnicoder-9b" "$MODELS_DIR/omnicoder-9b" $CODER_PORT "text"
start_server "glm-4v-9b" "$MODELS_DIR/glm-4v-9b" $VLM_PORT "vlm"

echo ""
echo "=== 所有服务器启动完成 ==="
echo ""
echo "服务端点："
echo "  - Qwen3.5-9B:     http://0.0.0.0:$QWEN_PORT/v1"
echo "  - OmniCoder-9B:   http://0.0.0.0:$CODER_PORT/v1"
echo "  - GLM-4V-9B:      http://0.0.0.0:$VLM_PORT/v1"
echo ""
echo "查看日志: tail -f $LOG_DIR/<服务名>.log"
echo "停止服务: $PROJECT_ROOT/scripts/stop-all.sh"
```

#### 停止脚本

```bash
# ~/mlx-ai-server/scripts/stop-all.sh
#!/bin/bash

PROJECT_ROOT="$HOME/mlx-ai-server"
PID_DIR="$PROJECT_ROOT/pids"

echo "=== 停止 MLX AI 服务器 ==="

# 停止所有服务
for pid_file in "$PID_DIR"/*.pid; do
    if [ -f "$pid_file" ]; then
        name=$(basename "$pid_file" .pid)
        pid=$(cat "$pid_file")

        if ps -p $pid > /dev/null 2>&1; then
            echo "→ 停止 $name（PID: $pid）"
            kill $pid
            sleep 2

            # 强制杀死如果还在运行
            if ps -p $pid > /dev/null 2>&1; then
                echo "  强制停止 $name"
                kill -9 $pid
            fi

            echo "✓ $name 已停止"
        else
            echo "✗ $name 未运行"
        fi

        rm -f "$pid_file"
    fi
done

echo "=== 所有服务器已停止 ==="
```

#### 状态检查脚本

```bash
# ~/mlx-ai-server/scripts/status.sh
#!/bin/bash

PROJECT_ROOT="$HOME/mlx-ai-server"
PID_DIR="$PROJECT_ROOT/pids"
LOG_DIR="$PROJECT_ROOT/logs"

echo "=== MLX AI 服务器状态 ==="
echo "检查时间: $(date)"
echo ""

# 定义服务配置
declare -A SERVICES=(
    ["qwen2.5-9b"]="8000"
    ["omnicoder-9b"]="8001"
    ["glm-4v-9b"]="8002"
)

for name in "${!SERVICES[@]}"; do
    port=${SERVICES[$name]}
    pid_file="$PID_DIR/${name}.pid"

    printf "%-15s " "$name:"

    if [ -f "$pid_file" ]; then
        pid=$(cat "$pid_file")
        if ps -p $pid > /dev/null 2>&1; then
            # 检查端口是否监听
            if lsof -i :$port > /dev/null 2>&1; then
                echo -e "\033[32m✓ 运行中\033[0m (PID: $pid, Port: $port)"

                # 显示内存使用
                memory=$(ps -o rss= -p $pid | awk '{printf "%.0f MB", $1/1024}')
                echo "  └─ 内存: $memory"

                # 显示最近的日志
                log_file="$LOG_DIR/${name}.log"
                if [ -f "$log_file" ]; then
                    echo "  └─ 最新日志: $(tail -1 "$log_file" | cut -c1-60)..."
                fi
            else
                echo -e "\033[33m⚠ 进程存在但端口未监听\033[0m (PID: $pid)"
            fi
        else
            echo -e "\033[31m✗ 未运行（PID 文件过期）\033[0m"
            rm -f "$pid_file"
        fi
    else
        echo -e "\033[31m✗ 未运行\033[0m"
    fi
    echo ""
done

# 系统资源
echo "=== 系统资源 ==="
echo "CPU: $(sysctl -n hw.ncpu) 核心"
echo "内存: $(sysctl -n hw.memsize | awk '{printf "%.0f GB", $1/1024/1024/1024}') 总计"
echo "可用内存: $(vm_stat | perl -ne '/page size of (\d+)/ and $ps=$1; /Pages free\s+(\d+)/ and printf "%.2f GB", $1*$ps/1024/1024/1024') 空闲"
echo ""
```

### 4.2 赋予执行权限

```bash
chmod +x ~/mlx-ai-server/scripts/*.sh

# 验证
ls -la ~/mlx-ai-server/scripts/
```

---

## 🌐 第五阶段：网络配置

### 5.1 获取 Mac Mini IP 地址

```bash
# 查看网络配置
ifconfig | grep "inet "

# 或者使用
ipconfig getifaddr en0  # 以太网
ipconfig getifaddr en1  # Wi-Fi
```

### 5.2 配置防火墙（可选）

```bash
# 允许 Python 接受传入连接
sudo /usr/libexec/ApplicationFirewall/socketfilterfw --add /usr/bin/python3
sudo /usr/libexec/ApplicationFirewall/socketfilterfw --unblockapp /usr/bin/python3

# 或者禁用防火墙（仅限受信任的局域网）
# 系统设置 → 网络 → 防火墙 → 关闭
```

### 5.3 测试局域网访问

```bash
# 在 Mac Mini 上测试
curl http://localhost:8000/v1/models

# 从局域网其他设备测试（替换为实际 IP）
curl http://192.168.x.x:8000/v1/models
```

---

## 💻 第六阶段：客户端配置

### 6.1 联想 ThinkBook+ - Claude Code 配置

#### 方法 1: settings.json（推荐）

```bash
# Windows PowerShell
# 编辑配置文件
notepad ~/.claude/settings.json
```

添加以下内容：

```json
{
  "apiBaseUrl": "http://192.168.x.x:8000/v1",
  "apiKey": "dummy",
  "model": "qwen2.5-9b",

  // 如果需要使用代码模型
  "providers": {
    "custom": {
      "baseUrl": "http://192.168.x.x:8001/v1",
      "apiKey": "dummy",
      "models": {
        "omnicoder": "omnicoder-9b"
      }
    }
  }
}
```

#### 方法 2: 环境变量

```powershell
# PowerShell
$env:OPENAI_BASE_URL="http://192.168.x.x:8000/v1"
$env:OPENAI_API_KEY="dummy"

# 或添加到系统环境变量（永久）
setx OPENAI_BASE_URL "http://192.168.x.x:8000/v1"
setx OPENAI_API_KEY "dummy"
```

#### 方法 3: 项目级配置（推荐）

在项目目录创建 `.claude/settings.json`:

```json
{
  "apiBaseUrl": "http://192.168.x.x:8000/v1",
  "apiKey": "dummy",
  "model": "qwen2.5-9b"
}
```

#### 验证连接

```bash
# 在 Claude Code 中测试
claude-code "你好，请介绍一下你自己"
```

### 6.2 铭凡UM773 - OpenClaw (WSL2) 配置

#### 步骤 1: 找到 OpenClaw 配置文件

```bash
# WSL2 Ubuntu
cd ~/.openclaw
ls -la

# 或者在 Windows 中
# \\wsl$\Ubuntu\home\你的用户名\.openclaw\
```

#### 步骤 2: 编辑配置文件

```bash
# 编辑 config.json 或 models.yaml
nano ~/.openclaw/config.json
```

添加以下配置：

```json
{
  "providers": {
    "mlx-qwen": {
      "type": "openai-completions",
      "baseUrl": "http://192.168.x.x:8000/v1",
      "apiKey": "dummy",
      "models": {
        "qwen": {
          "id": "qwen2.5-9b",
          "name": "Qwen3.5-9B (本地)"
        }
      }
    },
    "mlx-coder": {
      "type": "openai-completions",
      "baseUrl": "http://192.168.x.x:8001/v1",
      "apiKey": "dummy",
      "models": {
        "coder": {
          "id": "omnicoder-9b",
          "name": "OmniCoder-9B (本地)"
        }
      }
    },
    "mlx-vlm": {
      "type": "openai-completions",
      "baseUrl": "http://192.168.x.x:8002/v1",
      "apiKey": "dummy",
      "models": {
        "ocr": {
          "id": "glm-4v-9b",
          "name": "GLM-4V-9B (本地)"
        }
      }
    }
  }
}
```

#### 步骤 3: 验证配置

```bash
# 重启 OpenClaw
openclaw restart

# 测试连接
curl http://192.168.x.x:8000/v1/models
```

### 6.3 Python 客户端配置

```python
# ~/.mlx_config.py
MLX_CONFIG = {
    "qwen": {
        "base_url": "http://192.168.x.x:8000/v1",
        "api_key": "dummy",
        "model": "qwen2.5-9b"
    },
    "coder": {
        "base_url": "http://192.168.x.x:8001/v1",
        "api_key": "dummy",
        "model": "omnicoder-9b"
    },
    "vlm": {
        "base_url": "http://192.168.x.x:8002/v1",
        "api_key": "dummy",
        "model": "glm-4v-9b"
    }
}

# 使用示例
from openai import OpenAI

# 通用对话
client = OpenAI(
    base_url=MLX_CONFIG["qwen"]["base_url"],
    api_key=MLX_CONFIG["qwen"]["api_key"]
)

response = client.chat.completions.create(
    model=MLX_CONFIG["qwen"]["model"],
    messages=[{"role": "user", "content": "你好"}]
)

print(response.choices[0].message.content)
```

### 6.4 客户端支持确认

| 工具 | 支持自定义 API | 配置难度 | 推荐度 |
|------|--------------|---------|--------|
| **Claude Code** | ✅ 完全支持 | ⭐ 简单 | ⭐⭐⭐⭐⭐ |
| **OpenClaw** | ✅ 完全支持 | ⭐⭐ 中等 | ⭐⭐⭐⭐⭐ |
| **Cursor** | ✅ 支持 | ⭐⭐ 中等 | ⭐⭐⭐⭐ |
| **Continue.dev** | ✅ 支持 | ⭐ 简单 | ⭐⭐⭐⭐ |
| **其他 OpenAI SDK** | ✅ 完全支持 | ⭐ 简单 | ⭐⭐⭐⭐⭐ |

### 6.5 网络配置要点

#### 获取 Mac Mini IP 地址

```bash
# 在 Mac Mini 上执行
ifconfig | grep "inet "
# 记录类似 192.168.1.100 的地址
```

#### 测试连通性

```powershell
# Windows (ThinkBook+)
ping 192.168.x.x
curl http://192.168.x.x:8000/v1/models

# WSL2 (铭凡UM773)
ping 192.168.x.x
curl http://192.168.x.x:8000/v1/models
```

#### WSL2 网络注意事项

如果 WSL2 无法访问 Mac Mini，可能需要：

```bash
# 检查 WSL2 网络模式
# 在 Windows PowerShell (管理员) 中
wsl --status

# 如果是 NAT 模式，可能需要端口转发
netsh interface portproxy add v4tov4 `
  listenport=8000 `
  listenaddress=0.0.0.0 `
  connectport=8000 `
  connectaddress=192.168.x.x
```

### 6.6 使用场景示例

#### 场景 1: Claude Code 开发时使用本地模型

```bash
# ThinkBook+ 上
cd ~/my-project
claude-code "帮我优化这个函数的性能"

# 自动调用 Mac Mini 上的 Qwen3.5-9B
# 无需联网，无 API 费用
```

#### 场景 2: OpenClaw 调用代码生成模型

```bash
# 铭凡UM773 WSL2 上
openclaw "用 Python 写一个快速排序"

# 自动调用 Mac Mini 上的 OmniCoder-9B
# 生成高质量的代码
```

#### 场景 3: OCR 任务

```python
# 任意客户端
import requests
import base64

# 读取图片并编码
with open("screenshot.png", "rb") as f:
    image_data = base64.b64encode(f.read()).decode()

response = requests.post(
    "http://192.168.x.x:8002/v1/chat/completions",
    json={
        "model": "glm-4v-9b",
        "messages": [
            {
                "role": "user",
                "content": [
                    {"type": "text", "text": "识别图片中的文字"},
                    {"type": "image_url", "image_url": {"url": f"data:image/jpeg;base64,{image_data}"}}
                ]
            }
        ]
    }
)

print(response.json()["choices"][0]["message"]["content"])
```

### 6.7 性能对比

| 操作 | 云端 API | 本地 MLX |
|------|---------|---------|
| 首次响应 | 500-1000ms | 100-200ms |
| Token 生成 | 50-100 t/s | 60-93 t/s |
| 成本 | $0.001/1K tokens | 免费 |
| 隐私 | 数据上传 | 完全本地 |
| 可用性 | 需要网络 | 局域网即可 |

---

## 🔄 第七阶段：开机自启动

### 7.1 创建 LaunchAgent 配置

```bash
# ~/Library/LaunchAgents/com.user.mlx-ai-server.plist
cat > ~/Library/LaunchAgents/com.user.mlx-ai-server.plist << 'EOF'
<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE plist PUBLIC "-//Apple//DTD PLIST 1.0//EN" "http://www.apple.com/DTDs/PropertyList-1.0.dtd">
<plist version="1.0">
<dict>
    <key>Label</key>
    <string>com.user.mlx-ai-server</string>

    <key>ProgramArguments</key>
    <array>
        <string>/bin/bash</string>
        <string>/Users/你的用户名/mlx-ai-server/scripts/start-all.sh</string>
    </array>

    <key>RunAtLoad</key>
    <true/>

    <key>StandardOutPath</key>
    <string>/Users/你的用户名/mlx-ai-server/logs/launch-agent.log</string>

    <key>StandardErrorPath</key>
    <string>/Users/你的用户名/mlx-ai-server/logs/launch-agent.err</string>

    <key>WorkingDirectory</key>
    <string>/Users/你的用户名/mlx-ai-server</string>

    <key>EnvironmentVariables</key>
    <dict>
        <key>PATH</key>
        <string>/usr/local/bin:/usr/bin:/bin:/usr/sbin:/sbin</string>
    </dict>
</dict>
</plist>
EOF

# 替换你的用户名
sed -i '' 's/你的用户名/'$(whoami)'/g' ~/Library/LaunchAgents/com.user.mlx-ai-server.plist
```

### 7.2 加载 LaunchAgent

```bash
# 加载配置
launchctl load ~/Library/LaunchAgents/com.user.mlx-ai-server.plist

# 启动服务
launchctl start com.user.mlx-ai-server

# 查看状态
launchctl list | grep mlx

# 查看日志
tail -f ~/mlx-ai-server/logs/launch-agent.log
```

---

## 📊 第八阶段：监控和维护

### 8.1 实时监控脚本

```bash
# ~/mlx-ai-server/scripts/monitor.sh
#!/bin/bash

clear
while true; do
    tput cup 0 0
    echo "=== MLX AI 服务器监控 ==="
    echo "更新时间: $(date '+%Y-%m-%d %H:%M:%S')"
    echo ""

    # 调用状态脚本
    ~/mlx-ai-server/scripts/status.sh

    # 等待 5 秒刷新
    sleep 5
done
```

### 8.2 日志轮转配置

```bash
# /usr/local/etc/logrotate.d/mlx-ai-server
/Users/$(whoami)/mlx-ai-server/logs/*.log {
    daily
    rotate 7
    compress
    delaycompress
    missingok
    notifempty
    create 644 $(whoami) staff
}
```

### 8.3 健康检查脚本

```bash
# ~/mlx-ai-server/scripts/health-check.sh
#!/bin/bash

PROJECT_ROOT="$HOME/mlx-ai-server"

check_service() {
    local name=$1
    local port=$2
    local url="http://localhost:$port/v1/models"

    if curl -s -f "$url" > /dev/null 2>&1; then
        echo "✓ $name 健康检查通过（Port: $port）"
        return 0
    else
        echo "✗ $name 健康检查失败（Port: $port）"
        return 1
    fi
}

echo "=== MLX AI 服务器健康检查 ==="
echo ""

check_service "qwen2.5-9b" 8000
check_service "omnicoder-9b" 8001
check_service "glm-4v-9b" 8002

echo ""
echo "完成时间: $(date)"
```

---

## 🎯 完整部署清单

### 步骤 1: 初始化（30分钟）

```bash
# ✅ 安装依赖
brew install python@3.11
pip install mlx mlx-lm vllm-mlx mlx-vlm huggingface_hub

# ✅ 创建目录
mkdir -p ~/mlx-ai-server/{models,logs,scripts,pids,config}

# ✅ 下载模型（约 60GB，时间取决于网速）
huggingface-cli download Qwen/Qwen2.5-9B-Instruct --local-dir ~/.cache/huggingface/hub/models--Qwen--Qwen2.5-9B-Instruct/snapshots/main
huggingface-cli download Tesslate/OmniCoder-9B --local-dir ~/.cache/huggingface/hub/models--Tesslate--OmniCoder-9B/snapshots/main
huggingface-cli download THUDM/glm-4v-9b --local-dir ~/.cache/huggingface/hub/models--THUDM--glm-4v-9b/snapshots/main
```

### 步骤 2: 部署脚本（15分钟）

```bash
# ✅ 创建启动脚本（复制上面的 start-all.sh）
# ✅ 创建停止脚本（复制上面的 stop-all.sh）
# ✅ 创建状态脚本（复制上面的 status.sh）
# ✅ 赋予执行权限
chmod +x ~/mlx-ai-server/scripts/*.sh
```

### 步骤 3: 测试启动（10分钟）

```bash
# ✅ 启动所有服务
~/mlx-ai-server/scripts/start-all.sh

# ✅ 检查状态
~/mlx-ai-server/scripts/status.sh

# ✅ 测试 API
curl http://localhost:8000/v1/models
curl http://localhost:8001/v1/models
curl http://localhost:8002/v1/models
```

### 步骤 4: 局域网测试（10分钟）

```bash
# ✅ 获取 Mac Mini IP
ifconfig | grep "inet "

# ✅ 从其他设备测试
curl http://192.168.x.x:8000/v1/models
```

### 步骤 5: 配置自启动（5分钟）

```bash
# ✅ 创建 LaunchAgent（复制上面的配置）
# ✅ 加载服务
launchctl load ~/Library/LaunchAgents/com.user.mlx-ai-server.plist
```

---

## 📈 性能预期

### Mac Mini M2 Pro 32GB

| 模型 | 内存占用 | 推理速度 | 并发支持 | 建议用途 |
|------|---------|---------|---------|---------|
| Qwen3.5-9B | 12GB | 60-93 t/s | 4-8 用户 | 通用对话 |
| OmniCoder-9B | 12GB | 60-93 t/s | 4-8 用户 | 代码生成 |
| GLM-4V-9B | 14GB | 40-60 t/s | 2-4 用户 | OCR/视觉 |

### 总资源占用

- **内存**: 约 38GB（需要 32GB+ 内存）
- **磁盘**: 约 60GB（模型文件）
- **功耗**: 约 30-50W（满载）

---

## 🔧 故障排除

### 常见问题

#### 1. 模型下载失败

```bash
# 使用镜像加速
export HF_ENDPOINT=https://hf-mirror.com
huggingface-cli download ...
```

#### 2. 端口被占用

```bash
# 查看占用端口的进程
lsof -i :8000

# 杀死进程
kill -9 <PID>
```

#### 3. 内存不足

```bash
# 减少最大上下文长度
python -m vllm_mlx.openai_server \
  --model-path ... \
  --max-model-len 2048  # 默认是 4096
```

#### 4. 服务器启动失败

```bash
# 查看日志
tail -f ~/mlx-ai-server/logs/qwen2.5-9b.log

# 常见错误：
# - CUDA/Metal 相关：确保 MLX 正确安装
# - 模型文件缺失：重新下载模型
# - 权限问题：检查脚本执行权限
```

---

## 📝 总结

### 一键启动命令

```bash
# 启动所有服务
~/mlx-ai-server/scripts/start-all.sh

# 查看状态
~/mlx-ai-server/scripts/status.sh

# 停止所有服务
~/mlx-ai-server/scripts/stop-all.sh

# 实时监控
~/mlx-ai-server/scripts/monitor.sh
```

### API 端点

```
Qwen3.5-9B (通用):    http://192.168.x.x:8000/v1
OmniCoder-9B (代码):  http://192.168.x.x:8001/v1
GLM-4V-9B (视觉):     http://192.168.x.x:8002/v1
```

### 客户端示例

```python
from openai import OpenAI

# 通用对话
client = OpenAI(base_url="http://192.168.x.x:8000/v1", api_key="dummy")
response = client.chat.completions.create(
    model="qwen2.5-9b",
    messages=[{"role": "user", "content": "你好"}]
)
```

---

**文档版本**: v1.0
**维护者**: IT 团队
**最后更新**: 2026-03-24
**预计部署时间**: 1-2 小时
