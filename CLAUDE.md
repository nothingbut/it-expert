# CLAUDE.md

本文件为 Claude Code (claude.ai/code) 提供在此仓库中工作的指导。

## 仓库概述

这是一个**纯文档仓库**，用于跟踪 IT 基础设施项目和游戏系统部署。仓库记录了硬件清单、软件安装计划、部署流程以及个人 IT 项目的进度。

**目标设备**:
- **M4 Mac mini** (32GB, Apple Silicon) - AI 推理服务器 ⭐
- 铭凡UM773 小主机（AMD 7735, 64GB RAM, 2TB SSD）- 游戏前端 + NAS
- 联想 ThinkBook+（Intel Ultra 155H, RTX 4060）- 日常工作站

**主要语言**: 中文（简体）

**框架**: 使用 oh-my-claudecode (OMC) 进行项目组织和记忆管理。

## 文档结构

### 核心文档

- **BASELINE.md** - IT 环境基线文档
  - 多设备硬件清单（铭凡UM773、联想 ThinkBook+）
  - 系统配置跟踪（Windows 11、Hyper-V、WSL2 状态）
  - 项目进度跟踪（含任务完成百分比）
  - WSL2、OpenClaw、ClawBot、网络配置参数
  - 网络拓扑图
  - 问题跟踪和风险评估
  - 变更历史记录

- **DEPLOYMENT-CHECKLIST.md** - Playnite 游戏前端详细部署检查清单
  - 分步安装流程（1200+ 行）
  - 5 个主要部署阶段，每步都有验证方法
  - 软件下载链接和模拟器配置说明
  - 常见问题故障排除指南
  - 预计时间：12-16 小时，分 2-3 天完成

- **openclaw-installation-plan.md** - OpenClaw + 腾讯 ClawBot 部署方案
  - WSL2 配置到 D 盘（分配 40-60GB）
  - Ubuntu 24.04 LTS 安装步骤
  - Docker Compose 部署 OpenClaw
  - 腾讯 ClawBot SDK 集成
  - 网络端口转发配置
  - 维护和故障排除流程

- **playnite-requirements-temp.md** - 需求澄清文档
  - 已确认的项目需求和设计决策
  - 不同游戏平台选定的模拟器组合
  - 存储结构规划
  - 内存分配策略（Hyper-V + WSL2 + 游戏）

- **QUICKSTART-OMLX.md** - M4 Mac mini oMLX 快速部署指南 ⭐ 新增
  - 5 步快速部署流程（15-30 分钟）
  - 系统要求检查脚本
  - 模型下载和配置
  - 客户端配置（Claude Code、OpenClaw）
  - 性能优化和自动启动
  - 常见问题故障排除

- **mac-omlx-deployment-plan.md** - Mac Mini oMLX 完整部署方案 ⭐ 新增
  - 详细部署流程（6 个阶段，26 个任务）
  - 推荐模型配置（Qwen3.5-9B、OmniCoder-9B、GLM-4V-9B）
  - 网络配置和局域网访问
  - 性能优化建议
  - 监控和管理工具
  - 预计部署时间：15-30 分钟（不含模型下载）

### 设计规范

- **docs/mlx-vs-omlx-comparison.md** - MLX vs oMLX 详细对比分析 ⭐ 新增
  - 快速决策矩阵（9 个核心维度对比）
  - 架构对比（MLX 自建 vs oMLX 开箱即用）
  - 7 大功能对比（服务部署、模型管理、上下文缓存等）
  - 成本对比（开发成本、维护成本）
  - 性能测试结果（实际场景数据）
  - 推荐方案：oMLX（99% 场景）

- **docs/mlx-flexibility-deep-dive.md** - MLX 灵活性深度分析 ⭐ 新增
  - MLX 7 大核心优势详解
  - 实验性推理算法实现示例（Tree of Thoughts、Speculative Decoding、MoE）
  - 自定义模型架构扩展
  - 底层性能调优技巧
  - 何时选择 MLX（研究、特殊集成、极致性能）
  - 混合方案建议（先 oMLX 验证，需要时迁移 MLX）

- **mac-mlx-deployment-plan.md** - Mac Mini 纯 MLX 手动部署方案（备选）
  - 零 Ollama 依赖的 MLX 架构
  - 手动编写启动/停止/监控脚本
  - 自定义 API 服务器实现
  - 适用场景：研究、深度定制、学习目的
  - 部署时间：1-2 小时（手动开发）

- **docs/superpowers/specs/2026-03-24-playnite-gaming-frontend-design.md** - 综合设计文档（27k+ tokens）
  - 统一游戏前端的完整系统架构
  - 软件资源和官方下载链接
  - 全平台模拟器配置（FC 到 Switch）
  - 性能优化设置
  - 备份和维护策略
  - 验收标准和故障排除

## 项目背景

本仓库跟踪三个主要部署项目：

1. **M4 Mac mini AI 服务器** - 局域网 AI 推理服务 ⭐ 优先级最高
  - 部署方案：oMLX (github.com/jundot/omlx)
  - 统一 API 网关：提供 OpenAI + Anthropic 兼容接口
  - 多模型服务：Qwen3.5-9B (对话)、OmniCoder-9B (代码)、GLM-4V-9B (视觉)
  - 性能优化：持久化缓存（40-100x 加速）+ 连续批处理（6x 吞吐量）
  - 客户端支持：Claude Code、OpenClaw、Python SDK
  - 部署时间：15-30 分钟（不含模型下载）

