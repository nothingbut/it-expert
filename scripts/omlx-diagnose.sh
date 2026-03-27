#!/bin/bash

# oMLX 诊断脚本 - 查找正确的配置方法

echo "======================================"
echo "oMLX 环境诊断"
echo "======================================"
echo ""

# 1. 检查 oMLX 安装
echo "[1/6] 检查 oMLX 安装..."
if command -v omlx &> /dev/null; then
    echo "✅ oMLX 已安装"
    OMLX_PATH=$(which omlx)
    echo "   路径: $OMLX_PATH"

    # 查看版本信息
    omlx --version 2>/dev/null || echo "   无法获取版本信息"
else
    echo "❌ oMLX 未安装或不在 PATH 中"
    exit 1
fi
echo ""

# 2. 查看可用命令
echo "[2/6] 查看 oMLX 可用命令..."
echo "--- omlx --help ---"
omlx --help 2>&1 | head -20
echo ""

# 3. 查看 serve 命令选项
echo "[3/6] 查看 serve 命令选项..."
echo "--- omlx serve --help ---"
omlx serve --help 2>&1 | head -30
echo ""

# 4. 查看 launch 命令选项
echo "[4/6] 查看 launch 命令选项..."
echo "--- omlx launch --help ---"
omlx launch --help 2>&1 | head -30
echo ""

# 5. 查找配置文件
echo "[5/6] 查找配置文件..."
CONFIG_LOCATIONS=(
    "$HOME/.omlx/config.yaml"
    "$HOME/.omlx/config.yml"
    "$HOME/omlx/config.yaml"
    "$HOME/.config/omlx/config.yaml"
    "./config.yaml"
)

FOUND_CONFIG=""
for config in "${CONFIG_LOCATIONS[@]}"; do
    if [ -f "$config" ]; then
        echo "✅ 找到配置文件: $config"
        FOUND_CONFIG="$config"
        echo ""
        echo "--- 配置文件内容（前20行）---"
        head -20 "$config"
        break
    fi
done

if [ -z "$FOUND_CONFIG" ]; then
    echo "⚠️  未找到现有配置文件"
    echo "   搜索位置："
    for config in "${CONFIG_LOCATIONS[@]}"; do
        echo "   - $config"
    done
fi
echo ""

# 6. 检查 oMLX 进程
echo "[6/6] 检查 oMLX 运行状态..."
if pgrep -f "omlx" > /dev/null; then
    echo "✅ oMLX 进程运行中"
    echo ""
    echo "--- 进程信息 ---"
    ps aux | grep omlx | grep -v grep
    echo ""

    # 尝试访问 API
    echo "--- 测试 API 连接 ---"
    if curl -s http://localhost:8080/health > /dev/null 2>&1; then
        echo "✅ API 可访问: http://localhost:8080"

        # 列出已加载的模型
        echo ""
        echo "--- 当前已加载的模型 ---"
        curl -s http://localhost:8080/v1/models | jq '.' 2>/dev/null || curl -s http://localhost:8080/v1/models
    else
        echo "⚠️  API 不可访问（可能监听其他端口）"
        echo "   尝试其他端口："
        for port in 8000 8001 8080 8888; do
            if curl -s http://localhost:$port/health > /dev/null 2>&1; then
                echo "   ✅ 找到服务: http://localhost:$port"
            fi
        done
    fi
else
    echo "⚠️  oMLX 进程未运行"
    echo "   启动命令: omlx serve"
fi
echo ""

# 7. 查看 Python 模块信息（如果是 Python 包）
echo "======================================"
echo "Python 模块信息"
echo "======================================"
python3 -c "import omlx; print('oMLX 版本:', omlx.__version__)" 2>/dev/null || echo "⚠️  无法导入 omlx Python 模块"
echo ""

# 8. 总结和建议
echo "======================================"
echo "总结和建议"
echo "======================================"
echo ""
echo "根据上述信息，请执行以下操作："
echo ""
echo "1. 如果配置文件存在，请编辑它添加新模型"
echo "2. 如果配置文件不存在，请创建一个（见下方示例）"
echo "3. 使用 'omlx serve' 启动服务"
echo ""
echo "--- 配置文件示例 ---"
cat << 'EOF'
# ~/.omlx/config.yaml

models:
  - repo_id: "Qwen/Qwen3.5-9B-Instruct"
    model_type: "text-generation"

  - repo_id: "nomic-ai/nomic-embed-text-v2-moe"
    model_type: "embedding"

server:
  host: "0.0.0.0"
  port: 8080

cache:
  enabled: true
  size: 2048

quantization:
  enabled: true
  bits: 4
EOF
echo ""
