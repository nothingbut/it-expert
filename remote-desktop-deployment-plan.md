# 远程桌面部署方案

> **目标**: 从联想 ThinkBook+ 远程访问铭凡 UM773
> **日期**: 2026-03-27
> **预计时间**: 20-35 分钟
> **难度**: ⭐⭐ 简单

---

## 目录
- [部署概览](#部署概览)
- [阶段 1: Windows RDP](#阶段-1-windows-rdp)
- [阶段 2: Parsec（可选）](#阶段-2-parsec可选)
- [阶段 3: Tailscale VPN（可选）](#阶段-3-tailscale-vpn可选)
- [验收测试](#验收测试)
- [日常使用](#日常使用)

---

## 部署概览

### 部署架构

```
联想 ThinkBook+ (客户端)
    |
    +--- 局域网连接 (主要)
    |       |
    |       +--- Windows RDP → 192.168.x.x:3389
    |       +--- Parsec → 自动发现
    |
    +--- 远程连接 (备选)
            |
            +--- Tailscale VPN → 100.x.x.x
                    |
                    +--- RDP 通过 VPN
                    +--- Parsec 自动穿透
    |
    ↓
铭凡 UM773 (服务端)
```

### 阶段规划

| 阶段 | 内容 | 时间 | 优先级 | 状态 |
|------|------|------|--------|------|
| 阶段 1 | Windows RDP | 5-10 分钟 | P0 | ⬜ 待开始 |
| 阶段 2 | Parsec 安装配置 | 10-15 分钟 | P1 | ⬜ 待开始 |
| 阶段 3 | Tailscale VPN | 5-10 分钟 | P2 | ⬜ 待开始 |
| 验收 | 功能测试 | 5 分钟 | - | ⬜ 待开始 |

---

## 阶段 1: Windows RDP

### 服务端配置（铭凡 UM773）

#### 任务 1.1：启用远程桌面 ⭐ 核心

**方法 A：图形界面（推荐）**

1. 打开设置
```
Windows 键 → 设置 → 系统 → 远程桌面
```

2. 启用远程桌面
```
远程桌面 → 开关打开 → 确认
```

3. 记录设置
```
记录下显示的 PC 名称（例如：MINGFAN-UM773）
记录下当前用户名
```

**方法 B：PowerShell（管理员）**

```powershell
# 1. 打开 PowerShell（管理员）
# 右键开始菜单 → Windows PowerShell (管理员)

# 2. 启用远程桌面
Set-ItemProperty -Path 'HKLM:\System\CurrentControlSet\Control\Terminal Server' -Name "fDenyTSConnections" -Value 0

# 3. 启用防火墙规则
Enable-NetFirewallRule -DisplayGroup "远程桌面"

# 4. 验证状态
Get-ItemProperty -Path 'HKLM:\System\CurrentControlSet\Control\Terminal Server' -Name "fDenyTSConnections"
# 输出 0 表示成功
```

#### 任务 1.2：配置网络级别身份验证（NLA）

**图形界面方法**：
```
系统属性 → 远程 → 勾选 "仅允许运行使用网络级别身份验证的远程桌面的计算机连接"
```

**PowerShell 方法**：
```powershell
Set-ItemProperty -Path 'HKLM:\System\CurrentControlSet\Control\Terminal Server\WinStations\RDP-Tcp' -Name "UserAuthentication" -Value 1
```

#### 任务 1.3：获取 IP 地址

```powershell
# 获取局域网 IP
ipconfig | findstr IPv4

# 或者
Get-NetIPAddress -AddressFamily IPv4 | Where-Object {$_.IPAddress -like "192.168.*"}
```

**记录 IP 地址**：
```
铭凡 UM773 IP：192.168.___.___ （填写实际 IP）
```

#### 任务 1.4：测试 RDP 服务

```powershell
# 检查 RDP 端口是否监听
Test-NetConnection -ComputerName localhost -Port 3389
```

**期望输出**：
```
TcpTestSucceeded : True
```

---

### 客户端配置（联想 ThinkBook+）

#### 任务 1.5：使用内置远程桌面连接

**快速测试**：
```
1. Windows 键 → 搜索 "mstsc"
2. 输入铭凡 IP：192.168.x.x
3. 点击连接
4. 输入用户名和密码
5. 确认连接
```

#### 任务 1.6：安装 Microsoft Remote Desktop（推荐）

**下载安装**：
```
1. 打开 Microsoft Store
2. 搜索 "Microsoft Remote Desktop"
3. 点击安装
```

**创建连接配置**：
```
1. 打开 Microsoft Remote Desktop
2. 点击 "+" → "Add PC"
3. 配置参数：
   - PC name: 192.168.x.x（铭凡 IP）
   - User account: 添加用户凭据
   - Friendly name: 铭凡 UM773
   - Display settings: 全屏 或 1920x1080
```

**高级设置**：
```
显示设置：
  ✅ Update the session resolution on resize
  ✅ Use all monitors

设备与音频：
  ✅ 播放声音
  ✅ 播放音频
  ✅ 重定向剪贴板

本地资源：
  ✅ Printers（如需打印）
  ✅ 驱动器（如需文件传输）
```

#### 任务 1.7：连接测试

```
1. 双击 "铭凡 UM773" 连接
2. 等待连接建立
3. 验证功能：
   - 桌面显示正常
   - 鼠标键盘响应流畅
   - 音频播放正常
   - 剪贴板复制粘贴正常
```

#### 任务 1.8：创建桌面快捷方式

**方法 A：RDP 文件**
```
1. 在远程桌面连接中配置好连接
2. 点击 "显示选项" → "常规" → "另存为"
3. 保存为 "铭凡UM773.rdp"
4. 放到桌面或快速访问
```

**方法 B：Microsoft Remote Desktop 固定**
```
1. 右键连接 → Pin to Start
2. 或直接从开始菜单快速访问
```

---

### 性能优化（可选）

#### 任务 1.9：调整显示性能

**客户端设置**：
```
mstsc → 显示选项 → 体验：

连接速度：LAN (10 Mbps 或更高)

勾选：
✅ 桌面背景
✅ 字体平滑
✅ 桌面组合
✅ 显示窗口内容在拖动时
✅ 菜单和窗口动画
✅ 视觉样式
```

#### 任务 1.10：配置会话超时（服务端）

```powershell
# 30 分钟无操作自动断开
Set-ItemProperty -Path 'HKLM:\System\CurrentControlSet\Control\Terminal Server\WinStations\RDP-Tcp' -Name "MaxIdleTime" -Value 1800000

# 禁用超时（不推荐）
Set-ItemProperty -Path 'HKLM:\System\CurrentControlSet\Control\Terminal Server\WinStations\RDP-Tcp' -Name "MaxIdleTime" -Value 0
```

---

## 阶段 2: Parsec（可选）

### 服务端配置（铭凡 UM773）

#### 任务 2.1：下载安装 Parsec

**下载地址**：
```
官网：https://parsec.app/downloads
版本：Windows 10/11 64-bit
大小：约 30MB
```

**安装步骤**：
```
1. 下载 ParsecSetup.exe
2. 双击运行安装程序
3. 同意条款 → 安装
4. 等待安装完成（2-3 分钟）
5. 启动 Parsec
```

#### 任务 2.2：注册并登录账号

```
1. 打开 Parsec
2. 点击 "Sign Up"（或使用 Google/Discord 登录）
3. 填写信息：
   - Email: your_email@example.com
   - Password: [设置密码]
   - Name: [你的名字]
4. 确认邮箱（检查收件箱）
5. 登录 Parsec
```

#### 任务 2.3：配置 Hosting 设置

```
1. Parsec → 设置 (⚙️) → Hosting

基础设置：
  ✅ Host Enabled（启用托管）
  Resolution: 1920x1080
  FPS: 60

高级设置（Settings → Host）：
  Bandwidth Limit: 50 Mbps（局域网可更高）
  ✅ H.265 (HEVC)（启用）
  ✅ Hardware Decoding（启用）
  Encoder: 自动选择
```

#### 任务 2.4：验证 Hosting 状态

```
Parsec 主界面应显示：
✅ "Ready to Host" 或 "Online"
✅ 显示主机名称
```

---

### 客户端配置（联想 ThinkBook+）

#### 任务 2.5：安装 Parsec 客户端

```
1. 下载：https://parsec.app/downloads
2. 安装 Parsec
3. 登录同一账号（与服务端相同）
```

#### 任务 2.6：连接测试

**局域网自动发现**：
```
1. 打开 Parsec
2. 查看 "Computers" 列表
3. 应自动显示 "铭凡 UM773"（或你设置的名称）
4. 点击连接图标
5. 等待连接建立（2-5 秒）
```

#### 任务 2.7：快捷键配置

**显示统计信息**：
```
Ctrl + Alt + Shift + D
查看延迟、帧率、带宽等
```

**断开连接**：
```
Ctrl + Alt + Shift + Q
```

**切换鼠标模式**：
```
Ctrl + Alt + Shift + M
```

#### 任务 2.8：游戏测试（可选）

```
1. 通过 Parsec 连接到铭凡
2. 启动一个游戏
3. 验证：
   - 延迟 < 10ms（局域网）
   - 帧率 60fps
   - 画质清晰
   - 无卡顿
```

---

## 阶段 3: Tailscale VPN（可选）

### 服务端配置（铭凡 UM773）

#### 任务 3.1：下载安装 Tailscale

**下载地址**：
```
官网：https://tailscale.com/download/windows
版本：Windows 10/11
大小：约 20MB
```

**安装步骤**：
```
1. 下载 tailscale-setup.exe
2. 运行安装程序
3. 安装完成后自动启动
```

#### 任务 3.2：登录并连接

```
1. Tailscale 托盘图标 → "Log in"
2. 选择登录方式：
   - Google
   - Microsoft
   - GitHub
   - Email
3. 完成授权
4. 等待连接建立（自动）
```

#### 任务 3.3：记录 Tailscale IP

```
方法 1：托盘图标
  右键 Tailscale 图标 → 显示详情
  记录 Tailscale IP（例如：100.64.x.x）

方法 2：PowerShell
  tailscale status
  记录输出的 IP 地址
```

**记录 Tailscale IP**：
```
铭凡 UM773 Tailscale IP：100.___.___.___
```

---

### 客户端配置（联想 ThinkBook+）

#### 任务 3.4：安装 Tailscale

```
1. 下载：https://tailscale.com/download/windows
2. 安装 Tailscale
3. 登录同一账号（与服务端相同）
```

#### 任务 3.5：验证连接

```
1. 右键 Tailscale 托盘图标
2. 查看设备列表
3. 应看到 "铭凡 UM773"（或你的主机名）
4. 状态显示为 "Online"
```

#### 任务 3.6：测试 Ping 连通性

```powershell
# 测试 Tailscale IP
ping 100.x.x.x

# 期望输出
Reply from 100.x.x.x: bytes=32 time<10ms TTL=64
```

#### 任务 3.7：通过 VPN 使用 RDP

```
方法 1：mstsc
  1. Windows + R → mstsc
  2. 输入：100.x.x.x（Tailscale IP）
  3. 连接

方法 2：Microsoft Remote Desktop
  1. 添加新 PC
  2. PC name: 100.x.x.x
  3. Friendly name: 铭凡 UM773 (远程)
  4. 保存并连接
```

---

## 验收测试

### 测试清单

#### 1. Windows RDP 测试

| 测试项 | 测试方法 | 期望结果 | 状态 |
|--------|----------|----------|------|
| 局域网连接 | mstsc 连接 192.168.x.x | 成功连接 | ⬜ |
| 桌面显示 | 查看远程桌面 | 清晰、流畅 | ⬜ |
| 鼠标操作 | 移动鼠标、点击 | 响应及时 | ⬜ |
| 键盘输入 | 打开记事本输入文字 | 输入正常 | ⬜ |
| 剪贴板 | 本地复制 → 远程粘贴 | 复制成功 | ⬜ |
| 音频播放 | 播放音乐 | 声音正常 | ⬜ |
| 文件传输 | 拖拽文件到远程 | 传输成功 | ⬜ |

#### 2. Parsec 测试

| 测试项 | 测试方法 | 期望结果 | 状态 |
|--------|----------|----------|------|
| 自动发现 | 打开 Parsec 查看设备列表 | 显示铭凡 | ⬜ |
| 连接速度 | 点击连接 | < 5 秒 | ⬜ |
| 延迟 | Ctrl+Alt+Shift+D 查看 | < 10ms | ⬜ |
| 帧率 | 查看统计信息 | 60fps | ⬜ |
| 游戏测试 | 启动游戏 | 流畅无卡顿 | ⬜ |

#### 3. Tailscale VPN 测试

| 测试项 | 测试方法 | 期望结果 | 状态 |
|--------|----------|----------|------|
| VPN 连接 | 查看 Tailscale 状态 | Online | ⬜ |
| Ping 测试 | ping 100.x.x.x | < 50ms | ⬜ |
| RDP 通过 VPN | mstsc 连接 100.x.x.x | 成功连接 | ⬜ |
| Parsec 通过 VPN | 关闭局域网，仅用 VPN | 自动使用 VPN | ⬜ |

---

## 日常使用

### 使用场景 1：局域网日常操作（90%）

**推荐方式**：Windows RDP

```
1. 打开 Microsoft Remote Desktop
2. 双击 "铭凡 UM773"
3. 完成日常操作：
   - 文件管理
   - 软件配置
   - 系统维护
   - Playnite 设置
4. 完成后关闭窗口
```

**快捷方式**：
```
桌面创建 .rdp 快捷方式
双击即可连接
```

---

### 使用场景 2：局域网游戏（5%）

**推荐方式**：Parsec

```
1. 打开 Parsec
2. 点击铭凡 UM773 连接
3. 启动游戏：
   - Playnite 全屏模式
   - Steam Big Picture
   - 其他游戏
4. Ctrl+Alt+Shift+Q 断开
```

**性能提示**：
```
- 确保局域网千兆连接
- 关闭其他占用带宽的应用
- 铭凡主机连接显示器（可选，提升性能）
```

---

### 使用场景 3：远程简单交互（5%）

**推荐方式**：RDP + Tailscale

```
1. 启动 Tailscale（两端）
2. mstsc 连接 100.x.x.x
3. 完成轻量操作：
   - 检查服务状态
   - 简单文件操作
   - 查看日志
4. 完成后断开
```

**备选方式**：Parsec 直连
```
1. 打开 Parsec
2. 自动 P2P 穿透
3. 连接速度更快
4. 画质更好
```

---

## 常见问题

### Q1：RDP 连接提示 "找不到计算机"

**原因**：
- 铭凡 IP 地址错误
- 铭凡未开机
- 防火墙阻止

**解决**：
```powershell
# 1. 验证 IP（在铭凡上）
ipconfig | findstr IPv4

# 2. 测试连通性（在 ThinkBook+ 上）
ping 192.168.x.x

# 3. 检查防火墙（在铭凡上）
Get-NetFirewallRule -DisplayGroup "远程桌面"
```

---

### Q2：Parsec 延迟很高

**原因**：
- 网络质量差
- 带宽不足
- 编码器问题

**解决**：
```
1. 降低分辨率：1920x1080 → 1280x720
2. 降低 FPS：60 → 30
3. 禁用 H.265，使用 H.264
4. 检查网络：确保千兆局域网
5. 更新 GPU 驱动
```

---

### Q3：Tailscale 无法连接

**原因**：
- 防火墙阻止
- 账号未同步
- NAT 穿透失败

**解决**：
```
1. 检查状态：
   tailscale status

2. 重启服务：
   tailscale down
   tailscale up

3. 允许防火墙：
   Windows 安全中心 → 防火墙 → 允许 Tailscale

4. 启用 DERP 中继：
   Tailscale 设置 → Advanced → Enable DERP
```

---

## 维护建议

### 定期检查（每月）

```
1. Windows Update（两台设备）
2. 更新 Parsec（如已安装）
3. 更新 Tailscale（如已安装）
4. 检查防火墙规则
5. 清理远程桌面会话
```

### 安全建议

```
1. 使用强密码
2. 启用 Windows Hello（生物识别）
3. 定期更改密码
4. 不在公网暴露 RDP 端口
5. 使用 VPN 进行远程访问
```

---

## 总结

### 部署完成检查

- ✅ Windows RDP 配置完成并测试通过
- ✅ Microsoft Remote Desktop 已安装
- ⬜ Parsec 已安装（可选）
- ⬜ Tailscale VPN 已安装（可选）
- ✅ 所有测试用例通过
- ✅ 快捷方式已创建

### 下一步

1. **立即使用**：尝试通过 RDP 连接铭凡进行日常操作
2. **游戏测试**：如需游戏，安装 Parsec 并测试
3. **远程访问**：如需外网访问，安装 Tailscale
4. **更新 BASELINE.md**：记录部署进度

---

**文档版本**: v1.0
**创建日期**: 2026-03-27
**预计部署时间**: 20-35 分钟
**下一步**: 开始阶段 1 部署 🚀
