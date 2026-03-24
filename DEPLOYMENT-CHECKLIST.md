# Playnite 游戏前端部署检查清单

> **目标设备**: 铭凡UM773 小主机（AMD 7735, 64GB RAM, 2T SSD）
>
> **预计时间**: 12-16 小时（分 2-3 天完成）
>
> **文档版本**: v1.0
>
> **创建日期**: 2026-03-24

---

## 📋 使用说明

**检查清单格式**：
- `[ ]` 表示待完成的任务
- `[x]` 表示已完成的任务（手工打勾）
- 每个任务后都有验证方法
- 遇到问题请参考[故障排除](#故障排除快速索引)

**建议执行方式**：
1. 打印此清单或在另一台设备上打开（便于对照执行）
2. 按顺序完成每个阶段
3. 完成一个任务后立即打勾
4. 每个阶段完成后更新 `BASELINE.md`

---

## 📥 阶段 0：准备工作（开始前完成）

### 软件下载清单

**核心软件**：
- [ ] Playnite 便携版（约 80 MB）
  - 下载地址: https://playnite.link/download.html
  - 选择 "Portable" 版本
  - 文件名示例: `Playnite10.x.zip`

**模拟器软件**（按优先级排序）：
- [ ] RetroArch（约 200 MB）
  - 下载地址: https://www.retroarch.com/?page=platforms
  - 选择 "Windows x64"

- [ ] PCSX2（约 150 MB）
  - 下载地址: https://pcsx2.net/downloads/
  - 选择最新稳定版

- [ ] Dolphin（约 120 MB）
  - 下载地址: https://dolphin-emu.org/download/
  - 选择 "Stable" 版本

- [ ] Ryujinx（约 150 MB）
  - **注意**: 官方项目已停止，需从第三方镜像下载
  - 搜索关键词: "Ryujinx last stable release"

- [ ] DuckStation（约 40 MB）
  - 下载地址: https://github.com/stenzek/duckstation/releases
  - 选择 `duckstation-windows-x64-release.zip`

- [ ] Citra（约 60 MB）（可选）
  - 下载地址: https://citra-emu.org/download/
  - 选择 "Nightly" 版本

- [ ] RPCS3（约 300 MB）（可选）
  - 下载地址: https://rpcs3.net/download

- [ ] Xenia（约 100 MB）（可选）
  - 下载地址: https://github.com/xenia-project/xenia/releases

**BIOS 文件准备**：
- [ ] PS1 BIOS（scph5501.bin 等）
- [ ] PS2 BIOS（SCPH-xxxxx.bin）
- [ ] GBA BIOS（gba_bios.bin）（可选）
- [ ] Switch 固件和密钥（prod.keys, title.keys）

**手柄驱动**（如需要）：
- [ ] DS4Windows（如使用 PlayStation 手柄）
  - 下载地址: https://ds4-windows.com/

**将所有下载文件保存到**：`D:\Downloads\Gaming-Setup\`

---

## 🔧 阶段 1：基础环境准备（2-3 小时）

### 1.1 创建目录结构（15 分钟）

- [ ] 打开 PowerShell（管理员）

- [ ] 创建主目录结构
```powershell
New-Item -ItemType Directory -Path "E:\Games\PC-Games" -Force
New-Item -ItemType Directory -Path "E:\Games\ROMs" -Force
New-Item -ItemType Directory -Path "E:\Games\Game-Assets" -Force
New-Item -ItemType Directory -Path "E:\Emulators" -Force
New-Item -ItemType Directory -Path "E:\Playnite" -Force
New-Item -ItemType Directory -Path "D:\Backups\Gaming" -Force
```

**验证**: 打开文件资源管理器，确认 E 盘和 D 盘目录已创建

- [ ] 创建 ROM 平台子目录
```powershell
$platforms = @("FC","SFC","MD","GB","GBC","GBA","N64","PS1","PS2","PSP","NGC","Wii","3DS","Switch","PS3","Arcade")
foreach ($platform in $platforms) {
    New-Item -ItemType Directory -Path "E:\Games\ROMs\$platform" -Force
}
```

**验证**: 确认 `E:\Games\ROMs\` 下有 16 个平台子目录

- [ ] 创建备份子目录
```powershell
New-Item -ItemType Directory -Path "D:\Backups\Gaming\Playnite" -Force
New-Item -ItemType Directory -Path "D:\Backups\Gaming\Saves" -Force
New-Item -ItemType Directory -Path "D:\Backups\Gaming\Configs" -Force
New-Item -ItemType Directory -Path "D:\Backups\Gaming\BIOS" -Force
```

**验证**: 确认备份目录结构完整

---

### 1.2 安装 Playnite（30 分钟）

- [ ] 解压 Playnite 到 `E:\Playnite\`
  - 右键 `Playnite10.x.zip` > 解压到 `E:\Playnite\`

- [ ] 首次启动 Playnite
  - 运行 `E:\Playnite\Playnite.DesktopApp.exe`
  - 选择语言：**简体中文**（或英文）
  - 跳过库集成（稍后配置）
  - 完成初始向导

**验证**: Playnite 桌面模式正常打开，显示空白游戏库

- [ ] 测试全屏模式
  - 运行 `E:\Playnite\Playnite.FullscreenApp.exe`
  - 确认全屏模式可以启动
  - 按 `Esc` 退出

**验证**: 全屏模式正常显示

---

### 1.3 配置 Playnite 基础设置（30 分钟）

- [ ] 打开设置（F4）

- [ ] 通用设置 (General)
  - 启动模式: **全屏模式 (Fullscreen mode)**
  - 启动时最小化: **禁用**
  - 更新检查: **启用**
  - 统计追踪: **启用**

- [ ] 输入设置 (Input)
  - 启用手柄支持: **✓**
  - 连接手柄测试按键响应

**验证**: 手柄可以在 Playnite 界面中导航

- [ ] 保存设置并重启 Playnite

---

### 1.4 安装必备插件（45 分钟）

- [ ] 安装 IGDB Metadata Provider
  - `Add-ons` > `Browse` > 搜索 "IGDB"
  - 点击 "Install"
  - 重启 Playnite

- [ ] 配置 IGDB API 密钥
  - 访问 https://www.igdb.com/api
  - 注册并获取 API 密钥（Client ID 和 Secret）
  - `Settings` > `Metadata` > `IGDB`
  - 输入 API 密钥
  - 保存

**验证**: 在插件设置中显示 "Connected"

- [ ] 安装 Emulators Library 插件
  - `Add-ons` > `Browse` > 搜索 "Emulators Library"
  - 安装并重启

- [ ] 安装 Controller Support 插件
  - `Add-ons` > `Browse` > 搜索 "Controller Support"
  - 安装并重启

- [ ] 安装 RetroAchievements 插件（可选）
  - `Add-ons` > `Browse` > 搜索 "RetroAchievements"
  - 安装并重启

**验证**: 所有插件在 `Add-ons` > `Installed` 中显示

---

### 1.5 安装和配置主题（30 分钟）

- [ ] 安装 Strata Fullscreen 主题
  - `Add-ons` > `Browse` > `Themes Fullscreen`
  - 搜索 "Strata"
  - 安装

- [ ] 应用主题
  - `Settings` > `Appearance` > `Fullscreen Theme`
  - 选择 "Strata"
  - 保存并重启全屏模式

- [ ] 测试主题
  - 启动 `Playnite.FullscreenApp.exe`
  - 使用手柄导航测试
  - 检查界面美观性

**验证**: 全屏模式显示现代风格界面，手柄导航流畅

---

### ✅ 阶段 1 验收清单

- [ ] E 盘目录结构完整（Games, Emulators, Playnite）
- [ ] D 盘备份目录已创建
- [ ] Playnite 桌面模式和全屏模式都能正常启动
- [ ] 必备插件已安装并配置（IGDB API 密钥已设置）
- [ ] Strata 主题已应用，界面美观
- [ ] 手柄可以导航 Playnite 界面

**完成后**：更新 `BASELINE.md` 记录阶段 1 完成

---

## 🎮 阶段 2：模拟器安装和配置（4-6 小时）

### 2.1 安装 RetroArch（1 小时）

- [ ] 解压 RetroArch 到 `E:\Emulators\RetroArch\`

- [ ] 首次启动 RetroArch
  - 运行 `E:\Emulators\RetroArch\retroarch.exe`
  - 选择语言：**简体中文**
  - 设置驱动程序：
    - 视频驱动：**Vulkan**
    - 音频驱动：**XAudio**
    - 输入驱动：**XInput**

- [ ] 下载核心（Core）
  - `Main Menu` > `Online Updater` > `Core Downloader`
  - 下载以下核心（按顺序）：
    - [ ] Mesen (FC/NES)
    - [ ] Snes9x (SFC/SNES)
    - [ ] Genesis Plus GX (MD/Genesis)
    - [ ] mGBA (GBA)
    - [ ] Mupen64Plus-Next (N64)
    - [ ] Beetle PSX HW (PS1)
    - [ ] PPSSPP (PSP)

**验证**: 进入 `Main Menu` > `Load Core`，确认所有核心已安装

- [ ] 放置 BIOS 文件
  - 复制 BIOS 文件到 `E:\Emulators\RetroArch\system\`
  - 需要的文件：
    - `scph5501.bin` (PS1 BIOS)
    - `gba_bios.bin` (GBA BIOS，可选)

- [ ] 验证 BIOS
  - `Settings` > `Directory` > `System/BIOS`
  - 确认路径为 `E:\Emulators\RetroArch\system\`
  - `Information` > `System Information`
  - 检查 BIOS 是否识别

**验证**: PS1 BIOS 显示为 "Present"

- [ ] 配置视频设置
  - `Settings` > `Video`
  - 视频驱动: **Vulkan**
  - 全屏: **启用**
  - 垂直同步: **启用**
  - 保存配置

- [ ] 配置输入设置
  - `Settings` > `Input` > `Port 1 Controls`
  - 选择设备类型: **RetroPad**
  - 映射手柄按键（使用自动映射或手动映射）

**验证**: 手柄在 RetroArch 菜单中可以导航

- [ ] 配置快捷键
  - `Settings` > `Input` > `Hotkeys`
  - 推荐配置：
    - 菜单切换: **F1**
    - 快速存档: **F2**
    - 快速读档: **F4**
    - 退出模拟器: **Esc**

- [ ] 测试一个游戏（如有 ROM）
  - `Load Content` > 选择一个 ROM 文件
  - 游戏可以正常运行
  - 手柄按键响应正常
  - 退出游戏返回菜单

**验证**: 至少测试一个平台的游戏成功运行

---

### 2.2 安装 PCSX2（45 分钟）

- [ ] 安装 PCSX2 到 `E:\Emulators\PCSX2\`
  - 运行安装程序或解压便携版

- [ ] 首次配置
  - 启动 `E:\Emulators\PCSX2\pcsx2.exe`
  - 选择语言：**简体中文**

- [ ] 放置 PS2 BIOS
  - 复制 PS2 BIOS 文件到 `E:\Emulators\PCSX2\bios\`
  - 文件名示例: `SCPH-39001.bin`

- [ ] 配置 BIOS
  - `Config` > `BIOS Selector`
  - 选择一个 BIOS 作为默认

**验证**: BIOS 列表中显示已识别的 BIOS

- [ ] 配置图形设置
  - `Config` > `Graphics Settings`
  - Renderer: **Vulkan**
  - Internal Resolution: **2x Native** (1280x896)
  - Texture Filtering: **Bilinear (PS2)**
  - Anisotropic Filtering: **16x**
  - Aspect Ratio: **16:9 Widescreen**
  - V-Sync: **On**

- [ ] 配置手柄
  - `Config` > `Controllers`
  - Controller 1 Type: **DualShock 2**
  - 使用 "Automatic Mapping" 映射手柄

**验证**: 手柄按键在配置界面中响应

- [ ] 测试一个 PS2 游戏（如有）
  - `File` > `Boot ISO`
  - 选择 ISO 文件
  - 游戏可以运行

**验证**: PS2 游戏可以启动并运行流畅（目标 60 FPS）

---

### 2.3 安装 Dolphin（45 分钟）

- [ ] 解压 Dolphin 到 `E:\Emulators\Dolphin\`

- [ ] 首次启动
  - 运行 `E:\Emulators\Dolphin\Dolphin.exe`

- [ ] 配置 ROM 路径
  - `Config` > `Paths`
  - 添加路径：`E:\Games\ROMs\NGC\`
  - 添加路径：`E:\Games\ROMs\Wii\`

- [ ] 配置图形设置
  - `Graphics` 或 `Options` > `Graphics Settings`
  - Backend: **Vulkan**
  - Internal Resolution: **3x Native** (1920x1584)
  - Anisotropic Filtering: **16x**
  - V-Sync: **On**
  - Skip EFB Access from CPU: **On**
  - Store EFB Copies to Texture Only: **On**

- [ ] 配置音频
  - `Options` > `Audio Settings`
  - DSP Emulation Engine: **DSP HLE**
  - Backend: **Cubeb**

- [ ] 配置手柄
  - `Controllers`
  - Port 1: **Standard Controller**
  - 使用 "AutoMap" 映射手柄

**验证**: 手柄在配置中响应

- [ ] 测试一个 NGC/Wii 游戏（如有）
  - 双击游戏列表中的游戏
  - 游戏可以运行

**验证**: 游戏流畅运行（目标 60 FPS）

---

### 2.4 安装 Ryujinx（1 小时）

- [ ] 解压 Ryujinx 到 `E:\Emulators\Ryujinx\`

- [ ] 首次启动
  - 运行 `E:\Emulators\Ryujinx\Ryujinx.exe`
  - 选择语言：**简体中文**

- [ ] 放置密钥文件
  - 复制 `prod.keys` 和 `title.keys` 到：
    `E:\Emulators\Ryujinx\portable\system\`

**验证**: 密钥文件存在于正确位置

- [ ] 安装 Switch 固件
  - `Tools` > `Install Firmware`
  - 选择固件 .zip 文件（约 300MB）
  - 等待安装完成（可能需要 5-10 分钟）

**验证**: `Help` > `About` 显示固件版本

- [ ] 配置游戏目录
  - `Options` > `Settings` > `General`
  - Game Directories: 添加 `E:\Games\ROMs\Switch\`

- [ ] 配置图形设置
  - `Options` > `Settings` > `Graphics`
  - Graphics Backend: **Vulkan**
  - Resolution Scale: **1x** (720p/1080p)
  - Max Anisotropy: **16x**
  - Enable Shader Cache: **✓**
  - Enable V-Sync: **✓**

- [ ] 配置手柄
  - `Options` > `Settings` > `Input`
  - Player 1 Controller Type: **Pro Controller**
  - 使用 "AutoMap" 或手动映射

**验证**: 手柄按键响应

- [ ] 测试一个 Switch 游戏（如有）
  - 双击游戏列表中的游戏
  - **注意**: 首次运行会编译着色器，需要等待 10-30 分钟
  - 耐心等待进度完成

**验证**: 游戏可以启动（首次会卡顿，正常现象）

---

### 2.5 安装其他模拟器（1-2 小时）

#### DuckStation (PS1) - 30 分钟

- [ ] 解压到 `E:\Emulators\DuckStation\`
- [ ] 放置 PS1 BIOS 到 `E:\Emulators\DuckStation\bios\`
- [ ] 启动并配置：
  - Renderer: **Vulkan**
  - Resolution: **4x-8x Native**
  - PGXP Geometry Correction: **启用**
- [ ] 映射手柄
- [ ] 测试一个 PS1 游戏

**验证**: PS1 游戏运行流畅

#### Citra (3DS) - 30 分钟（可选）

- [ ] 解压到 `E:\Emulators\Citra\`
- [ ] 启动并配置：
  - Renderer: **OpenGL**
  - Resolution: **2x-3x**
  - Layout: **上下布局**
- [ ] 映射手柄
- [ ] 测试一个 3DS 游戏

**验证**: 3DS 游戏运行正常

#### RPCS3 (PS3) - 1 小时（可选）

- [ ] 解压到 `E:\Emulators\RPCS3\`
- [ ] 安装 PS3 固件：
  - 下载 PS3UPDAT.PUP（约 200MB）
  - `File` > `Install Firmware`
  - 选择固件文件安装
- [ ] 配置：
  - CPU PPU Decoder: **Recompiler (LLVM)**
  - CPU SPU Decoder: **Recompiler (LLVM)**
  - GPU Renderer: **Vulkan**
- [ ] 映射手柄
- [ ] 测试一个 PS3 游戏

**验证**: PS3 游戏可以启动（性能可能不完美）

---

### ✅ 阶段 2 验收清单

- [ ] RetroArch 已安装并配置，至少 7 个核心已下载
- [ ] PCSX2 已安装，BIOS 已识别
- [ ] Dolphin 已安装，ROM 路径已配置
- [ ] Ryujinx 已安装，固件已安装
- [ ] 其他计划安装的模拟器已完成
- [ ] 手柄在所有模拟器中都能正常工作
- [ ] 每个模拟器至少测试运行 1 个游戏成功

**完成后**：更新 `BASELINE.md` 记录阶段 2 完成

---

## 🔗 阶段 3：Playnite 整合（2-3 小时）

### 3.1 配置模拟器连接（1 小时）

- [ ] 打开 Playnite 桌面模式

- [ ] 添加 RetroArch
  - `Settings` (F4) > `Emulators` > `Add` > `Import Installed`
  - 选择 `E:\Emulators\RetroArch\retroarch.exe`
  - 或手动添加：
    - Name: **RetroArch**
    - Installation Folder: `E:\Emulators\RetroArch\`
    - Executable: `retroarch.exe`

- [ ] 配置 RetroArch 平台映射
  - 为每个平台创建配置：

    **FC/NES**:
    - Emulator: RetroArch
    - Arguments: `-L "cores\mesen_libretro.dll" "{ImagePath}"`

    **SFC/SNES**:
    - Emulator: RetroArch
    - Arguments: `-L "cores\snes9x_libretro.dll" "{ImagePath}"`

    **MD/Genesis**:
    - Emulator: RetroArch
    - Arguments: `-L "cores\genesis_plus_gx_libretro.dll" "{ImagePath}"`

    **GBA**:
    - Emulator: RetroArch
    - Arguments: `-L "cores\mgba_libretro.dll" "{ImagePath}"`

    **N64**:
    - Emulator: RetroArch
    - Arguments: `-L "cores\mupen64plus_next_libretro.dll" "{ImagePath}"`

    **PS1**:
    - Emulator: RetroArch
    - Arguments: `-L "cores\beetle_psx_hw_libretro.dll" "{ImagePath}"`

    **PSP**:
    - Emulator: RetroArch
    - Arguments: `-L "cores\ppsspp_libretro.dll" "{ImagePath}"`

- [ ] 添加 PCSX2
  - `Emulators` > `Add`
  - Name: **PCSX2**
  - Installation Folder: `E:\Emulators\PCSX2\`
  - Executable: `pcsx2.exe`
  - Arguments: `--fullscreen --nogui "{ImagePath}"`

- [ ] 添加 Dolphin
  - Name: **Dolphin**
  - Installation Folder: `E:\Emulators\Dolphin\`
  - Executable: `Dolphin.exe`
  - Arguments: `--batch --exec="{ImagePath}"`

- [ ] 添加 Ryujinx
  - Name: **Ryujinx**
  - Installation Folder: `E:\Emulators\Ryujinx\`
  - Executable: `Ryujinx.exe`
  - Arguments: `"{ImagePath}"`

- [ ] 添加其他已安装的模拟器
  - DuckStation, Citra, RPCS3 等
  - 参考设计文档第 5.5 节

**验证**: 所有模拟器在 `Settings` > `Emulators` 列表中显示

---

### 3.2 导入游戏（45 分钟）

- [ ] 使用 Emulators Library 插件扫描
  - `Library` > `Update Game Library`
  - 选择要扫描的平台
  - 等待扫描完成

- [ ] 手动添加测试游戏（如自动扫描失败）
  - `Add Game` > `Manually`
  - 填写游戏信息：
    - Name: 游戏名称
    - Platform: 对应平台
    - Installation Path: ROM 文件路径
    - Play Action > Emulator: 选择对应模拟器
  - 保存

- [ ] 测试从 Playnite 启动游戏
  - 选择一个游戏
  - 点击 "Play" 或按 Enter
  - 游戏应该通过对应模拟器启动

**验证**: 至少 3 个不同平台的游戏可以从 Playnite 成功启动

---

### 3.3 元数据刮削（45 分钟）

- [ ] 自动下载元数据
  - 选中多个游戏（Ctrl + A 全选）
  - 右键 > `Edit` > `Download Metadata`
  - 选择数据源: **IGDB**
  - 勾选：
    - ✓ Download cover images
    - ✓ Download background images
    - ✓ Download game description
    - ✓ Download release date
  - 点击 "Download"
  - 等待完成（可能需要 10-20 分钟）

**验证**: 游戏库中大部分游戏显示封面和信息

- [ ] 手动修正错误匹配
  - 检查封面不正确的游戏
  - 右键 > `Edit` > `Download Metadata`
  - 搜索正确的游戏名称
  - 选择正确的匹配项

---

### 3.4 添加应用程序（30 分钟）

- [ ] 添加 Microsoft Edge（浏览器）
  - `Add Game` > `Manually`
  - Name: **浏览器** 或 **Web Browser**
  - Platform: **PC (Windows)**
  - Installation Folder: `C:\Program Files (x86)\Microsoft\Edge\Application\`
  - Executable: `msedge.exe`
  - Arguments: `--kiosk --start-fullscreen`（可选，全屏浏览）
  - 添加自定义图标（Edge 图标）
  - Category: **应用程序**
  - Tags: **娱乐, 工具**

- [ ] 添加网易云音乐
  - Name: **网易云音乐**
  - Installation Folder: [网易云安装路径]
  - Executable: `cloudmusic.exe`
  - 添加网易云图标
  - Category: **应用程序**
  - Tags: **音乐, 娱乐**

- [ ] 添加哔哩哔哩客户端
  - Name: **哔哩哔哩**
  - Installation Folder: [哔哩哔哩安装路径]
  - Executable: `哔哩哔哩.exe`
  - 添加 B 站图标
  - Category: **应用程序**
  - Tags: **视频, 娱乐**

- [ ] 添加极空间
  - Name: **极空间**
  - Installation Folder: [极空间安装路径]
  - Executable: `JiKongJian.exe`
  - 添加极空间图标
  - Category: **应用程序**
  - Tags: **工具, 存储**

- [ ] 测试应用程序启动
  - 从 Playnite 启动每个应用
  - 确认可以正常打开

**验证**: 所有应用程序可以从 Playnite 启动

---

### 3.5 创建分类和筛选器（15 分钟）

- [ ] 创建自定义类别
  - `Settings` > `Library` > `Categories`
  - 添加类别：
    - **PC游戏**
    - **模拟器游戏**
    - **应用程序**

- [ ] 为游戏分配类别
  - 选中相关游戏
  - 右键 > `Edit` > `Categories`
  - 勾选对应类别

- [ ] 创建自定义标签
  - 例如：单人、多人、RPG、动作、休闲等
  - 批量编辑游戏添加标签

- [ ] 配置筛选器
  - 在全屏模式中测试：
  - 使用 LB/RB 切换类别
  - 测试平台筛选
  - 测试标签筛选

**验证**: 筛选器可以快速过滤游戏

---

### ✅ 阶段 3 验收清单

- [ ] 所有模拟器已添加到 Playnite
- [ ] 游戏可以从 Playnite 直接启动（不报错）
- [ ] 游戏封面和元数据显示正确（至少 80%）
- [ ] 应用程序（浏览器、音乐、视频）可以启动
- [ ] 分类和筛选器正常工作
- [ ] 游戏时长开始记录

**完成后**：更新 `BASELINE.md` 记录阶段 3 完成

---

## 🎨 阶段 4：界面优化和自动化（1-2 小时）

### 4.1 全屏模式界面定制（30 分钟）

- [ ] 启动全屏模式
  - 运行 `E:\Playnite\Playnite.FullscreenApp.exe`

- [ ] 调整界面设置
  - 按 `Guide` 键（或 `F4`）打开菜单
  - 进入 `Settings`

- [ ] 配置显示
  - 游戏展示: **网格视图 (Grid)**
  - 封面尺寸: **大 (Large)**
  - 默认排序: **最近游玩** 或 **按名称**

- [ ] 配置筛选器显示
  - 启用平台筛选
  - 启用类别筛选
  - 隐藏已隐藏的游戏

- [ ] 测试导航
  - 使用手柄 LB/RB 切换类别
  - 测试响应速度
  - 确认界面流畅

**验证**: 界面美观，导航流畅（响应 < 1 秒）

---

### 4.2 手柄优化（30 分钟）

- [ ] 配置全局快捷键
  - 在 Playnite 全屏模式设置中：
  - Guide + Start: **关闭游戏**
  - Guide + Back: **切换桌面模式**（如需要）
  - Guide + Y: **搜索**

- [ ] 测试手柄功能
  - 导航游戏列表
  - 启动游戏
  - 游戏内使用手柄
  - 退出游戏返回 Playnite
  - 测试快捷键

- [ ] 调整灵敏度（如需要）
  - 摇杆死区设置
  - 按键延迟设置

**验证**: 手柄操作流畅，无明显延迟或卡顿

---

### 4.3 配置自动启动（30 分钟）

- [ ] 创建启动脚本
  - 在 `C:\Users\[您的用户名]\` 创建文件 `startup-playnite.bat`
  - 内容如下：

```batch
@echo off
:: Playnite 自动启动脚本

:: 等待 15 秒确保系统完全启动
timeout /t 15 /nobreak >nul

:: 启动 Playnite 全屏模式
start "" "E:\Playnite\Playnite.FullscreenApp.exe"

exit
```

- [ ] 保存文件

- [ ] 添加到 Windows 启动项（方法 1：简单）
  - 按 `Win + R`
  - 输入 `shell:startup`
  - 将 `startup-playnite.bat` 复制到打开的文件夹

**验证**: 重启电脑，检查 Playnite 是否自动启动

**或者使用任务计划程序（方法 2：推荐）**:

- [ ] 打开任务计划程序
  - 按 `Win + R`
  - 输入 `taskschd.msc`

- [ ] 创建基本任务
  - 右键 "任务计划程序库" > "创建基本任务"
  - 名称: **Playnite 自动启动**
  - 描述: **开机自动启动 Playnite 全屏模式**
  - 触发器: **用户登录时**
  - 延迟任务: **15 秒**
  - 操作: **启动程序**
  - 程序/脚本: `C:\Users\[您的用户名]\startup-playnite.bat`
  - 完成

- [ ] 测试任务
  - 右键任务 > **运行**
  - 检查 Playnite 是否启动

**验证**: 手动运行任务成功启动 Playnite

- [ ] 重启电脑测试
  - 完全重启系统
  - 等待 15 秒
  - Playnite 应自动进入全屏模式

**验证**: 开机自动启动成功

---

### 4.4 添加退出机制（15 分钟）

- [ ] 方法 1：添加"退出到桌面"快捷方式
  - 在 Playnite 中 `Add Game` > `Manually`
  - Name: **退出到桌面**
  - Executable: `C:\Windows\explorer.exe`
  - Category: **系统**
  - 保存

- [ ] 测试退出
  - 在全屏模式中选择"退出到桌面"
  - 应该返回 Windows 桌面

**验证**: 可以从 Playnite 退出到桌面

---

### ✅ 阶段 4 验收清单

- [ ] 全屏模式界面美观，符合现代风格
- [ ] 手柄操作流畅，无明显延迟
- [ ] 开机自动进入 Playnite 全屏模式
- [ ] 可以方便地退出到 Windows 桌面
- [ ] 所有快捷键正常工作
- [ ] 从启动到进入界面 < 30 秒

**完成后**：更新 `BASELINE.md` 记录阶段 4 完成

---

## 💾 阶段 5：备份和测试（1-2 小时）

### 5.1 配置备份系统（45 分钟）

- [ ] 创建备份脚本
  - 在 `D:\Backups\Gaming\` 创建文件 `backup-gaming.bat`
  - 复制以下内容：

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

:: 备份 Playnite 库
echo 备份 Playnite 库... >> "%LOGFILE%"
robocopy "%SOURCE_ROOT%\Playnite\library" "%BACKUP_ROOT%\Playnite\library" /MIR /R:3 /W:5 /LOG+:"%LOGFILE%"

:: 备份 RetroArch 存档
echo 备份 RetroArch 存档... >> "%LOGFILE%"
robocopy "%SOURCE_ROOT%\Emulators\RetroArch\saves" "%BACKUP_ROOT%\Saves\RetroArch" /MIR /R:3 /W:5 /LOG+:"%LOGFILE%"

:: 备份 PCSX2 记忆卡
echo 备份 PCSX2 记忆卡... >> "%LOGFILE%"
robocopy "%SOURCE_ROOT%\Emulators\PCSX2\memcards" "%BACKUP_ROOT%\Saves\PCSX2" /MIR /R:3 /W:5 /LOG+:"%LOGFILE%"

:: 备份 Dolphin 存档
echo 备份 Dolphin 存档... >> "%LOGFILE%"
robocopy "%SOURCE_ROOT%\Emulators\Dolphin\User\Saves" "%BACKUP_ROOT%\Saves\Dolphin" /MIR /R:3 /W:5 /LOG+:"%LOGFILE%"

:: 备份 Ryujinx 存档
echo 备份 Ryujinx 存档... >> "%LOGFILE%"
robocopy "%SOURCE_ROOT%\Emulators\Ryujinx\portable\bis\user\save" "%BACKUP_ROOT%\Saves\Ryujinx" /MIR /R:3 /W:5 /LOG+:"%LOGFILE%"

echo ================================================ >> "%LOGFILE%"
echo 备份完成时间: %date% %time% >> "%LOGFILE%"
echo ================================================ >> "%LOGFILE%"

exit /b 0
```

- [ ] 保存文件

- [ ] 测试备份脚本
  - 双击 `backup-gaming.bat` 运行
  - 等待完成
  - 检查 `D:\Backups\Gaming\` 目录
  - 查看日志文件确认备份成功

**验证**: 备份目录中有 Playnite 库和模拟器存档

- [ ] 配置自动备份任务
  - 打开任务计划程序
  - 创建基本任务：
    - 名称: **游戏数据自动备份**
    - 触发器: **每周日凌晨 3:00**
    - 操作: `D:\Backups\Gaming\backup-gaming.bat`
  - 保存

**验证**: 任务已创建，可以手动运行测试

---

### 5.2 全面功能测试（45 分钟）

- [ ] 测试每个平台的游戏（每个平台 2-3 个）

  **RetroArch 平台**:
  - [ ] FC/NES 游戏运行正常
  - [ ] SFC/SNES 游戏运行正常
  - [ ] MD/Genesis 游戏运行正常
  - [ ] GBA 游戏运行正常
  - [ ] N64 游戏运行正常（可能有掉帧）
  - [ ] PS1 游戏运行正常
  - [ ] PSP 游戏运行正常

  **独立模拟器**:
  - [ ] PS2 游戏运行正常（PCSX2）
  - [ ] NGC 游戏运行正常（Dolphin）
  - [ ] Wii 游戏运行正常（Dolphin）
  - [ ] 3DS 游戏运行正常（Citra）
  - [ ] Switch 游戏运行正常（Ryujinx）

- [ ] 测试存档功能
  - [ ] 游戏内存档保存成功
  - [ ] 退出游戏后重新加载存档
  - [ ] RetroArch 快速存档（F2）和读档（F4）

**验证**: 存档可以正常保存和读取

- [ ] 测试应用程序
  - [ ] 浏览器可以打开
  - [ ] 网易云音乐可以播放
  - [ ] 哔哩哔哩可以观看视频
  - [ ] 极空间可以访问文件

**验证**: 所有应用程序功能正常

- [ ] 测试手柄功能
  - [ ] 所有按键响应正常
  - [ ] 摇杆精确无漂移
  - [ ] 震动功能（如支持）
  - [ ] 多人游戏（如有第二个手柄）

**验证**: 手柄功能完整

---

### 5.3 性能验证（30 分钟）

- [ ] 监控系统资源
  - 打开任务管理器（Ctrl + Shift + Esc）
  - 切换到"性能"选项卡

  **空闲状态检查**:
  - [ ] 内存使用 < 10 GB
  - [ ] CPU 使用率 < 10%

  **游戏运行检查**（运行一个中等负载游戏）:
  - [ ] 内存使用 < 30 GB
  - [ ] CPU 使用率合理（< 80%）
  - [ ] GPU 使用率显示（集显）

**验证**: 资源使用在正常范围内

- [ ] 检查温度（可选）
  - 如安装了 HWiNFO64 或其他监控工具
  - CPU 温度 < 75°C（游戏中）

- [ ] 验证游戏帧率
  - 使用模拟器内置 FPS 显示
  - 或使用 MSI Afterburner + RivaTuner

  **预期性能**（参考设计文档 7.7.2）:
  - [ ] FC/SFC/MD/GBA: 60 FPS 满速
  - [ ] PS2 大部分游戏: 60 FPS
  - [ ] NGC/Wii: 60 FPS
  - [ ] Switch 主流游戏: 30 FPS 可玩

**验证**: 性能符合预期

---

### 5.4 长时间稳定性测试（可选）

- [ ] 连续运行测试（1-2 小时）
  - 启动 Playnite
  - 游玩几个不同的游戏
  - 切换游戏多次（至少 10 次）
  - 观察是否有崩溃或卡死

**验证**: 系统稳定，无崩溃

---

### 5.5 更新文档（30 分钟）

- [ ] 更新 `BASELINE.md`
  - 记录所有已安装的软件和版本
  - 更新项目进度为"已完成"
  - 记录任何遇到的问题和解决方案
  - 记录配置参数

- [ ] 创建快速参考指南（可选）
  - 常用快捷键
  - 常见问题解决方案
  - 备份恢复步骤

---

### ✅ 阶段 5 验收清单

- [ ] 备份系统配置完成，自动任务已创建
- [ ] 所有测试游戏运行稳定，无崩溃
- [ ] 系统性能符合预期（见设计文档 7.7.2）
- [ ] 手柄所有功能正常
- [ ] 应用程序全部可用
- [ ] 文档已更新（BASELINE.md）

**完成后**：项目部署完成！

---

## ✅ 最终验收清单

### 功能性验收

- [ ] 可以从 Playnite 启动所有类型的游戏
- [ ] 手柄在 Playnite 和所有模拟器中正常工作
- [ ] 开机自动进入 Playnite 全屏模式
- [ ] 可以访问浏览器和应用程序
- [ ] 游戏存档正常保存和读取

### 用户体验验收

- [ ] 界面美观现代
- [ ] 操作响应迅速（< 1 秒）
- [ ] 游戏封面和信息完整
- [ ] 导航逻辑清晰直观

### 性能验收

- [ ] 经典平台游戏 60 FPS 满速
- [ ] PS2/NGC/Wii 游戏流畅（60 FPS）
- [ ] Switch 游戏可玩（30 FPS+）
- [ ] 内存使用 < 40GB
- [ ] CPU 温度 < 75°C

### 可靠性验收

- [ ] 连续运行 2 小时无崩溃
- [ ] 切换游戏 10 次以上无问题
- [ ] 重启系统后正常进入
- [ ] 备份系统正常工作

---

## 🔧 故障排除快速索引

### Playnite 问题

**Playnite 无法启动**:
1. 检查 .NET 6.0 运行库是否安装
2. 尝试删除 `E:\Playnite\library\*.db` 后从备份恢复
3. 检查文件夹权限

**游戏无法启动**:
1. 检查模拟器路径是否正确
2. 检查 ROM 文件是否存在
3. 尝试直接用模拟器打开 ROM 测试

**封面不显示**:
1. 重新下载元数据
2. 清理缓存：删除 `E:\Playnite\cache\`
3. 检查 IGDB API 配额

### RetroArch 问题

**游戏黑屏**:
1. 检查核心是否正确加载
2. 尝试切换视频驱动（Vulkan ↔ OpenGL）
3. 检查 BIOS 是否存在（PS1 等）

**手柄不响应**:
1. 重新映射手柄
2. 检查输入驱动设置
3. 测试手柄在 Windows 中是否正常

### PCSX2 问题

**游戏卡顿**:
1. 降低内部分辨率（2x → 1x）
2. 降低 Blending Accuracy
3. 关闭 Anisotropic Filtering

### Dolphin 问题

**音频爆音**:
1. 更换音频后端（Cubeb → OpenAL）
2. 调整 DSP 设置
3. 启用 V-Sync

### Ryujinx 问题

**首次运行很卡**:
- 这是正常现象（着色器编译）
- 耐心等待 10-30 分钟
- 第二次运行会流畅

**游戏无法启动**:
1. 检查固件是否安装
2. 检查密钥文件是否正确
3. 查看控制台错误信息

### 系统性能问题

**整体卡顿**:
1. 检查 CPU 温度（任务管理器）
2. 关闭后台程序
3. 检查磁盘空间

**磁盘空间不足**:
1. 清理不玩的游戏
2. 清理模拟器缓存
3. 清理旧的即时存档

### 自动启动问题

**开机不自动启动**:
1. 检查启动脚本路径
2. 检查任务计划程序配置
3. 增加延迟时间（15秒 → 30秒）

---

## 📚 参考文档

- **详细设计文档**: `docs/superpowers/specs/2026-03-24-playnite-gaming-frontend-design.md`
- **环境基线文档**: `BASELINE.md`
- **临时需求文档**: `playnite-requirements-temp.md`

---

## 📝 执行记录

### 开始日期
- [ ] 记录开始日期: __________

### 完成日期
- [ ] 阶段 1 完成: __________
- [ ] 阶段 2 完成: __________
- [ ] 阶段 3 完成: __________
- [ ] 阶段 4 完成: __________
- [ ] 阶段 5 完成: __________
- [ ] 项目完成: __________

### 总耗时
- 预计: 12-16 小时
- 实际: __________ 小时

### 遇到的问题
```
记录遇到的主要问题和解决方案：

1.

2.

3.

```

---

## ✨ 完成后的后续工作

- [ ] 添加更多游戏和 ROM
- [ ] 定期执行备份（每周日自动）
- [ ] 每月检查软件更新
- [ ] 优化游戏分类和标签
- [ ] 探索更多 Playnite 主题和插件
- [ ] 配置远程串流（如 Steam Link）

---

**祝您游戏愉快！** 🎮

如有问题，请参考详细设计文档或故障排除指南。
