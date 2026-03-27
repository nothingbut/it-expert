# OpenClaw 最新安装方案（WSL2）

> **更新日期**: 2026-03-27
> **OpenClaw 版本**: v2026.3.24（最新）
> **目标设备**: 铭凡UM773（Windows 11 + WSL2）
> **变化**: 官方推荐方式变更，不再使用 Docker

---

## ⚠️ 重要更新

OpenClaw 在 **v2026.3.24** 进行了重大升级：
- ✅ 推荐使用 `openclaw onboard` 命令行安装
- ✅ WSL2 为官方强烈推荐方式
- ✅ 需要 Node.js 24（推荐）或 22.16+
- ✅ 新增 OpenAI 兼容 API（`/v1/models`、`/v1/embeddings`）
- ❌ 不再推荐 Docker 方式

---

## 🚀 快速安装（3步）

### 第1步：配置 WSL2（如果未安装）

```powershell
# 管理员 PowerShell
wsl --install Ubuntu-24.04
wsl --set-default-version 2

# 重启计算机
Restart-Computer
```

### 第2步：在 WSL2 中安装 Node.js 24

```bash
# 进入 WSL2
wsl

# 安装 Node.js 24（推荐使用 fnm）
curl -fsSL https://fnm.vercel.app/install | bash
source ~/.bashrc

fnm install 24
fnm use 24
fnm default 24

# 验证
node --version  # 应显示 v24.x.x
npm --version
```

### 第3步：安装并启动 OpenClaw

```bash
# 全局安装 OpenClaw
npm install -g openclaw@latest

# 运行引导式安装（推荐）
openclaw onboard --install-daemon

# 或手动启动 Gateway
openclaw gateway --port 18789 --verbose
```

---

## 📋 详细配置

### WSL2 优化配置

创建 `C:\Users\<你的用户名>\.wslconfig`：

```ini
[wsl2]
memory=20GB
processors=8
swap=8GB
autoMemoryReclaim=gradual
```

### OpenClaw 配置位置

```bash
# 配置文件
~/.openclaw/config.yaml

# 数据目录
~/.openclaw/workspace/

# 日志
~/.openclaw/logs/
```

### 连接 oMLX（本地模型）

编辑 `~/.openclaw/config.yaml`：

```yaml
models:
  providers:
    - id: omlx-local
      type: openai
      baseURL: http://192.168.x.x:8000/v1
      apiKey: "2348"
      models:
        - id: qwen-0.5b
          name: Qwen2.5-0.5B-Instruct

agent:
  defaultModel: qwen-0.5b
  defaultProvider: omlx-local
```

---

## 🎯 验证安装

```bash
# 检查服务状态
openclaw doctor

# 测试 Agent
openclaw agent --message "你好" --thinking high

# 查看模型列表
curl http://localhost:18789/v1/models
```

---

## 🔄 与 oMLX 集成

OpenClaw 现在完全兼容 OpenAI API 格式：

```bash
# OpenClaw Gateway
http://localhost:18789/v1/chat/completions
http://localhost:18789/v1/models
http://localhost:18789/v1/embeddings

# 可以无缝对接 oMLX
OpenClaw → oMLX (http://192.168.x.x:8000/v1)
```

---

## 📊 资源占用

| 组件 | 内存 | 存储 | 备注 |
|------|------|------|------|
| WSL2 Ubuntu | 20GB | 10GB | 可调整 |
| Node.js + OpenClaw | ~500MB | 2GB | 运行时 |
| 配置/数据 | <100MB | 5GB | 增长 |
| **总计** | **~20.5GB** | **~17GB** | |

**铭凡UM773（64GB 内存）**: ✅ 完全够用

---

## 🔧 常用命令

```bash
# 启动/停止
openclaw gateway --port 18789 --daemon
pkill -f openclaw

# 更新
openclaw update --channel stable

# 健康检查
openclaw doctor

# 发送消息
openclaw message send --to +1234567890 --message "测试"

# 配置向导
openclaw onboard
```

---

## 📝 与旧方案对比

| 项目 | 旧方案（Docker + ClawBot）| 新方案（OpenClaw Onboard）|
|------|-------------------------|---------------------------|
| 安装方式 | Docker Compose | npm 全局安装 |
| 配置难度 | ⭐⭐⭐⭐ | ⭐⭐ |
| 资源占用 | 较高 | 较低 |
| 更新维护 | 手动拉取镜像 | `openclaw update` |
| OpenAI 兼容 | 部分 | ✅ 完整 |
| 官方支持 | ❌ 已过时 | ✅ 当前推荐 |

---

## 🔗 参考资源

- [OpenClaw 官方文档](https://docs.openclaw.ai)
- [快速开始指南](https://docs.openclaw.ai/start/getting-started)
- [GitHub 仓库](https://github.com/openclaw/openclaw)
- [更新日志](https://github.com/openclaw/openclaw/releases/latest)

---

## ⚠️ 旧文档状态

- **`openclaw-installation-plan.md`** - 标记为过时，仅供参考
- **当前文档** - 基于 v2026.3.24 最新版本

---

**创建时间**: 2026-03-27
**OpenClaw 版本**: v2026.3.24
**测试状态**: 待验证