2. **Playnite 游戏前端** - 带模拟器支持的统一游戏中心
  - 全屏启动器，Xbox/PlayStation 风格界面
  - 模拟器支持：RetroArch、PCSX2、Dolphin、Ryujinx、DuckStation、Citra、RPCS3
  - 客厅模式自动启动配置
  - 集成应用：Edge 浏览器、网易云音乐、哔哩哔哩、极空间

3. **OpenClaw + ClawBot** - 基于 WSL2 的开发环境
  - WSL2 Ubuntu 安装在 D 盘（与现有 Hyper-V 虚拟机共存）
  - 基于 Docker 的部署
  - 腾讯 ClawBot 集成实现聊天机器人功能
  - 端口转发实现外部访问

## 硬件配置

**主要设备 1：M4 Mac mini** ⭐ AI 服务器
- CPU：Apple M4 芯片（10 核 CPU，10 核 GPU）
- 内存：32GB 统一内存
- 存储：256GB 内置 SSD + 2TB 外置 SSD（扩展坞）
- 网络：千兆以太网 + Wi-Fi 6E
- 部署：oMLX AI 服务器（端口 8080）
- 服务：Qwen3.5-9B、OmniCoder-9B、GLM-4V-9B

**主要设备 2：铭凡UM773** - 游戏前端 + NAS
- CPU：AMD 7735（8 核 16 线程）
- 内存：64GB DDR5 4800
- 存储：500GB M.2 SSD（C: Windows 系统）+ 2TB SATA SSD（E: 数据盘）
- 虚拟化：已启用 Hyper-V（飞牛NAS 虚拟机，60GB）
- 客户端：OpenClaw (WSL2) → 访问 Mac mini oMLX

**主要设备 3：联想 ThinkBook+** - 日常工作站
- CPU：Intel Core Ultra 155H
- GPU：NVIDIA RTX 4060（8GB 显存）
- 存储：1TB M.2 SSD + 4TB M.2 SSD
- 客户端：Claude Code → 访问 Mac mini oMLX

## 在此仓库中工作

### 阅读文档
- 所有文档均为中文（简体）
- 文档使用 Markdown 格式，包含表格、代码块和 shell 命令
- BASELINE.md 是主跟踪文档 - 进行更改时需要更新它

### 更新文档
- 保持中文语言以保持一致性
- 完成任务时更新 BASELINE.md 中的进度跟踪表
- 使用复选框 `[ ]` 表示待办任务，`[x]` 表示已完成
- 在变更历史中包含时间戳和版本号

### 代码和命令
- PowerShell 命令用于 Windows 11 管理
- Bash 命令用于 WSL2 Ubuntu 环境
- Docker Compose 命令用于容器管理
- **无构建/测试/检查命令** - 这只是文档仓库

### 项目记忆
`.omc/project-memory.json` 文件跟踪项目元数据，但显示没有活跃的代码库：
- `techStack`：空（无编程语言或框架）
- `build`：无构建、测试或开发命令
- `structure`：只有一个 `docs` 目录用于文档

## 核心概念

**存储布局**：
```
D:\ （来自 500GB M.2 SSD 的 200GB）
├── WSL\               # WSL2 Ubuntu 安装（40-60GB）
├── openclaw-data\     # OpenClaw 应用数据
└── Backups\           # 备份存储

E:\ （2TB SATA SSD）
├── Games\             # 游戏库
│   ├── PC-Games\      # PC 游戏安装
│   ├── ROMs\          # 模拟器 ROM（按平台分类）
│   └── Game-Assets\   # 封面图、元数据
├── Emulators\         # 模拟器安装
└── Playnite\          # Playnite 便携版安装
```

**内存分配**（总计 64GB）：
- Hyper-V（飞牛NAS）：4-8GB（固定）
- WSL2（Ubuntu + OpenClaw）：20GB（通过 .wslconfig 固定）
- Windows + 游戏：36-52GB（动态共享池）

**模拟器覆盖**：
- 经典主机（FC/SFC/MD/GBA）：RetroArch 核心
- PlayStation：DuckStation (PS1)、PCSX2 (PS2)
- Nintendo：Dolphin (NGC/Wii)、Ryujinx (Switch)、Citra (3DS)
- 实验性：RPCS3 (PS3)、Xenia (Xbox 360)

## 文件编辑指南

修改文档时：
1. 保持中文语言和格式风格
2. 如需跨多个文档更新相关章节
3. 维护表格结构用于进度跟踪
4. 保持下载链接和版本号最新
5. 发现并解决问题时添加故障排除笔记

## 无构建/测试/运行命令

本仓库**不包含可执行代码**。所有文件都是文档（Markdown 格式）。没有：
- 构建命令
- 测试套件
- 开发服务器
- 包安装
- 运行时环境

**不要尝试运行构建命令或测试** - 这纯粹是一个用于 IT 项目规划和跟踪的文档仓库。
