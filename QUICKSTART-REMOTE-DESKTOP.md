# 远程桌面快速开始 🚀

> **5 分钟快速配置 Windows RDP**
>
> **目标**: 联想 ThinkBook+ → 铭凡 UM773
> **场景**: 局域网日常操作

---

## 📋 前提条件

- ✅ 铭凡 UM773：Windows 11 **专业版**
- ✅ 联想 ThinkBook+：Windows 11（任意版本）
- ✅ 两台设备在同一局域网
- ⏱️ 预计时间：5-10 分钟

---

## 🎯 5 步快速配置

### 第 1 步：启用远程桌面（铭凡 UM773）⏱️ 1 分钟

```
1. Windows 键 → 设置
2. 系统 → 远程桌面
3. 启用远程桌面 → 确认
```

![提示] 记下显示的 **PC 名称**（例如：MINGFAN-UM773）

---

### 第 2 步：获取 IP 地址（铭凡）⏱️ 30 秒

按 `Win + R`，输入 `cmd`，回车，然后输入：

```bash
ipconfig | findstr IPv4
```

![记录] 记下局域网 IP 地址：**192.168.x.x**

---

### 第 3 步：连接测试（联想 ThinkBook+）⏱️ 1 分钟

按 `Win + R`，输入：

```
mstsc
```

在弹出窗口输入：
- 计算机：**192.168.x.x**（步骤 2 的 IP）
- 用户名：你的 Windows 用户名
- 密码：你的 Windows 密码

点击 **连接**！

---

### 第 4 步：安装更好的客户端（ThinkBook+）⏱️ 2 分钟

```
1. 打开 Microsoft Store
2. 搜索 "Microsoft Remote Desktop"
3. 点击 "获取" → 安装
```

---

### 第 5 步：创建永久连接（ThinkBook+）⏱️ 1 分钟

1. 打开 **Microsoft Remote Desktop**
2. 点击 **"+"** → **"Add PC"**
3. 填写信息：
   - **PC name**: 192.168.x.x
   - **Friendly name**: 铭凡 UM773
   - **User account**: 添加凭据
4. 点击 **"Save"**

✅ 完成！双击 "铭凡 UM773" 即可连接

---

## 🎮 可选：游戏串流（Parsec）

如需**游戏功能**，额外 10 分钟：

### 服务端（铭凡）

1. 下载：https://parsec.app/downloads
2. 安装并注册免费账号
3. 设置 → Hosting → 启用

### 客户端（ThinkBook+）

1. 下载并安装 Parsec
2. 登录同一账号
3. 点击铭凡主机图标连接

---

## 🌐 可选：远程访问（Tailscale VPN）

如需**外网访问**，额外 5 分钟：

### 两台设备都安装

1. 下载：https://tailscale.com/download/windows
2. 安装并登录（选择 Google/Microsoft）
3. 自动建立 VPN 连接

### 通过 VPN 连接 RDP

```
mstsc → 输入 Tailscale IP (100.x.x.x)
```

![查看 IP] 右键 Tailscale 托盘图标 → 详情

---

## ✅ 验证功能

### 测试清单

- [ ] 桌面显示清晰流畅
- [ ] 鼠标键盘响应正常
- [ ] 复制粘贴功能正常
- [ ] 音频播放正常
- [ ] 文件拖拽传输正常

---

## 📱 日常使用

### 局域网连接（90% 场景）

```
打开 Microsoft Remote Desktop
→ 双击 "铭凡 UM773"
→ 完成日常操作
```

### 游戏串流（5% 场景）

```
打开 Parsec
→ 点击铭凡图标
→ 启动游戏
```

### 远程访问（5% 场景）

```
启动 Tailscale
→ mstsc 连接 100.x.x.x
→ 轻量操作
```

---

## 🔧 常见问题

### ❓ 无法连接

**检查**：
1. 铭凡是否开机
2. IP 地址是否正确
3. 远程桌面是否启用

**快速修复**：
```powershell
# 在铭凡上运行（PowerShell 管理员）
Set-ItemProperty -Path 'HKLM:\System\CurrentControlSet\Control\Terminal Server' -Name "fDenyTSConnections" -Value 0
Enable-NetFirewallRule -DisplayGroup "远程桌面"
```

---

### ❓ 提示需要专业版

**解决**：
- 铭凡 UM773 必须是 Windows 11 **专业版**
- 联想 ThinkBook+ 可以是任意版本

---

### ❓ 延迟很高

**优化**：
1. 确保千兆局域网连接
2. 关闭其他占用带宽的应用
3. mstsc → 体验 → 选择 "LAN (10 Mbps 或更高)"

---

## 📚 进阶文档

- **[详细方案对比](./docs/remote-desktop-solutions.md)** - 6 种方案对比
- **[完整部署计划](./remote-desktop-deployment-plan.md)** - 3 阶段部署
- **[BASELINE 更新](./BASELINE.md)** - 项目进度跟踪

---

## 🎉 总结

### ✅ 完成清单

- ✅ Windows RDP 配置完成（5 分钟）
- ⬜ Parsec 游戏串流（可选，10 分钟）
- ⬜ Tailscale VPN（可选，5 分钟）

### 🚀 下一步

1. **立即使用**：尝试连接铭凡进行日常操作
2. **性能测试**：测试文件传输、音频播放
3. **游戏测试**：如需游戏，安装 Parsec
4. **远程访问**：如需外网，安装 Tailscale

---

**文档版本**: v1.0
**创建日期**: 2026-03-27
**更新日期**: -

**享受远程桌面体验！** 🎉
