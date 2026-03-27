# ⚠️ 过时文档 - OpenClaw + 腾讯 ClawBot 安装方案

> **状态**: ❌ **已过时** - OpenClaw 在 v2026.3.24 进行了重大升级
>
> **请查看最新文档**: [openclaw-installation-plan-updated.md](./openclaw-installation-plan-updated.md)
>
> **更新日期**: 2026-03-27
> **原因**: 官方不再推荐 Docker 方式，改用 `openclaw onboard` 命令行安装

---

## 环境概述（历史参考）
- **目标机器**: 铭凡UM773 小主机
- **系统**: Windows 11 专业版
- **安装位置**: D盘（200G，已有60G Hyper-V虚拟机）
- **方案**: WSL2 + Ubuntu 容器（此方案已过时）

## 前置检查

### 1. 磁盘空间检查
D盘剩余空间约 140G（200G - 60G虚拟机），建议为 WSL2 预留 40-60G：
- Ubuntu 基础系统: ~10G
- OpenClaw + 依赖: ~10G
- 运行空间 + 数据: ~20-40G

### 2. 系统要求确认
- Windows 11 专业版 ✓（已满足）
- CPU 虚拟化支持（AMD-V）✓（需在BIOS中启用）
- 内存 64G ✓（充足）

---

## 安装步骤

### 阶段一：WSL2 配置到 D 盘

#### 1. 启用 WSL2 功能
在管理员权限的 PowerShell 中执行：

```powershell
# 启用 WSL 和虚拟机平台
dism.exe /online /enable-feature /featurename:Microsoft-Windows-Subsystem-Linux /all /norestart
dism.exe /online /enable-feature /featurename:VirtualMachinePlatform /all /norestart

# 重启计算机
Restart-Computer
```

#### 2. 安装 WSL2 内核更新
重启后，下载并安装 WSL2 Linux 内核更新包：
- 下载地址: https://aka.ms/wsl2kernel
- 或使用命令: `wsl --update`

#### 3. 设置 WSL2 为默认版本
```powershell
wsl --set-default-version 2
```

#### 4. 配置 WSL2 安装到 D 盘

创建 D 盘 WSL 目录：
```powershell
mkdir D:\WSL
mkdir D:\WSL\Ubuntu
```

创建 WSL 配置文件 `%USERPROFILE%\.wslconfig`：
```ini
[wsl2]
# 限制内存使用（建议分配 16-24G）
memory=20GB
# 限制处理器核心数
processors=8
# 启用虚拟硬盘自动压缩
autoMemoryReclaim=gradual
# 设置交换文件大小
swap=8GB
# 交换文件路径到 D 盘
swapFile=D:\\WSL\\swap.vhdx
# 网络模式（可选 NAT 或 mirrored）
networkingMode=NAT
```

#### 5. 安装 Ubuntu 到 D 盘

方法一：使用 Microsoft Store（推荐）
1. 打开 Microsoft Store
2. 搜索 "Ubuntu 24.04 LTS"（或 22.04）
3. 点击"获取"下载（但**不要直接安装**）

下载完成后，使用 PowerShell 导出并移动到 D 盘：
```powershell
# 安装到默认位置（临时）
wsl --install Ubuntu-24.04

# 导出到 D 盘
wsl --export Ubuntu-24.04 D:\WSL\ubuntu-backup.tar

# 注销原有实例
wsl --unregister Ubuntu-24.04

# 导入到 D 盘
wsl --import Ubuntu-24.04 D:\WSL\Ubuntu D:\WSL\ubuntu-backup.tar --version 2

# 设置为默认发行版
wsl --set-default Ubuntu-24.04

# 删除备份文件（可选）
Remove-Item D:\WSL\ubuntu-backup.tar
```

方法二：直接下载并导入
```powershell
# 下载 Ubuntu 根文件系统
# 从 https://cloud-images.ubuntu.com/releases/24.04/release/ 下载
# ubuntu-24.04-server-cloudimg-amd64-wsl.rootfs.tar.gz

# 导入到 D 盘
wsl --import Ubuntu-24.04 D:\WSL\Ubuntu D:\Downloads\ubuntu-24.04-server-cloudimg-amd64-wsl.rootfs.tar.gz --version 2

# 设置默认
wsl --set-default Ubuntu-24.04
```

