# Playnite 游戏前端系统设计文档

> **项目名称**: 统一游戏娱乐前端系统
>
> **目标设备**: 铭凡UM773 小主机（AMD 7735, 64GB RAM, 2T SSD）
>
> **创建日期**: 2026-03-24
>
> **设计方案**: 统一 Playnite 前端 + 多模拟器后端
>
> **预计工期**: 12-16 小时（分 2-3 天完成）
>
> **总成本**: ¥0（全开源/免费软件）

---

## 目录

1. [项目概述](#1-项目概述)
2. [软件资源和下载链接](#2-软件资源和下载链接)
3. [系统架构设计](#3-系统架构设计)
4. [目录结构设计](#4-目录结构设计)
5. [Playnite 配置方案](#5-playnite-配置方案)
6. [模拟器配置方案](#6-模拟器配置方案)
7. [性能优化配置](#7-性能优化配置)
8. [备份和维护方案](#8-备份和维护方案)
9. [实施路线图](#9-实施路线图)
10. [验收标准](#10-验收标准)
11. [故障排除指南](#11-故障排除指南)

---

## 1. 项目概述

### 1.1 项目目标

打造一个**统一的游戏娱乐中心**，实现：
- ✅ 开机自动进入游戏模式（客厅模式）
- ✅ 全手柄友好操作（Xbox/PlayStation 风格）
- ✅ 统一管理 PC 游戏 + 模拟器游戏 + 娱乐应用
- ✅ 简洁现代的界面风格
- ✅ 全平台模拟器支持（FC 到 Switch）

### 1.2 核心需求

| 需求项 | 具体要求 |
|--------|----------|
| 游戏库规模 | 中型（50-200 款游戏） |
| 模拟器平台 | 全平台覆盖（FC/SFC/MD/GBA/N64/PS1/PS2/NGC/Wii/3DS/Switch/PS3） |
| 存储位置 | E 盘（2T SATA SSD）独立游戏库 |
| 使用场景 | 客厅模式为主（手柄），游戏内可切换键鼠 |
| 启动方式 | 开机自动进入 Playnite 全屏模式 |
| 应用整合 | 浏览器、网易云音乐、哔哩哔哩、极空间 |
| 界面风格 | 简洁现代（Xbox/PlayStation 风格） |

### 1.3 设计原则

1. **统一入口**: Playnite 作为唯一交互界面
2. **零成本**: 全部使用开源/免费软件
3. **易维护**: 单一软件栈，配置简单
4. **高性能**: 充分利用 AMD 7735 + 64GB 内存
5. **数据安全**: 完善的备份和恢复机制

### 1.4 方案优势

| 优势 | 说明 |
|------|------|
| 统一体验 | 单一界面管理所有游戏和应用 |
| 手柄友好 | Xbox/PlayStation 手柄原生支持 |
| 自动化 | 开机即用，无需手动操作 |
| 免费开源 | 软件成本为零 |
| 易于维护 | 配置简单，故障排查方便 |
| 可扩展性 | 轻松添加新游戏和模拟器 |

---

## 2. 软件资源和下载链接

### 2.1 核心软件

#### Playnite（游戏前端）

- **官方网站**: https://playnite.link/
- **GitHub 仓库**: https://github.com/JosefNemec/Playnite
- **下载页面**: https://playnite.link/download.html
- **推荐版本**: Playnite 10.x（最新稳定版）
- **安装类型**: 便携版（Portable）
- **文件大小**: 约 50-80 MB
- **许可证**: MIT License（开源免费）

**下载说明**:
- 选择 "Portable" 版本下载
- 解压到 `E:\Playnite\`
- 无需安装，直接运行

#### Playnite 插件和主题

**插件下载（Playnite 内置商店）**:
- 启动 Playnite 后，进入 `Add-ons` > `Browse`
- 搜索并安装推荐插件（见 5.3 节）

**主题下载**:
- **Strata Fullscreen** (推荐):
  - GitHub: https://github.com/CertainWitch/Strata
  - 内置商店直接下载

- **Harmony**:
  - GitHub: https://github.com/darklinkpower/Harmony
  - 内置商店直接下载

- **ModernUI Fullscreen**:
  - 内置商店直接下载

---

### 2.2 模拟器软件

#### RetroArch（多平台模拟器核心）

- **官方网站**: https://www.retroarch.com/
- **下载页面**: https://www.retroarch.com/?page=platforms
- **推荐版本**: 最新稳定版（Windows x64）
- **文件大小**: 约 200-300 MB（主程序）
- **许可证**: GPL-3.0（开源免费）

**下载步骤**:
1. 访问下载页面
2. 选择 "Windows" > "Windows x64"
3. 下载安装包或便携版
4. 安装到 `E:\Emulators\RetroArch\`

**核心（Core）下载**:
- 启动 RetroArch 后
- 进入 `Online Updater` > `Core Downloader`
- 下载推荐核心（见 6.2.1 节）

---

#### PCSX2（PS2 模拟器）

- **官方网站**: https://pcsx2.net/
- **下载页面**: https://pcsx2.net/downloads/
- **GitHub 仓库**: https://github.com/PCSX2/pcsx2
- **推荐版本**: 1.7.x 或 2.0+（最新稳定版）
- **文件大小**: 约 80-150 MB
- **许可证**: GPL-3.0（开源免费）

**下载说明**:
- 选择 Windows 版本
- 下载独立安装程序
- 安装到 `E:\Emulators\PCSX2\`

**BIOS 要求**:
- 需要 PS2 BIOS 文件（约 4MB）
- 放置在 `E:\Emulators\PCSX2\bios\` 目录

---

#### Dolphin（NGC/Wii 模拟器）

- **官方网站**: https://dolphin-emu.org/
- **下载页面**: https://dolphin-emu.org/download/
- **GitHub 仓库**: https://github.com/dolphin-emu/dolphin
- **推荐版本**: 最新稳定版（Stable）或开发版（Dev）
- **文件大小**: 约 80-120 MB
- **许可证**: GPL-2.0（开源免费）

**下载说明**:
- 推荐下载 "Stable" 版本
- 选择 Windows x64 版本
- 解压到 `E:\Emulators\Dolphin\`

**无需 BIOS**: Dolphin 不需要 BIOS 文件

---

#### Citra（3DS 模拟器）

- **官方网站**: https://citra-emu.org/
- **下载页面**: https://citra-emu.org/download/
- **GitHub 仓库**: https://github.com/citra-emu/citra
- **推荐版本**: 最新 Nightly 版本
- **文件大小**: 约 50-80 MB
- **许可证**: GPL-2.0（开源免费）

**注意**: Citra 官方已停止开发，建议下载最新的 Nightly 版本

**下载说明**:
- 选择 "Nightly" 版本（最新）
- 下载 Windows x64 版本
- 解压到 `E:\Emulators\Citra\`

---

#### Ryujinx（Switch 模拟器）推荐⭐

- **官方网站**: https://ryujinx.org/
- **下载页面**: https://ryujinx.org/download
- **GitHub 仓库**: https://github.com/Ryujinx/Ryujinx
- **推荐版本**: 最新稳定版
- **文件大小**: 约 100-200 MB
- **许可证**: MIT License（开源免费）

**下载说明**:
- **注意**: Ryujinx 官方项目已于 2024 年停止开发，官方网站可能无法访问
- 建议下载最后的稳定版本（可从第三方镜像或社区维护的 fork 版本获取）
- 下载 Windows 版本（.zip 文件）
- 解压到 `E:\Emulators\Ryujinx\`

**固件和密钥要求**:
- Switch 固件（约 300MB）
- prod.keys 和 title.keys 文件
- 放置在程序指定目录

**为什么选择 Ryujinx 而非 Yuzu**:
- 兼容性更稳定
- 内存占用更低（对 AMD 7735 更友好）
- 开源活跃维护

---

#### RPCS3（PS3 模拟器）

- **官方网站**: https://rpcs3.net/
- **下载页面**: https://rpcs3.net/download
- **GitHub 仓库**: https://github.com/RPCS3/rpcs3
- **推荐版本**: 最新版本
- **文件大小**: 约 250-400 MB（含固件）
- **许可证**: GPL-2.0（开源免费）

**下载说明**:
- 下载 Windows 版本
- 解压到 `E:\Emulators\RPCS3\`

**固件要求**:
- PS3 固件（约 200MB）
- 官网提供固件下载链接
- 首次启动时安装固件

**性能注意**:
- PS3 模拟器性能要求高
- AMD 7735 可以运行部分游戏
- 建议查看兼容性列表

---

#### DuckStation（PS1 模拟器）

- **官方网站**: https://www.duckstation.org/
- **GitHub 仓库**: https://github.com/stenzek/duckstation
- **下载页面**: https://github.com/stenzek/duckstation/releases
- **推荐版本**: 最新 Release 版本
- **文件大小**: 约 30-50 MB
- **许可证**: GPL-3.0（开源免费）

**下载说明**:
- 从 GitHub Releases 下载 Windows 版本
- 选择 `duckstation-windows-x64-release.zip`
- 解压到 `E:\Emulators\DuckStation\`

**BIOS 要求**:
- PS1 BIOS 文件（约 512KB）
- 放置在程序指定 BIOS 目录

---

#### Xenia（Xbox 360 模拟器）可选

- **官方网站**: https://xenia.jp/
- **GitHub 仓库**: https://github.com/xenia-project/xenia
- **下载页面**: https://github.com/xenia-project/xenia/releases
- **推荐版本**: 最新 Master 版本
- **文件大小**: 约 80-150 MB
- **许可证**: BSD-3-Clause（开源免费）

**下载说明**:
- 从 GitHub Releases 下载
- 选择 `xenia_master.zip`
- 解压到 `E:\Emulators\Xenia\`

**注意**: Xenia 仍处于实验阶段，兼容性有限

---

### 2.3 辅助工具

#### 手柄驱动（如需要）

**Xbox 手柄**:
- Windows 11 原生支持，无需驱动

**PlayStation DualSense/DualShock 4**:
- **DS4Windows**: https://ds4-windows.com/
- GitHub: https://github.com/Ryochan7/DS4Windows
- 下载最新版本
- 安装后可将 PS 手柄模拟为 Xbox 手柄

**8BitDo 手柄**:
- **8BitDo Ultimate Software**: https://support.8bitdo.com/
- 根据手柄型号下载对应工具
- 支持按键映射和固件升级

---

### 2.4 BIOS 和固件资源

**重要说明**:
- BIOS 和固件文件受版权保护
- 必须从您合法拥有的设备中提取
- 本文档不提供下载链接

**所需 BIOS/固件清单**:

| 模拟器 | 文件 | 大小 | 说明 |
|--------|------|------|------|
| RetroArch (GBA) | gba_bios.bin | 16 KB | GBA BIOS |
| RetroArch (PS1) | scph*.bin | 512 KB | PS1 BIOS（多个区域） |
| PCSX2 | SCPH-xxxxx.bin | 4 MB | PS2 BIOS |
| Ryujinx | prod.keys, title.keys | < 1 KB | Switch 密钥 |
| Ryujinx | 固件文件 | 300 MB | Switch 固件 |
| RPCS3 | PS3UPDAT.PUP | 200 MB | PS3 固件 |
| DuckStation | scph*.bin | 512 KB | PS1 BIOS |

**BIOS 放置位置**:
- 见各模拟器配置章节（第 6 节）

---

## 3. 系统架构设计

### 3.1 整体架构图

```
┌─────────────────────────────────────────────────────────┐
│                  Windows 11 开机启动                      │
└────────────────────┬────────────────────────────────────┘
                     │
                     ▼
          ┌──────────────────────┐
          │  启动脚本 (15s延迟)   │
          └──────────┬───────────┘
                     │
                     ▼
     ┌───────────────────────────────────┐
     │  Playnite 全屏模式（唯一入口）      │
     │  - 手柄导航                        │
     │  - 现代主题                        │
     │  - 自动元数据                      │
     └───────────┬───────────────────────┘
                 │
       ┌─────────┼─────────┬─────────┬──────────┐
       │         │         │         │          │
       ▼         ▼         ▼         ▼          ▼
    PC游戏   模拟器游戏  应用程序  Steam库   Epic库
       │         │         │
       │    ┌────┴────┐    │
       │    ▼         ▼    │
       │ RetroArch  独立   │
       │  (核心)   模拟器  │
       │    │         │    │
       │    ▼         ▼    ▼
       └────┴─────────┴────┘
              │
              ▼
      ┌───────────────┐
      │  游戏/应用启动 │
      └───────────────┘
```

### 3.2 数据流架构

```
用户操作（手柄/键鼠）
    ↓
Playnite 界面
    ↓
选择游戏/应用
    ↓
┌─────────────┬─────────────┬─────────────┐
│  PC 游戏    │ 模拟器游戏   │  应用程序    │
│  直接启动   │ 调用模拟器   │  直接启动    │
└─────────────┴─────────────┴─────────────┘
    ↓              ↓              ↓
游戏运行      模拟器 + ROM     应用界面
    ↓              ↓              ↓
    └──────────────┴──────────────┘
                   ↓
            退出返回 Playnite
                   ↓
            更新游戏时长/成就
```

### 3.3 存储架构

```
E:\（2T SATA SSD - 游戏专用）
├─ 热数据区（频繁访问）
│  ├─ Playnite\library\        # 游戏库数据库
│  ├─ Emulators\[各模拟器]\     # 模拟器程序
│  └─ Games\PC-Games\常玩\      # 常玩PC游戏
│
├─ 冷数据区（较少访问）
│  ├─ Games\ROMs\               # ROM 文件
│  └─ Games\PC-Games\其他\      # 其他PC游戏
│
└─ 缓存区（可重建）
   └─ Games\Game-Assets\        # 封面、截图

D:\（200G M.2 SSD - 系统和项目）
└─ Backups\Gaming\              # 游戏配置备份
   ├─ Playnite\                 # Playnite 数据库
   ├─ Saves\                    # 模拟器存档
   └─ Configs\                  # 配置文件
```

### 3.4 内存架构（64GB 总内存）

```
┌─────────────────────────────────────────────┐
│              64GB 总内存                     │
└──┬────────────────────────┬─────────────────┘
   │                        │
   │ 固定分配（配置限制）    │ 动态共享池
   │                        │
   ▼                        ▼
┌──────────────┐    ┌──────────────────────┐
│ Hyper-V: 4-8GB│    │ 约 36-52GB 可用      │
│              │    │                      │
│ WSL2: 20GB   │    │ - Windows 系统       │
│              │    │ - Playnite           │
└──────────────┘    │ - 游戏/模拟器进程    │
                    │ - 后台应用           │
                    │                      │
                    │ Windows 自动管理     │
                    └──────────────────────┘
```

**说明**:
- Hyper-V 和 WSL2 需要在配置文件中设置上限
- 其他应用共享系统内存池，按需动态分配
- 游戏高负载时可用内存充足（30GB+）

---

## 4. 目录结构设计

### 4.1 E 盘完整目录结构

```
E:\
├─ Games\                                    # 游戏根目录
│   │
│   ├─ PC-Games\                            # PC 游戏目录
│   │   ├─ Steam\                           # Steam 游戏库（可以是符号链接）
│   │   ├─ Epic\                            # Epic Games 游戏库
│   │   ├─ GOG\                             # GOG 游戏库
│   │   └─ Standalone\                      # 独立安装/绿色版游戏
│   │       ├─ [游戏名称1]\
│   │       ├─ [游戏名称2]\
│   │       └─ ...
│   │
│   ├─ ROMs\                                # 模拟器游戏 ROM
│   │   ├─ FC\                              # 红白机/Famicom
│   │   ├─ SFC\                             # 超级任天堂/Super Famicom
│   │   ├─ MD\                              # 世嘉 MD/Genesis
│   │   ├─ GB\                              # Game Boy
│   │   ├─ GBC\                             # Game Boy Color
│   │   ├─ GBA\                             # Game Boy Advance
│   │   ├─ N64\                             # Nintendo 64
│   │   ├─ PS1\                             # PlayStation 1
│   │   ├─ PS2\                             # PlayStation 2
│   │   │   ├─ [游戏1]\
│   │   │   └─ [游戏2]\
│   │   ├─ PSP\                             # PlayStation Portable
│   │   ├─ NGC\                             # GameCube
│   │   ├─ Wii\                             # Nintendo Wii
│   │   ├─ 3DS\                             # Nintendo 3DS
│   │   ├─ Switch\                          # Nintendo Switch
│   │   │   ├─ [游戏1].xci / .nsp
│   │   │   └─ [游戏2].xci / .nsp
│   │   ├─ PS3\                             # PlayStation 3
│   │   │   ├─ [游戏1]\
│   │   │   └─ [游戏2]\
│   │   ├─ Arcade\                          # 街机游戏
│   │   └─ [其他平台]\
│   │
│   └─ Game-Assets\                         # 游戏资产（可重建）
│       ├─ Covers\                          # 游戏封面图
│       │   ├─ PC\
│       │   └─ [各平台]\
│       ├─ Screenshots\                     # 游戏截图
│       ├─ Backgrounds\                     # 背景图
│       └─ Metadata\                        # 元数据缓存
│
├─ Emulators\                               # 模拟器安装目录
│   │
│   ├─ RetroArch\                           # RetroArch 主目录
│   │   ├─ retroarch.exe                    # 主程序
│   │   ├─ cores\                           # 核心目录
│   │   │   ├─ mesen_libretro.dll          # FC/NES 核心
│   │   │   ├─ snes9x_libretro.dll         # SNES 核心
│   │   │   ├─ genesis_plus_gx_libretro.dll# MD 核心
│   │   │   ├─ mgba_libretro.dll           # GBA 核心
│   │   │   ├─ mupen64plus_next_libretro.dll# N64 核心
│   │   │   ├─ beetle_psx_hw_libretro.dll  # PS1 核心
│   │   │   └─ ppsspp_libretro.dll         # PSP 核心
│   │   ├─ system\                          # BIOS 目录
│   │   │   ├─ gba_bios.bin
│   │   │   ├─ scph5501.bin                # PS1 BIOS
│   │   │   └─ [其他 BIOS]
│   │   ├─ saves\                           # 存档目录
│   │   ├─ states\                          # 即时存档
│   │   ├─ screenshots\                     # 截图
│   │   └─ config\                          # 配置文件
│   │
│   ├─ PCSX2\                               # PS2 模拟器
│   │   ├─ pcsx2.exe
│   │   ├─ bios\                            # PS2 BIOS
│   │   ├─ memcards\                        # 记忆卡
│   │   ├─ sstates\                         # 即时存档
│   │   └─ inis\                            # 配置文件
│   │
│   ├─ Dolphin\                             # NGC/Wii 模拟器
│   │   ├─ Dolphin.exe
│   │   ├─ User\
│   │   │   ├─ Saves\                       # 存档
│   │   │   ├─ StateSaves\                  # 即时存档
│   │   │   ├─ Config\                      # 配置
│   │   │   └─ GameSettings\                # 游戏特定设置
│   │   └─ Sys\
│   │
│   ├─ Citra\                               # 3DS 模拟器
│   │   ├─ citra-qt.exe
│   │   └─ user\
│   │       ├─ sdmc\                        # 虚拟 SD 卡
│   │       ├─ nand\                        # 虚拟 NAND
│   │       └─ states\                      # 即时存档
│   │
│   ├─ Ryujinx\                             # Switch 模拟器
│   │   ├─ Ryujinx.exe
│   │   ├─ bis\
│   │   │   └─ user\
│   │   │       └─ save\                    # 存档目录
│   │   ├─ system\                          # 固件和密钥
│   │   │   ├─ prod.keys
│   │   │   └─ title.keys
│   │   └─ profiles\                        # 用户配置
│   │
│   ├─ RPCS3\                               # PS3 模拟器
│   │   ├─ rpcs3.exe
│   │   ├─ dev_hdd0\                        # 虚拟硬盘
│   │   │   └─ home\
│   │   │       └─ [用户ID]\
│   │   │           └─ savedata\            # 存档
│   │   └─ dev_flash\                       # 系统文件
│   │
│   ├─ DuckStation\                         # PS1 模拟器
│   │   ├─ duckstation-qt-x64-ReleaseLTCG.exe
│   │   ├─ bios\                            # PS1 BIOS
│   │   ├─ memcards\                        # 记忆卡
│   │   └─ savestates\                      # 即时存档
│   │
│   └─ Xenia\                               # Xbox 360 模拟器（可选）
│       ├─ xenia.exe
│       └─ content\
│
└─ Playnite\                                # Playnite 便携版
    ├─ Playnite.DesktopApp.exe             # 桌面模式
    ├─ Playnite.FullscreenApp.exe          # 全屏模式
    │
    ├─ library\                             # 游戏库数据库（重要）
    │   ├─ games.db                         # 游戏数据库
    │   ├─ platforms.db                     # 平台数据
    │   └─ files\                           # 附加文件
    │
    ├─ themes\                              # 主题目录
    │   ├─ Fullscreen\                      # 全屏模式主题
    │   │   ├─ Strata\                      # Strata 主题（推荐）
    │   │   ├─ Harmony\                     # Harmony 主题
    │   │   └─ [其他主题]\
    │   └─ Desktop\                         # 桌面模式主题
    │
    ├─ Extensions\                          # 插件目录
    │   ├─ [插件1]\
    │   └─ [插件2]\
    │
    ├─ ExtensionsData\                      # 插件数据
    │   ├─ [插件数据1]\
    │   └─ [插件数据2]\
    │
    ├─ cache\                               # 缓存目录
    │
    └─ backups\                             # 自动备份
        ├─ games_[日期].db
        └─ ...
```

### 4.2 D 盘备份目录结构

```
D:\
└─ Backups\                                 # 备份根目录
    └─ Gaming\                              # 游戏备份
        │
        ├─ Playnite\                        # Playnite 备份
        │   ├─ library\                     # 数据库备份
        │   │   └─ [日期备份]\
        │   └─ configs\                     # 配置备份
        │
        ├─ Saves\                           # 模拟器存档备份
        │   ├─ RetroArch\
        │   │   └─ saves\
        │   ├─ PCSX2\
        │   │   └─ memcards\
        │   ├─ Dolphin\
        │   │   └─ Saves\
        │   ├─ Ryujinx\
        │   │   └─ save\
        │   └─ [其他模拟器]\
        │
        ├─ Configs\                         # 配置文件备份
        │   ├─ RetroArch\
        │   │   └─ retroarch.cfg
        │   ├─ PCSX2\
        │   │   └─ inis\
        │   └─ [其他模拟器]\
        │
        └─ BIOS\                            # BIOS 备份
            ├─ RetroArch\
            ├─ PCSX2\
            └─ [其他模拟器]\
```

### 4.3 目录权限和注意事项

**权限要求**:
- 所有目录使用 Windows 标准用户权限
- 无需管理员权限
- 确保有读写权限

**注意事项**:
1. **ROMs 目录**: 按平台分类，便于管理和扫描
2. **存档目录**: 定期备份到 D 盘
3. **BIOS 目录**: 妥善保管，备份到 D 盘
4. **Game-Assets**: 可重建数据，不必备份（网络允许时）
5. **符号链接**: Steam 库可使用符号链接指向原安装位置

**磁盘空间预估**:
- 模拟器程序: 2.5-3.5 GB
- Playnite: 500 MB - 1 GB（含插件和主题）
- BIOS 文件: 500 MB - 1 GB
- PC 游戏: 根据安装数量（10-500 GB）
- ROMs: 根据平台和数量（10-500 GB）
- 游戏资产: 5-20 GB（可重建）
- **总预估**: 30-1000 GB（取决于游戏数量）

**空间管理建议**:
- 始终保留 200 GB 可用空间
- 定期清理不玩的游戏
- 大型游戏（Switch/PS3）优先删除

---

## 5. Playnite 配置方案

### 5.1 首次安装和设置

#### 5.1.1 安装步骤

1. **下载 Playnite 便携版**
   - 访问 https://playnite.link/download.html
   - 选择 "Portable" 版本下载
   - 解压到 `E:\Playnite\`

2. **首次启动**
   ```
   运行: E:\Playnite\Playnite.DesktopApp.exe
   ```

3. **初始配置向导**
   - 选择语言：简体中文或英文
   - 跳过库集成（稍后配置）
   - 完成向导

4. **基础设置**
   - 进入 `Settings` (F4)
   - 设置数据存储位置（默认即可）
   - 配置全屏模式为默认启动

#### 5.1.2 关键设置

**通用设置 (General)**:
```yaml
语言: 简体中文（或 English）
启动模式: 全屏模式 (Fullscreen mode)
启动时最小化: 禁用
更新检查: 启用
统计追踪: 启用（记录游戏时长）
```

**外观设置 (Appearance)**:
```yaml
桌面模式主题: 默认或自选
全屏模式主题: Strata（需要先安装）
图标: 默认
字体: 默认
```

**输入设置 (Input)**:
```yaml
启用手柄支持: ✓
手柄指南按钮: 打开快速菜单
手柄热键:
  - Guide + Start: 关闭游戏
  - Guide + Back: 切换桌面模式
  - Guide + Y: 搜索

键盘快捷键:
  - F11: 切换全屏/窗口
  - Ctrl+Q: 退出 Playnite
  - Ctrl+F: 搜索
```

---

### 5.2 库整合配置

#### 5.2.1 Steam 库整合

**步骤**:
1. 进入 `Settings` > `Integrations` > `Steam`
2. 勾选 "Enable Steam library integration"
3. 配置 Steam 安装路径（自动检测）
4. 选择导入选项：
   - ✓ 导入已安装游戏
   - ✓ 导入未安装游戏
   - ✓ 导入游戏元数据
5. 点击 "Authenticate" 登录 Steam 账号（可选）
6. 点击 "Import library"

**元数据设置**:
- ✓ 下载游戏图标
- ✓ 下载封面图
- ✓ 下载背景图
- ✓ 同步游戏时长

#### 5.2.2 Epic Games 库整合

**步骤**:
1. 安装 Epic Library 插件（见 5.3 节）
2. 进入 `Settings` > `Integrations` > `Epic`
3. 勾选 "Enable Epic library integration"
4. 登录 Epic Games 账号
5. 导入游戏库

#### 5.2.3 其他启动器整合

**GOG Galaxy**:
- 安装 GOG 插件
- 导入 GOG 游戏库

**Xbox Game Pass**:
- 安装 Xbox Game Pass 插件
- 导入订阅游戏

**手动添加游戏**（独立安装/绿色版）:
1. 点击 `Add Game` > `Manually`
2. 填写游戏信息：
   - 名称：游戏名称
   - 安装目录：游戏根目录
   - 可执行文件：游戏主程序（.exe）
   - 平台：PC（Windows）
3. 手动下载封面或使用自动刮削

---

### 5.3 插件和扩展

#### 5.3.1 必装插件

**IGDB Metadata Provider** (必装):
- **功能**: 从 IGDB 数据库获取游戏元数据
- **安装**: `Add-ons` > `Browse` > 搜索 "IGDB"
- **配置**:
  - 注册 IGDB API 密钥（免费）
  - 访问 https://www.igdb.com/api
  - 在插件设置中输入 API 密钥

**Universal Steam Metadata** (必装):
- **功能**: 增强 Steam 游戏元数据
- **安装**: 从插件商店搜索 "Universal Steam"
- **配置**: 默认即可

**Epic Library** (必装):
- **功能**: Epic Games 库整合
- **安装**: 从插件商店搜索 "Epic"
- **配置**: 登录 Epic 账号

**Emulators Library** (强烈推荐):
- **功能**: 简化模拟器游戏导入
- **安装**: 搜索 "Emulators Library"
- **配置**: 见 5.5 节

#### 5.3.2 推荐插件

**Controller Support**:
- **功能**: 增强手柄支持和按键映射
- **安装**: 搜索 "Controller"

**RetroAchievements**:
- **功能**: 复古游戏成就系统
- **安装**: 搜索 "RetroAchievements"
- **配置**: 注册账号 https://retroachievements.org/

**GameActivity**:
- **功能**: 游戏活动追踪和统计
- **安装**: 搜索 "GameActivity"

**SuccessStory**:
- **功能**: 成就展示和追踪
- **安装**: 搜索 "SuccessStory"

**Extensions Updater**:
- **功能**: 自动更新插件
- **安装**: 搜索 "Extensions Updater"

#### 5.3.3 插件配置示例

**IGDB Metadata 配置**:
```yaml
API 设置:
  Client ID: [您的 API 密钥]
  Client Secret: [您的 API 密钥]

元数据选项:
  ✓ 下载封面
  ✓ 下载背景
  ✓ 下载图标
  ✓ 下载截图
  ✓ 导入游戏描述
  ✓ 导入发行日期
  ✓ 导入开发商/发行商

图片质量: 高 (1080p)
语言: 简体中文（或 English）
```

---

### 5.4 主题配置

#### 5.4.1 Strata Fullscreen 主题（推荐）⭐

**安装步骤**:
1. 进入 `Add-ons` > `Browse` > `Themes Fullscreen`
2. 搜索 "Strata"
3. 点击 "Install"
4. 重启 Playnite 全屏模式

**主题特点**:
- Xbox Series X/S 风格
- 大图标网格布局
- 深色主题，突出游戏封面
- 流畅动画效果
- 手柄导航优化

**自定义选项**:
```yaml
布局:
  游戏展示: 网格视图 (Grid)
  封面尺寸: 大 (Large)
  每行数量: 4-6 个（根据屏幕分辨率）

颜色:
  主色调: 深蓝/深灰（可自定义）
  强调色: 亮蓝（可自定义）

信息显示:
  ✓ 显示游戏标题
  ✓ 显示平台图标
  ✓ 显示游戏时长
  □ 显示最后游玩日期

动画:
  过渡效果: 启用
  速度: 中等
```

#### 5.4.2 Harmony 主题（备选）

**特点**:
- PlayStation 5 风格
- 横向卡片布局
- 动态背景支持
- 现代扁平化设计

**安装**: 同 Strata，搜索 "Harmony"

#### 5.4.3 ModernUI Fullscreen 主题（备选）

**特点**:
- Windows Modern Design
- 高度可定制
- 多种布局选项
- 轻量级

**安装**: 同上，搜索 "ModernUI"

---

### 5.5 模拟器游戏导入

#### 5.5.1 自动扫描配置

**使用 Emulators Library 插件**:

1. **安装插件**:
   - `Add-ons` > `Browse` > 搜索 "Emulators Library"
   - 安装并重启

2. **配置模拟器**:
   - 进入插件设置
   - 添加模拟器：

   **RetroArch 配置**:
   ```yaml
   名称: RetroArch
   可执行文件: E:\Emulators\RetroArch\retroarch.exe
   工作目录: E:\Emulators\RetroArch\

   平台映射:
     FC/NES:
       核心: mesen_libretro.dll
       ROM路径: E:\Games\ROMs\FC\
     SFC/SNES:
       核心: snes9x_libretro.dll
       ROM路径: E:\Games\ROMs\SFC\
     MD/Genesis:
       核心: genesis_plus_gx_libretro.dll
       ROM路径: E:\Games\ROMs\MD\
     GBA:
       核心: mgba_libretro.dll
       ROM路径: E:\Games\ROMs\GBA\
     N64:
       核心: mupen64plus_next_libretro.dll
       ROM路径: E:\Games\ROMs\N64\
     PS1:
       核心: beetle_psx_hw_libretro.dll
       ROM路径: E:\Games\ROMs\PS1\
     PSP:
       核心: ppsspp_libretro.dll
       ROM路径: E:\Games\ROMs\PSP\
   ```

   **PCSX2 配置**:
   ```yaml
   名称: PCSX2
   可执行文件: E:\Emulators\PCSX2\pcsx2.exe
   工作目录: E:\Emulators\PCSX2\
   ROM路径: E:\Games\ROMs\PS2\
   ROM扩展名: .iso, .bin, .img, .chd
   启动参数: --fullscreen --nogui "{ImagePath}"
   ```

   **Dolphin 配置**:
   ```yaml
   名称: Dolphin
   可执行文件: E:\Emulators\Dolphin\Dolphin.exe
   工作目录: E:\Emulators\Dolphin\
   ROM路径:
     - E:\Games\ROMs\NGC\
     - E:\Games\ROMs\Wii\
   ROM扩展名: .iso, .gcm, .wbfs, .ciso, .rvz
   启动参数: --batch --exec="{ImagePath}"
   ```

   **Ryujinx 配置**:
   ```yaml
   名称: Ryujinx
   可执行文件: E:\Emulators\Ryujinx\Ryujinx.exe
   工作目录: E:\Emulators\Ryujinx\
   ROM路径: E:\Games\ROMs\Switch\
   ROM扩展名: .nsp, .xci, .nca
   启动参数: "{ImagePath}"
   ```

3. **扫描和导入**:
   - 点击 `Library` > `Update Game Library`
   - 选择要扫描的平台
   - 等待扫描完成
   - 插件会自动添加游戏到库中

#### 5.5.2 手动添加模拟器游戏

**步骤**:
1. 点击 `Add Game` > `Manually`
2. 填写信息：
   ```yaml
   名称: [游戏名称]
   平台: [选择对应模拟器平台，如 Nintendo 64]
   ROM路径: E:\Games\ROMs\[平台]\[游戏文件]
   启动动作:
     类型: 模拟器
     模拟器: [选择对应模拟器，如 RetroArch]
     附加参数: [如需要]
   ```
3. 点击 "Download Metadata" 自动获取封面和信息
4. 保存

#### 5.5.3 元数据刮削

**自动刮削**:
- 选中游戏 > 右键 > `Edit` > `Download Metadata`
- 选择数据源（推荐 IGDB）
- 选择正确的游戏匹配
- 下载封面、背景、截图

**手动编辑**:
- 如果自动匹配不准确，手动编辑游戏信息
- 上传自定义封面和背景

---

### 5.6 应用程序整合

#### 5.6.1 添加浏览器

**Microsoft Edge 配置**:
```yaml
名称: 浏览器 / Web Browser
平台: PC (Windows)
图标: [使用 Edge 图标或自定义]
安装目录: C:\Program Files (x86)\Microsoft\Edge\Application\
可执行文件: msedge.exe
启动参数: --kiosk --start-fullscreen

类别: 应用程序
标签: 娱乐, 工具
```

**可选启动参数**:
- `--app=https://www.bilibili.com`: 直接打开哔哩哔哩
- `--new-window`: 新窗口模式
- 留空: 正常浏览器模式

#### 5.6.2 添加音乐应用

**网易云音乐配置**:
```yaml
名称: 网易云音乐
平台: PC (Windows)
图标: [使用网易云图标]
安装目录: [网易云安装路径，如 C:\Program Files\Netease\CloudMusic\]
可执行文件: cloudmusic.exe

类别: 应用程序
标签: 音乐, 娱乐
```

#### 5.6.3 添加视频应用

**哔哩哔哩客户端配置**:
```yaml
名称: 哔哩哔哩
平台: PC (Windows)
图标: [使用B站图标]
安装目录: [哔哩哔哩安装路径]
可执行文件: 哔哩哔哩.exe

类别: 应用程序
标签: 视频, 娱乐
```

#### 5.6.4 添加云盘应用

**极空间配置**:
```yaml
名称: 极空间
平台: PC (Windows)
图标: [使用极空间图标]
安装目录: [极空间安装路径]
可执行文件: JiKongJian.exe

类别: 应用程序
标签: 工具, 存储
```

#### 5.6.5 分类和组织

**创建自定义类别**:
1. 进入 `Settings` > `Library` > `Categories`
2. 添加新类别：
   - 游戏类别：PC游戏、模拟器游戏
   - 应用类别：娱乐、工具、媒体

**应用筛选器**:
- 在全屏模式中：
- 使用手柄 LB/RB 切换类别
- 创建筛选器：
  - 仅显示已安装
  - 按平台筛选
  - 按类别筛选
  - 按标签筛选

---

### 5.7 自动启动配置

#### 5.7.1 创建启动脚本

**脚本位置**: `C:\Users\[用户名]\startup-playnite.bat`

**脚本内容**:
```batch
@echo off
:: Playnite 自动启动脚本
:: 延迟启动，确保系统服务完全加载

:: 等待 15 秒
echo 等待系统启动完成...
timeout /t 15 /nobreak >nul

:: 启动 Playnite 全屏模式
echo 启动 Playnite 全屏模式...
start "" "E:\Playnite\Playnite.FullscreenApp.exe"

:: 可选：关闭资源管理器（纯游戏机模式）
:: 注意：这会隐藏桌面和任务栏
:: taskkill /f /im explorer.exe

exit
```

**高级版本（带日志）**:
```batch
@echo off
setlocal enabledelayedexpansion

:: 设置日志文件
set LOGFILE=C:\Users\%USERNAME%\playnite-startup.log

:: 记录启动时间
echo [%date% %time%] 开始启动 Playnite >> "%LOGFILE%"

:: 等待系统就绪
echo 等待系统启动... >> "%LOGFILE%"
timeout /t 15 /nobreak >nul

:: 检查 Playnite 是否已运行
tasklist /FI "IMAGENAME eq Playnite.FullscreenApp.exe" 2>NUL | find /I /N "Playnite.FullscreenApp.exe">NUL
if "%ERRORLEVEL%"=="0" (
    echo [%date% %time%] Playnite 已在运行 >> "%LOGFILE%"
    exit
)

:: 启动 Playnite
echo [%date% %time%] 启动 Playnite 全屏模式 >> "%LOGFILE%"
start "" "E:\Playnite\Playnite.FullscreenApp.exe"

:: 验证启动
timeout /t 5 /nobreak >nul
tasklist /FI "IMAGENAME eq Playnite.FullscreenApp.exe" 2>NUL | find /I /N "Playnite.FullscreenApp.exe">NUL
if "%ERRORLEVEL%"=="0" (
    echo [%date% %time%] Playnite 启动成功 >> "%LOGFILE%"
) else (
    echo [%date% %time%] Playnite 启动失败 >> "%LOGFILE%"
)

exit
```

#### 5.7.2 添加到 Windows 启动项

**方法 1：shell:startup 文件夹**（简单）:
1. 按 `Win + R`
2. 输入 `shell:startup` 并回车
3. 将 `startup-playnite.bat` 复制到此文件夹
4. 或创建快捷方式

**方法 2：任务计划程序**（推荐）:
1. 打开"任务计划程序"（Task Scheduler）
2. 创建基本任务：
   ```yaml
   名称: Playnite 自动启动
   描述: 开机自动启动 Playnite 全屏模式

   触发器:
     类型: 用户登录时
     延迟任务: 15 秒

   操作:
     程序/脚本: C:\Users\[用户名]\startup-playnite.bat

   条件:
     □ 只有在计算机使用交流电源时启动
     ✓ 如果任务失败，每隔 1 分钟重新启动

   设置:
     ✓ 允许按需运行任务
     □ 如果任务已运行，不启动新实例
   ```

3. 保存任务

#### 5.7.3 退出机制

**方案 1：添加"桌面模式"快捷方式到 Playnite**:
```yaml
名称: 退出到桌面
可执行文件: C:\Windows\explorer.exe
参数: 无
图标: Windows 图标
类别: 系统
```

**方案 2：重启 Explorer 脚本**（如果关闭了 explorer.exe）:
创建 `restart-explorer.bat`:
```batch
@echo off
taskkill /f /im Playnite.FullscreenApp.exe
start explorer.exe
exit
```

添加到 Playnite 作为"退出到桌面"应用

**方案 3：手柄快捷键**:
- 配置 `Guide + Select` 组合键退出 Playnite
- 在 Playnite 设置中配置

---

### 5.8 界面优化技巧

#### 5.8.1 封面优化

**自动下载高质量封面**:
- 使用 IGDB Metadata 插件
- 设置图片质量为"高"或"原始"
- 优先选择"封面"类型

**手动替换封面**:
1. 右键游戏 > `Edit` > `Images`
2. 点击封面区域
3. 选择本地图片或从 URL 导入
4. 推荐尺寸：600x900 像素（2:3 比例）

#### 5.8.2 背景和横幅

**动态背景**:
- 某些主题支持游戏背景自动切换
- 下载游戏背景图（通过元数据插件）

**自定义横幅**:
- 尺寸推荐：1920x600 像素
- 放置在游戏编辑界面的"背景"栏

#### 5.8.3 游戏分组

**按平台分组**:
- 全屏模式中使用筛选器
- LB/RB 切换平台分类

**自定义标签**:
- 创建标签：单人、多人、RPG、动作等
- 批量编辑游戏添加标签
- 使用标签筛选游戏

#### 5.8.4 隐藏和收藏

**隐藏游戏**:
- 不想显示的游戏：右键 > `Hide`
- 隐藏的游戏不会在库中显示

**收藏游戏**:
- 常玩游戏：右键 > `Add to Favorites`
- 创建"收藏"筛选器快速访问

---

## 6. 模拟器配置方案

### 6.1 模拟器安装顺序

**推荐安装顺序**（按优先级）:

1. **RetroArch**（核心多平台） - 必装
2. **PCSX2**（PS2） - 必装
3. **Dolphin**（NGC/Wii） - 必装
4. **Ryujinx**（Switch） - 强烈推荐
5. **DuckStation**（PS1） - 推荐
6. **Citra**（3DS） - 推荐
7. **RPCS3**（PS3） - 可选
8. **Xenia**（Xbox 360） - 可选

---

### 6.2 RetroArch 详细配置

#### 6.2.1 安装和初始设置

**下载和安装**:
1. 访问 https://www.retroarch.com/?page=platforms
2. 下载 Windows x64 版本
3. 解压到 `E:\Emulators\RetroArch\`
4. 运行 `retroarch.exe`

**首次配置向导**:
1. 选择语言：简体中文
2. 设置驱动程序：
   - 视频驱动：Vulkan（AMD GPU 最佳）
   - 音频驱动：XAudio
   - 输入驱动：DInput 或 XInput
3. 设置存储路径（默认即可）

#### 6.2.2 核心安装

**推荐核心列表**:

| 平台 | 核心名称 | 说明 |
|------|---------|------|
| FC/NES | Mesen | 精准度最高 |
| SFC/SNES | Snes9x | 性能与精度平衡 |
| MD/Genesis | Genesis Plus GX | 兼容性最好 |
| GB/GBC | Gambatte | 精准度高 |
| GBA | mGBA | 功能全面，性能好 |
| N64 | Mupen64Plus-Next | 兼容性较好 |
| PS1 | Beetle PSX HW | 硬件加速，画质增强 |
| PSP | PPSSPP | 性能优秀 |
| 街机 | FinalBurn Neo | 支持大量街机游戏 |

**安装核心步骤**:
1. 启动 RetroArch
2. 进入 `Main Menu` > `Online Updater` > `Core Downloader`
3. 滚动列表找到推荐核心
4. 点击下载安装
5. 重复安装所有需要的核心

#### 6.2.3 BIOS 配置

**BIOS 放置位置**: `E:\Emulators\RetroArch\system\`

**所需 BIOS 文件**:

| 平台 | 文件名 | 大小 | 备注 |
|------|--------|------|------|
| GBA | gba_bios.bin | 16 KB | 可选，提升兼容性 |
| PS1 | scph5500.bin | 512 KB | 日版 BIOS |
| PS1 | scph5501.bin | 512 KB | 美版 BIOS（推荐） |
| PS1 | scph5502.bin | 512 KB | 欧版 BIOS |

**验证 BIOS**:
1. 进入 `Settings` > `Directory` > `System/BIOS`
2. 确认路径为 `E:\Emulators\RetroArch\system\`
3. 进入 `Information` > `System Information`
4. 检查 BIOS 是否识别

#### 6.2.4 视频设置

**进入设置**: `Settings` > `Video`

**推荐配置**（AMD 7735 集显）:
```yaml
视频驱动: Vulkan

显示设置:
  全屏: 启用
  全屏模式: 独占全屏
  窗口宽度: 1920
  窗口高度: 1080
  刷新率: 60 Hz
  垂直同步: 启用
  最大交换间隔: 1

缩放设置:
  整数倍缩放: 禁用
  保持纵横比: 启用
  裁剪超扫描: 自动

性能设置:
  线程视频: 启用
  GPU 截图: 启用
  视频过滤器: 线性（或选择着色器）
```

**着色器（Shaders）配置**（可选，复古风格）:
1. 进入 `Quick Menu` > `Shaders` > `Load Shader Preset`
2. 推荐预设：
   - `crt/crt-easymode`: 简单 CRT 效果
   - `crt/crt-royale`: 高质量 CRT 效果（性能要求高）
   - `hqx/hq4x`: 像素艺术增强
   - `xbr/xbr-lv2`: 平滑缩放

#### 6.2.5 音频设置

**进入设置**: `Settings` > `Audio`

**推荐配置**:
```yaml
音频驱动: XAudio

音频设置:
  启用音频: 启用
  音频延迟: 64 ms（可根据体验调整）
  最大时间差: 0.06
  音量: 0 dB（默认）
  启用音频DSP插件: 禁用

同步设置:
  音频同步: 启用
  音频速率控制增量: 0.005
```

#### 6.2.6 输入设置

**手柄配置**:
1. 进入 `Settings` > `Input` > `Port 1 Controls`
2. 选择设备类型：RetroPad（推荐）
3. 映射按键：
   ```yaml
   Xbox 手柄映射:
     A → B (确认)
     B → A (返回)
     X → Y
     Y → X
     LB → L
     RB → R
     LT → L2
     RT → R2
     Start → Start
     Back → Select
   ```
4. 保存配置为 `autoconfig` 文件

**快捷键配置**:
进入 `Settings` > `Input` > `Hotkeys`

推荐快捷键：
```yaml
菜单切换: F1
快速存档: F2
快速读档: F4
即时存档槽+: F6
即时存档槽-: F7
快进: Space
倒带: R
暂停: P
截图: F8
退出模拟器: Esc
```

#### 6.2.7 存档设置

**进入设置**: `Settings` > `Saving`

**推荐配置**:
```yaml
即时存档设置:
  即时存档目录: E:\Emulators\RetroArch\states\
  启用自动存档: 启用
  存档间隔: 10 秒
  启用即时存档压缩: 启用

游戏存档设置:
  SRAM目录: E:\Emulators\RetroArch\saves\
  SRAM自动保存间隔: 10 秒
```

**备份重要**：定期备份 `saves` 和 `states` 目录到 D 盘

#### 6.2.8 每个平台的核心配置

**FC/NES (Mesen)**:
```yaml
系统: FC / NES
核心: mesen_libretro.dll
ROM格式: .nes, .fds, .unf
BIOS: 无需（内置）

核心选项:
  过扫描: 禁用
  调色板: Smooth（或其他）
  纵横比: Auto
```

**SFC/SNES (Snes9x)**:
```yaml
系统: SFC / SNES
核心: snes9x_libretro.dll
ROM格式: .smc, .sfc, .fig, .swc
BIOS: 无需

核心选项:
  超级FX时钟速度: 100%
  减少闪烁: 启用
```

**MD/Genesis (Genesis Plus GX)**:
```yaml
系统: MD / Genesis / Sega CD
核心: genesis_plus_gx_libretro.dll
ROM格式: .md, .gen, .smd, .bin, .cue (Sega CD)
BIOS (Sega CD):
  bios_CD_U.bin (美版)
  bios_CD_J.bin (日版)
  bios_CD_E.bin (欧版)

核心选项:
  系统区域: 自动
  音频过滤: 启用
```

**GBA (mGBA)**:
```yaml
系统: Game Boy Advance
核心: mgba_libretro.dll
ROM格式: .gba, .agb
BIOS: gba_bios.bin（可选）

核心选项:
  跳过BIOS: 否（如有 BIOS）
  色彩校正: GBA
  空闲循环移除: 启用（提升性能）
```

**N64 (Mupen64Plus-Next)**:
```yaml
系统: Nintendo 64
核心: mupen64plus_next_libretro.dll
ROM格式: .n64, .v64, .z64
BIOS: 无需

核心选项:
  渲染器: parallel (Vulkan)
  分辨率: 1920x1080 (2x)
  抗锯齿: 启用
  纹理过滤: 三线性过滤
```

**PS1 (Beetle PSX HW)**:
```yaml
系统: PlayStation 1
核心: beetle_psx_hw_libretro.dll
ROM格式: .cue, .bin, .img, .chd
BIOS: scph5501.bin（必需）

核心选项:
  渲染器: Vulkan
  内部分辨率: 4x (1920x1440)
  纹理过滤: xBR
  PGXP几何精度: 启用
  PGXP纹理校正: 启用
  抖动模式: 1x (Native)
```

**PSP (PPSSPP)**:
```yaml
系统: PlayStation Portable
核心: ppsspp_libretro.dll
ROM格式: .iso, .cso, .pbp
BIOS: 无需

核心选项:
  渲染器: Vulkan
  内部分辨率: 2x-3x
  纹理过滤: Linear
  跳帧: 禁用
```

---

### 6.3 PCSX2（PS2 模拟器）配置

#### 6.3.1 安装和初始设置

**下载和安装**:
1. 访问 https://pcsx2.net/downloads/
2. 下载最新稳定版（1.7.x 或 2.0+）
3. 安装到 `E:\Emulators\PCSX2\`
4. 运行 `pcsx2.exe`

**首次配置向导**:
1. 选择语言：简体中文
2. 设置 BIOS：
   - BIOS 文件夹：`E:\Emulators\PCSX2\bios\`
   - 选择 BIOS 版本（推荐日版或美版）
3. 设置文件夹：
   - 文档：默认
   - 存档：`E:\Emulators\PCSX2\memcards\`
   - 即时存档：`E:\Emulators\PCSX2\sstates\`

#### 6.3.2 BIOS 配置

**BIOS 放置位置**: `E:\Emulators\PCSX2\bios\`

**所需文件**: PS2 BIOS（约 4MB，文件名如 `SCPH-39001.bin`）

**验证 BIOS**:
1. 进入 `Config` > `BIOS Selector`
2. 检查 BIOS 列表中是否有识别的 BIOS
3. 选择一个 BIOS 作为默认

#### 6.3.3 图形设置

**进入设置**: `Config` > `Graphics Settings`

**推荐配置**（AMD 7735 集显）:
```yaml
渲染器:
  Renderer: Vulkan
  Adapter: AMD 集显
  Internal Resolution: 2x Native (1280x896) 或 3x
  Texture Filtering: Bilinear (PS2)
  Anisotropic Filtering: 16x

显示设置:
  Aspect Ratio: 16:9 Widescreen
  FMV Aspect Ratio: Off
  V-Sync: On
  Integer Scaling: Off

增强设置:
  Mipmapping: Automatic
  CRC Hack Level: Automatic
  Blending Accuracy: Basic
  Texture Preloading: Full

高级设置:
  Hardware Download Mode: Accurate
  GPU Palette Conversion: Off
  Manual Hardware Settings: Off
```

**性能调优**（如果卡顿）:
- 降低 Internal Resolution 到 1x 或 1.5x
- 降低 Blending Accuracy 到 Minimum
- 关闭 Anisotropic Filtering

#### 6.3.4 音频和输入设置

**音频设置**: `Config` > `Audio Settings`
```yaml
Output Module: Cubeb
Latency: 100-200ms
Volume: 100%
同步模式: TimeStretch
```

**输入设置**: `Config` > `Controllers`
```yaml
Controller 1:
  Type: DualShock 2
  Mapping: 使用 "Automatic Mapping" 自动映射手柄
```

#### 6.3.5 游戏特定设置

某些游戏可能需要特殊设置：
1. 右键游戏 > `Properties`
2. 调整特定游戏的 CRC Hack 或图形设置
3. 查看 PCSX2 兼容性列表获取推荐设置

---

### 6.4 Dolphin（NGC/Wii 模拟器）配置

#### 6.4.1 安装和初始设置

**下载和安装**:
1. 访问 https://dolphin-emu.org/download/
2. 下载最新稳定版
3. 解压到 `E:\Emulators\Dolphin\`
4. 运行 `Dolphin.exe`

**首次配置**:
1. 设置路径：`Config` > `Paths`
   - 添加 ROM 路径：`E:\Games\ROMs\NGC\` 和 `E:\Games\ROMs\Wii\`
2. 设置语言：简体中文

#### 6.4.2 图形设置

**进入设置**: `Graphics` 或 `Options` > `Graphics Settings`

**推荐配置**（AMD 7735）:
```yaml
通用设置:
  Backend: Vulkan
  Adapter: AMD 集显
  Fullscreen Resolution: Auto
  V-Sync: On

增强设置:
  Internal Resolution: 3x Native (1920x1584) 或 4x
  Anisotropic Filtering: 8x 或 16x
  Anti-Aliasing: SSAA（或 None 如果性能不足）
  Post-Processing Effect: None（或选择喜欢的效果）

Hacks:
  Skip EFB Access from CPU: On（提升性能）
  Ignore Format Changes: Off
  Store EFB Copies to Texture Only: On
  Texture Cache: Fast

高级设置:
  Enable Progressive Scan: On
  Backend Multithreading: On
  Shader Compilation: Specialized（推荐）或 Hybrid
```

#### 6.4.3 音频和控制器设置

**音频设置**: `Options` > `Audio Settings`
```yaml
DSP Emulation Engine: DSP HLE（推荐）
Backend: Cubeb
Volume: 100%
```

**控制器设置**: `Controllers`

**NGC 手柄配置**:
```yaml
Port 1: Standard Controller
Device: [您的手柄设备]
Mapping: 使用 "AutoMap" 自动映射
```

**Wii 遥控器配置**:
```yaml
Wii Remote 1: Emulated Wii Remote
Extension: Classic Controller（推荐）或 Nunchuk
Mapping:
  - 方向：右摇杆模拟指针
  - A/B 按钮：手柄对应按键
  - Shake: 映射到某个按键
```

#### 6.4.4 Wii 特殊设置

**Wii 系统菜单**（可选）:
- 需要 Wii NAND 备份和系统菜单 WAD
- 放置在 `E:\Emulators\Dolphin\User\Wii\`

**Wii 存档管理**:
- 位置：`E:\Emulators\Dolphin\User\Wii\title\`
- 可导入/导出真实 Wii 存档

---

### 6.5 Ryujinx（Switch 模拟器）配置

#### 6.5.1 安装和初始设置

**下载和安装**:
1. 访问 https://ryujinx.org/download
2. 下载最新版本（.zip 文件）
3. 解压到 `E:\Emulators\Ryujinx\`
4. 运行 `Ryujinx.exe`

**首次配置向导**:
1. 选择语言：简体中文
2. 设置游戏目录：`E:\Games\ROMs\Switch\`
3. 跳过固件安装（稍后手动安装）

#### 6.5.2 固件和密钥配置

**密钥文件放置**:
- 位置：`E:\Emulators\Ryujinx\portable\system\`
- 文件：`prod.keys` 和 `title.keys`

**安装固件**:
1. 进入 `Tools` > `Install Firmware`
2. 选择固件 .zip 文件（约 300MB）
3. 等待安装完成
4. 重启 Ryujinx

**验证**:
- 进入 `Help` > `About`
- 检查固件版本是否显示

#### 6.5.3 图形设置

**进入设置**: `Options` > `Settings` > `Graphics`

**推荐配置**（AMD 7735）:
```yaml
图形后端:
  Graphics Backend: Vulkan
  Preferred GPU: AMD 集显

分辨率:
  Resolution Scale: 1x (720p/1080p) 或 2x
  Aspect Ratio: 16:9
  Max Anisotropy: 16x

性能设置:
  Enable Shader Cache: ✓
  Enable Texture Recompression: ✓

高级:
  Enable V-Sync: ✓
  Use Persistent Buffer: ✓
```

**性能建议**:
- 部分游戏可能需要降低到 1x 分辨率
- 初次运行游戏时会编译着色器，稍有卡顿属正常

#### 6.5.4 系统和输入设置

**系统设置**: `Options` > `Settings` > `System`
```yaml
区域: 中国大陆（或其他）
语言: 简体中文
时区: Asia/Shanghai
系统时间: 自动
忽略固件缺失警告: Off
```

**输入设置**: `Options` > `Settings` > `Input`
```yaml
Player 1:
  Input Device: [您的手柄]
  Controller Type: Pro Controller（推荐）
  Mapping: 使用 "AutoMap" 或手动映射

按键映射:
  确认键: A
  返回键: B
  左摇杆: L3
  右摇杆: R3
```

#### 6.5.5 存档位置

**存档目录**:
- 位置：`E:\Emulators\Ryujinx\portable\bis\user\save\`
- 按游戏 ID 分类存储

**备份建议**:
- 定期备份整个 `save` 目录到 D 盘

---

### 6.6 其他模拟器快速配置

#### 6.6.1 DuckStation（PS1）

**安装**: 解压到 `E:\Emulators\DuckStation\`

**关键设置**:
```yaml
BIOS: E:\Emulators\DuckStation\bios\scph5501.bin
渲染器: Vulkan
分辨率: 4x-8x Native
纹理过滤: PGXP
PGXP 几何校正: 启用
宽屏补丁: 16:9（部分游戏支持）
```

#### 6.6.2 Citra（3DS）

**安装**: 解压到 `E:\Emulators\Citra\`

**关键设置**:
```yaml
渲染器: OpenGL
分辨率: 2x-3x
布局: 上下布局（或并排）
触摸屏: 鼠标模拟
```

#### 6.6.3 RPCS3（PS3）

**安装**: 解压到 `E:\Emulators\RPCS3\`

**安装固件**:
1. 下载 PS3 固件（PS3UPDAT.PUP）
2. `File` > `Install Firmware`
3. 选择固件文件安装

**关键设置**:
```yaml
CPU:
  PPU Decoder: Recompiler (LLVM)
  SPU Decoder: Recompiler (LLVM)
  Thread数: 8（利用 AMD 7735 的 8 核）

GPU:
  Renderer: Vulkan
  Resolution Scale: 100%（或 150%）
  Anisotropic Filter: 16x
```

**注意**: PS3 模拟器性能要求很高，部分游戏可能无法流畅运行

#### 6.6.4 Xenia（Xbox 360）

**安装**: 解压到 `E:\Emulators\Xenia\`

**关键设置**:
```yaml
GPU: Vulkan
Resolution Scale: 1x（原生）
V-Sync: On
```

**注意**: Xenia 处于早期开发阶段，兼容性有限

---

### 6.7 统一手柄配置标准

#### 6.7.1 标准按键映射

**所有模拟器统一映射方案**（Xbox 布局）:

```yaml
基础按键:
  A (Xbox) → 确认
  B (Xbox) → 返回/取消
  X (Xbox) → 功能键1
  Y (Xbox) → 功能键2
  LB → L1/L
  RB → R1/R
  LT → L2
  RT → R2
  Start → 开始
  Back/Select → 选择

摇杆:
  左摇杆 → 移动/方向
  右摇杆 → 视角/辅助操作
  L3 (按下左摇杆) → 特殊功能
  R3 (按下右摇杆) → 特殊功能

十字键:
  D-Pad → 方向键/菜单导航
```

#### 6.7.2 PlayStation 手柄适配

如果使用 PS 手柄（DualSense/DualShock 4）:
1. 安装 DS4Windows
2. 配置为 Xbox 手柄模拟
3. 或在每个模拟器中手动映射

---

---

## 7. 性能优化配置

### 7.1 Windows 系统优化

#### 7.1.1 游戏模式

**启用 Windows 游戏模式**:
1. 打开 `设置` > `游戏` > `游戏模式`
2. 启用"游戏模式"
3. 功能：优先分配 CPU/GPU 资源给游戏进程

#### 7.1.2 电源计划

**设置高性能模式**:
```powershell
# 打开控制面板 > 电源选项
# 选择 "高性能" 计划

# 或使用命令行:
powercfg /setactive SCHEME_MIN  # 高性能模式
```

**自定义电源计划**:
- 关闭显示器：从不
- 使计算机进入睡眠状态：从不
- USB 设置：禁用选择性暂停
- PCI Express：关闭链路状态电源管理

#### 7.1.3 后台应用优化

**禁用不必要的启动项**:
1. `Win + R` > `msconfig` > `启动`
2. 禁用非必要的启动程序
3. 保留：
   - ✓ 显卡驱动
   - ✓ 音频驱动
   - ✓ Playnite 启动脚本
4. 禁用：
   - ✗ OneDrive
   - ✗ 不常用的第三方软件

**优化 Windows 更新**:
- 设置为"深夜时段"自动更新
- 避免游戏时间段更新

**禁用索引服务**（E 盘游戏目录）:
1. 右键 E 盘 > `属性`
2. 取消勾选"除了文件属性外，还允许索引此驱动器上文件的内容"
3. 应用到所有文件和文件夹

---

### 7.2 AMD 图形设置

#### 7.2.1 AMD Software 配置

**打开 AMD Software**:
- 右键桌面 > `AMD Software: Adrenalin Edition`

**游戏优化设置**:
```yaml
全局图形:
  抗锯齿模式: 应用程序控制
  抗锯齿方法: 多重采样
  变形过滤: 关
  纹理过滤质量: 性能
  曲面格式优化: 开
  各向异性过滤: 应用程序控制
  等待垂直刷新: 始终开启（减少撕裂）
  OpenGL 三重缓冲: 开

显示设置:
  AMD FreeSync: 启用（如显示器支持）
  Radeon Chill: 禁用
```

**性能调优**:
```yaml
图形配置文件:
  为模拟器创建自定义配置文件
  示例: PCSX2.exe, Dolphin.exe, Ryujinx.exe

  配置:
    纹理过滤质量: 高质量
    各向异性过滤: 16x
    抗锯齿: 应用程序控制
    垂直同步: 应用程序控制
```

#### 7.2.2 VRAM 分配（BIOS 设置）

**进入 BIOS 分配更多显存**:
1. 重启电脑，按 `Del` 或 `F2` 进入 BIOS
2. 找到 `Advanced` > `Integrated Graphics Configuration`
3. 设置 `UMA Frame Buffer Size`: 4GB 或 8GB
4. 保存并重启

**说明**: AMD 7735 集成显卡共享系统内存，分配 4-8GB 显存可提升模拟器性能

---

### 7.3 内存管理优化

#### 7.3.1 虚拟内存配置

**推荐配置**（64GB 物理内存）:
```yaml
C 盘虚拟内存:
  初始大小: 4096 MB
  最大大小: 8192 MB

D 盘虚拟内存:
  初始大小: 8192 MB
  最大大小: 16384 MB

说明: 虽然物理内存充足，但部分应用仍需要虚拟内存
```

**配置步骤**:
1. `此电脑` 右键 > `属性` > `高级系统设置`
2. `性能` > `设置` > `高级` > `虚拟内存` > `更改`
3. 取消勾选"自动管理所有驱动器的分页文件大小"
4. 按上述配置设置各盘符
5. 应用并重启

#### 7.3.2 内存清理

**定期清理内存**:
- 使用 Windows 内置"存储感知"
- 或使用第三方工具（如 CCleaner）

---

### 7.4 存储优化

#### 7.4.1 SSD 优化

**E 盘（SATA SSD）优化**:
```yaml
启用 TRIM:
  # 检查 TRIM 状态
  fsutil behavior query DisableDeleteNotify
  # 结果为 0 表示 TRIM 已启用

  # 如果禁用，启用 TRIM:
  fsutil behavior set DisableDeleteNotify 0

禁用碎片整理:
  - SSD 不需要碎片整理
  - 确保计划碎片整理中 E 盘为"从不"

预留空间:
  - 保持至少 10% 空闲空间（200GB）
  - 避免 SSD 性能下降
```

**M.2 SSD（D 盘）优化**:
- 同上，确保 TRIM 启用
- 用于 WSL2 交换文件和备份，保持高性能

#### 7.4.2 缓存优化

**模拟器缓存管理**:
```yaml
RetroArch 着色器缓存:
  位置: E:\Emulators\RetroArch\shaders\
  建议: 保留，加快游戏启动

Ryujinx 着色器缓存:
  位置: E:\Emulators\Ryujinx\portable\bis\user\cache\
  建议: 保留，首次运行后显著提升性能

Playnite 缓存:
  位置: E:\Playnite\cache\
  清理: 定期清理临时文件（不影响功能）
```

---

### 7.5 网络优化（可选）

#### 7.5.1 本地网络优化

**如果使用远程串流或 NAS**:
```yaml
网络设置:
  连接类型: 有线千兆以太网（推荐）
  WiFi: 5GHz 频段（如必须用 WiFi）

QoS 设置（路由器）:
  优先级: 小主机 IP > 高优先级
  带宽预留: 游戏流量优先

MTU 优化:
  默认 1500（通常无需调整）
```

#### 7.5.2 关闭不必要的网络服务

```yaml
禁用服务:
  - Windows 网络发现（如不需要）
  - 远程桌面（如不使用）

保留服务:
  - Windows Update（设置为手动）
  - Steam（如使用）
```

---

### 7.6 模拟器性能调优

#### 7.6.1 优先级设置

**提高模拟器进程优先级**（高负载游戏）:
```batch
# 创建启动脚本提高优先级
# 示例: high-priority-ryujinx.bat

@echo off
start /high "Ryujinx" "E:\Emulators\Ryujinx\Ryujinx.exe" %*
```

**注意**: 仅在游戏卡顿时使用，可能影响系统响应

#### 7.6.2 CPU 亲和性

**手动设置 CPU 核心**（特定模拟器）:
- 打开任务管理器
- 右键模拟器进程 > `设置亲和性`
- 选择所有核心（8 个）

**自动化脚本**:
```batch
# 示例: 为 RPCS3 设置所有核心
start "" /affinity FF "E:\Emulators\RPCS3\rpcs3.exe"
# FF = 11111111 (8核心)
```

---

### 7.7 性能监控

#### 7.7.1 监控工具

**推荐工具**:
1. **MSI Afterburner + RivaTuner**:
   - 实时显示 FPS、CPU/GPU 使用率、温度
   - OSD 叠加层显示

2. **HWiNFO64**:
   - 详细硬件监控
   - 记录温度、频率、功耗

3. **Windows 任务管理器**:
   - 快速查看资源使用
   - 快捷键 `Ctrl + Shift + Esc`

#### 7.7.2 性能基准

**预期性能**（AMD 7735 + 64GB RAM）:

| 模拟器 | 典型游戏 | 预期 FPS | 备注 |
|--------|---------|----------|------|
| RetroArch (FC/SFC/MD) | 任意游戏 | 60 FPS 满速 | 无压力 |
| RetroArch (N64) | 马里奥64 | 60 FPS | 部分游戏可能卡顿 |
| PCSX2 | 最终幻想10 | 60 FPS | 大部分游戏流畅 |
| Dolphin | 塞尔达：风之杖 | 60 FPS | 无压力 |
| Ryujinx | 塞尔达：旷野之息 | 30 FPS (锁定) | 可玩，部分场景掉帧 |
| Ryujinx | 动物森友会 | 60 FPS | 流畅 |
| RPCS3 | 战神3 | 20-30 FPS | 勉强可玩 |
| DuckStation | FF7 | 60 FPS 满速 | 无压力 |

---

## 8. 备份和维护方案

### 8.1 备份策略

#### 8.1.1 备份数据分类

**优先级 1 - 关键数据（每周备份）**:
```yaml
Playnite 游戏库:
  源: E:\Playnite\library\
  目标: D:\Backups\Gaming\Playnite\library\
  大小: < 500 MB
  内容: 游戏列表、元数据、用户配置

模拟器存档:
  RetroArch:
    源: E:\Emulators\RetroArch\saves\
    目标: D:\Backups\Gaming\Saves\RetroArch\

  PCSX2:
    源: E:\Emulators\PCSX2\memcards\
    目标: D:\Backups\Gaming\Saves\PCSX2\

  Dolphin:
    源: E:\Emulators\Dolphin\User\Saves\
    目标: D:\Backups\Gaming\Saves\Dolphin\

  Ryujinx:
    源: E:\Emulators\Ryujinx\portable\bis\user\save\
    目标: D:\Backups\Gaming\Saves\Ryujinx\

  总大小: < 1 GB
```

**优先级 2 - 重要数据（每月备份）**:
```yaml
模拟器配置:
  RetroArch: E:\Emulators\RetroArch\retroarch.cfg
  PCSX2: E:\Emulators\PCSX2\inis\
  Dolphin: E:\Emulators\Dolphin\User\Config\
  Ryujinx: E:\Emulators\Ryujinx\portable\Config.json

  目标: D:\Backups\Gaming\Configs\
  大小: < 100 MB

Playnite 扩展和主题:
  源: E:\Playnite\Extensions\, E:\Playnite\Themes\
  目标: D:\Backups\Gaming\Playnite\Extensions\
  大小: < 500 MB

BIOS 文件:
  源: 各模拟器 BIOS 目录
  目标: D:\Backups\Gaming\BIOS\
  大小: < 1 GB
```

**优先级 3 - 可选数据（不定期）**:
```yaml
游戏封面和截图:
  源: E:\Games\Game-Assets\
  大小: 5-20 GB
  说明: 可重新下载，仅在网络不便时备份

即时存档:
  RetroArch states, PCSX2 sstates 等
  大小: 1-5 GB
  说明: 非永久存档，可选备份
```

#### 8.1.2 自动备份脚本

**创建备份脚本**: `D:\Backups\Gaming\backup-gaming.bat`

```batch
@echo off
setlocal enabledelayedexpansion

:: 设置变量
set SOURCE_ROOT=E:
set BACKUP_ROOT=D:\Backups\Gaming
set DATE=%date:~0,4%%date:~5,2%%date:~8,2%
set LOGFILE=%BACKUP_ROOT%\backup-%DATE%.log

echo ================================================ >> "%LOGFILE%"
echo 备份开始时间: %date% %time% >> "%LOGFILE%"
echo ================================================ >> "%LOGFILE%"

:: 1. 备份 Playnite 库
echo 备份 Playnite 库... >> "%LOGFILE%"
robocopy "%SOURCE_ROOT%\Playnite\library" "%BACKUP_ROOT%\Playnite\library" /MIR /R:3 /W:5 /LOG+:"%LOGFILE%"

:: 2. 备份模拟器存档
echo 备份 RetroArch 存档... >> "%LOGFILE%"
robocopy "%SOURCE_ROOT%\Emulators\RetroArch\saves" "%BACKUP_ROOT%\Saves\RetroArch" /MIR /R:3 /W:5 /LOG+:"%LOGFILE%"

echo 备份 PCSX2 记忆卡... >> "%LOGFILE%"
robocopy "%SOURCE_ROOT%\Emulators\PCSX2\memcards" "%BACKUP_ROOT%\Saves\PCSX2" /MIR /R:3 /W:5 /LOG+:"%LOGFILE%"

echo 备份 Dolphin 存档... >> "%LOGFILE%"
robocopy "%SOURCE_ROOT%\Emulators\Dolphin\User\Saves" "%BACKUP_ROOT%\Saves\Dolphin" /MIR /R:3 /W:5 /LOG+:"%LOGFILE%"

echo 备份 Ryujinx 存档... >> "%LOGFILE%"
robocopy "%SOURCE_ROOT%\Emulators\Ryujinx\portable\bis\user\save" "%BACKUP_ROOT%\Saves\Ryujinx" /MIR /R:3 /W:5 /LOG+:"%LOGFILE%"

:: 3. 备份配置文件（月度）
set DAY=%date:~8,2%
if "%DAY%"=="01" (
    echo 执行月度配置备份... >> "%LOGFILE%"

    robocopy "%SOURCE_ROOT%\Emulators\RetroArch" "%BACKUP_ROOT%\Configs\RetroArch" retroarch.cfg /R:3 /W:5 /LOG+:"%LOGFILE%"
    robocopy "%SOURCE_ROOT%\Emulators\PCSX2\inis" "%BACKUP_ROOT%\Configs\PCSX2" /MIR /R:3 /W:5 /LOG+:"%LOGFILE%"
    robocopy "%SOURCE_ROOT%\Emulators\Dolphin\User\Config" "%BACKUP_ROOT%\Configs\Dolphin" /MIR /R:3 /W:5 /LOG+:"%LOGFILE%"
    robocopy "%SOURCE_ROOT%\Playnite\Extensions" "%BACKUP_ROOT%\Playnite\Extensions" /MIR /R:3 /W:5 /LOG+:"%LOGFILE%"
)

echo ================================================ >> "%LOGFILE%"
echo 备份完成时间: %date% %time% >> "%LOGFILE%"
echo ================================================ >> "%LOGFILE%"

exit /b 0
```

#### 8.1.3 配置自动备份任务

**使用任务计划程序**:
1. 打开"任务计划程序"
2. 创建基本任务：
   ```yaml
   名称: 游戏数据自动备份
   描述: 每周备份 Playnite 和模拟器存档

   触发器:
     类型: 每周
     日期: 每周日
     时间: 凌晨 3:00

   操作:
     程序: D:\Backups\Gaming\backup-gaming.bat

   条件:
     ✓ 只有在计算机使用交流电源时启动
     □ 唤醒计算机运行此任务

   设置:
     ✓ 如果任务失败，每隔 10 分钟重新启动
     □ 如果任务运行时间超过 2 小时，停止任务
   ```
3. 保存任务

**测试备份**:
- 手动运行一次任务
- 检查 `D:\Backups\Gaming\` 目录
- 查看日志文件确认备份成功

#### 8.1.4 云端备份（可选）

**使用飞牛 NAS 同步**:
```yaml
方案 1: 手动同步
  - 定期将 D:\Backups\Gaming\ 复制到 NAS
  - 使用 Windows 文件资源管理器或 FreeFileSync

方案 2: 自动同步
  - 配置 Windows 任务计划程序
  - 使用 robocopy 同步到 \\nas\backups\gaming\

  示例脚本:
    robocopy "D:\Backups\Gaming" "\\nas\backups\gaming" /MIR /R:3 /W:5
```

---

### 8.2 恢复方案

#### 8.2.1 Playnite 库恢复

**恢复步骤**:
1. 关闭 Playnite
2. 删除或重命名 `E:\Playnite\library\`
3. 复制备份：
   ```batch
   robocopy "D:\Backups\Gaming\Playnite\library" "E:\Playnite\library" /MIR
   ```
4. 重启 Playnite
5. 验证游戏列表恢复

#### 8.2.2 模拟器存档恢复

**通用步骤**（以 RetroArch 为例）:
1. 关闭 RetroArch
2. 恢复存档：
   ```batch
   robocopy "D:\Backups\Gaming\Saves\RetroArch" "E:\Emulators\RetroArch\saves" /MIR
   ```
3. 重启 RetroArch
4. 加载游戏验证存档

**其他模拟器同理**：
- PCSX2: 恢复 `memcards\`
- Dolphin: 恢复 `User\Saves\`
- Ryujinx: 恢复 `portable\bis\user\save\`

#### 8.2.3 完整系统重建

**场景：系统重装或硬盘故障**

**步骤**:
1. **重新安装 Windows 11**
2. **恢复 E 盘数据**（如果盘符保持不变且数据完好）
3. **重新安装 Playnite**:
   - 下载便携版到 `E:\Playnite\`
   - 从备份恢复 `library\` 目录
4. **重新安装模拟器**:
   - 下载各模拟器到 `E:\Emulators\`
   - 从备份恢复配置文件
   - 从备份恢复 BIOS 文件
5. **恢复存档**:
   - 从备份恢复各模拟器存档
6. **验证功能**:
   - 启动 Playnite
   - 测试启动游戏
   - 检查存档加载

**预计时间**: 4-6 小时（取决于数据量和网速）

---

### 8.3 维护计划

#### 8.3.1 日常维护（自动）

```yaml
自动备份:
  频率: 每周日凌晨 3:00
  内容: Playnite 库 + 模拟器存档
  工具: Windows 任务计划程序

自动清理:
  磁盘清理: 每月自动（Windows 存储感知）
  临时文件: 自动清理
  日志文件: 保留最近 30 天

性能监控:
  温度监控: 使用 HWiNFO（可选）
  磁盘健康: 使用 CrystalDiskInfo（可选）
```

#### 8.3.2 每月维护清单

```yaml
软件更新:
  - [ ] 检查 Playnite 更新
  - [ ] 检查模拟器更新（RetroArch, PCSX2, Dolphin, Ryujinx）
  - [ ] 更新 Playnite 插件
  - [ ] 更新 AMD 显卡驱动（如有）

数据整理:
  - [ ] 验证备份完整性
  - [ ] 清理不玩的游戏（释放空间）
  - [ ] 整理游戏分类和标签
  - [ ] 更新游戏元数据（新游戏）

性能检查:
  - [ ] 检查磁盘空间（E 盘剩余 > 200GB）
  - [ ] 检查系统温度（< 75°C）
  - [ ] 测试关键游戏性能

配置备份:
  - [ ] 手动备份配置文件到 D 盘
  - [ ] （可选）备份到 NAS
```

#### 8.3.3 每季度维护清单

```yaml
深度清理:
  - [ ] 清理 RetroArch 着色器缓存（如过大）
  - [ ] 清理 Playnite 缓存目录
  - [ ] 清理模拟器临时文件
  - [ ] 整理 ROM 文件（移除重复/损坏文件）

系统优化:
  - [ ] 运行磁盘清理工具
  - [ ] 检查虚拟内存设置
  - [ ] 优化启动项
  - [ ] 检查 Windows 更新

文档更新:
  - [ ] 更新 BASELINE.md 记录变更
  - [ ] 记录新安装的模拟器和游戏
  - [ ] 更新配置文档
```

#### 8.3.4 每年维护清单

```yaml
全面审查:
  - [ ] 完整系统备份（包括系统盘）
  - [ ] 评估存储空间需求（是否需要扩容）
  - [ ] 审查不常用模拟器（考虑移除）
  - [ ] 更新 BIOS 和固件（如有新版）

性能评估:
  - [ ] 重新测试关键游戏性能
  - [ ] 评估硬件升级需求
  - [ ] 检查风扇和散热（清灰）

数据归档:
  - [ ] 归档旧存档（不玩的游戏）
  - [ ] 清理旧日志文件
  - [ ] 备份到外部存储（长期保存）
```

---

## 9. 实施路线图

### 9.1 总体时间规划

**总实施时间**: 12-16 小时
**建议分配**: 分 2-3 天完成，每天 4-6 小时

---

### 9.2 阶段 1：基础环境准备（2-3 小时）

#### 任务清单

**1.1 创建目录结构**（15 分钟）:
```powershell
# 在 PowerShell 中执行
New-Item -ItemType Directory -Path "E:\Games\PC-Games" -Force
New-Item -ItemType Directory -Path "E:\Games\ROMs" -Force
New-Item -ItemType Directory -Path "E:\Games\Game-Assets" -Force
New-Item -ItemType Directory -Path "E:\Emulators" -Force
New-Item -ItemType Directory -Path "E:\Playnite" -Force
New-Item -ItemType Directory -Path "D:\Backups\Gaming" -Force

# 创建各平台 ROM 子目录
$platforms = @("FC","SFC","MD","GB","GBC","GBA","N64","PS1","PS2","PSP","NGC","Wii","3DS","Switch","PS3")
foreach ($platform in $platforms) {
    New-Item -ItemType Directory -Path "E:\Games\ROMs\$platform" -Force
}
```

**1.2 下载和安装 Playnite**（30 分钟）:
1. 访问 https://playnite.link/download.html
2. 下载便携版
3. 解压到 `E:\Playnite\`
4. 首次运行配置
5. 设置语言和基础选项

**1.3 安装必备插件**（45 分钟）:
- IGDB Metadata Provider
  - 注册 IGDB API 密钥
  - 配置插件
- Emulators Library
- Epic Library（如需要）
- Controller Support
- RetroAchievements（可选）

**1.4 安装和配置主题**（30 分钟）:
- 下载 Strata Fullscreen 主题
- 应用主题
- 自定义颜色和布局
- 测试手柄导航

#### 验收标准
- ✓ E 盘目录结构创建完成
- ✓ Playnite 可以正常启动（桌面和全屏模式）
- ✓ 插件安装成功并可使用
- ✓ 主题应用成功，界面美观
- ✓ 手柄可以导航 Playnite 界面

---

### 9.3 阶段 2：模拟器安装和配置（4-6 小时）

#### 任务清单

**2.1 安装 RetroArch**（1 小时）:
1. 下载 RetroArch Windows x64 版本
2. 解压到 `E:\Emulators\RetroArch\`
3. 首次配置（语言、驱动）
4. 下载推荐核心（Mesen, Snes9x, Genesis Plus GX, mGBA, Mupen64Plus-Next, Beetle PSX HW, PPSSPP）
5. 放置 BIOS 文件到 `system\` 目录
6. 配置视频、音频、输入设置
7. 测试一个游戏（每个平台）

**2.2 安装 PCSX2**（45 分钟）:
1. 下载 PCSX2 最新版
2. 安装到 `E:\Emulators\PCSX2\`
3. 放置 PS2 BIOS 到 `bios\`
4. 配置图形设置（Vulkan, 2x-3x 分辨率）
5. 配置手柄
6. 测试一个 PS2 游戏

**2.3 安装 Dolphin**（45 分钟）:
1. 下载 Dolphin 稳定版
2. 解压到 `E:\Emulators\Dolphin\`
3. 配置图形设置（Vulkan, 3x-4x 分辨率）
4. 配置 NGC 手柄和 Wii 遥控器
5. 测试一个 NGC/Wii 游戏

**2.4 安装 Ryujinx**（1 小时）:
1. 下载 Ryujinx 最新版
2. 解压到 `E:\Emulators\Ryujinx\`
3. 放置 prod.keys 和 title.keys
4. 安装 Switch 固件
5. 配置图形设置（Vulkan, 1x-2x）
6. 配置手柄
7. 测试一个 Switch 游戏（耐心等待首次着色器编译）

**2.5 安装其他模拟器**（1-2 小时）:
- DuckStation（PS1）：30 分钟
- Citra（3DS）：30 分钟
- RPCS3（PS3）：1 小时（含固件安装）
- Xenia（Xbox 360）：30 分钟（可选）

#### 验收标准
- ✓ 所有计划安装的模拟器可以独立启动
- ✓ 手柄在每个模拟器中正常工作
- ✓ 每个平台至少测试运行 1 个游戏
- ✓ BIOS/固件正确加载
- ✓ 游戏画面、音频、输入均正常

---

### 9.4 阶段 3：Playnite 整合（2-3 小时）

#### 任务清单

**3.1 配置模拟器连接**（1 小时）:
1. 在 Playnite 中添加每个模拟器
2. 配置启动参数
3. 为每个平台指定模拟器和核心
4. 配置 ROM 扫描路径

**3.2 导入游戏**（45 分钟）:
- 自动扫描 ROM 目录
- 手动添加 PC 游戏
- 整合 Steam/Epic 库（如有）
- 验证游戏可以从 Playnite 启动

**3.3 元数据刮削**（45 分钟）:
- 自动下载游戏信息、封面、背景
- 手动修正错误匹配
- 为自定义游戏添加封面
- 整理游戏分类

**3.4 添加应用程序**（30 分钟）:
- 添加 Microsoft Edge（浏览器）
- 添加网易云音乐
- 添加哔哩哔哩客户端
- 添加极空间
- 创建"应用程序"分类
- 为应用添加图标和封面

#### 验收标准
- ✓ 游戏可以从 Playnite 直接启动（不报错）
- ✓ 封面和元数据显示正确（至少 80% 游戏）
- ✓ 应用程序可以从 Playnite 打开
- ✓ 分类和筛选器正常工作
- ✓ 游戏时长正确记录

---

### 9.5 阶段 4：界面优化和自动化（1-2 小时）

#### 任务清单

**4.1 界面定制**（30 分钟）:
- 应用和微调主题
- 配置封面显示样式（大图标网格）
- 设置默认排序（最近游玩）
- 配置筛选器（平台、类别）
- 隐藏不需要的 UI 元素

**4.2 手柄优化**（30 分钟）:
- 配置全局手柄快捷键
- 测试导航流畅度（每个界面）
- 调整按键延迟和灵敏度
- 配置退出游戏快捷键

**4.3 配置自动启动**（30 分钟）:
- 创建 `startup-playnite.bat` 脚本
- 添加到 Windows 任务计划程序
- 设置延迟启动（15 秒）
- 测试开机自动进入全屏模式
- 添加"退出到桌面"快捷方式

#### 验收标准
- ✓ 界面美观，符合现代风格
- ✓ 手柄操作流畅，无明显延迟
- ✓ 开机自动进入 Playnite 全屏模式
- ✓ 可以方便地退出到 Windows 桌面
- ✓ 所有快捷键正常工作（Guide + Start 等）
- ✓ 从启动到进入界面 < 30 秒

---

### 9.6 阶段 5：备份和测试（1-2 小时）

#### 任务清单

**5.1 配置备份系统**（45 分钟）:
- 创建 `backup-gaming.bat` 脚本
- 设置 Windows 任务计划（每周日凌晨 3:00）
- 配置 NAS 同步（可选）
- 执行首次完整备份
- 验证备份文件完整性

**5.2 全面功能测试**（45 分钟）:
- 测试每个平台 2-3 个游戏
  - FC, SFC, MD, GBA, N64, PS1, PS2, NGC, Wii, 3DS, Switch
- 测试存档保存和读取
- 测试应用程序启动（浏览器、音乐、视频）
- 测试手柄所有功能（按键、摇杆、震动）
- 测试快捷键（退出、截图、快速存档等）

**5.3 性能验证**（30 分钟）:
- 监控内存使用（应 < 40GB）
- 检查 CPU/GPU 温度（应 < 75°C）
- 验证游戏帧率稳定性
- 测试长时间运行稳定性（1-2 小时）

**5.4 文档整理**（30 分钟）:
- 记录所有配置参数
- 更新 BASELINE.md
- 创建快速参考指南
- 记录已知问题和解决方案

#### 验收标准
- ✓ 备份系统运行正常，自动备份成功
- ✓ 所有测试游戏运行稳定，无崩溃
- ✓ 系统性能符合预期（见 7.7.2 性能基准）
- ✓ 文档完整准确，便于日后参考
- ✓ 无严重 Bug 或性能问题

---

## 10. 验收标准

### 10.1 功能性验收

#### 10.1.1 核心功能

```yaml
游戏启动:
  ✓ 可以从 Playnite 启动所有类型的游戏
  ✓ 游戏启动时间 < 30 秒（大型游戏除外）
  ✓ 退出游戏后正确返回 Playnite
  ✓ 游戏时长正确记录

手柄操作:
  ✓ 手柄在 Playnite 界面中正常导航
  ✓ 手柄在所有模拟器中正常工作
  ✓ 快捷键功能正常（Guide + Start 退出等）
  ✓ 支持多个手柄（多人游戏）

自动化:
  ✓ 开机自动进入 Playnite 全屏模式
  ✓ 延迟启动（15 秒）正常
  ✓ 可以手动退出到桌面

应用整合:
  ✓ 浏览器可以从 Playnite 启动
  ✓ 网易云音乐可以启动
  ✓ 哔哩哔哩客户端可以启动
  ✓ 极空间可以启动

存档管理:
  ✓ 游戏存档正常保存
  ✓ 读取存档正常
  ✓ 即时存档功能正常（支持的模拟器）
  ✓ 存档备份自动执行
```

#### 10.1.2 用户体验

```yaml
界面设计:
  ✓ 界面美观现代，符合预期风格
  ✓ 游戏封面显示完整（至少 80% 游戏有封面）
  ✓ 游戏信息准确（标题、平台、发行年份等）
  ✓ 分类和标签清晰合理

操作响应:
  ✓ 界面响应迅速（< 1 秒）
  ✓ 手柄导航流畅，无明显延迟
  ✓ 游戏启动流畅，无卡顿
  ✓ 切换界面/筛选器快速

导航逻辑:
  ✓ 菜单结构清晰直观
  ✓ 可以快速找到想玩的游戏
  ✓ 筛选器功能有效（按平台、类别、标签）
  ✓ 搜索功能快速准确
```

---

### 10.2 性能验收

#### 10.2.1 帧率要求

```yaml
经典平台（FC/SFC/MD/GBA）:
  ✓ 所有游戏 60 FPS 满速运行
  ✓ 无明显掉帧或卡顿

中等平台（N64/PS1/PSP）:
  ✓ 主流游戏 60 FPS（或游戏原生帧率）
  ✓ 部分高需求游戏允许偶尔掉帧

高级平台（PS2/NGC/Wii）:
  ✓ 大部分游戏 60 FPS 稳定
  ✓ 少数高需求游戏 30-60 FPS 波动

现代平台（3DS/Switch）:
  ✓ 3DS 游戏 30-60 FPS
  ✓ Switch 主流游戏 30 FPS 可玩
  ✓ Switch 轻量级游戏 60 FPS

实验性平台（PS3/Xbox 360）:
  ✓ 部分游戏可玩（20-30 FPS）
  ✓ 不强制要求完美性能
```

#### 10.2.2 系统资源

```yaml
内存使用:
  ✓ 空闲时 < 10 GB
  ✓ 运行轻量级游戏 < 20 GB
  ✓ 运行高需求游戏 < 40 GB
  ✓ 始终保留 > 20 GB 可用内存

CPU 使用:
  ✓ 空闲时 < 10%
  ✓ 运行经典游戏 < 30%
  ✓ 运行现代游戏 < 80%
  ✓ 无长时间 100% 占用

温度:
  ✓ CPU 温度 < 75°C（游戏中）
  ✓ CPU 温度 < 85°C（峰值）
  ✓ 风扇噪音可接受（主观）

磁盘空间:
  ✓ E 盘剩余 > 200 GB
  ✓ D 盘备份空间 > 50 GB
```

---

### 10.3 可靠性验收

#### 10.3.1 稳定性

```yaml
长时间运行:
  ✓ 连续运行 4 小时无崩溃
  ✓ 切换游戏 20 次无问题
  ✓ 内存泄漏检查（内存使用稳定）

系统重启:
  ✓ 重启后正常进入 Playnite
  ✓ 自动启动功能正常
  ✓ 配置未丢失

异常恢复:
  ✓ 游戏崩溃后可以返回 Playnite
  ✓ 模拟器异常退出不影响系统
  ✓ Playnite 崩溃可以重启恢复
```

#### 10.3.2 数据安全

```yaml
备份系统:
  ✓ 自动备份任务正常执行
  ✓ 备份文件完整可用
  ✓ 可以成功从备份恢复

存档保护:
  ✓ 存档文件不丢失
  ✓ 存档可以正常读取
  ✓ 存档恢复测试成功

配置保存:
  ✓ Playnite 配置正确保存
  ✓ 模拟器配置正确保存
  ✓ 自定义设置不会丢失
```

#### 10.3.3 兼容性

```yaml
手柄兼容性:
  ✓ Xbox 手柄即插即用
  ✓ PlayStation 手柄正常工作（通过 DS4Windows）
  ✓ 第三方手柄兼容性良好

ROM 兼容性:
  ✓ 常见 ROM 格式正常加载
  ✓ 压缩 ROM 正确识别（.zip, .7z）
  ✓ CHD 格式支持（PS1/PS2）

系统兼容性:
  ✓ 与 Hyper-V 共存无冲突
  ✓ 与 WSL2 共存无冲突
  ✓ 不影响其他应用运行
```

---

## 11. 故障排除指南

### 11.1 常见问题和解决方案

#### 11.1.1 Playnite 相关问题

**问题：Playnite 无法启动**
```yaml
症状: 双击程序无反应，或闪退
可能原因:
  1. .NET 运行库缺失
  2. 数据库损坏
  3. 权限问题

解决方案:
  1. 安装 .NET 6.0 或更高版本
     下载: https://dotnet.microsoft.com/download

  2. 恢复数据库:
     - 删除 E:\Playnite\library\*.db
     - 从备份恢复

  3. 检查权限:
     - 右键 Playnite 文件夹 > 属性 > 安全
     - 确保当前用户有完全控制权限
```

**问题：游戏无法从 Playnite 启动**
```yaml
症状: 点击游戏后无反应，或报错
可能原因:
  1. 模拟器路径错误
  2. ROM 文件丢失或损坏
  3. 启动参数配置错误

解决方案:
  1. 验证模拟器路径:
     - Settings > Emulators
     - 检查可执行文件路径是否正确

  2. 检查 ROM 文件:
     - 确认文件存在
     - 尝试直接用模拟器打开 ROM

  3. 检查启动参数:
     - 右键游戏 > Edit > Play Action
     - 验证参数格式正确
     - 参考本文档第 5.5 节
```

**问题：游戏封面不显示**
```yaml
症状: 游戏列表中封面为空白
可能原因:
  1. 元数据未下载
  2. 图片缓存损坏
  3. IGDB API 配额用尽

解决方案:
  1. 手动下载元数据:
     - 右键游戏 > Edit > Download Metadata
     - 选择正确的游戏匹配

  2. 清理缓存:
     - 删除 E:\Playnite\cache\
     - 重启 Playnite
     - 重新下载元数据

  3. 检查 API 配额:
     - IGDB 免费版有请求限制
     - 等待 24 小时重置
     - 或手动上传封面
```

#### 11.1.2 模拟器相关问题

**问题：RetroArch 游戏黑屏**
```yaml
症状: 启动游戏后屏幕黑屏，有声音或无声音
可能原因:
  1. 核心未正确加载
  2. 视频驱动问题
  3. BIOS 缺失（某些核心）

解决方案:
  1. 检查核心:
     - Main Menu > Load Core
     - 手动选择正确核心
     - 或重新下载核心

  2. 更换视频驱动:
     - Settings > Video > Driver
     - 尝试 Vulkan → OpenGL → D3D11

  3. 检查 BIOS:
     - 确认 BIOS 文件在 system\ 目录
     - Information > System Information 验证
```

**问题：PCSX2 游戏运行缓慢**
```yaml
症状: 游戏帧率 < 30 FPS，明显卡顿
可能原因:
  1. 图形设置过高
  2. CPU 占用过高
  3. 游戏兼容性问题

解决方案:
  1. 降低图形设置:
     - Internal Resolution: 2x → 1x
     - Blending Accuracy: Basic → Minimum
     - 关闭 Anisotropic Filtering

  2. 优化 CPU:
     - Enable MTVU (Multi-Threaded VU1)
     - 在游戏特定设置中调整

  3. 查看兼容性列表:
     - 访问 PCSX2 官网
     - 搜索游戏兼容性
     - 应用推荐设置
```

**问题：Dolphin 音频爆音**
```yaml
症状: 游戏音频有噪音、爆音或失真
可能原因:
  1. 音频后端问题
  2. DSP 设置问题
  3. 帧率不稳定

解决方案:
  1. 更换音频后端:
     - Options > Audio Settings > Backend
     - 尝试 Cubeb → OpenAL → XAudio2

  2. 调整 DSP:
     - DSP Emulation Engine: DSP HLE → DSP LLE
     - （注意：LLE 性能要求更高）

  3. 稳定帧率:
     - 降低图形设置
     - 启用 V-Sync
```

**问题：Ryujinx 首次运行非常卡**
```yaml
症状: 新游戏首次运行严重卡顿
可能原因:
  1. 着色器编译（正常现象）
  2. 缓存未建立

解决方案:
  1. 耐心等待:
     - 首次运行会编译着色器
     - 等待 10-30 分钟（取决于游戏）
     - 进度会显示在窗口标题

  2. 启用着色器缓存:
     - Options > Settings > Graphics
     - Enable Shader Cache: ✓

  3. 下载着色器缓存（可选）:
     - 某些社区提供预编译缓存
     - 放置在 portable\bis\user\cache\
     - （注意版权和安全性）
```

#### 11.1.3 手柄相关问题

**问题：手柄无法识别**
```yaml
症状: Playnite 或模拟器无法识别手柄
可能原因:
  1. 手柄驱动问题
  2. USB 端口问题
  3. 蓝牙连接问题

解决方案:
  1. 检查手柄连接:
     - 有线：更换 USB 端口
     - 无线：重新配对蓝牙

  2. 安装/更新驱动:
     - Xbox 手柄：Windows 自动识别
     - PS 手柄：安装 DS4Windows
     - 其他：安装制造商驱动

  3. 测试手柄:
     - 控制面板 > 设备和打印机
     - 右键手柄 > 游戏控制器设置 > 属性
     - 测试按键和摇杆
```

**问题：手柄按键映射错误**
```yaml
症状: 按 A 键触发 B 键功能
可能原因:
  1. 映射配置错误
  2. 模拟器配置不统一
  3. Xbox/PlayStation 布局差异

解决方案:
  1. 重新映射:
     - 在对应模拟器中重新配置按键
     - 使用"自动映射"功能
     - 或手动逐个映射

  2. 统一配置:
     - 参考本文档 6.7 节统一手柄标准
     - 所有模拟器使用相同映射逻辑

  3. PS 手柄用户:
     - 使用 DS4Windows 模拟为 Xbox 手柄
     - 或在每个模拟器中适配 PS 布局
```

#### 11.1.4 性能相关问题

**问题：系统整体卡顿**
```yaml
症状: Windows 桌面和游戏都卡顿
可能原因:
  1. 内存不足（不太可能，64GB 内存）
  2. CPU 过热降频
  3. 后台程序占用资源

解决方案:
  1. 检查资源使用:
     - 任务管理器 (Ctrl + Shift + Esc)
     - 查看 CPU/内存/磁盘使用率

  2. 检查温度:
     - 使用 HWiNFO64 监控
     - CPU 温度 > 85°C 需要降温
     - 清理风扇灰尘或改善散热

  3. 关闭后台程序:
     - 结束不必要的进程
     - 禁用启动项
     - 参考本文档 7.1.3 节
```

**问题：磁盘空间不足**
```yaml
症状: E 盘剩余空间 < 100 GB
可能原因:
  1. 游戏和 ROM 文件过多
  2. 缓存文件累积
  3. 即时存档占用过多

解决方案:
  1. 清理不玩的游戏:
     - 卸载 PC 游戏
     - 删除不玩的 ROM

  2. 清理缓存:
     - RetroArch 着色器缓存
     - Ryujinx 着色器缓存
     - Playnite 缓存目录

  3. 清理即时存档:
     - 保留常用存档
     - 删除旧的或不用的即时存档（states 目录）

  4. 外部存储:
     - 将不常玩的游戏移动到外部硬盘
     - 或上传到 NAS
```

#### 11.1.5 自动启动相关问题

**问题：开机不自动启动 Playnite**
```yaml
症状: 启动到 Windows 桌面，Playnite 未运行
可能原因:
  1. 启动脚本路径错误
  2. 任务计划程序配置错误
  3. 延迟时间不够

解决方案:
  1. 检查脚本路径:
     - 确认 startup-playnite.bat 存在
     - 路径中不含特殊字符

  2. 检查任务计划:
     - 打开任务计划程序
     - 找到 Playnite 启动任务
     - 右键 > 运行 测试是否工作
     - 检查触发器和操作配置

  3. 增加延迟:
     - 修改脚本中的 timeout 时间
     - 从 15 秒增加到 30 秒
     - 某些系统启动较慢
```

**问题：自动启动后卡在加载界面**
```yaml
症状: Playnite 启动但一直加载不进入界面
可能原因:
  1. 数据库损坏
  2. 插件冲突
  3. 网络连接问题（元数据同步）

解决方案:
  1. 修复数据库:
     - 结束 Playnite 进程
     - 从备份恢复 library\

  2. 禁用插件:
     - 以安全模式启动（如有）
     - 或手动删除 Extensions\ 中的插件
     - 逐个重新启用定位问题插件

  3. 离线模式:
     - 断开网络连接
     - 启动 Playnite
     - 在设置中禁用自动同步
```

---

### 11.2 高级故障排除

#### 11.2.1 日志分析

**Playnite 日志位置**:
```
E:\Playnite\playnite.log
```

**查看最近错误**:
```powershell
Get-Content E:\Playnite\playnite.log -Tail 50 | Select-String "ERROR"
```

**RetroArch 日志**:
```
E:\Emulators\RetroArch\retroarch.log
```

**其他模拟器日志**:
- PCSX2: `E:\Emulators\PCSX2\emulog.txt`
- Dolphin: `E:\Emulators\Dolphin\User\Logs\`
- Ryujinx: 控制台窗口输出

#### 11.2.2 完全重置

**Playnite 重置**（保留游戏列表）:
1. 备份 `E:\Playnite\library\`
2. 删除 `E:\Playnite\` 所有其他文件
3. 重新下载 Playnite
4. 恢复 `library\` 目录
5. 重新安装插件和主题

**模拟器重置**:
1. 备份存档和配置
2. 删除模拟器目录
3. 重新下载安装
4. 恢复存档和配置
5. 重新测试

#### 11.2.3 寻求帮助

**官方支持渠道**:

**Playnite**:
- 官方论坛: https://playnite.link/forum/
- GitHub Issues: https://github.com/JosefNemec/Playnite/issues
- Discord: 链接见官网

**RetroArch**:
- 官方论坛: https://forums.libretro.com/
- Discord: https://discord.gg/C4amCeV

**其他模拟器**:
- 各模拟器官网通常有论坛或 Discord
- GitHub Issues 页面

**提问建议**:
1. 描述问题症状
2. 列出尝试过的解决方案
3. 提供错误日志
4. 说明系统配置
5. 提供复现步骤

---

## 结语

### 项目总结

本设计文档详细描述了在铭凡 UM773 小主机上构建统一游戏娱乐前端系统的完整方案。通过使用 Playnite 作为统一界面，配合多个开源模拟器，实现了：

✅ **零成本**：所有软件完全免费开源
✅ **统一体验**：单一界面管理所有游戏和应用
✅ **客厅模式**：开机自动进入，全手柄操作
✅ **全平台覆盖**：从 FC 到 Switch 的完整支持
✅ **易于维护**：完善的备份和恢复机制

### 预期效果

完成本方案后，您将拥有：
- 一个类似游戏主机的统一娱乐中心
- 简洁现代的用户界面
- 流畅的手柄操作体验
- 中型游戏库（50-200 款游戏）的高效管理
- 安全可靠的数据备份体系

### 后续扩展

本系统具有良好的可扩展性：
- 随时添加新游戏和模拟器
- 更换主题和界面风格
- 集成更多娱乐应用
- 配置远程串流（如 Steam Link）
- 扩展存储容量

### 维护建议

为了保持系统长期稳定运行：
- 遵循每月维护清单（见 8.3.2）
- 定期备份关键数据
- 保持软件更新（但测试后再更新）
- 监控系统性能和温度
- 及时清理不需要的文件

### 文档版本

- **版本**: v1.0
- **创建日期**: 2026-03-24
- **最后更新**: 2026-03-24
- **作者**: IT 专家团队
- **审阅状态**: 待用户审阅

---

**感谢使用本设计文档。祝您游戏愉快！** 🎮

---

*（文档完成）*
