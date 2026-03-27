# 远程桌面方案对比与选型

> **目标**: 从联想 ThinkBook+ 远程访问铭凡 UM773 小主机
> **日期**: 2026-03-27
> **设备**: 联想 ThinkBook+ (客户端) → 铭凡 UM773 (服务端)

---

## 目录
- [需求分析](#需求分析)
- [方案对比](#方案对比)
- [推荐方案](#推荐方案)
- [详细配置](#详细配置)
- [性能对比](#性能对比)

---

## 需求分析

### 使用场景
| 场景 | 频率 | 需求 | 优先级 |
|------|------|------|--------|
| 日常操作 | 高 | 文件管理、软件配置、系统维护 | **高** |
| 偶尔游戏 | 中 | 低延迟、GPU 加速、流畅体验 | 中 |
| 局域网访问 | 高 | 高性能、低延迟 | **高** |
| 远程访问 | 低 | 简单交互、轻量操作 | 低 |

### 技术要求
- **延迟**: 局域网 < 20ms，远程 < 100ms
- **分辨率**: 1080p（日常）/ 1080p 60fps（游戏）
- **带宽**: 局域网千兆，远程 10Mbps+
- **安全**: 加密传输、认证机制
- **易用性**: 开箱即用、配置简单

---

## 方案对比

### 快速决策矩阵

| 方案 | 日常操作 | 游戏性能 | 局域网 | 远程访问 | 免费 | 推荐度 |
|------|----------|----------|--------|----------|------|--------|
| **Windows RDP** | ⭐⭐⭐⭐⭐ | ⭐⭐ | ⭐⭐⭐⭐⭐ | ⭐⭐⭐⭐ | ✅ | ⭐⭐⭐⭐⭐ |
| **Parsec** | ⭐⭐⭐⭐ | ⭐⭐⭐⭐⭐ | ⭐⭐⭐⭐⭐ | ⭐⭐⭐⭐⭐ | ✅ | ⭐⭐⭐⭐⭐ |
| Moonlight/Sunshine | ⭐⭐⭐ | ⭐⭐⭐⭐⭐ | ⭐⭐⭐⭐⭐ | ⭐⭐⭐ | ✅ | ⭐⭐⭐⭐ |
| Rustdesk | ⭐⭐⭐⭐ | ⭐⭐⭐ | ⭐⭐⭐⭐ | ⭐⭐⭐⭐ | ✅ | ⭐⭐⭐⭐ |
| ToDesk | ⭐⭐⭐⭐ | ⭐⭐ | ⭐⭐⭐⭐ | ⭐⭐⭐⭐⭐ | 部分 | ⭐⭐⭐ |
| 向日葵 | ⭐⭐⭐ | ⭐⭐ | ⭐⭐⭐ | ⭐⭐⭐⭐⭐ | 部分 | ⭐⭐⭐ |

---

## 推荐方案 🎯

### 主方案：Windows RDP（日常操作）

**适用场景**：
- ✅ 日常系统管理、文件操作
- ✅ 软件安装配置
- ✅ 局域网高性能访问
- ✅ 远程简单交互

**优势**：
1. **原生集成**：Windows 自带，无需安装
2. **低延迟**：局域网延迟 < 10ms
3. **高性能**：支持硬件加速
4. **安全性**：TLS 加密 + NLA 认证
5. **免费**：完全免费，无限制

**限制**：
- ❌ 游戏支持有限（全屏独占游戏不可用）
- ❌ 服务端需要专业版（铭凡已有 ✅）
- ❌ 远程访问需要端口转发或 VPN

---

### 辅助方案：Parsec（游戏场景）

**适用场景**：
- ✅ 游戏串流
- ✅ 低延迟需求
- ✅ 局域网 + 远程访问
- ✅ GPU 加速应用

**优势**：
1. **游戏优化**：专为游戏设计，支持全屏独占
2. **超低延迟**：局域网 < 5ms
3. **高质量**：支持 1080p 60fps / 4K 60fps
4. **自动穿透**：P2P 连接，无需端口转发
5. **免费版**：个人使用免费

**限制**：
- ⚠️ 需要注册账号
- ⚠️ 免费版限制 4 小时/会话（实际很少触及）
- ⚠️ 网络依赖较高

---

### 远程访问：Tailscale VPN

**适用场景**：
- ✅ 外网访问内网设备
- ✅ 安全隧道
- ✅ 零配置穿透

**优势**：
1. **零配置**：自动 NAT 穿透
2. **安全**：WireGuard 协议，端到端加密
3. **免费**：个人使用免费（最多 100 设备）
4. **跨平台**：Windows/Mac/Linux/iOS/Android

---

## 详细配置

### 方案 1：Windows RDP

#### 服务端配置（铭凡 UM773）

##### 1. 启用远程桌面
```powershell
# 方法 1：图形界面
# 设置 → 系统 → 远程桌面 → 启用远程桌面

# 方法 2：PowerShell（管理员）
Set-ItemProperty -Path 'HKLM:\System\CurrentControlSet\Control\Terminal Server' -Name "fDenyTSConnections" -Value 0
Enable-NetFirewallRule -DisplayGroup "远程桌面"
```

##### 2. 配置防火墙
```powershell
# 允许 RDP 端口 3389
New-NetFirewallRule -DisplayName "RDP" -Direction Inbound -Protocol TCP -LocalPort 3389 -Action Allow
```

##### 3. 创建远程用户（可选）
```powershell
# 创建专用远程用户
$Password = Read-Host -AsSecureString
New-LocalUser "remote_user" -Password $Password -FullName "远程访问用户"
Add-LocalGroupMember -Group "Remote Desktop Users" -Member "remote_user"
```

##### 4. 性能优化
```powershell
# 启用网络级别身份验证（NLA）
Set-ItemProperty -Path 'HKLM:\System\CurrentControlSet\Control\Terminal Server\WinStations\RDP-Tcp' -Name "UserAuthentication" -Value 1

# 调整会话超时（30 分钟无操作断开）
Set-ItemProperty -Path 'HKLM:\System\CurrentControlSet\Control\Terminal Server\WinStations\RDP-Tcp' -Name "MaxIdleTime" -Value 1800000
```

#### 客户端配置（联想 ThinkBook+）

##### 1. 使用内置远程桌面连接
```
开始 → 搜索 "mstsc" → 远程桌面连接
```

##### 2. 推荐客户端：Microsoft Remote Desktop
- **下载**：Microsoft Store 搜索 "Microsoft Remote Desktop"
- **优势**：现代 UI、多连接管理、更好的性能

##### 3. 连接配置
```
服务器地址：192.168.x.x（铭凡 IP）
用户名：your_username
密码：your_password

显示设置：
- 分辨率：全屏或 1920x1080
- 颜色深度：32 位
- 连接速度：LAN (10 Mbps 或更高)

高级选项：
- ✅ 启用桌面合成
- ✅ 启用字体平滑
- ✅ 启用音频
- ✅ 重定向剪贴板
- ✅ 重定向驱动器（可选）
```

---

### 方案 2：Parsec

#### 服务端配置（铭凡 UM773）

##### 1. 下载安装 Parsec
```
官网：https://parsec.app/downloads
版本：Windows 10/11 64-bit
```

##### 2. 注册并登录账号
```
1. 创建 Parsec 账号（免费）
2. 服务端登录账号
3. 设置 → Hosting → 启用 Hosting
```

##### 3. 性能优化
```
Parsec 设置 → Hosting Settings:
- Resolution: 1920x1080
- FPS: 60
- Bandwidth Limit: 50 Mbps（局域网可更高）
- H.265 (HEVC): 启用（更高压缩比）
- Hardware Decoding: 启用
```

##### 4. 防火墙配置
```
Parsec 安装时会自动配置防火墙
端口：UDP 8000-8010（自动选择）
```

#### 客户端配置（联想 ThinkBook+）

##### 1. 安装 Parsec 客户端
```
下载：https://parsec.app/downloads
登录同一账号
```

##### 2. 连接方式
```
方式 1：自动发现（局域网）
- Parsec 会自动发现同一网络的主机
- 点击铭凡 UM773 图标连接

方式 2：远程连接
- Parsec 自动建立 P2P 连接
- 无需端口转发或 VPN
```

##### 3. 快捷键
```
Ctrl + Alt + Shift + D：显示统计信息
Ctrl + Alt + Shift + Q：断开连接
Ctrl + Alt + Shift + M：切换鼠标模式
```

---

### 方案 3：Tailscale VPN（远程访问）

#### 安装配置

##### 1. 服务端（铭凡 UM773）
```powershell
# 下载安装
下载：https://tailscale.com/download/windows
安装后登录账号

# 验证
tailscale status
```

##### 2. 客户端（联想 ThinkBook+）
```powershell
# 同样安装 Tailscale
登录同一账号

# 获取铭凡的 Tailscale IP
tailscale status
# 例如：100.x.x.x
```

##### 3. 使用方式
```
通过 Tailscale IP 访问 RDP：
mstsc /v:100.x.x.x

或 Parsec 自动通过 Tailscale 连接
```

---

## 性能对比

### 局域网延迟测试（预期）

| 方案 | 延迟 | 带宽占用 | CPU 占用 | 画质 |
|------|------|----------|----------|------|
| RDP | 5-10ms | 5-20 Mbps | 低 | 中-高 |
| Parsec | 3-8ms | 10-50 Mbps | 中 | 高-极高 |
| Moonlight | 3-8ms | 10-50 Mbps | 中 | 高-极高 |
| Rustdesk | 10-20ms | 5-15 Mbps | 中 | 中 |

### 远程访问延迟测试（预期）

| 方案 | 延迟 | 带宽需求 | 稳定性 | 穿透能力 |
|------|------|----------|--------|----------|
| RDP + Tailscale | 50-100ms | 5-10 Mbps | 高 | 高 |
| Parsec | 30-80ms | 10-20 Mbps | 高 | 极高 |
| ToDesk | 50-150ms | 5-15 Mbps | 中 | 极高 |

---

## 使用场景推荐

### 场景 1：局域网日常操作（90%）
```
推荐：Windows RDP
- 启动 mstsc 或 Microsoft Remote Desktop
- 连接 192.168.x.x
- 完成日常文件管理、软件配置
```

### 场景 2：局域网游戏（5%）
```
推荐：Parsec
- 启动 Parsec 客户端
- 点击铭凡主机图标
- 享受低延迟游戏体验
```

### 场景 3：远程简单交互（5%）
```
方案 A：RDP + Tailscale（推荐）
- 启动 Tailscale
- mstsc 连接 100.x.x.x
- 适合轻量操作

方案 B：Parsec 直连
- 直接启动 Parsec
- 自动 P2P 穿透
- 适合需要更好画质的场景
```

---

## 成本分析

### 免费方案（推荐）

| 方案 | 成本 | 限制 | 适用 |
|------|------|------|------|
| Windows RDP | 免费 | 无 | ✅ 最佳 |
| Parsec 免费版 | 免费 | 4 小时/会话 | ✅ 足够 |
| Tailscale 免费版 | 免费 | 100 设备 | ✅ 足够 |

### 付费方案（可选）

| 方案 | 价格 | 额外功能 |
|------|------|----------|
| Parsec Teams | $30/月 | 团队协作、无时长限制 |
| ToDesk 专业版 | ¥180/年 | 无广告、文件传输 |

---

## 安全建议

### 1. 强密码策略
```powershell
# 设置密码复杂度要求
$Password = ConvertTo-SecureString "Complex!Pass123" -AsPlainText -Force
```

### 2. 启用防火墙
```powershell
# RDP 仅允许局域网访问
New-NetFirewallRule -DisplayName "RDP LAN Only" -Direction Inbound -Protocol TCP -LocalPort 3389 -RemoteAddress 192.168.0.0/16 -Action Allow
```

### 3. 定期更新
```
- Windows Update 保持最新
- Parsec/Tailscale 保持最新版本
```

### 4. 使用 VPN 而非端口转发
```
推荐：Tailscale VPN
避免：路由器端口转发（安全风险高）
```

---

## 故障排除

### 问题 1：RDP 无法连接

**症状**：远程桌面连接失败

**解决**：
```powershell
# 1. 检查远程桌面是否启用
Get-ItemProperty -Path 'HKLM:\System\CurrentControlSet\Control\Terminal Server' -Name "fDenyTSConnections"
# 0 = 启用, 1 = 禁用

# 2. 检查防火墙
Get-NetFirewallRule -DisplayGroup "远程桌面"

# 3. 检查服务
Get-Service TermService
```

### 问题 2：Parsec 延迟高

**症状**：游戏卡顿、延迟大

**解决**：
```
1. 检查网络质量：Parsec 设置 → Overlay → 显示统计
2. 降低分辨率：1920x1080 → 1280x720
3. 降低 FPS：60 → 30
4. 禁用 H.265：使用 H.264（兼容性更好）
5. 检查 GPU 驱动：更新到最新版本
```

### 问题 3：Tailscale 无法穿透

**症状**：无法建立连接

**解决**：
```
1. 检查 Tailscale 状态：tailscale status
2. 重启 Tailscale：tailscale down && tailscale up
3. 检查防火墙：允许 Tailscale 应用
4. 使用 DERP 中继：设置 → Advanced → 启用 DERP
```

---

## 总结

### 最终推荐方案

**日常使用（90%）**：
- **主力**：Windows RDP
- **备选**：无

**游戏场景（5%）**：
- **主力**：Parsec
- **备选**：Moonlight + Sunshine

**远程访问（5%）**：
- **主力**：RDP + Tailscale VPN
- **备选**：Parsec 直连

### 部署优先级
1. **P0**：Windows RDP（立即配置）
2. **P1**：Parsec（需要游戏时安装）
3. **P2**：Tailscale VPN（需要远程访问时安装）

### 预计部署时间
- Windows RDP：5-10 分钟
- Parsec：10-15 分钟
- Tailscale：5-10 分钟
- **总计**：20-35 分钟

---

**文档版本**: v1.0
**创建日期**: 2026-03-27
**下一步**: 创建部署计划（remote-desktop-deployment-plan.md）