#### 6. 配置 Ubuntu 用户
启动 WSL 并创建用户：
```bash
# 启动 WSL
wsl -d Ubuntu-24.04

# 创建用户（在 Ubuntu 中执行）
adduser clawuser
usermod -aG sudo clawuser

# 设置为默认用户（退出 WSL 后在 PowerShell 执行）
ubuntu2404.exe config --default-user clawuser
```

---

### 阶段二：安装 OpenClaw

#### 1. 更新系统并安装基础依赖
```bash
# 更新包管理器
sudo apt update && sudo apt upgrade -y

# 安装基础工具
sudo apt install -y \
    build-essential \
    git \
    curl \
    wget \
    ca-certificates \
    gnupg \
    lsb-release
```

#### 2. 安装 Docker（推荐方式）
```bash
# 添加 Docker 官方 GPG 密钥
sudo install -m 0755 -d /etc/apt/keyrings
curl -fsSL https://download.docker.com/linux/ubuntu/gpg | sudo gpg --dearmor -o /etc/apt/keyrings/docker.gpg
sudo chmod a+r /etc/apt/keyrings/docker.gpg

# 添加 Docker 仓库
echo \
  "deb [arch=$(dpkg --print-architecture) signed-by=/etc/apt/keyrings/docker.gpg] https://download.docker.com/linux/ubuntu \
  $(lsb_release -cs) stable" | sudo tee /etc/apt/sources.list.d/docker.list > /dev/null

# 安装 Docker
sudo apt update
sudo apt install -y docker-ce docker-ce-cli containerd.io docker-buildx-plugin docker-compose-plugin

# 将当前用户添加到 docker 组
sudo usermod -aG docker $USER

# 重新加载组权限
newgrp docker

# 验证安装
docker --version
docker compose version
```

#### 3. 克隆 OpenClaw 仓库
```bash
# 创建工作目录
mkdir -p ~/projects
cd ~/projects

# 克隆 OpenClaw（假设仓库地址）
# 注：请替换为实际的 OpenClaw 仓库地址
git clone https://github.com/your-org/openclaw.git
cd openclaw
```

#### 4. 配置 OpenClaw
```bash
# 复制配置文件模板
cp config.example.yaml config.yaml

# 编辑配置文件
nano config.yaml
```

主要配置项：
```yaml
# config.yaml 示例
server:
  host: "0.0.0.0"
  port: 8080

database:
  type: "postgresql"
  host: "localhost"
  port: 5432
  database: "openclaw"
  user: "clawuser"
  password: "your_secure_password"

storage:
  type: "local"
  path: "/mnt/d/openclaw-data"  # 映射到 D 盘
```

#### 5. 使用 Docker Compose 启动服务
```bash
# 创建数据目录（映射到 D 盘）
sudo mkdir -p /mnt/d/openclaw-data
sudo chown -R $USER:$USER /mnt/d/openclaw-data

# 启动服务
docker compose up -d

# 查看日志
docker compose logs -f

# 检查服务状态
docker compose ps
```

---

### 阶段三：集成腾讯 ClawBot

#### 1. 获取 ClawBot 凭证
在腾讯云控制台获取：
- App ID
- App Key
- Secret Key
- Bot Token

#### 2. 安装 ClawBot SDK
```bash
# 如果是 Python 项目
pip install tencentcloud-sdk-python

# 如果是 Node.js 项目
npm install tencentcloud-sdk-nodejs

# 如果是 Go 项目
go get -u github.com/tencentcloud/tencentcloud-sdk-go
```

#### 3. 配置 ClawBot 连接
创建 `clawbot-config.yaml`：
```yaml
clawbot:
  enabled: true
  app_id: "your_app_id"
  app_key: "your_app_key"
  secret_key: "your_secret_key"
  bot_token: "your_bot_token"
  webhook_url: "http://your-domain.com/webhook"

  # 回调配置
  callback:
    url: "http://localhost:8080/api/clawbot/callback"
    verify_token: "your_verify_token"

  # 功能配置
  features:
    auto_reply: true
    command_handling: true
    file_upload: true
```

