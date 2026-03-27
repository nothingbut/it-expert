# 远程桌面Microsoft账户应用密码配置指南

## 快速导航

- [创建应用密码](#创建应用密码)
- [配置远程桌面](#配置远程桌面)
- [常见问题](#常见问题)
- [快捷脚本使用](#快捷脚本使用)

---

## 创建应用密码

### 步骤1：启用两步验证

1. 访问：[Microsoft账户安全页面](https://account.microsoft.com/security)
2. 登录你的Microsoft账户
3. 找到"两步验证"部分
4. 点击"启用"并完成设置

### 步骤2：生成应用密码

**直接访问应用密码页面**：
```
https://account.live.com/proofs/AppPassword
```

**或者通过安全页面导航**：
1. 访问：https://account.microsoft.com/security
2. 找到"高级安全选项"
3. 点击"应用密码"
4. 点击"创建新的应用密码"

**命名建议**：
```
远程桌面-小主机
或
RDP-UM773
```

**⚠️ 重要提醒**：
- 密码格式：`xxxx-xxxx-xxxx-xxxx`（16位，带连字符）
- 只显示一次，务必立即保存！
- 关闭页面后无法再查看，只能删除重建

---

## 配置远程桌面

### 方法1：手动配置（适合首次使用）

1. **在ThinkBook上打开"远程桌面连接"**
   ```
   Win + R → 输入 mstsc → 回车
   ```

2. **点击"显示选项"**

3. **填写连接信息**：
   ```
   计算机：192.168.1.100（小主机IP，根据实际修改）

   用户名：MicrosoftAccount\your-email@outlook.com
   （或：.\your-email@outlook.com）

   密码：应用密码（xxxx-xxxx-xxxx-xxxx）
   ```

4. **勾选"允许我保存凭据"** ✅

5. **点击"连接"**

---

### 方法2：使用快捷脚本（推荐）

**在ThinkBook上运行**：

```powershell
# 1. 下载或创建脚本文件
# 保存为：rdp-to-minipc.ps1

# 2. 修改脚本中的配置
$MiniPCIP = "192.168.1.100"  # 你的小主机IP
$Username = "MicrosoftAccount\your-email@outlook.com"  # 你的账户

# 3. 运行脚本
powershell -ExecutionPolicy Bypass -File .\rdp-to-minipc.ps1

# 4. 桌面会生成"连接小主机.rdp"文件
# 双击即可连接
```

---

## 用户名格式说明

三种格式都可以尝试：

| 格式 | 示例 | 适用场景 |
|------|------|----------|
| `MicrosoftAccount\邮箱` | `MicrosoftAccount\user@outlook.com` | 标准格式（推荐） |
| `.\邮箱` | `.\user@outlook.com` | 简化格式 |
| `AzureAD\邮箱` | `AzureAD\user@outlook.com` | Azure AD账户 |

**⚠️ 注意**：不要直接输入邮箱，必须加上前缀！

---

## 常见问题

### Q1：提示"你的凭据不工作"

**解决方案**：
1. 检查用户名格式是否正确（必须有前缀）
2. 确认密码是**应用密码**，不是Microsoft账户主密码
3. 尝试删除旧的应用密码，重新生成新的
4. 确认小主机防火墙允许远程桌面（端口3389）

---

### Q2：连接后立即断开

**可能原因**：
- 小主机已有其他用户登录（同一账户只能单会话）
- 网络级别身份验证(NLA)配置问题

**解决方案**：
```powershell
# 在小主机上执行（允许多会话）
# 注意：Windows 10/11家庭版不支持多会话
# 需要专业版或企业版

# 添加远程桌面用户
net localgroup "Remote Desktop Users" "MicrosoftAccount\your-email@outlook.com" /add
```

---

### Q3：应用密码会过期吗？

**回答**：
- ❌ 不会自动过期
- ❌ 不会自动变更
- ✅ 永久有效（除非手动撤销）

**会失效的情况**：
1. 手动删除应用密码
2. 修改Microsoft账户主密码
3. 关闭两步验证
4. 账户安全异常

---

### Q4：可以创建多个应用密码吗？

**回答**：可以！

建议为每个设备/应用创建单独的密码：
```
- "远程桌面-小主机"
- "远程桌面-工作电脑"
- "Outlook-手机"
- "OneDrive-平板"
```

这样撤销单个密码不会影响其他设备。

---

### Q5：如何删除应用密码？

```
1. 访问：https://account.live.com/proofs/AppPassword
2. 找到要删除的密码
3. 点击旁边的"删除"或"撤销"
4. 确认删除
```

删除后，使用该密码的设备将无法连接。

---

## 安全最佳实践

### 1. 密码管理

✅ **推荐方式**：
- Windows凭据管理器（自动保存）
- 密码管理器（Bitwarden、1Password）
- 加密文本文件

❌ **避免**：
- 明文保存在桌面
- 发送到微信/QQ
- 存储在云笔记未加密

---

### 2. 应用密码命名

使用清晰的命名规则：
```
✅ "RDP-铭凡小主机"
✅ "远程桌面-家用电脑"
✅ "ThinkBook-to-MiniPC"

❌ "密码1"
❌ "test"
❌ "临时"
```

---

### 3. 定期检查

每季度检查一次：
```
1. 访问应用密码页面
2. 删除不再使用的密码
3. 确认活跃密码都是当前设备在用
```

---

## 测试验证

### 验证检查清单

- [ ] 能成功连接到小主机
- [ ] 凭据已保存（下次无需输入密码）
- [ ] 桌面快捷方式可用
- [ ] 网络稳定时连接流畅
- [ ] 剪贴板共享正常
- [ ] 文件传输功能正常

---

## 快速参考

### 重要链接

| 功能 | 链接 |
|------|------|
| Microsoft账户安全 | https://account.microsoft.com/security |
| 应用密码管理 | https://account.live.com/proofs/AppPassword |
| 登录活动检查 | https://account.microsoft.com/activity |

### 小主机信息

```
设备名称：铭凡UM773
局域网IP：192.168.1.xxx（根据实际填写）
操作系统：Windows 11 专业版
远程桌面端口：3389（默认）
```

### ThinkBook信息

```
设备名称：联想ThinkBook 14+
操作系统：Windows 11
RDP配置文件：桌面\连接小主机.rdp
```

---

## 附录：PowerShell快捷命令

### 快速打开远程桌面

```powershell
# 连接到小主机
mstsc /v:192.168.1.100

# 全屏模式连接
mstsc /v:192.168.1.100 /f

# 使用已保存的RDP文件
mstsc "C:\Users\YourName\Desktop\连接小主机.rdp"
```

---

### 查看已保存的凭据

```powershell
# 打开凭据管理器
control /name Microsoft.CredentialManager

# 或者
rundll32.exe keymgr.dll,KRShowKeyMgr
```

---

### 测试网络连接

```powershell
# 测试小主机是否在线
Test-Connection -ComputerName 192.168.1.100 -Count 4

# 测试远程桌面端口是否开放
Test-NetConnection -ComputerName 192.168.1.100 -Port 3389
```

---

## 文档更新记录

| 日期 | 版本 | 说明 |
|------|------|------|
| 2026-03-27 | 1.0 | 初始版本 |

---

## 相关文档

- [BASELINE.md](../BASELINE.md) - 系统基线配置
- [remote-desktop-solutions.md](./remote-desktop-solutions.md) - 远程桌面方案对比
