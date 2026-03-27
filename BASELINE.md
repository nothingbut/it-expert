# IT 环境基线文档

> **文档用途**: 记录设备状态、系统配置和项目进度，作为环境管理的参考基准
>
> **最后更新**: 2026-03-24
>
> **更新原则**: 每次系统变更、软件安装或配置修改后更新相应章节

---

## 目录
- [设备清单](#设备清单)
- [系统状态](#系统状态)
- [项目进度](#项目进度)
- [配置参数](#配置参数)
- [网络拓扑](#网络拓扑)
- [问题跟踪](#问题跟踪)
- [变更历史](#变更历史)

---

## 设备清单

### 主设备 1: 铭凡UM773 小主机

#### 硬件配置
| 项目 | 规格 | 状态 |
|------|------|------|
| 型号 | 铭凡 UM773 | ✅ 正常 |
| CPU | AMD 7735 | ✅ 正常 |
| 内存 | 64G DDR5 4800 | ✅ 正常 |
| 主硬盘 | 500G M.2 SSD | ✅ 正常 |
| 副硬盘 | 2T SATA SSD | ✅ 正常 |

#### 磁盘分区
| 盘符 | 容量 | 来源 | 用途 | 已用 | 可用 | 使用率 |
|------|------|------|------|------|------|--------|
| C: | 300G | 500G M.2 SSD | Windows 11 系统盘 | ? | ? | ? |
| D: | 200G | 500G M.2 SSD | 数据盘 + WSL2 | 60G | 140G | 30% |
| E: | 2T | 2T SATA SSD | 数据存储 | ? | ? | ? |

**D盘空间分配**:
- Hyper-V 虚拟机（飞牛NAS）: 60G
- WSL2 + OpenClaw (计划): ~17GB（Node.js 方式更轻量）
- 预留空间: ~123GB

#### 操作系统
| 项目 | 版本 | 状态 |
|------|------|------|
| OS | Windows 11 专业版 | ✅ 已安装 |
| 版本号 | ? | 待确认 |
| 构建版本 | ? | 待确认 |
| WSL2 | 未安装 | 🔄 计划安装 |

#### 虚拟化环境
| 项目 | 状态 | 备注 |
|------|------|------|
| Hyper-V | ✅ 已启用 | 运行飞牛NAS (60G) |
| AMD-V | 待确认 | 需在BIOS中检查 |
| WSL2 | 未安装 | 🔄 计划安装到 D:\WSL |

---

### 主设备 2: M4 Mac mini

#### 硬件配置
| 项目 | 规格 | 状态 |
|------|------|------|
| 型号 | Mac mini (M4, 2024) | ✅ 正常 |
| CPU | Apple M4 芯片 | ✅ 正常 |
| 内存 | 32GB 统一内存 | ✅ 正常 |
| 内置硬盘 | 256GB SSD | ✅ 正常 |
| 外置硬盘 | 2TB SSD（扩展坞） | ✅ 正常 |

#### 磁盘分区
| 盘符 | 容量 | 来源 | 用途 | 已用 | 可用 | 使用率 |
|------|------|------|------|------|------|--------|
| 内置 | 256G | 内置 SSD | macOS 系统盘 | ? | ? | ? |
| 外置 | 2T | USB/Thunderbolt 扩展坞 | AI 模型存储 + 数据 | ? | ? | ? |

#### 操作系统
| 项目 | 版本 | 状态 |
|------|------|------|
| OS | macOS Sequoia | ✅ 已安装 |
| 版本号 | 15.0+ | 待确认 |
| AI 框架 | **oMLX** | ✅ 已部署 |
| 安装方式 | DMG + Homebrew | ✅ 已安装 |

#### 角色定位
| 角色 | 优先级 | 说明 |
|------|--------|------|
| AI 推理服务器 | 高 | 使用 oMLX 为局域网提供大模型 API 服务 |
| 多模型服务 | 高 | 已部署 4 个模型（对话、代码、视觉、嵌入） |
| 统一 API 网关 | 高 | 提供 OpenAI 兼容 API 接口 |
| Agent 服务节点 | 中 | 支持 Claude Code、OpenClaw 等客户端 |
| 开发测试环境 | 低 | 可选支持模型微调（MLX/Unsloth） |

#### 部署方案
| 方案 | 状态 | 部署时间 | 推荐度 |
|------|------|----------|--------|
| **oMLX DMG** | ✅ 已部署 | 15-30 分钟 | ⭐⭐⭐⭐⭐ 强烈推荐 |
| MLX 手动部署 | 备选 | 1-2 小时 | ⭐⭐ 研究用途 |

#### 实际部署模型
| 模型 | 用途 | 大小 | 状态 |
|------|------|------|------|
| Qwen3.5-0.8B | 通用对话（轻量） | 1.71GB | ✅ 已加载 |
| OmniCoder-9B | 代码生成 | 18.40GB | ✅ 已加载 |
| GLM-OCR | 视觉/OCR | 2.59GB | ✅ 已加载 |
| **nomic-embed-4bit** | **文本嵌入** | **0.08GB** | ✅ 已加载 |

#### oMLX 服务配置
| 配置项 | 值 | 说明 |
|--------|-----|------|
| 服务地址 | http://0.0.0.0:8000 | 局域网可访问 |
| Web 管理界面 | http://localhost:8000/admin/chat | 图形化管理 |
| API 端点 | http://localhost:8000/v1 | OpenAI 兼容 |
| API Key | `2348` | 认证密钥 |
| 模型目录 | `/Users/shichang/models` | 模型存储路径 |
| 最大内存 | 25.92GB | 自动配置 |
| 缓存启用 | ✅ 是 | 持久化缓存 |
| 量化 | 4-bit | 节省内存 |

---

### 主设备 3: 联想 ThinkBook+

#### 硬件配置
| 项目 | 规格 | 状态 |
|------|------|------|
| 型号 | 联想 ThinkBook+ | ✅ 正常 |
| CPU | Intel Core Ultra 155H | ✅ 正常 |
| 内存 | 32G | ✅ 正常 |
| 显卡 | NVIDIA RTX 4060 (8G 显存) | ✅ 正常 |
| 硬盘 1 | 1T M.2 SSD | ✅ 正常 |
| 硬盘 2 | 4T M.2 SSD | ✅ 正常 |

#### 磁盘分区
| 盘符 | 容量 | 来源 | 用途 | 已用 | 可用 | 使用率 |
|------|------|------|------|------|------|--------|
| C: | 1T | 1T M.2 SSD | Windows 11 系统盘 | ? | ? | ? |
| D: | 4T | 4T M.2 SSD | 数据存储 | ? | ? | ? |

#### 操作系统
| 项目 | 版本 | 状态 |
|------|------|------|
| OS | Windows 11 家庭版 | ✅ 已安装 |
| 版本号 | ? | 待确认 |
| AI 框架 | 可选（Ollama/LM Studio） | 🔄 待评估 |

#### 角色定位
| 角色 | 优先级 | 说明 |
|------|--------|------|
| 日常使用 | 高 | 主要工作笔记本 |
| GPU 加速推理 | 中 | RTX 4060 可用于某些 AI 模型 |
| 游戏娱乐 | 高 | 游戏 + 多媒体 |

---

### 设备角色总览

| 设备 | 主要角色 | AI 能力 | 网络服务 | 客户端支持 |
|------|----------|---------|----------|------------|
| 铭凡UM773 | 游戏前端 + NAS | 辅助 | 飞牛NAS | OpenClaw (WSL2) |
| **M4 Mac mini** | **AI 推理服务器** | **主力** | **oMLX (端口 8080)** | **局域网内所有设备** |
| 联想 ThinkBook+ | 日常工作站 | 备用 | 可选推理服务 | Claude Code |

#### AI 服务架构
```
M4 Mac mini (oMLX) - http://192.168.x.x:8000
    |
    +--- 通用对话: Qwen3.5-0.8B (1.71GB)
    +--- 代码生成: OmniCoder-9B (18.40GB)
    +--- 视觉/OCR: GLM-OCR (2.59GB)
    +--- 文本嵌入: nomic-embed-4bit (0.08GB) ⭐ 新增
    |
    +--- API 兼容: OpenAI 格式
    +--- Web 界面: http://localhost:8000/admin/chat
    +--- API Key: 2348
    +--- 性能优化: 持久化缓存 + 4-bit 量化
    +--- 内存优化: TurboQuant (73-79% 减少)
```

**客户端访问示例**:
```bash
# 对话 API
curl http://192.168.x.x:8000/v1/chat/completions \
  -H "Authorization: Bearer 2348" \
  -d '{"model": "Qwen3.5-0.8B", "messages": [...]}'

# 嵌入 API
curl http://192.168.x.x:8000/v1/embeddings \
  -H "Authorization: Bearer 2348" \
  -d '{"model": "nomic-embed-4bit", "input": "..."}'
```

---

## 系统状态

### 铭凡UM773 小主机

#### Windows 功能状态
| 功能 | 状态 | 备注 |
|------|------|------|
| Hyper-V | ✅ 已启用 | 运行飞牛NAS |
| WSL | ⬜ 未安装 | |
| 虚拟机平台 | ⬜ 未安装 | |
| Windows Defender | 待确认 | |
| 防火墙 | 待确认 | |

#### 已安装软件
| 软件 | 版本 | 用途 | 状态 |
|------|------|------|------|
| Hyper-V Manager | - | 虚拟化管理 | ✅ 运行中 |
| 飞牛NAS (VM) | ? | NAS 服务 | ✅ 运行中 |
| (其他软件待补充) | - | - | - |

#### WSL2 环境（计划安装）
| 组件 | 版本 | 安装路径 | 状态 |
|------|------|----------|------|
| WSL2 内核 | - | - | ⬜ 未安装 |
| Ubuntu | 24.04 LTS (计划) | D:\WSL\Ubuntu | ⬜ 未安装 |
| Node.js | 24 (计划) | - | ⬜ 未安装 |
| OpenClaw | v2026.3.24 | npm global | ⬜ 未安装 |

---

## 项目进度

### M4 Mac mini oMLX AI 服务器部署项目

#### 项目信息
- **项目名称**: M4 Mac mini oMLX AI 服务器部署
- **目标设备**: M4 Mac mini (32GB 内存)
- **开始日期**: 2026-03-25
- **预计完成**: 2026-03-25（1 小时内）
- **当前状态**: 🔄 待开始
- **部署方案**: oMLX (github.com/jundot/omlx)

#### 阶段进度

##### 阶段 1: 环境检查和准备（5 分钟）
| 任务 | 状态 | 完成日期 | 备注 |
|------|------|----------|------|
| 1.1 检查 macOS 版本（需要 15.0+） | ⬜ 待开始 | - | sw_vers |
| 1.2 检查内存（建议 32GB+） | ⬜ 待开始 | - | sysctl hw.memsize |
| 1.3 检查磁盘空间（需要 100GB+） | ⬜ 待开始 | - | df -h |
| 1.4 确认 Apple Silicon | ⬜ 待开始 | - | uname -m |
| **阶段 1 完成度** | **0/4 (0%)** | - | |

##### 阶段 2: 安装 oMLX（5 分钟）
| 任务 | 状态 | 完成日期 | 备注 |
|------|------|----------|------|
| 2.1 下载 oMLX DMG | ⬜ 待开始 | - | 从 GitHub Releases |
| 2.2 安装 oMLX 到 Applications | ⬜ 待开始 | - | 拖拽安装 |
| 2.3 启动 oMLX 应用 | ⬜ 待开始 | - | open -a oMLX |
| 2.4 验证服务启动 | ⬜ 待开始 | - | http://localhost:8080 |
| **阶段 2 完成度** | **0/4 (0%)** | - | |

##### 阶段 3: 模型下载（5 分钟配置 + 30-60 分钟下载）
| 任务 | 状态 | 完成日期 | 备注 |
|------|------|----------|------|
| 3.1 访问 Web 管理界面 | ⬜ 待开始 | - | http://localhost:8080/admin |
| 3.2 下载 Qwen2.5-9B-Instruct | ⬜ 待开始 | - | 18GB |
| 3.3 下载 OmniCoder-9B | ⬜ 待开始 | - | 18GB |
| 3.4 下载 GLM-4V-9B | ⬜ 待开始 | - | 19GB |
| 3.5 验证模型加载 | ⬜ 待开始 | - | curl /v1/models |
| **阶段 3 完成度** | **0/5 (0%)** | - | |

##### 阶段 4: 网络配置（5 分钟）
| 任务 | 状态 | 完成日期 | 备注 |
|------|------|----------|------|
| 4.1 获取 Mac mini IP 地址 | ⬜ 待开始 | - | ipconfig getifaddr en0 |
| 4.2 配置防火墙允许局域网访问 | ⬜ 待开始 | - | 系统设置 |
| 4.3 测试本地 API 访问 | ⬜ 待开始 | - | curl localhost:8080/v1/models |
| 4.4 测试局域网 API 访问 | ⬜ 待开始 | - | 从其他设备测试 |
| **阶段 4 完成度** | **0/4 (0%)** | - | |

##### 阶段 5: 客户端配置（5-10 分钟）
| 任务 | 状态 | 完成日期 | 备注 |
|------|------|----------|------|
| 5.1 配置联想 ThinkBook+ (Claude Code) | ⬜ 待开始 | - | 编辑 settings.json |
| 5.2 配置铭凡UM773 (OpenClaw WSL2) | ⬜ 待开始 | - | 编辑 config.json |
| 5.3 验证 Claude Code 连接 | ⬜ 待开始 | - | 测试对话 |
| 5.4 验证 OpenClaw 连接 | ⬜ 待开始 | - | 测试对话 |
| **阶段 5 完成度** | **0/4 (0%)** | - | |

##### 阶段 6: 性能优化和自动启动（5 分钟）
| 任务 | 状态 | 完成日期 | 备注 |
|------|------|----------|------|
| 6.1 配置 LRU 缓存 | ⬜ 待开始 | - | Web UI Settings |
| 6.2 调整缓存大小 | ⬜ 待开始 | - | Hot: 8GB, Cold: 50GB |
| 6.3 启用连续批处理 | ⬜ 待开始 | - | Web UI Settings |
| 6.4 配置自动启动 | ⬜ 待开始 | - | 登录项 |
| 6.5 运行性能测试 | ⬜ 待开始 | - | omlx benchmark |
| **阶段 6 完成度** | **0/5 (0%)** | - | |

#### 总体进度
- **总任务数**: 26
- **已完成**: 0
- **进行中**: 0
- **未开始**: 26
- **总完成度**: **0%**
- **预计部署时间**: **15-30 分钟**（不含模型下载）

#### 关键配置参数
```yaml
# oMLX 配置
server:
  host: 0.0.0.0
  port: 8080

models:
  max_loaded: 2           # 同时加载 2 个模型
  ttl_minutes: 30         # 30 分钟不用自动卸载
  lru_enabled: true       # 启用 LRU 缓存

cache:
  hot_tier_gb: 8          # RAM 缓存 8GB
  cold_tier_gb: 50        # SSD 缓存 50GB
  prefix_sharing: true    # 启用前缀共享

performance:
  max_batch_size: 8       # 批处理大小
  continuous_batching: true
```

---

### OpenClaw 部署项目

#### OpenClaw 版本信息
- **当前版本**: v2026.3.24（2026-03-25发布）
- **安装方式**: npm global + onboard wizard
- **需要**: Node.js 24（推荐）或 22.16+
- **文档**: openclaw-installation-plan-updated.md
- **官方文档**: https://docs.openclaw.ai/start/getting-started

#### 项目信息
- **项目名称**: OpenClaw 部署
- **目标设备**: 铭凡UM773 小主机
- **开始日期**: 2026-03-23
- **预计完成**: 待定
- **当前状态**: 🔄 规划阶段

#### 阶段进度

##### 阶段 1: WSL2 准备（如已安装跳过）
| 任务 | 状态 | 完成日期 | 备注 |
|------|------|----------|------|
| 1.1 启用 WSL 功能 | ⬜ 待开始 | - | |
| 1.2 启用虚拟机平台 | ⬜ 待开始 | - | |
| 1.3 系统重启 | ⬜ 待开始 | - | |
| 1.4 安装 WSL2 内核更新 | ⬜ 待开始 | - | |
| 1.5 设置 WSL2 为默认版本 | ⬜ 待开始 | - | |
| 1.6 创建 D:\WSL 目录 | ⬜ 待开始 | - | |
| 1.7 配置 .wslconfig 文件 | ⬜ 待开始 | - | |
| 1.8 安装 Ubuntu 到 D 盘 | ⬜ 待开始 | - | |
| 1.9 创建用户并配置 | ⬜ 待开始 | - | |
| **阶段 1 完成度** | **0/9 (0%)** | - | |

##### 阶段 2: Node.js 24 安装
| 任务 | 状态 | 完成日期 | 备注 |
|------|------|----------|------|
| 2.1 更新 Ubuntu 系统 | ⬜ 待开始 | - | sudo apt update && sudo apt upgrade |
| 2.2 安装 Node.js 24 | ⬜ 待开始 | - | 使用 nvm 或官方仓库 |
| 2.3 验证 Node.js 版本 | ⬜ 待开始 | - | node --version |
| 2.4 验证 npm 版本 | ⬜ 待开始 | - | npm --version |
| **阶段 2 完成度** | **0/4 (0%)** | - | |

##### 阶段 3: OpenClaw 安装（npm global）
| 任务 | 状态 | 完成日期 | 备注 |
|------|------|----------|------|
| 3.1 全局安装 OpenClaw | ⬜ 待开始 | - | npm install -g openclaw |
| 3.2 验证安装 | ⬜ 待开始 | - | openclaw --version |
| **阶段 3 完成度** | **0/2 (0%)** | - | |

##### 阶段 4: 配置引导（openclaw onboard）
| 任务 | 状态 | 完成日期 | 备注 |
|------|------|----------|------|
| 4.1 运行配置引导 | ⬜ 待开始 | - | openclaw onboard --install-daemon |
| 4.2 配置 oMLX 连接 | ⬜ 待开始 | - | 输入 Mac mini oMLX 地址 |
| 4.3 验证配置文件 | ⬜ 待开始 | - | cat ~/.openclaw/config.yaml |
| **阶段 4 完成度** | **0/3 (0%)** | - | |

##### 阶段 5: 连接 oMLX
| 任务 | 状态 | 完成日期 | 备注 |
|------|------|----------|------|
| 5.1 测试 oMLX 连接 | ⬜ 待开始 | - | curl Mac mini oMLX API |
| 5.2 启动 OpenClaw Gateway | ⬜ 待开始 | - | openclaw start 或 daemon 启动 |
| 5.3 验证服务运行 | ⬜ 待开始 | - | http://localhost:18789 |
| 5.4 测试对话功能 | ⬜ 待开始 | - | OpenClaw CLI 测试 |
| **阶段 5 完成度** | **0/4 (0%)** | - | |

#### 总体进度
- **总任务数**: 22
- **已完成**: 0
- **进行中**: 0
- **未开始**: 22
- **总完成度**: **0%**

---

### 远程桌面部署项目

#### 项目信息
- **项目名称**: 联想 ThinkBook+ 远程访问铭凡 UM773
- **目标**: 日常操作 + 偶尔游戏 + 局域网/远程访问
- **开始日期**: 2026-03-27
- **预计完成**: 2026-03-27（20-35 分钟）
- **当前状态**: 🔄 待开始

#### 方案架构
```
联想 ThinkBook+ (客户端) → 铭凡 UM773 (服务端)
    |
    +--- 主方案：Windows RDP (日常操作 90%)
    +--- 辅助方案：Parsec (游戏场景 5%)
    +--- 远程访问：Tailscale VPN (外网访问 5%)
```

#### 阶段进度

##### 阶段 1: Windows RDP 配置（P0 - 必须）
| 任务 | 状态 | 完成日期 | 备注 |
|------|------|----------|------|
| 1.1 启用远程桌面（铭凡） | ⬜ 待开始 | - | 设置 → 系统 → 远程桌面 |
| 1.2 配置 NLA 身份验证 | ⬜ 待开始 | - | 安全性增强 |
| 1.3 获取铭凡 IP 地址 | ⬜ 待开始 | - | ipconfig |
| 1.4 测试 RDP 服务 | ⬜ 待开始 | - | Test-NetConnection |
| 1.5 客户端连接测试（ThinkBook+） | ⬜ 待开始 | - | mstsc |
| 1.6 安装 Microsoft Remote Desktop | ⬜ 待开始 | - | Microsoft Store |
| 1.7 创建连接配置 | ⬜ 待开始 | - | 保存凭据 |
| 1.8 创建桌面快捷方式 | ⬜ 待开始 | - | .rdp 文件 |
| **阶段 1 完成度** | **0/8 (0%)** | - | |

##### 阶段 2: Parsec 游戏串流（P1 - 推荐）
| 任务 | 状态 | 完成日期 | 备注 |
|------|------|----------|------|
| 2.1 下载安装 Parsec（铭凡） | ⬜ 待开始 | - | https://parsec.app |
| 2.2 注册并登录账号 | ⬜ 待开始 | - | 免费账号 |
| 2.3 配置 Hosting 设置 | ⬜ 待开始 | - | 1080p 60fps |
| 2.4 验证 Hosting 状态 | ⬜ 待开始 | - | Ready to Host |
| 2.5 安装客户端（ThinkBook+） | ⬜ 待开始 | - | 同账号登录 |
| 2.6 局域网连接测试 | ⬜ 待开始 | - | 自动发现 |
| 2.7 配置快捷键 | ⬜ 待开始 | - | Ctrl+Alt+Shift+D |
| 2.8 游戏性能测试 | ⬜ 待开始 | - | 延迟 < 10ms |
| **阶段 2 完成度** | **0/8 (0%)** | - | |

##### 阶段 3: Tailscale VPN（P2 - 可选）
| 任务 | 状态 | 完成日期 | 备注 |
|------|------|----------|------|
| 3.1 下载安装 Tailscale（铭凡） | ⬜ 待开始 | - | https://tailscale.com |
| 3.2 登录并连接 | ⬜ 待开始 | - | 选择登录方式 |
| 3.3 记录 Tailscale IP | ⬜ 待开始 | - | 100.x.x.x |
| 3.4 安装客户端（ThinkBook+） | ⬜ 待开始 | - | 同账号登录 |
| 3.5 验证 VPN 连接 | ⬜ 待开始 | - | tailscale status |
| 3.6 测试 Ping 连通性 | ⬜ 待开始 | - | ping 100.x.x.x |
| 3.7 RDP 通过 VPN 连接 | ⬜ 待开始 | - | mstsc 100.x.x.x |
| **阶段 3 完成度** | **0/7 (0%)** | - | |

#### 总体进度
- **总任务数**: 23（核心 8 + 可选 15）
- **已完成**: 0
- **进行中**: 0
- **未开始**: 23
- **总完成度**: **0%**

#### 验收标准
| 测试项 | 目标 | 状态 |
|--------|------|------|
| RDP 局域网连接 | < 10ms 延迟 | ⬜ 待测试 |
| RDP 桌面显示 | 流畅清晰 | ⬜ 待测试 |
| RDP 剪贴板 | 双向复制 | ⬜ 待测试 |
| Parsec 游戏延迟 | < 10ms | ⬜ 待测试 |
| Parsec 帧率 | 60fps | ⬜ 待测试 |
| Tailscale VPN | 稳定连接 | ⬜ 待测试 |

---

## 配置参数

### WSL2 配置（计划值）

#### .wslconfig 文件
位置: `%USERPROFILE%\.wslconfig`

```ini
[wsl2]
memory=20GB                    # 内存限制（总内存64G，分配20G）
processors=8                   # CPU核心数（AMD 7735为8核16线程）
autoMemoryReclaim=gradual      # 自动内存回收
swap=8GB                       # 交换文件大小
swapFile=D:\\WSL\\swap.vhdx    # 交换文件路径（D盘）
networkingMode=NAT             # 网络模式
```

#### Ubuntu 安装参数
- **发行版**: Ubuntu 24.04 LTS
- **安装路径**: D:\WSL\Ubuntu
- **WSL 版本**: 2
- **默认用户**: clawuser

### OpenClaw 配置（v2026.3.24）

#### 配置文件位置
- **配置文件**: ~/.openclaw/config.yaml
- **数据目录**: ~/.openclaw/workspace/
- **日志目录**: ~/.openclaw/logs/

#### config.yaml 示例
```yaml
models:
  providers:
    - id: omlx-local
      type: openai
      baseURL: http://192.168.x.x:8000/v1
      apiKey: "2348"

server:
  port: 18789
  host: "0.0.0.0"
```

#### 说明
- **模型提供商**: 连接到 Mac mini oMLX 服务器
- **API Key**: 使用 oMLX 配置的密钥
- **端口**: 默认 18789（v2026.3.24 改为此端口）

### 远程桌面配置（计划值）

#### Windows RDP 配置
```ini
# 服务端（铭凡 UM773）
远程桌面：启用
网络级别身份验证（NLA）：启用
端口：3389（默认）
防火墙规则：允许远程桌面

# 客户端（联想 ThinkBook+）
连接地址：192.168.x.x（局域网）或 100.x.x.x（VPN）
分辨率：1920x1080 或全屏
颜色深度：32 位
连接速度：LAN (10 Mbps 或更高)
```

#### Parsec 配置
```yaml
# 服务端（铭凡 UM773）
hosting:
  enabled: true
  resolution: 1920x1080
  fps: 60
  bandwidth_limit: 50mbps
  h265_enabled: true
  hardware_decode: true

# 连接方式
局域网：自动发现（P2P）
远程：自动穿透（无需端口转发）
端口：UDP 8000-8010（自动选择）
```

#### Tailscale VPN 配置
```
# 网络模式
模式：Peer-to-peer + DERP 中继
协议：WireGuard
加密：端到端加密

# IP 分配
铭凡 UM773：100.x.x.x（自动分配）
联想 ThinkBook+：100.y.y.y（自动分配）

# 访问方式
RDP：mstsc /v:100.x.x.x
Parsec：自动通过 VPN 连接
```

### 网络配置（计划值）

#### 端口转发规则
| 服务 | WSL2 端口 | Windows 端口 | 协议 | 状态 |
|------|-----------|--------------|------|------|
| OpenClaw Gateway | 18789 | 18789 | TCP | ⬜ 未配置 |
| Windows RDP | - | 3389 | TCP | ⬜ 未配置 |
| Parsec | - | UDP 8000-8010 | UDP | ⬜ 未配置 |

#### 防火墙规则
| 规则名称 | 端口 | 方向 | 操作 | 状态 |
|----------|------|------|------|------|
| WSL2 OpenClaw | 18789 | Inbound | Allow | ⬜ 未配置 |
| 远程桌面 | 3389 | Inbound | Allow | ⬜ 未配置 |
| Parsec | 8000-8010 | Inbound | Allow | ⬜ 未配置 |

---

## 网络拓扑

### 当前网络架构

```
互联网
   |
   |
[路由器] (192.168.x.1)
   |
   +--- [M4 Mac mini] (192.168.x.x) - AI 推理服务器 ⭐
   |       |
   |       +--- [oMLX Server] - http://192.168.x.x:8080
   |               |
   |               +--- Qwen2.5-9B (通用对话)
   |               +--- OmniCoder-9B (代码生成)
   |               +--- GLM-4V-9B (视觉/OCR)
   |
   +--- [铭凡UM773 小主机] (192.168.x.x) (Windows 11)
   |       |
   |       +--- [Hyper-V] - 飞牛NAS (60G VM)
   |       |
   |       +--- [WSL2] (计划) - D:\WSL\Ubuntu
   |               |
   |               +--- [Node.js 24]
   |               |       |
   |               |       +--- OpenClaw Gateway (port 18789)
   |               |
   |               +--- [客户端] OpenClaw → 访问 Mac mini oMLX
   |
   +--- [联想 ThinkBook+] (192.168.x.x) (Windows 11)
           |
           +--- [客户端] Claude Code → 访问 Mac mini oMLX
```

#### API 访问路径
```
联想 ThinkBook+ (Claude Code)
    ↓
    HTTP 请求: POST http://192.168.x.x:8080/v1/chat/completions
    ↓
M4 Mac mini (oMLX Server)
    ↓
    模型推理: Qwen2.5-9B / OmniCoder-9B / GLM-4V-9B
    ↓
    HTTP 响应: JSON (OpenAI 兼容格式)
    ↓
联想 ThinkBook+ (Claude Code)
```

### IP 地址分配（待确认）
| 设备 | IP 地址 | 子网掩码 | 网关 | oMLX 端口 |
|------|---------|----------|------|-----------|
| **M4 Mac mini** | ? | ? | ? | **8080** |
| 铭凡UM773 | ? | ? | ? | - |
| 联想 ThinkBook+ | ? | ? | ? | - |
| WSL2 (Ubuntu) | 动态分配 | - | - | - |

#### 服务端口分配
| 设备 | 服务 | 端口 | 协议 | 外部访问 |
|------|------|------|------|----------|
| M4 Mac mini | oMLX API | 8080 | HTTP | ✅ 局域网 |
| M4 Mac mini | oMLX Admin | 8080/admin | HTTP | ✅ 局域网 |
| 铭凡UM773 | OpenClaw Gateway | 18789 | HTTP | ⬜ 计划 |
| 铭凡UM773 | 远程桌面 (RDP) | 3389 | TCP | ⬜ 计划 |
| 铭凡UM773 | Parsec 游戏串流 | 8000-8010 | UDP | ⬜ 可选 |
| 铭凡UM773 | 飞牛NAS | ? | HTTP | ⬜ 待确认 |

---

## 问题跟踪

### 待解决问题

| ID | 问题描述 | 优先级 | 状态 | 创建日期 | 解决方案 |
|----|----------|--------|------|----------|----------|
| - | 无待解决问题 | - | - | - | - |

### 待确认信息

| ID | 项目 | 说明 | 优先级 | 状态 |
|----|------|------|--------|------|
| INFO-001 | C盘使用情况 | 需要确认已用空间和可用空间 | 低 | ⬜ 待确认 |
| INFO-002 | E盘使用情况 | 需要确认已用空间和可用空间 | 低 | ⬜ 待确认 |
| INFO-003 | Windows 版本号 | 需要确认详细版本号和构建号 | 低 | ⬜ 待确认 |
| INFO-004 | AMD-V 状态 | 需要确认BIOS中是否已启用 | 中 | ⬜ 待确认 |
| INFO-005 | OpenClaw npm 包 | v2026.3.24 已确认可通过 npm 全局安装 | 低 | ✅ 已确认 |
| INFO-006 | 网络IP地址 | 需要确认两台设备的IP地址 | 低 | ⬜ 待确认 |

### 风险清单

| ID | 风险描述 | 影响 | 可能性 | 缓解措施 | 状态 |
|----|----------|------|--------|----------|------|
| RISK-001 | D盘空间不足 | 中 | 低 | 定期清理+监控磁盘使用 | ⬜ 待实施 |
| RISK-002 | WSL2 与 Hyper-V 冲突 | 高 | 低 | Win11已支持共存，验证后确认 | ⬜ 待验证 |
| RISK-003 | 内存资源竞争 | 中 | 中 | 限制WSL2内存为20G，监控使用率 | ⬜ 待实施 |

---

## 变更历史

### 2026-03-27
- **[部署]** M4 Mac mini oMLX AI 服务器配置完成 ⭐⭐⭐
  - 安装方式：Homebrew (`brew install omlx`)
  - 服务地址：http://0.0.0.0:8000
  - Web 管理界面：http://localhost:8000/admin/chat
  - API Key：`2348`
  - 已部署 4 个模型（总计 22.78GB）：
    - Qwen3.5-0.8B (1.71GB) - 通用对话
    - OmniCoder-9B (18.40GB) - 代码生成
    - GLM-OCR (2.59GB) - 视觉/OCR
    - **nomic-embed-4bit (0.08GB) - 文本嵌入** ⭐ 新增
- **[新增]** 嵌入模型支持
  - 模型：mlx-community/nomicai-modernbert-embed-base-4bit
  - 维度：768
  - 量化：4-bit（内存占用仅 80MB）
  - 用途：语义搜索、RAG、文本分类、去重检测
  - API 端点：`POST /v1/embeddings`
  - 测试状态：✅ 已验证（返回正确的 768 维向量）
- **[更新]** oMLX 配置优化
  - 监听地址：0.0.0.0（局域网可访问）
  - 端口：8000（从默认 8080 改为 8000）
  - 模型目录：/Users/shichang/models
  - 最大内存：25.92GB（自动配置）
  - 缓存：已启用（持久化 SSD 缓存）
  - 量化：4-bit（TurboQuant 技术，减少 73-79% 内存）
- **[创建]** oMLX 部署文档
  - docs/omlx-quick-reference.md - 快速参考指南
  - docs/omlx-embedding-models.md - 嵌入模型配置指南
  - scripts/omlx-diagnose.sh - 环境诊断脚本
  - scripts/omlx-embedding-client.py - Python 客户端示例
- **[新增]** 远程桌面部署项目 ⭐
  - 目标：联想 ThinkBook+ 远程访问铭凡 UM773
  - 主方案：Windows RDP（日常操作 90%）
  - 辅助方案：Parsec（游戏场景 5%）
  - 远程访问：Tailscale VPN（外网访问 5%）
  - 预计部署时间：20-35 分钟
- **[创建]** 远程桌面方案对比文档（docs/remote-desktop-solutions.md）
  - 6 种方案详细对比（RDP、Parsec、Moonlight、Rustdesk、ToDesk、向日葵）
  - 快速决策矩阵（日常操作、游戏性能、局域网、远程访问）
  - 性能对比（延迟、带宽、CPU 占用、画质）
  - 使用场景推荐和成本分析
- **[创建]** 远程桌面部署计划（remote-desktop-deployment-plan.md）
  - 3 个阶段详细部署步骤（RDP、Parsec、Tailscale）
  - 23 个任务清单（核心 8 + 可选 15）
  - 验收测试标准（延迟、帧率、功能测试）
  - 日常使用指南和故障排除
- **[配置]** 更新网络配置参数
  - 添加 RDP 端口 3389
  - 添加 Parsec 端口 UDP 8000-8010
  - 添加防火墙规则配置
- **[更新]** OpenClaw 部署方案升级到 v2026.3.24 ⭐
  - 安装方式从 Docker 改为 npm global + onboard wizard
  - 删除腾讯 ClawBot SDK（官方已移除该功能）
  - 添加 Node.js 24 依赖要求
  - 默认端口从 8080 改为 18789
  - 配置文件从 Docker compose 改为 ~/.openclaw/config.yaml
- **[优化]** WSL2 + OpenClaw 空间估算从 40-55GB 降低到 ~17GB
  - Node.js 方式比 Docker 方式更轻量
  - D 盘预留空间增加到 ~123GB
- **[更新]** 部署流程简化为 5 个阶段（从原 4 阶段）
  - 阶段1: WSL2 准备（如已安装跳过）
  - 阶段2: Node.js 24 安装
  - 阶段3: OpenClaw 安装（npm global）
  - 阶段4: 配置引导（openclaw onboard）
  - 阶段5: 连接 oMLX
- **[清理]** 删除过时的待确认信息和风险项
  - 删除腾讯云账号确认项
  - 删除 ClawBot 凭证风险项
  - 更新 OpenClaw 仓库地址为 npm 包确认

### 2026-03-25
- **[决策]** 确定 M4 Mac mini 使用 **oMLX** 作为 AI 服务器部署方案 ⭐
  - 理由：开箱即用（15-30 分钟部署），持久化缓存（40-100x 加速），连续批处理（6x 吞吐量）
  - 对比 MLX 手动部署节省 1-2 小时初始开发 + 月均 4-8 小时维护成本
- **[创建]** MLX vs oMLX 详细对比分析文档 (docs/mlx-vs-omlx-comparison.md)
  - 7 大核心对比维度：推理控制、算法实现、架构扩展、数据流、集成、性能调优、研究
  - 决策矩阵：oMLX 在易用性、部署时间、维护成本上优势明显
  - MLX 灵活性优势仅在研究和特殊场景下有价值（<5% 使用场景）
- **[创建]** Mac Mini oMLX 部署方案文档 (mac-omlx-deployment-plan.md)
  - 完整部署流程：6 个阶段，26 个任务，预计 15-30 分钟完成
  - 推荐模型配置：Qwen2.5-9B、OmniCoder-9B、GLM-4V-9B
  - 客户端配置指南：Claude Code、OpenClaw、Python SDK
- **[创建]** MLX 灵活性深度分析文档 (docs/mlx-flexibility-deep-dive.md)
  - 详细说明 MLX 在底层控制、实验算法、模型扩展等方面的优势
  - 提供 Tree of Thoughts、Speculative Decoding、MoE 路由等实现示例
  - 明确 MLX 适用场景：研究、特殊集成、极致性能优化
- **[架构]** 更新网络拓扑图，M4 Mac mini 作为中心 AI 服务器
  - oMLX 统一端口 8080，提供 OpenAI + Anthropic 兼容 API
  - 支持局域网内所有设备访问（联想 ThinkBook+、铭凡UM773）
- **[配置]** 定义 oMLX 推荐配置参数
  - 缓存：Hot Tier 8GB (RAM) + Cold Tier 50GB (SSD)
  - 性能：连续批处理（批次大小 8）、前缀共享
  - 模型管理：LRU 缓存、TTL 30 分钟、最多同时加载 2 个模型
- **[文档]** 更新 BASELINE.md，添加 M4 Mac mini oMLX 部署项目进度跟踪

### 2026-03-24
- **[新增]** 添加 M4 Mac mini 设备记录（32GB 内存，256GB 内置 + 2TB 外置 SSD）
- **[创建]** AI 硬件对比分析文档（ai-hardware-comparison.md）
- **[评估]** M4 Mac mini vs RTX 4060 本地大模型性能对比
- **[规划]** 确定 M4 Mac mini 作为主力 AI 服务器角色
- **[架构]** 设计 Mac mini 为中心的 AI 服务网络拓扑

### 2026-03-24
- **[创建]** Mac Mini 纯 MLX AI 服务器部署方案 (mac-mlx-deployment-plan.md)
  - 设计零 Ollama 依赖的 MLX 部署架构
  - 配置 3 个模型服务（Qwen3.5-9B, OmniCoder-9B, GLM-OCR）
  - 编写完整的启动/停止/监控脚本
  - 提供 Claude Code 和 OpenClaw 客户端配置指南
- **[创建]** Mac 小规模模型微调工具对比文档 (mac-finetuning-tools-comparison.md)
  - 对比 Ollama、LM Studio、Unsloth Studio 在 Mac 上的微调能力
  - 推荐 MLX 框架作为 Mac 微调的首选方案
  - 提供 Swift MLX 性能优化建议
- **[决策]** 确认 Mac Mini 采用纯 MLX 方案，不安装 Ollama
  - 理由：更简洁、更高性能、原生微调支持
  - 使用 vllm-mlx 获取 21-87% 性能提升
- **[验证]** 确认 Claude Code 和 OpenClaw 可通过局域网访问 Mac Mini MLX 服务
  - Claude Code：支持 OpenAI 兼容 API，配置简单
  - OpenClaw：支持自定义 provider，配置中等难度
- **[文档]** 更新基线文档，记录新增部署方案和决策

### 2026-03-23
- **[创建]** 初始化基线文档
- **[规划]** 创建 OpenClaw + ClawBot 部署计划
- **[文档]** 记录铭凡UM773和联想ThinkBook+硬件配置
- **[进度]** 项目处于规划阶段，总完成度 0%

---

## 附录

### 相关文档链接

#### M4 Mac mini AI 服务器部署（推荐方案）⭐
- **[快速部署指南 (QUICKSTART)](./QUICKSTART-OMLX.md)** - 5 步快速部署，适合直接执行 🚀
- **[Mac Mini oMLX 完整部署方案](./mac-omlx-deployment-plan.md)** - 详细部署流程和配置说明
- [MLX vs oMLX 详细对比](./docs/mlx-vs-omlx-comparison.md) - 方案选型决策依据
- [MLX 灵活性深度分析](./docs/mlx-flexibility-deep-dive.md) - MLX 优势场景说明

#### 备选方案和工具对比
- [Mac Mini 纯 MLX 部署方案](./mac-mlx-deployment-plan.md) - 手动部署方案（研究用途）
- [Mac 小规模模型微调工具对比](./docs/mac-finetuning-tools-comparison.md) - Unsloth/MLX 微调
- [本地 AI 推理平台对比分析](./docs/ai-hardware-comparison.md) - 硬件选型

#### 远程桌面项目
- **[快速开始指南 (QUICKSTART)](./QUICKSTART-REMOTE-DESKTOP.md)** - 5 分钟快速配置 RDP 🚀
- **[远程桌面方案对比](./docs/remote-desktop-solutions.md)** - 6 种方案详细对比和选型 🖥️
- **[远程桌面部署计划](./remote-desktop-deployment-plan.md)** - 3 阶段部署流程，20-35 分钟完成

#### 其他项目
- [OpenClaw 安装方案](./openclaw-installation-plan.md) - 铭凡UM773 WSL2 部署
- [OpenClaw 更新安装方案](./openclaw-installation-plan-updated.md) - v2026.3.24 新版本
- [硬件配置详情](./memory/hardware-config.md) - 设备详细配置

### 命令快速参考

#### 查看 Windows 版本
```powershell
winver
systeminfo | findstr /B /C:"OS Name" /C:"OS Version"
```

#### 查看磁盘空间
```powershell
Get-PSDrive C,D,E | Select-Object Name,Used,Free
```

#### 查看 AMD-V 状态
```powershell
systeminfo | findstr /C:"Hyper-V"
```

#### 查看网络配置
```powershell
ipconfig /all
```

### 更新指南

更新本文档时，请遵循以下原则：

1. **状态符号**:
   - ✅ 已完成/正常
   - 🔄 进行中
   - ⬜ 未开始/未配置
   - ❌ 失败/异常
   - ⚠️ 警告/需注意

2. **更新时机**:
   - 完成某个安装步骤后，立即更新进度表
   - 发现新问题时，添加到问题跟踪
   - 修改配置时，同步更新配置参数章节
   - 解决问题后，更新问题状态

3. **版本控制**:
   - 重大变更在变更历史中记录
   - 包含日期、类型和描述

4. **数据完整性**:
   - 确认的信息标记为确认状态
   - 待确认的信息保持问号标记
   - 定期审查待确认信息清单

---

**文档版本**: v1.0
**维护者**: IT 团队
**审阅周期**: 每周或每次重大变更后

---

## oMLX部署记录（2026-03-26）

### 部署信息
- **设备**: MacBook Pro M3 Pro (36GB)
- **oMLX版本**: v0.2.21 (Homebrew)
- **部署状态**: ✅ 成功
- **服务地址**: http://localhost:8000
- **API Key**: 2348

### 已部署模型
| 模型 | 大小 | 用途 | 状态 |
|------|------|------|------|
| Qwen3.5-0.8B | 1.71GB | 通用对话/微调 | ✅ |
| OmniCoder-9B | 18.40GB | 代码生成 | ✅ |
| GLM-OCR | 2.59GB | OCR识别 | ✅ |

### 相关文档
- [实际部署记录](./OMLX-DEPLOYMENT-ACTUAL.md) - 完整部署经验
- [快速指南](./QUICKSTART-OMLX.md) - 快速部署参考
- [使用指南](./OMLX-USAGE-GUIDE.md) - API使用说明