#### 4. 配置环境变量（安全方式）
```bash
# 创建 .env 文件
cat > ~/projects/openclaw/.env << EOF
CLAWBOT_APP_ID=your_app_id
CLAWBOT_APP_KEY=your_app_key
CLAWBOT_SECRET_KEY=your_secret_key
CLAWBOT_BOT_TOKEN=your_bot_token
EOF

# 设置文件权限
chmod 600 ~/projects/openclaw/.env
```

#### 5. 更新 Docker Compose 配置
编辑 `docker-compose.yml`：
```yaml
version: '3.8'

services:
  openclaw:
    build: .
    ports:
      - "8080:8080"
    volumes:
      - /mnt/d/openclaw-data:/app/data
    env_file:
      - .env
    environment:
      - CLAWBOT_ENABLED=true
    depends_on:
      - postgres
      - redis

  postgres:
    image: postgres:16
    environment:
      POSTGRES_DB: openclaw
      POSTGRES_USER: clawuser
      POSTGRES_PASSWORD: your_secure_password
    volumes:
      - /mnt/d/openclaw-data/postgres:/var/lib/postgresql/data

  redis:
    image: redis:7-alpine
    volumes:
      - /mnt/d/openclaw-data/redis:/data
```

#### 6. 重启服务
```bash
# 停止服务
docker compose down

# 重新构建并启动
docker compose up -d --build

# 验证 ClawBot 连接
curl http://localhost:8080/api/clawbot/health
```

---

### 阶段四：网络配置和外部访问

#### 1. WSL2 端口转发（从 Windows 访问）
在 PowerShell（管理员）中执行：
```powershell
# 获取 WSL2 IP 地址
wsl hostname -I

# 添加端口转发规则
netsh interface portproxy add v4tov4 listenport=8080 listenaddress=0.0.0.0 connectport=8080 connectaddress=<WSL2_IP>

# 查看端口转发规则
netsh interface portproxy show all

# 添加防火墙规则
New-NetFirewallRule -DisplayName "WSL2 OpenClaw" -Direction Inbound -LocalPort 8080 -Protocol TCP -Action Allow
```

#### 2. 自动端口转发脚本
创建 `D:\WSL\forward-ports.ps1`：
```powershell
$wsl_ip = (wsl hostname -I).Trim()
Write-Host "WSL2 IP: $wsl_ip"

# 移除旧规则
netsh interface portproxy delete v4tov4 listenport=8080

# 添加新规则
netsh interface portproxy add v4tov4 listenport=8080 listenaddress=0.0.0.0 connectport=8080 connectaddress=$wsl_ip

Write-Host "Port forwarding configured for OpenClaw on port 8080"
```

设置开机自动运行（可选）：
```powershell
# 创建计划任务
$action = New-ScheduledTaskAction -Execute "PowerShell.exe" -Argument "-ExecutionPolicy Bypass -File D:\WSL\forward-ports.ps1"
$trigger = New-ScheduledTaskTrigger -AtStartup
$principal = New-ScheduledTaskPrincipal -UserId "SYSTEM" -LogonType ServiceAccount -RunLevel Highest
Register-ScheduledTask -TaskName "WSL2-PortForward" -Action $action -Trigger $trigger -Principal $principal
```

#### 3. 配置反向代理（可选，用于 HTTPS）
在 Ubuntu 中安装 Nginx：
```bash
sudo apt install -y nginx

# 配置反向代理
sudo nano /etc/nginx/sites-available/openclaw

# 内容如下：
server {
    listen 80;
    server_name your-domain.com;

    location / {
        proxy_pass http://localhost:8080;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;

        # WebSocket 支持
        proxy_http_version 1.1;
        proxy_set_header Upgrade $http_upgrade;
        proxy_set_header Connection "upgrade";
    }
}

# 启用站点
sudo ln -s /etc/nginx/sites-available/openclaw /etc/nginx/sites-enabled/
sudo nginx -t
sudo systemctl restart nginx
```

---

## 维护和管理

### 日常操作命令

