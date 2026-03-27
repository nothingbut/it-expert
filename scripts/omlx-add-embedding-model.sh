#!/bin/bash

# oMLX 添加嵌入模型脚本
# 用于在 M4 Mac mini 上加载 nomic-embed-text-v2-moe
# 使用配置文件方式（正确方法）

set -e  # 遇到错误立即退出

# 颜色输出
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# 配置参数
MODEL_ID="nomic-ai/nomic-embed-text-v2-moe"
MODEL_TYPE="embedding"

echo -e "${GREEN}========================================${NC}"
echo -e "${GREEN}oMLX 嵌入模型配置脚本${NC}"
echo -e "${GREEN}========================================${NC}"
echo ""
echo -e "模型ID: ${YELLOW}${MODEL_ID}${NC}"
echo -e "模型类型: ${YELLOW}${MODEL_TYPE}${NC}"
echo ""

# 步骤1：查找配置文件
echo -e "${YELLOW}[1/6] 查找 oMLX 配置文件...${NC}"

CONFIG_LOCATIONS=(
    "$HOME/.omlx/config.yaml"
    "$HOME/.omlx/config.yml"
    "$HOME/omlx/config.yaml"
    "$HOME/.config/omlx/config.yaml"
)

CONFIG_FILE=""
for config in "${CONFIG_LOCATIONS[@]}"; do
    if [ -f "$config" ]; then
        CONFIG_FILE="$config"
        echo -e "${GREEN}✅ 找到配置文件: ${CONFIG_FILE}${NC}"
        break
    fi
done

if [ -z "$CONFIG_FILE" ]; then
    echo -e "${YELLOW}⚠️  未找到配置文件，将创建新的${NC}"
    CONFIG_FILE="$HOME/.omlx/config.yaml"
    mkdir -p "$(dirname "$CONFIG_FILE")"
    echo -e "${GREEN}   创建: ${CONFIG_FILE}${NC}"
fi
echo ""

# 步骤2：备份原配置
echo -e "${YELLOW}[2/6] 备份原配置文件...${NC}"
if [ -f "$CONFIG_FILE" ]; then
    BACKUP_FILE="${CONFIG_FILE}.backup.$(date +%Y%m%d_%H%M%S)"
    cp "$CONFIG_FILE" "$BACKUP_FILE"
    echo -e "${GREEN}✅ 备份已创建: ${BACKUP_FILE}${NC}"
else
    echo -e "${YELLOW}⚠️  无需备份（新建配置）${NC}"
fi
echo ""

# 步骤3：检查模型是否已在配置中
echo -e "${YELLOW}[3/6] 检查模型配置...${NC}"
if [ -f "$CONFIG_FILE" ] && grep -q "$MODEL_ID" "$CONFIG_FILE"; then
    echo -e "${YELLOW}⚠️  模型已存在于配置中${NC}"
    echo -e "${BLUE}   如需重新配置，请手动编辑: ${CONFIG_FILE}${NC}"
    ALREADY_CONFIGURED=true
else
    echo -e "${GREEN}✅ 模型未配置，将添加${NC}"
    ALREADY_CONFIGURED=false
fi
echo ""

# 步骤4：添加模型到配置
if [ "$ALREADY_CONFIGURED" = false ]; then
    echo -e "${YELLOW}[4/6] 添加模型到配置文件...${NC}"

    # 检查配置文件是否存在且不为空
    if [ -s "$CONFIG_FILE" ]; then
        # 配置文件已有内容，追加新模型
        echo -e "${BLUE}   追加模型配置...${NC}"

        # 检查是否有 models 部分
        if grep -q "^models:" "$CONFIG_FILE"; then
            # 在 models 部分下添加
            cat >> "$CONFIG_FILE" << EOF

  - repo_id: "${MODEL_ID}"
    model_type: "${MODEL_TYPE}"
    adapter_path: null
EOF
        else
            # 创建 models 部分
            cat >> "$CONFIG_FILE" << EOF

models:
  - repo_id: "${MODEL_ID}"
    model_type: "${MODEL_TYPE}"
    adapter_path: null
