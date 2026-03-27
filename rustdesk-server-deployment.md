# RustDesk 自建服务器部署指南

> **目标**: 在飞牛NAS上部署 RustDesk 中转服务器
> **环境**: 飞牛NAS（Hyper-V 虚拟机）
> **部署时间**: 15-20 分钟

---

## 目录
- [方案概述](#方案概述)
- [部署方式对比](#部署方式对比)
- [Docker 部署（推荐）](#docker-部署推荐)
- [网络配置](#网络配置)
- [客户端配置](#客户端配置)
- [故障排除](#故障排除)

---

## 方案概述

### RustDesk 服务器架构

```
互联网
    |
[路由器] - 端口转发
    |
[飞牛NAS] (192.168.x.x)
    |
    +--- RustDesk 服务器
            |
            +--- hbbs (21115, 21116, 21118) - ID/信令服务器
            +--- hbbr (21117, 21119) - 中继服务器
```

### 服务器组件

| 组件 | 功能 | 端口 | 协议 |
|------|------|------|------|
| **hbbs** | ID/信令服务器 | 21115 | TCP |
| | 注册与心跳 | 21116 | TCP |
| | WebSocket | 21118 | TCP |
| **hbbr** | 中继服务器 | 21117 | TCP |
| | 中继服务 | 21119 | TCP |

---

## 部署方式对比

### 方案 1: Docker 部署（推荐）⭐

**优势**：
- ✅ 最简单（一条命令）
- ✅ 自动更新
- ✅ 易于管理
- ✅ 隔离性好

**要求**：
- 飞牛NAS 支持 Docker

**部署时间**：10 分钟

---

### 方案 2: 二进制部署

**优势**：
- ✅ 性能最好
- ✅ 资源占用低

**劣势**：
- ⚠️ 配置复杂
- ⚠️ 需要手动管理

**部署时间**：20 分钟

---

## Docker 部署（推荐）

### 前提条件

1. **飞牛NAS 支持 Docker**
   - 检查：飞牛NAS 控制面板 → Docker
   - 如果没有，需要先安装 Docker

2. **网络要求**
   - 飞牛NAS 可以访问互联网
   - 有固定的局域网 IP

---

### 步骤 1: 登录飞牛NAS

```bash
# 方式 1: 通过 SSH（推荐）
ssh admin@192.168.x.x  # 飞牛NAS IP

# 方式 2: 通过飞牛NAS Web 界面的终端
```

---

### 步骤 2: 创建工作目录

```bash
# 创建数据目录
mkdir -p /volume1/docker/rustdesk-server/data

# 进入目录
cd /volume1/docker/rustdesk-server
```

**注意**：路径可能因飞牛NAS版本而异，常见路径：
- `/volume1/docker/`
- `/mnt/data/docker/`
- `/opt/docker/`

---

### 步骤 3: 创建 Docker Compose 文件

```bash
# 创建 docker-compose.yml
cat > docker-compose.yml <<'EOF'
version: '3'

services:
  hbbs:
    container_name: rustdesk-hbbs
    image: rustdesk/rustdesk-server:latest
    command: hbbs -r 192.168.x.x:21117  # 替换为飞牛NAS IP
    volumes:
      - ./data:/root
    ports:
      - 21115:21115
      - 21116:21116
      - 21116:21116/udp
      - 21118:21118
    restart: unless-stopped

  hbbr:
    container_name: rustdesk-hbbr
    image: rustdesk/rustdesk-server:latest
    command: hbbr
    volumes:
      - ./data:/root
    ports:
      - 21117:21117
      - 21119:21119
    restart: unless-stopped
EOF
```

**重要**：将 `192.168.x.x` 替换为你的飞牛NAS实际IP地址！

---

### 步骤 4: 启动服务

```bash
# 启动容器
docker-compose up -d

# 查看状态
docker-compose ps

# 查看日志
docker-compose logs -f
```

**期望输出**：
```
NAME                IMAGE                              STATUS
rustdesk-hbbs       rustdesk/rustdesk-server:latest    Up
rustdesk-hbbr       rustdesk/rustdesk-server:latest    Up
```

---

### 步骤 5: 获取服务器密钥

```bash
# 查看公钥
cat ./data/id_ed25519.pub
```

**输出示例**：
```
ABCD1234EFGH5678IJKL9012MNOP3456QRST7890UVWX=
```

**重要**：记录这个密钥，客户端配置时需要！

---

### 步骤 6: 验证服务

```bash
# 检查端口监听
netstat -tuln | grep -E "2111[5-9]"

# 或使用 ss
ss -tuln | grep -E "2111[5-9]"
```

**期望输出**：
```
tcp   0.0.0.0:21115
tcp   0.0.0.0:21116
tcp   0.0.0.0:21117
tcp   0.0.0.0:21118
tcp   0.0.0.0:21119
```

✅ 服务器部署完成！

---

## 网络配置

### 配置 1: 防火墙（飞牛NAS）

```bash
# 如果飞牛NAS有防火墙，需要开放端口

# 方式 1: iptables
iptables -I INPUT -p tcp --dport 21115 -j ACCEPT
iptables -I INPUT -p tcp --dport 21116 -j ACCEPT
iptables -I INPUT -p udp --dport 21116 -j ACCEPT
iptables -I INPUT -p tcp --dport 21117 -j ACCEPT
iptables -I INPUT -p tcp --dport 21118 -j ACCEPT
iptables -I INPUT -p tcp --dport 21119 -j ACCEPT

# 保存规则（根据系统不同）
iptables-save > /etc/iptables/rules.v4
```

**或者通过飞牛NAS Web界面配置防火墙**

---

### 配置 2: Windows 防火墙（铭凡 UM773）

如果飞牛NAS在铭凡的Hyper-V虚拟机上，需要配置铭凡的防火墙：

```powershell
# 打开 PowerShell（管理员）

# 允许端口
New-NetFirewallRule -DisplayName "RustDesk Server TCP" -Direction Inbound -Protocol TCP -LocalPort 21115,21116,21117,21118,21119 -Action Allow

New-NetFirewallRule -DisplayName "RustDesk Server UDP" -Direction Inbound -Protocol UDP -LocalPort 21116 -Action Allow
```

---

### 配置 3: 路由器端口转发（外网访问）

**如需外网访问，配置路由器端口转发**：

| 服务 | 外部端口 | 内部 IP | 内部端口 | 协议 |
|------|----------|---------|----------|------|
| RustDesk hbbs | 21115 | 192.168.x.x | 21115 | TCP |
| RustDesk hbbs | 21116 | 192.168.x.x | 21116 | TCP+UDP |
| RustDesk hbbr | 21117 | 192.168.x.x | 21117 | TCP |
| RustDesk Web | 21118 | 192.168.x.x | 21118 | TCP |
| RustDesk Relay | 21119 | 192.168.x.x | 21119 | TCP |

**配置步骤**（以TP-Link路由器为例）：
```
1. 登录路由器管理界面
2. 转发规则 → 虚拟服务器
3. 添加以上端口转发规则
4. 保存并重启路由器
```

---

## 客户端配置

### 配置 1: 铭凡 UM773（服务端）

```
1. 打开 RustDesk
2. 点击右上角 ⚙️（设置）
3. 网络 → ID 服务器：
   - ID服务器：192.168.x.x（飞牛NAS IP）
   - Key：[步骤5获取的公钥]
4. 点击 "应用"
5. 重启 RustDesk
```

**设置示例**：
```
ID服务器：192.168.1.100
中继服务器：192.168.1.100
API服务器：http://192.168.1.100:21118
Key：ABCD1234EFGH5678IJKL9012MNOP3456QRST7890UVWX=
```

---

### 配置 2: 联想 ThinkBook+（客户端）

**局域网访问**：
```
1. 打开 RustDesk
2. 设置 → 网络 → ID 服务器：
   - ID服务器：192.168.x.x（飞牛NAS IP）
   - Key：[公钥]
3. 应用并重启
4. 输入铭凡的ID连接
```

**外网访问**：
```
1. 设置 → 网络 → ID 服务器：
   - ID服务器：[你的公网IP或域名]
   - Key：[公钥]
2. 应用并重启
3. 输入铭凡的ID连接
```

---

## 验证连接

### 测试 1: 局域网测试

```
1. 铭凡和ThinkBook+都配置好自建服务器
2. 在ThinkBook+上输入铭凡的ID
3. 应显示 "就绪"（Ready）
4. 点击连接
5. ✅ 成功连接
```

### 测试 2: 查看服务器日志

```bash
# 查看 hbbs 日志
docker logs rustdesk-hbbs

# 查看 hbbr 日志
docker logs rustdesk-hbbr

# 实时查看
docker logs -f rustdesk-hbbs
```

**期望看到**：
```
Listening on 0.0.0.0:21115
Listening on 0.0.0.0:21116
...
New peer connected: [ID]
```

---

## 性能优化

### 优化 1: 限制内存使用

修改 `docker-compose.yml`：
```yaml
services:
  hbbs:
    ...
    mem_limit: 256m

  hbbr:
    ...
    mem_limit: 256m
```

### 优化 2: 启用日志轮转

```yaml
services:
  hbbs:
    ...
    logging:
      driver: "json-file"
      options:
        max-size: "10m"
        max-file: "3"
```

---

## 管理命令

### 常用命令

```bash
# 查看状态
docker-compose ps

# 查看日志
docker-compose logs

# 重启服务
docker-compose restart

# 停止服务
docker-compose stop

# 启动服务
docker-compose start

# 更新服务器
docker-compose pull
docker-compose up -d

# 完全卸载
docker-compose down
```

---

## 故障排除

### 问题 1: 容器无法启动

**检查**：
```bash
# 查看详细日志
docker-compose logs

# 检查端口占用
netstat -tuln | grep -E "2111[5-9]"
```

**解决**：
- 确保端口未被占用
- 检查Docker服务是否运行
- 查看磁盘空间是否充足

---

### 问题 2: 客户端无法连接

**检查清单**：
```
1. ✅ 服务器容器运行正常
2. ✅ 防火墙端口已开放
3. ✅ 客户端配置了正确的服务器地址
4. ✅ 客户端配置了正确的Key
5. ✅ 网络连通性（ping 飞牛NAS IP）
```

**测试连通性**：
```bash
# 从ThinkBook+测试
telnet 192.168.x.x 21115
telnet 192.168.x.x 21116
telnet 192.168.x.x 21117
```

---

### 问题 3: 外网无法访问

**检查清单**：
```
1. ✅ 路由器端口转发配置正确
2. ✅ 公网IP地址正确
3. ✅ 防火墙允许入站连接
4. ✅ ISP没有封禁端口
```

**测试方法**：
```
使用在线端口扫描工具：
https://www.yougetsignal.com/tools/open-ports/

输入公网IP和端口21115测试
```

---

### 问题 4: 连接速度慢

**原因分析**：
- 使用了中继而非直连（P2P）
- 网络质量问题

**优化方法**：
```
1. 确保两端都配置了自建服务器
2. 检查NAT类型（Full Cone最佳）
3. 尝试手动配置直连
```

---

## 安全建议

### 1. 使用密钥认证

- ✅ 始终配置Key（公钥）
- ✅ 不使用默认公共服务器

### 2. 限制访问

```bash
# 仅允许特定IP访问（可选）
iptables -A INPUT -p tcp --dport 21115 -s 192.168.0.0/16 -j ACCEPT
iptables -A INPUT -p tcp --dport 21115 -j DROP
```

### 3. 定期更新

```bash
# 每月更新一次
docker-compose pull
docker-compose up -d
```

### 4. 备份配置

```bash
# 备份数据目录
tar -czf rustdesk-backup-$(date +%Y%m%d).tar.gz ./data
```

---

## 高级配置

### 配置 1: 使用域名（推荐）

**如果有域名**：
```
1. 配置 DDNS（动态域名解析）
2. 客户端使用域名而非IP
   - ID服务器：rustdesk.yourdomain.com
```

**优势**：
- 公网IP变化后无需重新配置
- 更专业

---

### 配置 2: HTTPS/SSL（高级）

**使用 Nginx 反向代理**：
```nginx
server {
    listen 443 ssl;
    server_name rustdesk.yourdomain.com;

    ssl_certificate /path/to/cert.pem;
    ssl_certificate_key /path/to/key.pem;

    location / {
        proxy_pass http://localhost:21118;
    }
}
```

---

## 成本分析

### 自建 vs 公共服务器

| 项目 | 公共服务器 | 自建服务器 |
|------|-----------|-----------|
| **费用** | 免费 | 免费（利用现有NAS） |
| **隐私** | 中等 | 高 |
| **速度** | 中等 | 高（局域网） |
| **可控性** | 低 | 高 |
| **维护** | 无 | 需要 |

**结论**：自建服务器更适合注重隐私和控制的场景

---

## 监控和维护

### 每周检查

```bash
# 检查服务状态
docker-compose ps

# 检查磁盘空间
df -h

# 检查日志大小
du -sh ./data
```

### 每月维护

```bash
# 更新服务器
docker-compose pull
docker-compose up -d

# 清理旧日志
docker system prune -f
```

---

## 总结

### ✅ 部署完成清单

- ✅ Docker Compose 部署完成
- ✅ 服务器容器运行正常
- ✅ 防火墙端口已开放
- ✅ 客户端配置完成
- ✅ 连接测试通过

### 🎯 优势

- ✅ 完全自主可控
- ✅ 数据隐私保护
- ✅ 可能更快（局域网）
- ✅ 完全免费

### 📊 性能预期

| 场景 | 延迟 | 说明 |
|------|------|------|
| 局域网 | < 10ms | 可能直连（P2P） |
| 外网 | 50-100ms | 取决于网络质量 |

---

**文档版本**: v1.0
**创建日期**: 2026-03-27
**适用环境**: 飞牛NAS + Docker

**开始部署你的私有 RustDesk 服务器吧！** 🚀