```bash
# 启动 WSL
wsl -d Ubuntu-24.04

# 查看服务状态
cd ~/projects/openclaw
docker compose ps

# 查看日志
docker compose logs -f openclaw

# 重启服务
docker compose restart

# 停止服务
docker compose stop

# 备份数据
sudo tar -czf /mnt/d/backups/openclaw-backup-$(date +%Y%m%d).tar.gz /mnt/d/openclaw-data/
```

### Windows 管理命令

```powershell
# 查看 WSL 状态
wsl --list --verbose

# 停止 WSL
wsl --shutdown

# 启动特定发行版
wsl -d Ubuntu-24.04

# 查看 WSL 磁盘使用
wsl --list --verbose
Get-ChildItem D:\WSL\Ubuntu
```

### 性能优化

#### 1. WSL2 内存回收
创建定时任务自动释放内存：
```bash
# 在 Ubuntu 中创建脚本
cat > ~/cleanup-memory.sh << 'EOF'
#!/bin/bash
echo "Dropping caches..."
sync
echo 3 | sudo tee /proc/sys/vm/drop_caches
echo "Memory cleaned"
EOF

chmod +x ~/cleanup-memory.sh

# 添加到 crontab（每天凌晨2点执行）
crontab -e
# 添加: 0 2 * * * /home/clawuser/cleanup-memory.sh
```

#### 2. Docker 清理
```bash
# 清理未使用的镜像
docker image prune -a

# 清理未使用的容器
docker container prune

# 清理未使用的卷
docker volume prune

# 完整清理（谨慎使用）
docker system prune -a --volumes
```

### 监控和日志

```bash
# 实时监控资源使用
htop

# 查看磁盘使用
df -h

# 查看 Docker 资源使用
docker stats

# 导出日志
docker compose logs > /mnt/d/openclaw-data/logs/openclaw-$(date +%Y%m%d).log
```

---

## 故障排除

### 常见问题

#### 1. WSL2 启动失败
```powershell
# 检查虚拟化是否启用
systeminfo | findstr /C:"Hyper-V"

# 如果未启用，在 BIOS 中启用 AMD-V
# 然后重新安装 WSL2
```

#### 2. Docker 无法启动
```bash
# 检查 Docker 服务状态
sudo systemctl status docker

# 重启 Docker
sudo systemctl restart docker

# 查看 Docker 日志
sudo journalctl -u docker
```

#### 3. 网络连接问题
```bash
# 测试网络连接
ping 8.8.8.8
curl https://google.com

# 重置 WSL 网络
wsl --shutdown
# 在 PowerShell 中执行后重启 WSL
```

#### 4. 磁盘空间不足
```bash
# 压缩 WSL2 虚拟磁盘（在 PowerShell 中执行）
wsl --shutdown
Optimize-VHD -Path D:\WSL\Ubuntu\ext4.vhdx -Mode Full

# 或使用 diskpart
diskpart
select vdisk file="D:\WSL\Ubuntu\ext4.vhdx"
compact vdisk
exit
```

---

## 安全建议

1. **定期更新系统**
   ```bash
   sudo apt update && sudo apt upgrade -y
   ```

2. **使用强密码**
   - 数据库密码
   - ClawBot 凭证
   - 用户密码

3. **配置防火墙**
   ```bash
   sudo ufw enable
   sudo ufw allow 8080/tcp
   sudo ufw status
   ```

4. **定期备份**
   - 配置文件
   - 数据库
   - 用户数据

5. **环境变量隔离**
   - 使用 `.env` 文件
   - 不要提交敏感信息到 Git

---

## 总结

该方案通过以下步骤完成安装：
1. ✅ 配置 WSL2 到 D 盘（约 40-60G 空间）
2. ✅ 安装 Ubuntu 24.04 LTS
3. ✅ 使用 Docker 部署 OpenClaw
4. ✅ 集成腾讯 ClawBot
5. ✅ 配置网络端口转发
6. ✅ 设置监控和维护机制

**预计总时间**: 2-3 小时（取决于网络速度和熟悉程度）

**所需磁盘空间**:
- WSL2 系统: ~10G
- OpenClaw + Docker: ~10-15G
- 数据和日志: ~20-30G
- 总计: ~40-55G（D盘剩余140G足够）