EOF
        fi
    else
        # 创建新的配置文件
        echo -e "${BLUE}   创建新配置文件...${NC}"
        cat > "$CONFIG_FILE" << 'EOF'
# oMLX 配置文件
# 文档: https://github.com/jundot/omlx

models:
  - repo_id: "Qwen/Qwen3.5-9B-Instruct"
    model_type: "text-generation"
    adapter_path: null

  - repo_id: "deepseek-ai/OmniCoder-9B"
    model_type: "text-generation"
    adapter_path: null

  - repo_id: "THUDM/GLM-4V-9B"
    model_type: "vision"
    adapter_path: null

  - repo_id: "nomic-ai/nomic-embed-text-v2-moe"
    model_type: "embedding"
    adapter_path: null

server:
  host: "0.0.0.0"
  port: 8080

cache:
  enabled: true
  size_mb: 2048

quantization:
  enabled: true
  bits: 4
EOF
    fi

    echo -e "${GREEN}✅ 模型配置已添加${NC}"
else
    echo -e "${YELLOW}[4/6] 跳过添加（已配置）${NC}"
fi
echo ""

# 步骤5：显示配置文件
echo -e "${YELLOW}[5/6] 显示当前配置...${NC}"
echo -e "${BLUE}--- ${CONFIG_FILE} ---${NC}"
cat "$CONFIG_FILE"
echo ""

# 步骤6：重启服务提示
echo -e "${YELLOW}[6/6] 服务重启说明${NC}"
echo ""
echo -e "${GREEN}✅ 配置更新完成！${NC}"
echo ""
echo -e "${BLUE}请执行以下步骤使配置生效：${NC}"
echo ""
echo -e "1️⃣  ${YELLOW}停止当前 oMLX 服务（如果运行中）：${NC}"
echo -e "   pkill -f omlx"
echo ""
echo -e "2️⃣  ${YELLOW}启动 oMLX 服务：${NC}"
echo -e "   omlx serve"
echo -e "   或指定配置："
echo -e "   omlx serve --config ${CONFIG_FILE}"
echo ""
echo -e "3️⃣  ${YELLOW}验证模型加载：${NC}"
echo -e "   curl http://localhost:8080/v1/models"
echo ""
echo -e "4️⃣  ${YELLOW}测试嵌入：${NC}"
echo -e "   python3 scripts/omlx-embedding-client.py"
echo ""

# 附加信息
echo -e "${GREEN}========================================${NC}"
echo -e "${GREEN}使用说明${NC}"
echo -e "${GREEN}========================================${NC}"
echo ""
echo -e "${YELLOW}通过 Python 调用：${NC}"
cat << 'EOF'

import requests

response = requests.post(
    'http://localhost:8080/v1/embeddings',
    json={
        'model': 'nomic-ai/nomic-embed-text-v2-moe',
        'input': '你的文本'
    }
)
embedding = response.json()['data'][0]['embedding']
print(f"维度: {len(embedding)}")  # 768

EOF

echo ""
echo -e "${YELLOW}通过 curl 调用：${NC}"
cat << 'EOF'

curl http://localhost:8080/v1/embeddings \
  -H "Content-Type: application/json" \
  -d '{
    "model": "nomic-ai/nomic-embed-text-v2-moe",
    "input": "你的文本"
  }'

EOF

echo ""
echo -e "${GREEN}========================================${NC}"
echo -e "${GREEN}故障排除${NC}"
echo -e "${GREEN}========================================${NC}"
echo ""
echo -e "${YELLOW}如果模型未加载：${NC}"
echo -e "1. 检查配置文件语法（YAML 格式）"
echo -e "2. 查看 oMLX 日志："
echo -e "   omlx serve 2>&1 | tee omlx.log"
echo -e "3. 手动下载模型（如果网络问题）："
echo -e "   huggingface-cli download ${MODEL_ID}"
echo ""
echo -e "${YELLOW}检查服务状态：${NC}"
echo -e "   curl http://localhost:8080/v1/models"
echo ""
echo -e "${BLUE}配置文件位置: ${CONFIG_FILE}${NC}"
echo ""
