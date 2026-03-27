# 免费游戏串流快速开始 🎮

> **10 分钟部署完全免费的游戏串流方案**
>
> **方案**: Moonlight + Sunshine（开源免费）
> **替代**: Parsec（付费）

---

## 📋 前提条件

- ✅ 铭凡 UM773：Windows 11
- ✅ 联想 ThinkBook+：Windows 11
- ✅ 两台设备在同一局域网
- ✅ 显卡：NVIDIA/Intel（AMD 可用但性能稍差）
- ⏱️ 预计时间：10-15 分钟

---

## 🎯 2 步快速部署

### 第 1 步：服务端配置（铭凡 UM773）⏱️ 5-8 分钟

#### 1.1 下载安装 Sunshine

```
1. 打开浏览器
2. 访问：https://github.com/LizardByte/Sunshine/releases
3. 下载最新版：Sunshine-Windows.exe（约 40MB）
4. 运行安装程序
5. 完成安装（自动启动）
```

#### 1.2 配置 Sunshine

```
1. 浏览器打开：https://localhost:47990
2. 首次登录：
   - 用户名：admin
   - 密码：admin
   - 立即修改密码（重要！）

3. Configuration → Video：
   - Encoder: H.265 (HEVC)
   - Resolution: 1920x1080
   - FPS: 60
   - Bitrate: 20000 Kbps

4. Configuration → Input：
   - ✅ Enable Gamepad
   - ✅ Enable Keyboard
   - ✅ Enable Mouse
```

#### 1.3 添加应用

```
Applications → Add New:

应用 1 - 桌面：
  - Name: Desktop
  - Command: mstsc.exe /v:localhost

应用 2 - Playnite 全屏：
  - Name: Playnite
  - Command: C:\Program Files\Playnite\Playnite.FullscreenApp.exe

应用 3 - Steam Big Picture：
  - Name: Steam
  - Command: steam://open/bigpicture
```

#### 1.4 配置防火墙

```powershell
# 打开 PowerShell（管理员）
# 复制粘贴以下命令：

New-NetFirewallRule -DisplayName "Sunshine TCP" -Direction Inbound -Protocol TCP -LocalPort 47989,47990 -Action Allow
New-NetFirewallRule -DisplayName "Sunshine UDP" -Direction Inbound -Protocol UDP -LocalPort 47998,47999,48000,48010 -Action Allow
```

✅ 服务端配置完成！

---

### 第 2 步：客户端配置（联想 ThinkBook+）⏱️ 3-5 分钟

#### 2.1 下载安装 Moonlight

```
1. 访问：https://moonlight-stream.org/
2. 下载 Windows 版本（约 30MB）
3. 安装并启动 Moonlight
```

#### 2.2 配对服务器

```
自动发现（局域网）：
1. Moonlight 自动扫描局域网
2. 显示 "铭凡 UM773"（或你的主机名）
3. 点击主机图标
4. 输入 PIN 码（显示在铭凡的 Sunshine 界面）
5. 配对成功 ✅

手动添加（如自动发现失败）：
1. 点击 "+" 添加主机
2. 输入铭凡 IP：192.168.x.x
3. 配对
```

#### 2.3 启动游戏

```
1. Moonlight 中选择主机
2. 选择应用：
   - Desktop（桌面）
   - Playnite（游戏中心）
   - Steam（Steam 游戏）
3. 点击启动
4. 等待连接（2-5 秒）
5. 开始游戏 🎮
```

✅ 完成！现在可以开始游戏了

---

## ⌨️ 快捷键

```
Ctrl + Alt + Shift + Q  退出串流
Ctrl + Alt + Shift + S  显示统计（延迟、帧率）
Ctrl + Alt + Shift + F  全屏切换
```

---

## 🎮 使用场景

### 场景 1：玩 Playnite 游戏

```
1. Moonlight → 铭凡主机
2. 选择 "Playnite"
3. 进入全屏游戏中心
4. 选择游戏开始
```

### 场景 2：玩 Steam 游戏

```
1. Moonlight → 铭凡主机
2. 选择 "Steam"
3. 进入 Steam Big Picture
4. 选择游戏开始
```

### 场景 3：远程桌面操作

```
1. Moonlight → 铭凡主机
2. 选择 "Desktop"
3. 完整桌面访问
4. 可以进行任何操作
```

---

## 📊 性能参考

