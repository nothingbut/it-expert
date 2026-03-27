# 快速远程桌面连接脚本
# 用于从ThinkBook连接到铭凡小主机

# 配置参数
$MiniPCIP = "192.168.1.100"  # 修改为你的小主机IP地址
$Username = "MicrosoftAccount\your-email@outlook.com"  # 修改为你的Microsoft账户

# 创建RDP文件
$RdpContent = @"
screen mode id:i:2
use multimon:i:0
desktopwidth:i:1920
desktopheight:i:1080
session bpp:i:32
winposstr:s:0,3,0,0,800,600
compression:i:1
keyboardhook:i:2
audiocapturemode:i:0
videoplaybackmode:i:1
connection type:i:7
networkautodetect:i:1
bandwidthautodetect:i:1
displayconnectionbar:i:1
enableworkspacereconnect:i:0
disable wallpaper:i:0
allow font smoothing:i:0
allow desktop composition:i:0
disable full window drag:i:1
disable menu anims:i:1
disable themes:i:0
disable cursor setting:i:0
bitmapcachepersistenable:i:1
full address:s:$MiniPCIP
audiomode:i:0
redirectprinters:i:1
redirectcomports:i:0
redirectsmartcards:i:1
redirectclipboard:i:1
redirectposdevices:i:0
autoreconnection enabled:i:1
authentication level:i:2
prompt for credentials:i:0
negotiate security layer:i:1
remoteapplicationmode:i:0
alternate shell:s:
shell working directory:s:
gatewayhostname:s:
gatewayusagemethod:i:4
gatewaycredentialssource:i:4
gatewayprofileusagemethod:i:0
promptcredentialonce:i:0
gatewaybrokeringtype:i:0
use redirection server name:i:0
rdgiskdcproxy:i:0
kdcproxyname:s:
username:s:$Username
"@

# 保存RDP文件到桌面
$RdpFile = "$env:USERPROFILE\Desktop\连接小主机.rdp"
$RdpContent | Out-File -FilePath $RdpFile -Encoding ASCII

Write-Host "✅ RDP连接文件已创建：$RdpFile" -ForegroundColor Green
Write-Host ""
Write-Host "使用方法：" -ForegroundColor Cyan
Write-Host "1. 双击桌面上的'连接小主机.rdp'文件" -ForegroundColor Yellow
Write-Host "2. 首次连接时输入应用密码" -ForegroundColor Yellow
Write-Host "3. 勾选'允许我保存凭据'以便下次自动登录" -ForegroundColor Yellow
Write-Host ""
Write-Host "⚠️ 提醒：请先创建Microsoft应用密码" -ForegroundColor Magenta
Write-Host "访问：https://account.microsoft.com/security" -ForegroundColor Magenta
