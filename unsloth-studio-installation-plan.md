# Unsloth Studio 安装方案 - 联想 ThinkBook+

> **目标设备**: 联想 ThinkBook+（Intel Core Ultra 155H, NVIDIA RTX 4060 8GB, 32GB RAM）
>
> **操作系统**: Windows 11 家庭版
>
> **创建日期**: 2026-03-24
>
> **预计时间**: 2-3 小时
>
> **难度**: 中等

---

## 目录
- [系统要求分析](#系统要求分析)
- [安装方案选择](#安装方案选择)
- [阶段一：环境准备](#阶段一环境准备)
- [阶段二：WSL2 配置](#阶段二wsl2-配置)
- [阶段三：安装 Unsloth](#阶段三安装-unsloth)
- [阶段四：验证和测试](#阶段四验证和测试)
- [性能优化建议](#性能优化建议)
- [常见问题排除](#常见问题排除)

---

## 系统要求分析

### 硬件评估

| 组件 | 规范 | Unsloth 要求 | 评估 |
|------|------|--------------|------|
| **GPU** | NVIDIA RTX 4060 (8GB VRAM) | 推荐 8GB+ | ✅ 满足最低要求 |
| **CPU** | Intel Core Ultra 155H | 支持 AVX2 | ✅ 支持 |
| **内存** | 32GB DDR5 | 推荐 32GB+ | ✅ 满足推荐要求 |
| **存储** | 1TB + 4TB M.2 SSD | 50GB+ 可用空间 | ✅ 充足 |
| **虚拟化** | 未确认 | 需启用 | ⚠️ 需在 BIOS 中确认 |

### 性能预期

**可训练的模型规模**（基于 8GB VRAM）：

| 模型类型 | 参数量 | 微调方法 | 预期显存占用 | 可行性 |
|---------|--------|----------|--------------|--------|
| Llama-3.2-1B | 1B | LoRA/QLoRA | ~4GB | ✅ 推荐 |
| Llama-3.2-3B | 3B | QLoRA (4-bit) | ~6GB | ✅ 可行 |
| Llama-3.1-8B | 8B | QLoRA (4-bit) | ~7.5GB | ⚠️ 勉强可行 |
| Mistral-7B | 7B | QLoRA (4-bit) | ~7GB | ⚠️ 勉强可行 |
| Llama-3.1-70B | 70B | QLoRA | >16GB | ❌ 超出硬件限制 |

**推荐场景**：
- ✅ 小型模型微调（1B-3B）
- ✅ 教学和学习
- ✅ 实验性项目
- ⚠️ 中型模型微调（7B-8B）- 需要优化
- ❌ 大型模型（>30B）- 不推荐

---

## 安装方案选择

### 推荐方案：WSL2 + Ubuntu + Unsloth

**选择理由**：
1. **原生 Linux 环境**：Unsloth 在 Linux 下性能最优
2. **GPU 直通支持**：WSL2 支持 NVIDIA CUDA
3. **隔离性好**：不影响 Windows 主系统
4. **易于管理**：可随时重置环境

**替代方案**：

| 方案 | 优点 | 缺点 | 推荐度 |
|------|------|------|--------|
| **WSL2 + Ubuntu** | 性能好、GPU 支持 | 需要 20-30GB 空间 | ⭐⭐⭐⭐⭐ |
| **Anaconda (Windows)** | 安装简单 | 性能较差、兼容性问题 | ⭐⭐⭐ |
| **Docker** | 环境隔离 | GPU 配置复杂 | ⭐⭐ |
| **双系统 Linux** | 性能最佳 | 切换麻烦、风险高 | ⭐⭐⭐⭐ |

**最终选择**：**WSL2 + Ubuntu 24.04 LTS**（平衡性能和易用性）

---

## 阶段一：环境准备

### 1.1 硬件检查

**步骤 1：确认 GPU 驱动**

在 PowerShell（管理员）中执行：

```powershell
# 检查 NVIDIA GPU
nvidia-smi
```

**预期输出**：
```
+---------------------------------------------------------------------------------------+
| NVIDIA-SMI 535.xx.xx    Driver Version: 535.xx.xx    CUDA Version: 12.2     |
|-------------------------------+----------------------+----------------------+
| GPU  Name        Persistence-M| Bus-Id        Disp.A | Volatile Uncorr. ECC |
| Fan  Temp  Perf  Pwr:Usage/Cap|         Memory-Usage | GPU-Util  Compute M. |
|===============================+======================+======================|
|   0  NVIDIA RTX 4060    Off  | 00000000:00:02.0  On |                  N/A |
| N/A   45C    P8    12W / 115W |    456MiB /  8192MiB |      2%      Default |
+-------------------------------+----------------------+----------------------+
```

**验证点**：
- ✅ GPU 型号显示为 RTX 4060
- ✅ 显存为 8192 MiB (8GB)
- ✅ CUDA Version ≥ 12.1

**如果失败**：
1. 访问 https://www.nvidia.com/Download/index.aspx
2. 下载并安装最新的 RTX 4060 驱动
3. 重启计算机后再次检查

---

**步骤 2：确认虚拟化支持**

在 PowerShell 中执行：

```powershell
# 检查 Hyper-V 要求
systeminfo | findstr /C:"Hyper-V"
```

**预期输出**：
```
Hyper-V Requirements:      VM Monitor Mode Extensions: Yes
                          Virtualization Enabled In Firmware: Yes
                          Second Level Address Translation: Yes
                          Data Execution Prevention Available: Yes
```

**如果显示 "No"**：
1. 重启电脑进入 BIOS（通常按 F2 或 Del）
2. 找到虚拟化选项：
   - Intel VT-x 或 Intel Virtualization Technology
   - Intel VT-d 或 Intel Virtualization Technology for Directed I/O
3. 启用这些选项
4. 保存并重启

---

**步骤 3：检查磁盘空间**

```powershell
# 查看各盘剩余空间
Get-PSDrive C,D | Select-Object Name,Used,Free,@{Name="UsedGB";Expression={[math]::Round($_.Used/1GB,2)}},@{Name="FreeGB";Expression={[math]::Round($_.Free/1GB,2)}}
```

**要求**：
- C 盘或 D 盘至少有 **50GB 可用空间**（推荐 80GB+）
- 建议安装在 **D 盘**（1TB SSD），保留 C 盘给系统

---

### 1.2 启用 WSL2 功能

在 PowerShell（管理员）中执行：

```powershell
# 启用 WSL 功能
dism.exe /online /enable-feature /featurename:Microsoft-Windows-Subsystem-Linux /all /norestart

# 启用虚拟机平台
dism.exe /online /enable-feature /featurename:VirtualMachinePlatform /all /norestart

# 启用虚拟机监控程序
dism.exe /online /enable-feature /featurename:VirtualMachineMonitor /all /norestart
```

**预期输出**：
```
操作成功完成。
```

**重启计算机**：
```powershell
Restart-Computer
```

---

### 1.3 更新 WSL2 内核

重启后，下载并安装 WSL2 内核更新：

**方法一：自动更新（推荐）**
```powershell
wsl --update
wsl --update --accept-source-licensees
```

**方法二：手动下载**
- 访问：https://aka.ms/wsl2kernel
- 下载并安装 `wsl_update_x64.msi`

**验证安装**：
```powershell
wsl --version
```

**预期输出**：
```
WSL 版本: 2.x.x.x.0
内核版本: 5.x.x.x
WSLg 版本: 1.x.x.x
MSRDC 版本: 1.x.x.x
Direct3D 版本: 1.6xx.xxxxx
DXCore 版本: 1.6xx.xxxxx
Windows 版本: 10.x.xxxxx.x
```

---

### ✅ 阶段一验收清单

- [ ] NVIDIA 驱动已安装（nvidia-smi 正常显示）
- [ ] BIOS 虚拟化已启用
- [ ] 磁盘空间充足（≥50GB）
- [ ] WSL2 功能已启用
- [ ] WSL2 内核已更新
- [ ] 系统已重启

---

## 阶段二：WSL2 配置

### 2.1 设置 WSL2 安装到 D 盘

**创建 WSL 目录**：

```powershell
# 创建 WSL 目录
mkdir D:\WSL
mkdir D:\WSL\Ubuntu
```

---

**配置 WSL2 全局设置**：

创建用户目录下的 WSL 配置文件：

```powershell
# 创建 .wslconfig 文件
notepad $env:USERPROFILE\.wslconfig
```

**粘贴以下内容**：

```ini
[wsl2]
# 内存限制（ThinkBook+ 有 32GB，分配 16GB 给 WSL2）
memory=16GB

# 处理器核心数（Intel Ultra 155H 有 14 核，分配 8 核）
processors=8

# 交换文件大小
swap=8GB

# 交换文件路径（放在 D 盘）
swapFile=D:\\WSL\\swap.vhdx

# 自动内存回收
autoMemoryReclaim=gradual

# 网络模式（mirrored 模式提供更好的网络兼容性）
networkingMode=mirrored

# DNS 隧道模式
dnsTunneling=true

# 防火墙设置
firewall=true

# 自动代理检测
autoProxy=true
```

**保存并关闭**。

---

### 2.2 安装 Ubuntu 24.04 LTS

**方法一：Microsoft Store 安装（推荐）**

1. 打开 Microsoft Store
2. 搜索 "Ubuntu 24.04 LTS"
3. 点击"获取"或"安装"
4. 等待下载完成（约 1-2GB）

**方法二：命令行安装**

```powershell
# 直接安装 Ubuntu 24.04 LTS
wsl --install Ubuntu-24.04
```

安装完成后会自动打开 Ubuntu 终端窗口。

---

### 2.3 移动 WSL 到 D 盘（如果安装在了 C 盘）

**检查默认安装位置**：

```powershell
wsl -l -v
```

如果显示在 C 盘，执行以下步骤：

```powershell
# 1. 导出 Ubuntu 到 D 盘
wsl --export Ubuntu-24.04 D:\WSL\ubuntu-backup.tar

# 2. 注销原实例
wsl --unregister Ubuntu-24.04

# 3. 导入到 D 盘
wsl --import Ubuntu-24.04 D:\WSL\Ubuntu D:\WSL\ubuntu-backup.tar --version 2

# 4. 设置默认发行版
wsl --set-default Ubuntu-24.04

# 5. 删除备份文件（可选）
Remove-Item D:\WSL\ubuntu-backup.tar
```

---

### 2.4 初始化 Ubuntu

**首次启动 Ubuntu**：

```powershell
# 启动 Ubuntu
wsl -d Ubuntu-24.04
```

首次启动会提示创建用户账号：

```
Installing, this may take a few minutes...
Please create a default UNIX user account. The username does not need to match your Windows username.
For more information visit: https://aka.ms/wslusers
Enter new UNIX username: thinkbook
Enter new UNIX password:
Retype new UNIX password:
passwd: password updated successfully
Installation successful!
```

**记录信息**：
- 用户名：`thinkbook`（或自定义）
- 密码：（设置一个强密码并记住）

---

**设置默认用户**（如果需要）：

```powershell
# 在 Windows PowerShell 中执行
ubuntu2404 config --default-user thinkbook
```

---

### 2.5 更新 Ubuntu 系统

**在 Ubuntu 终端中执行**：

```bash
# 更新包列表
sudo apt update

# 升级已安装的包
sudo apt upgrade -y

# 安装基础工具
sudo apt install -y \
    build-essential \
    git \
    curl \
    wget \
    vim \
    htop \
    unzip \
    python3-pip \
    python3-venv
```

**预计时间**：10-15 分钟

---

### 2.6 验证 WSL2 GPU 支持

**检查 GPU 是否可见**：

```bash
# 在 Ubuntu 终端中执行
ls -la /usr/lib/wsl/lib/
```

**预期输出**（应包含 GPU 相关库）：
```
...
libcuda.so.1 -> libcuda.so.1.1
libcuda.so.1.1
libnvinfer.so.8 -> libnvinfer.so.8.6.1
...
```

---

**安装 NVIDIA CUDA 工具**（可选，用于验证）：

```bash
# 检查 CUDA 版本
nvidia-smi
```

**预期输出**：
```
+---------------------------------------------------------------------------------------+
| NVIDIA-SMI 535.xx.xx    Driver Version: 535.xx.xx    CUDA Version: 12.2     |
|-------------------------------+----------------------+----------------------+
| GPU  Name        Persistence-M| Bus-Id        Disp.A | Volatile Uncorr. ECC |
| Fan  Temp  Perf  Pwr:Usage/Cap|         Memory-Usage | GPU-Util  Compute M. |
|===============================+======================+======================+
|   0  NVIDIA RTX 4060    Off  | 00000000:00:02.0 Off |                  N/A |
| 0%   42C    P8    5W / 115W |      0MiB /  8192MiB |      0%      Default |
+-------------------------------+----------------------+----------------------+
```

如果看到此输出，说明 **WSL2 GPU 直通已成功配置**！✅

---

### ✅ 阶段二验收清单

- [ ] WSL2 已安装到 D 盘
- [ ] Ubuntu 24.04 LTS 已安装
- [ ] .wslconfig 已配置（16GB 内存，8 核）
- [ ] 用户账号已创建
- [ ] 系统包已更新
- [ ] GPU 在 WSL2 中可见（nvidia-smi 正常）

---

## 阶段三：安装 Unsloth

### 3.1 安装 Miniconda

**下载 Miniconda**：

```bash
# 下载 Miniconda 安装脚本
wget https://repo.anaconda.com/miniconda/Miniconda3-latest-Linux-x86_64.sh

# 运行安装脚本
bash Miniconda3-latest-Linux-x86_64.sh -b -p $HOME/miniconda3
```

**预计时间**：3-5 分钟

---

**初始化 Conda**：

```bash
# 初始化 conda
~/miniconda3/bin/conda init bash

# 重新加载 shell
source ~/.bashrc
```

---

**验证安装**：

```bash
conda --version
```

**预期输出**：
```
conda 24.x.x
```

---

### 3.2 创建 Python 虚拟环境

**创建环境**：

```bash
# 创建 Python 3.10 环境（Unsloth 推荐）
conda create -n unsloth python=3.10 -y
```

**预计时间**：2-3 分钟

---

**激活环境**：

```bash
# 激活 unsloth 环境
conda activate unsloth
```

**提示符会变为**：
```
(unsloth) thinkbook@THINKBOOK:~$
```

---

### 3.3 安装 PyTorch（CUDA 版本）

**检查 CUDA 版本**：

```bash
# 根据之前 nvidia-smi 的输出选择 CUDA 版本
# 假设显示 CUDA 12.2
```

---

**安装 PyTorch**（适用于 CUDA 12.x）：

```bash
# 安装 PyTorch 2.x（支持 CUDA 12.1+）
pip install torch torchvision torchaudio --index-url https://download.pytorch.org/whl/cu121
```

**预计时间**：5-10 分钟（取决于网络速度）

**替代方案**（如果上述方法失败）：

```bash
# 使用 conda 安装（更稳定）
conda install pytorch torchvision torchaudio pytorch-cuda=12.1 -c pytorch -c nvidia
```

---

**验证 PyTorch GPU 支持**：

```bash
python3 -c "import torch; print(f'PyTorch: {torch.__version__}'); print(f'CUDA Available: {torch.cuda.is_available()}'); print(f'CUDA Version: {torch.version.cuda}'); print(f'GPU Name: {torch.cuda.get_device_name(0) if torch.cuda.is_available() else \"N/A\"}')"
```

**预期输出**：
```
PyTorch: 2.x.x+cu121
CUDA Available: True
CUDA Version: 12.1
GPU Name: NVIDIA RTX 4060
```

如果看到 `CUDA Available: True`，说明 **PyTorch GPU 支持已成功配置**！✅

---

### 3.4 安装 Unsloth

**方法一：标准安装（推荐）**

```bash
# 确保在 unsloth 环境中
conda activate unsloth

# 安装 Unsloth
pip install "unsloth[colab-new] @ git+https://github.com/unslothai/unsloth.git"
```

**预计时间**：5-10 分钟

---

**方法二：开发版安装（包含最新功能）**

```bash
pip install "unsloth[cu121-torch240] @ git+https://github.com/unslothai/unsloth.git"
```

---

**安装 Hugging Face 依赖**：

```bash
# 安装 Transformers 和其他依赖
pip install transformers trl accelerate datasets peft bitsandbytes
```

---

### 3.5 安装 Xformers（可选，加速训练）

```bash
# 安装 xformers（兼容 PyTorch 2.x）
pip install xformers
```

**如果失败**，跳过此步骤（Unsloth 会自动处理）。

---

### 3.6 配置 Hugging Face（用于下载模型）

**登录 Hugging Face**（如果需要访问受限制的模型）：

```bash
# 安装 Hugging Face CLI
pip install huggingface_hub

# 登录
huggingface-cli login
```

**输入 Token**：
1. 访问 https://huggingface.co/settings/tokens
2. 创建一个 Access Token（选择 "Read" 权限）
3. 粘贴 Token 到终端

---

### ✅ 阶段三验收清单

- [ ] Miniconda 已安装
- [ ] unsloth conda 环境已创建
- [ ] PyTorch 已安装并支持 CUDA
- [ ] Unsloth 已安装
- [ ] Hugging Face CLI 已配置（如需要）

---

## 阶段四：验证和测试

### 4.1 运行 Unsloth 示例

**创建测试脚本**：

```bash
# 创建项目目录
mkdir -p ~/unsloth-projects
cd ~/unsloth-projects

# 创建测试脚本
vim test_unsloth.py
```

**粘贴以下代码**：

```python
from unsloth import FastLanguageModel
import torch
from transformers import TextStreamer

print("=" * 60)
print("Unsloth 安装验证测试")
print("=" * 60)

# 检查 CUDA
print(f"\n✅ PyTorch 版本: {torch.__version__}")
print(f"✅ CUDA 可用: {torch.cuda.is_available()}")
if torch.cuda.is_available():
    print(f"✅ GPU 设备: {torch.cuda.get_device_name(0)}")
    print(f"✅ GPU 显存: {torch.cuda.get_device_properties(0).total_memory / 1024**3:.1f} GB")
    print(f"✅ CUDA 版本: {torch.version.cuda}")

# 加载一个小模型测试
print("\n" + "=" * 60)
print("加载测试模型 (Llama-3.2-1B-Instruct)...")
print("=" * 60)

model, tokenizer = FastLanguageModel.from_pretrained(
    model_name = "unsloth/llama-3-8b-bnb-4bit",  # 使用 4-bit 量化版本
    max_seq_length = 2048,
    dtype = None,
    load_in_4bit = True,
)

print("\n✅ 模型加载成功！")
print(f"✅ 模型显存占用: {torch.cuda.memory_allocated() / 1024**3:.2f} GB")

# 测试推理
print("\n" + "=" * 60)
print("测试推理功能...")
print("=" * 60)

FastLanguageModel.for_inference(model)  # 启用快速推理

inputs = tokenizer(
[
    "请用一句话介绍 Python 编程语言。",
], return_tensors = "pt").to("cuda")

outputs = model.generate(**inputs, max_new_tokens = 64, use_cache = True)
print("\n生成结果:")
print(tokenizer.decode(outputs[0], skip_special_tokens = True))

print("\n" + "=" * 60)
print("🎉 所有测试通过！Unsloth 已成功安装并可用！")
print("=" * 60)
```

**保存并退出**（在 Vim 中按 `Esc`，输入 `:wq`，按 `Enter`）

---

**运行测试**：

```bash
# 确保在 unsloth 环境中
conda activate unsloth

# 运行测试脚本
python test_unsloth.py
```

**预计时间**：
- 首次运行：5-10 分钟（需要下载模型）
- 后续运行：1-2 分钟

---

**预期输出**：

```
==============================================================
Unsloth 安装验证测试
==============================================================

✅ PyTorch 版本: 2.1.0+cu121
✅ CUDA 可用: True
✅ GPU 设备: NVIDIA RTX 4060
✅ GPU 显存: 8.0 GB
✅ CUDA 版本: 12.1

==============================================================
加载测试模型 (Llama-3.2-1B-Instruct)...
==============================================================

正在下载模型文件...
model.safetensors: 100%|████████████████| 4.50G [00:10<00:00, 450MB/s]
...

✅ 模型加载成功！
✅ 模型显存占用: 5.23 GB

==============================================================
测试推理功能...
==============================================================

生成结果:
请用一句话介绍 Python 编程语言。
Python 是一种高级编程语言，以其简洁的语法、强大的功能和广泛的应用领域而闻名。

==============================================================
🎉 所有测试通过！Unsloth 已成功安装并可用！
==============================================================
```

---

### 4.2 创建微调示例

**创建微调脚本**：

```bash
vim finetune_example.py
```

**粘贴以下代码**：

```python
from unsloth import FastLanguageModel
import torch
from trl import SFTTrainer
from transformers import TrainingArguments
from datasets import load_dataset

# 加载模型
model, tokenizer = FastLanguageModel.from_pretrained(
    model_name = "unsloth/llama-3-8b-bnb-4bit",
    max_seq_length = 2048,
    dtype = None,
    load_in_4bit = True,
)

# 添加 LoRA 适配器
model = FastLanguageModel.get_peft_model(
    model,
    r = 16,
    target_modules = ["q_proj", "k_proj", "v_proj", "o_proj"],
    lora_alpha = 16,
    lora_dropout = 0,
    bias = "none",
    use_gradient_checkpointing = True,
    random_state = 3407,
    use_rslora = False,
    loftq_config = None,
)

# 准备训练数据
dataset = load_dataset("yahma/alpaca-cleaned", split = "train")

# 配置训练器
trainer = SFTTrainer(
    model = model,
    tokenizer = tokenizer,
    train_dataset = dataset,
    dataset_text_field = "text",
    max_seq_length = 2048,
    dataset_num_proc = 2,
    packing = False,
    args = TrainingArguments(
        per_device_train_batch_size = 2,
        gradient_accumulation_steps = 4,
        warmup_steps = 5,
        max_steps = 20,  # 仅用于演示
        learning_rate = 2e-4,
        fp16 = not torch.cuda.is_bf16_supported(),
        bf16 = torch.cuda.is_bf16_supported(),
        logging_steps = 1,
        optim = "adamw_8bit",
        weight_decay = 0.01,
        lr_scheduler_type = "linear",
        seed = 3407,
        output_dir = "outputs",
    ),
)

# 开始训练
print("开始微调...")
trainer.train()

# 保存模型
model.save_pretrained_gguf("model", tokenizer, quantization_method = "q4_k_m")
print("✅ 微调完成！模型已保存。")
```

**注意**：这是完整的微调示例，但由于 RTX 4060 8GB 的限制，建议：
- 使用更小的模型（1B-3B）
- 减少 `max_steps` 进行快速测试
- 降低 `per_device_train_batch_size` 到 1

---

### ✅ 阶段四验收清单

- [ ] Unsloth 测试脚本运行成功
- [ ] 模型可以正常加载
- [ ] CUDA GPU 正常工作
- [ ] 推理测试通过
- [ ] （可选）微调示例运行成功

---

## 性能优化建议

### 针对 RTX 4060 8GB 的优化

**1. 使用量化模型**

```python
# 4-bit 量化（推荐）
model, tokenizer = FastLanguageModel.from_pretrained(
    model_name = "unsloth/llama-3-8b-bnb-4bit",
    load_in_4bit = True,
)

# 或使用更小的模型
model, tokenizer = FastLanguageModel.from_pretrained(
    model_name = "unsloth/Llama-3.2-1B",
)
```

**2. 调整训练参数**

```python
trainer = SFTTrainer(
    ...
    args = TrainingArguments(
        per_device_train_batch_size = 1,  # 降低到 1
        gradient_accumulation_steps = 8,  # 增加梯度累积
        max_steps = 100,  # 限制训练步数
        ...
    ),
)
```

**3. 启用梯度检查点**

```python
model = FastLanguageModel.get_peft_model(
    model,
    use_gradient_checkpointing = True,  # 节省显存
    ...
)
```

**4. 监控显存使用**

```python
import torch

# 训练前
print(f"显存使用: {torch.cuda.memory_allocated() / 1024**3:.2f} GB")

# 训练中
print(f"显存峰值: {torch.cuda.max_memory_allocated() / 1024**3:.2f} GB")
```

---

### 推荐的模型配置

| 任务 | 推荐模型 | 量化 | 预期显存 | 批大小 |
|------|----------|------|----------|--------|
| **教学/学习** | Llama-3.2-1B | 无 | ~4GB | 4 |
| **实验性微调** | Llama-3.2-3B | 4-bit | ~6GB | 2 |
| **生产环境** | Mistral-7B | 4-bit | ~7GB | 1 |

---

## 常见问题排除

### 问题 1：CUDA 不可见

**症状**：
```python
torch.cuda.is_available()  # 返回 False
```

**解决方案**：

1. **检查 WSL2 GPU 支持**：
```bash
ls -la /usr/lib/wsl/lib/
```

2. **确保 .wslconfig 配置正确**：
```ini
[wsl2]
# 添加这行
nestedVirtualization=true
```

3. **重启 WSL**：
```powershell
wsl --shutdown
```

---

### 问题 2：显存不足（OOM）

**症状**：
```
RuntimeError: CUDA out of memory
```

**解决方案**：

1. **使用更小的模型**：
```python
model, tokenizer = FastLanguageModel.from_pretrained(
    model_name = "unsloth/Llama-3.2-1B",  # 使用 1B 模型
)
```

2. **减少批大小**：
```python
per_device_train_batch_size = 1
```

3. **清理 GPU 缓存**：
```python
import torch
torch.cuda.empty_cache()
```

---

### 问题 3：下载模型速度慢

**解决方案**：

1. **使用 Hugging Face 镜像**：
```bash
export HF_ENDPOINT=https://hf-mirror.com
```

2. **手动下载模型**：
```bash
# 从其他设备下载后复制到 WSL
cp /mnt/d/models/* ~/.cache/huggingface/hub/
```

---

### 问题 4：Unsloth 导入失败

**症状**：
```
ImportError: cannot import name 'FastLanguageModel'
```

**解决方案**：

1. **重新安装 Unsloth**：
```bash
pip uninstall unsloth -y
pip install "unsloth[colab-new] @ git+https://github.com/unslothai/unsloth.git"
```

2. **检查依赖版本**：
```bash
pip list | grep -E "torch|transformers|peft"
```

---

### 问题 5：WSL2 网络问题

**症状**：无法下载模型或包

**解决方案**：

1. **检查网络模式**：
```ini
[wsl2]
networkingMode=mirrored  # 或 NAT
```

2. **重置 WSL 网络**：
```powershell
wsl --shutdown
# 重新启动 WSL
wsl -d Ubuntu-24.04
```

---

## 后续工作

### 推荐的学习资源

1. **Unsloth 官方文档**：https://github.com/unslothai/unsloth
2. **Hugging Face 教程**：https://huggingface.co/learn
3. **微调示例**：https://github.com/unslothai/unsloth#-fine-tuning

### 推荐的下一步

1. ✅ 完成 Unsloth 安装和验证
2. 📚 学习 LoRA 微调基础知识
3. 🎯 选择一个实际项目进行微调
4. 📊 监控训练过程和性能指标
5. 💾 定期备份微调后的模型

### 项目创意

- **对话助手**：微调 Llama-3.2-1B 实现中文对话
- **代码生成**：微调 CodeLlama 辅助编程
- **文本摘要**：微调模型生成文章摘要
- **情感分析**：微调分类模型进行情感识别

---

## 总结

### 安装总结

**总耗时**：2-3 小时
- 环境准备：30 分钟
- WSL2 配置：45 分钟
- Unsloth 安装：45 分钟
- 验证测试：30 分钟

**磁盘占用**：
- WSL2 基础系统：~10GB
- Miniconda：~1GB
- 模型缓存：~5-10GB（取决于下载的模型）
- **总计**：~20-30GB

**硬件限制**：
- 最大可用显存：8GB
- 推荐模型规模：1B-3B
- 可训练模型：7B-8B（需要优化）

---

### 最终检查清单

- [ ] WSL2 + Ubuntu 24.04 已安装在 D 盘
- [ ] NVIDIA 驱动支持 WSL2 GPU 直通
- [ ] Miniconda + Python 3.10 环境已创建
- [ ] PyTorch + CUDA 12.x 已安装
- [ ] Unsloth 已成功安装
- [ ] 测试脚本运行通过
- [ ] 可以加载和运行模型
- [ ] GPU 显存使用正常（<8GB）

---

### 联系与支持

- **Unsloth Discord**: https://discord.gg/unsloth
- **Hugging Face Forum**: https://discuss.huggingface.co/
- **WSL2 GitHub**: https://github.com/microsoft/WSL

---

**祝您使用 Unsloth 愉快！** 🚀

如有任何问题，请参考上述故障排除指南或访问官方社区寻求帮助。