### 预期性能（局域网千兆）

| 指标 | 期望值 |
|------|--------|
| 延迟 | 3-5ms |
| 帧率 | 60fps |
| 分辨率 | 1080p |
| 画质 | 极高 |
| 带宽 | 10-20 Mbps |

### 实际测试方法

```
游戏中按：Ctrl + Alt + Shift + S
查看：
- Latency（延迟）：应 < 10ms
- FPS（帧率）：应 = 60
- Bitrate（码率）：10-20 Mbps
```

---

## 🔧 常见问题

### ❓ 无法发现服务器

**检查清单**：
1. ✅ 两台设备在同一 WiFi
2. ✅ 铭凡的 Sunshine 正在运行
3. ✅ 防火墙规则已添加

**快速修复**：
```
Moonlight → "+" → 手动输入铭凡 IP
```

---

### ❓ 延迟很高

**原因**：网络质量差或编码器设置不当

**解决**：
```
1. 降低码率：20000 → 10000 Kbps
2. 降低分辨率：1080p → 720p
3. 降低帧率：60 → 30 fps
4. 检查网络：确保千兆局域网
```

---

### ❓ 画面卡顿

**原因**：服务端性能不足

**解决**：
```
1. 关闭其他占用 CPU/GPU 的程序
2. Sunshine 配置：
   - Encoder: H.264（兼容性更好）
   - 降低分辨率/帧率
3. 更新显卡驱动
```

---

### ❓ 手柄不工作

**解决**：
```
1. Sunshine Web 界面
2. Configuration → Input
3. ✅ 确认 "Enable Gamepad" 已勾选
4. 重启串流
```

---

## 🆚 对比 Parsec

### 为什么选择 Moonlight？

| 对比项 | Moonlight + Sunshine | Parsec |
|--------|----------------------|--------|
| **费用** | 完全免费 | 免费版有限制 |
| **性能** | 极高（< 5ms） | 极高（< 5ms） |
| **限制** | 无 | 4 小时/会话 |
| **开源** | ✅ 是 | ❌ 否 |
| **易用性** | 中等（需配置） | 简单（自动） |

### 何时使用 Parsec？

如果你需要：
- ✅ 最简单的设置（5 分钟）
- ✅ 自动穿透（无需 VPN）
- ✅ 跨平台（支持 Android/iOS）
- ⚠️ 可以接受 4 小时限制

**Parsec 快速开始**：
```
1. 下载：https://parsec.app/downloads
2. 注册免费账号
3. 服务端登录 → 启用 Hosting
4. 客户端登录 → 点击主机连接
```

---

## 🌐 远程访问（外网）

Moonlight + Sunshine 默认只支持局域网。如需外网访问：

### 方案 1：Tailscale VPN（推荐）⏱️ 5 分钟

```
1. 两台设备都安装 Tailscale：https://tailscale.com/
2. 登录同一账号
3. 自动建立 VPN 连接
4. Moonlight 通过 Tailscale IP 连接
```

### 方案 2：端口转发（不推荐）

```
路由器配置：
- 转发端口 47989, 47998-48010 到铭凡 IP
- ⚠️ 安全风险高，不推荐
```

---

## 🎉 下一步

### 立即开始游戏

```
1. ✅ 服务端配置完成（铭凡）
2. ✅ 客户端配置完成（ThinkBook+）
3. ✅ 连接成功
4. 🎮 开始享受游戏！
```

### 进阶配置

如需了解更多：
- **[完整方案对比](./docs/free-gaming-remote-solutions.md)** - 多方案详细对比
- **[远程桌面部署](./remote-desktop-deployment-plan.md)** - RDP 配置
- **[BASELINE 更新](./BASELINE.md)** - 项目跟踪

---

## 💡 总结

### ✅ 完成清单

- ✅ Sunshine 安装配置（5-8 分钟）
- ✅ Moonlight 安装配对（3-5 分钟）
- ✅ 防火墙规则配置
- ✅ 应用添加完成

### 🚀 核心优势

- ✅ **完全免费**：零成本，无限制
- ✅ **性能极致**：< 5ms 延迟，60fps
- ✅ **开源可控**：无隐私担忧
- ✅ **游戏优化**：专为游戏设计

---

**文档版本**: v1.0
**创建日期**: 2026-03-27

**开始享受游戏串流吧！** 🎮🚀
