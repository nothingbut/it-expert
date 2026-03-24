# CLAUDE.md

本文件为 Claude Code (claude.ai/code) 提供在此仓库中工作的指导。

## 仓库概述

这是一个**纯文档仓库**，用于跟踪 IT 基础设施项目和游戏系统部署。仓库记录了硬件清单、软件安装计划、部署流程以及个人 IT 项目的进度。

**目标设备**: 铭凡UM773 小主机（AMD 7735, 64GB RAM, 2TB SSD）

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

### 设计规范

- **docs/superpowers/specs/2026-03-24-playnite-gaming-frontend-design.md** - 综合设计文档（27k+ tokens）
  - 统一游戏前端的完整系统架构
  - 软件资源和官方下载链接
  - 全平台模拟器配置（FC 到 Switch）
  - 性能优化设置
  - 备份和维护策略
  - 验收标准和故障排除

## 项目背景

本仓库跟踪两个主要部署项目：

1. **Playnite 游戏前端** - 带模拟器支持的统一游戏中心
  - 全屏启动器，Xbox/PlayStation 风格界面
  - 模拟器支持：RetroArch、PCSX2、Dolphin、Ryujinx、DuckStation、Citra、RPCS3
  - 客厅模式自动启动配置
  - 集成应用：Edge 浏览器、网易云音乐、哔哩哔哩、极空间

2. **OpenClaw + ClawBot** - 基于 WSL2 的开发环境
  - WSL2 Ubuntu 安装在 D 盘（与现有 Hyper-V 虚拟机共存）
  - 基于 Docker 的部署
  - 腾讯 ClawBot 集成实现聊天机器人功能
  - 端口转发实现外部访问

## 硬件配置

**主要设备：铭凡UM773**
- CPU：AMD 7735（8 核 16 线程）
- 内存：64GB DDR5 4800
- 存储：500GB M.2 SSD（C: Windows 系统）+ 2TB SATA SSD（E: 数据盘）
- 虚拟化：已启用 Hyper-V（飞牛NAS 虚拟机，60GB）

**次要设备：联想 ThinkBook+**
- CPU：Intel Core Ultra 155H
- GPU：NVIDIA RTX 4060（8GB 显存）
- 存储：1TB M.2 SSD + 4TB M.2 SSD

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
