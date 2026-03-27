# 完全免费的游戏串流方案

> **目标**: 替代 Parsec 的完全免费游戏串流方案
> **日期**: 2026-03-27
> **需求**: 零成本、无限制、游戏优化

---

## 目录
- [方案对比](#方案对比)
- [推荐方案 1: Moonlight + Sunshine](#推荐方案-1-moonlight--sunshine)
- [推荐方案 2: Rustdesk](#推荐方案-2-rustdesk)
- [方案对比总结](#方案对比总结)

---

## 方案对比

### 快速决策矩阵

| 方案 | 费用 | 游戏性能 | 延迟 | 设置难度 | 远程访问 | 推荐度 |
|------|------|----------|------|----------|----------|--------|
| **Moonlight + Sunshine** ⭐ | 完全免费 | ⭐⭐⭐⭐⭐ | < 5ms | 中 | ⭐⭐⭐ | ⭐⭐⭐⭐⭐ |
| **Rustdesk** | 完全免费 | ⭐⭐⭐⭐ | 10-20ms | 简单 | ⭐⭐⭐⭐⭐ | ⭐⭐⭐⭐ |
| Parsec 免费版 | 免费* | ⭐⭐⭐⭐⭐ | < 5ms | 简单 | ⭐⭐⭐⭐⭐ | ⭐⭐⭐⭐ |
| Steam Remote Play | 完全免费 | ⭐⭐⭐⭐ | 5-15ms | 简单 | ⭐⭐⭐ | ⭐⭐⭐ |

**说明**: Parsec 免费版可能有会话时长限制

---

## 推荐方案 1: Moonlight + Sunshine ⭐ 最佳免费方案

### 概述

**Moonlight + Sunshine** 是完全免费开源的游戏串流解决方案：
- **Moonlight**: 客户端（支持 Windows/Mac/Linux/Android/iOS）
- **Sunshine**: 服务端（替代 NVIDIA GameStream）

### 核心优势

✅ **完全免费开源**
- 无任何费用
- 无功能限制
- 无时长限制
- 无账号注册

✅ **极致性能**
- 延迟 < 5ms（局域网）
- 支持 4K 120fps
- H.265/AV1 编码
- GPU 硬件加速

✅ **游戏优化**
- 专为游戏设计
- 支持手柄输入
- 支持 HDR
- 低延迟模式

❌ **限制**
- 配置稍复杂（需手动设置）
- 远程访问需要端口转发或 VPN
- 不支持 AMD GPU 硬件编码（需 NVIDIA/Intel）

---

## Moonlight + Sunshine 部署

### 服务端配置（铭凡 UM773）

#### 步骤 1: 下载安装 Sunshine

**下载地址**:
```
GitHub: https://github.com/LizardByte/Sunshine/releases
版本: 最新稳定版（Windows x64）
大小: 约 40MB
```

**安装步骤**:
```
1. 下载 Sunshine-Windows.exe
2. 运行安装程序
3. 选择安装路径
4. 完成安装
5. 启动 Sunshine（自动在托盘）
```

#### 步骤 2: 配置 Sunshine

**访问 Web 界面**:
```
浏览器打开: https://localhost:47990
默认用户名: admin
默认密码: admin（首次登录后修改）
```

**基础配置**:
```
1. Configuration → Video
   - Encoder: H.265 (HEVC)
   - Resolution: 1920x1080
   - FPS: 60
   - Bitrate: 20000 Kbps（局域网可更高）

2. Configuration → Audio
   - Audio Sink: 默认设备
   - Codec: Opus

3. Configuration → Input
   - ✅ Enable Gamepad
   - ✅ Enable Keyboard
   - ✅ Enable Mouse

4. Configuration → Network
   - Port: 47989（默认）
   - ✅ Enable UPnP（局域网自动发现）
```

#### 步骤 3: 添加应用

**添加游戏/应用**:
```
1. Applications → Add New
2. 填写信息：
   - Application Name: Playnite（或游戏名）
   - Command: C:\Path\To\Playnite.exe
   - Working Directory: C:\Path\To\
   - Image: 封面图片（可选）
3. 保存
```

**预配置应用示例**:
```yaml
# 桌面
- Name: Desktop
  Command: explorer.exe

# Playnite
- Name: Playnite
  Command: C:\Program Files\Playnite\Playnite.FullscreenApp.exe

# Steam Big Picture
- Name: Steam
  Command: steam://open/bigpicture
```

#### 步骤 4: 配置防火墙

**允许 Sunshine 端口**:
```powershell
# PowerShell（管理员）
New-NetFirewallRule -DisplayName "Sunshine" -Direction Inbound -Protocol TCP -LocalPort 47989,47990 -Action Allow
New-NetFirewallRule -DisplayName "Sunshine UDP" -Direction Inbound -Protocol UDP -LocalPort 47998,47999,48000,48010 -Action Allow
```

---

### 客户端配置（联想 ThinkBook+）

#### 步骤 1: 下载安装 Moonlight

**下载地址**:
```
官网: https://moonlight-stream.org/
GitHub: https://github.com/moonlight-stream/moonlight-qt/releases
版本: Windows x64
大小: 约 30MB
```

**安装步骤**:
```
1. 下载 MoonlightSetup.exe
2. 运行安装程序
3. 完成安装
4. 启动 Moonlight
```

#### 步骤 2: 配对服务器

**自动发现（局域网）**:
```
1. 启动 Moonlight
2. 自动扫描局域网
3. 显示 "铭凡 UM773"（或主机名）
4. 点击主机图标
5. 输入 PIN 码（显示在服务端）
6. 配对成功
```

**手动添加（如自动发现失败）**:
```
1. 点击 "+" 添加主机
2. 输入 IP：192.168.x.x（铭凡 IP）
3. 点击添加
4. 输入 PIN 码配对
```

#### 步骤 3: 启动游戏

```
1. 打开 Moonlight
2. 选择主机
3. 选择应用（桌面/Playnite/游戏）
4. 点击启动
5. 等待连接（2-5 秒）
6. 开始游戏
```

#### 步骤 4: 快捷键

**退出串流**:
```
Ctrl + Alt + Shift + Q
```

**显示统计**:
```
Ctrl + Alt + Shift + S
```

**全屏切换**:
```
Ctrl + Alt + Shift + F
```

---

## 推荐方案 2: Rustdesk

### 概述

**Rustdesk** 是完全免费开源的远程桌面软件：
- 类似 TeamViewer，但完全免费
- 无功能限制
- 支持游戏（性能略逊于 Moonlight）

### 核心优势

✅ **完全免费开源**
- 零成本
- 无限制
- 无广告

✅ **简单易用**
- 5 分钟部署
- 自动穿透
- 无需配置

✅ **远程访问强**
- P2P 连接
- 自动中继
- 跨平台

❌ **限制**
- 游戏性能不如 Moonlight
- 延迟稍高（10-20ms）
- 画质略逊

---

## Rustdesk 部署

### 服务端配置（铭凡 UM773）

#### 步骤 1: 下载安装

**下载地址**:
```
官网: https://rustdesk.com/
GitHub: https://github.com/rustdesk/rustdesk/releases
版本: Windows x64
大小: 约 20MB
```

**安装步骤**:
```
1. 下载 rustdesk-1.x.x-x86_64.exe
2. 运行安装程序
3. 完成安装（自动启动）
```

#### 步骤 2: 配置

**获取 ID**:
```
1. 打开 Rustdesk
2. 查看窗口中央的 "您的桌面 ID"
3. 记录 ID（例如：123456789）
4. 设置密码（可选，推荐）
```

**启用无人值守**（可选）:
```
1. 点击 "设置"
2. 安全 → 启用 "允许使用永久密码"
3. 设置永久密码
4. ✅ 启用 "启用键盘/鼠标"
5. ✅ 启用 "启用剪贴板"
6. ✅ 启用 "启用文件传输"
```

---

### 客户端配置（联想 ThinkBook+）

#### 步骤 1: 安装 Rustdesk

```
下载并安装 Rustdesk（同服务端）
```

#### 步骤 2: 连接

**方式 1: ID 连接**
```
1. 打开 Rustdesk
2. 输入铭凡的 ID（123456789）
3. 点击 "连接"
4. 输入密码（如已设置）
5. 连接成功
```

**方式 2: 地址簿**
```
1. 点击 "地址簿"
2. 添加新连接：
   - 名称: 铭凡 UM773
   - ID: 123456789
   - 密码: [保存密码]
3. 保存
4. 双击连接
```

#### 步骤 3: 游戏模式

**优化游戏性能**:
```
连接后：
1. 右键菜单 → 显示
2. 选择 "质量优先"
3. ✅ 启用 "直接连接"（局域网）
4. 帧率: 60fps
```

---

## 方案对比总结

### 使用场景推荐

#### 场景 1: 主要玩游戏（推荐 Moonlight + Sunshine）

**优势**:
- ✅ 游戏性能最强
- ✅ 延迟最低（< 5ms）
- ✅ 支持 4K 120fps
- ✅ 完全免费无限制

**劣势**:
- ⚠️ 配置稍复杂（10-15 分钟）
- ⚠️ 远程访问需要 VPN

**适合**:
- 经常玩游戏
- 对性能要求高
- 局域网为主

---

#### 场景 2: 偶尔玩游戏 + 远程访问（推荐 Rustdesk）

**优势**:
- ✅ 简单易用（5 分钟）
- ✅ 自动穿透（无需 VPN）
- ✅ 完全免费无限制
- ✅ 游戏性能尚可

**劣势**:
- ⚠️ 游戏性能不如 Moonlight
- ⚠️ 延迟稍高（10-20ms）

**适合**:
- 偶尔玩游戏
- 需要远程访问
- 追求简单

---

#### 场景 3: 混合方案（推荐 Windows RDP + Moonlight）

**方案**:
- **日常操作**（90%）：Windows RDP
- **游戏场景**（10%）：Moonlight + Sunshine

**优势**:
- ✅ 日常操作最优（RDP）
- ✅ 游戏性能最强（Moonlight）
- ✅ 完全免费
- ✅ 各取所长

**劣势**:
- ⚠️ 需要安装两套软件
- ⚠️ 配置稍复杂

**适合**:
- 追求极致体验
- 不介意多装软件
- 局域网为主

---

## 性能对比

### 延迟测试（局域网）

| 方案 | 延迟 | 帧率 | 画质 | CPU 占用 |
|------|------|------|------|----------|
| Moonlight + Sunshine | 3-5ms | 60-120fps | 极高 | 中 |
| Rustdesk | 10-20ms | 30-60fps | 高 | 中 |
| Parsec 免费版 | 3-8ms | 60fps | 极高 | 中 |
| Windows RDP | 5-10ms | 30fps | 中-高 | 低 |

### 带宽占用

| 方案 | 1080p 60fps | 4K 60fps |
|------|-------------|----------|
| Moonlight (H.265) | 10-20 Mbps | 30-50 Mbps |
| Rustdesk | 5-15 Mbps | 15-30 Mbps |
| Parsec | 10-30 Mbps | 30-80 Mbps |

---

## 成本对比

### 完全免费方案

| 方案 | 费用 | 功能限制 | 时长限制 | 广告 |
|------|------|----------|----------|------|
| **Moonlight + Sunshine** | 免费 | 无 | 无 | 无 |
| **Rustdesk** | 免费 | 无 | 无 | 无 |
| Windows RDP | 免费 | 无 | 无 | 无 |
| Steam Remote Play | 免费 | 需 Steam | 无 | 无 |

### 付费方案对比

| 方案 | 费用 | 额外功能 |
|------|------|----------|
| Parsec Teams | $30/月 | 团队协作、无限客户端 |
| ToDesk 专业版 | ¥180/年 | 无广告、文件传输 |
| TeamViewer | $49/月 | 商业授权 |

**结论**: 完全免费方案完全够用，无需付费。

---

## 推荐部署策略

### 方案 A: 极简方案（推荐新手）⏱️ 10 分钟

```
1. 安装 Windows RDP（5 分钟）
   - 日常操作

2. 安装 Rustdesk（5 分钟）
   - 游戏场景
   - 远程访问
```

**优势**:
- ✅ 最简单
- ✅ 覆盖所有场景
- ✅ 完全免费

---

### 方案 B: 性能方案（推荐游戏玩家）⏱️ 20 分钟

```
1. 安装 Windows RDP（5 分钟）
   - 日常操作

2. 安装 Moonlight + Sunshine（15 分钟）
   - 游戏场景
   - 极致性能

3. （可选）安装 Tailscale VPN（5 分钟）
   - 远程访问
```

**优势**:
- ✅ 游戏性能最强
- ✅ 完全免费
- ✅ 体验最佳

---

### 方案 C: 万能方案 ⏱️ 25 分钟

```
1. 安装 Windows RDP（5 分钟）
2. 安装 Moonlight + Sunshine（15 分钟）
3. 安装 Rustdesk（5 分钟）
```

**优势**:
- ✅ 所有场景覆盖
- ✅ 多方案备选
- ✅ 完全免费

**使用策略**:
- 日常操作 → RDP
- 游戏场景（局域网）→ Moonlight
- 游戏场景（远程）→ Rustdesk
- 简单远程 → Rustdesk

---

## 快速开始

### Moonlight + Sunshine 快速部署

**服务端（铭凡）**:
```bash
1. 下载 Sunshine: https://github.com/LizardByte/Sunshine/releases
2. 安装并启动
3. 浏览器打开: https://localhost:47990
4. 配置视频: H.265, 1080p, 60fps
5. 添加应用: Playnite/Desktop
```

**客户端（ThinkBook+）**:
```bash
1. 下载 Moonlight: https://moonlight-stream.org/
2. 安装并启动
3. 自动发现铭凡主机
4. 配对（输入 PIN）
5. 选择应用启动
```

---

### Rustdesk 快速部署

**服务端（铭凡）**:
```bash
1. 下载 Rustdesk: https://rustdesk.com/
2. 安装并启动
3. 记录桌面 ID
4. 设置密码
```

**客户端（ThinkBook+）**:
```bash
1. 下载安装 Rustdesk
2. 输入铭凡 ID
3. 输入密码
4. 连接
```

---

## 故障排除

### Moonlight 无法发现服务器

**原因**: 防火墙阻止或不在同一网络

**解决**:
```powershell
# 1. 检查防火墙（铭凡）
Get-NetFirewallRule -DisplayName "Sunshine"

# 2. 允许端口
New-NetFirewallRule -DisplayName "Sunshine" -Direction Inbound -Protocol TCP -LocalPort 47989,47990 -Action Allow

# 3. 手动添加主机
Moonlight 客户端 → "+" → 输入 IP
```

---

### Rustdesk 延迟高

**原因**: 使用了公共中继服务器

**解决**:
```
1. 确认局域网连接
2. 启用 "直接连接"
3. 设置 → 网络 → 选择最近的中继服务器
4. 或部署自己的中继服务器（高级）
```

---

## 总结

### 最佳免费方案组合 ⭐

```
Windows RDP（日常）+ Moonlight + Sunshine（游戏）
```

**原因**:
- ✅ 完全免费无限制
- ✅ 性能最强
- ✅ 覆盖所有场景
- ✅ 开源可控

**成本**: ¥0
**部署时间**: 20 分钟
**推荐度**: ⭐⭐⭐⭐⭐

---

**文档版本**: v1.0
**创建日期**: 2026-03-27
**下一步**: 选择方案并开始部署 🚀
