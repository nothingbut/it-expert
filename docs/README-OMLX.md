# oMLX AI 服务器文档索引

> M4 Mac mini + oMLX 完整部署和使用指南

---

## 📚 文档概览

### 🚀 快速开始

| 文档 | 说明 | 适用场景 |
|------|------|----------|
| [QUICKSTART-OMLX.md](../QUICKSTART-OMLX.md) | oMLX 快速部署指南（5 步，15-30 分钟） | ⭐ 首次部署必读 |
| [omlx-embedding-quickstart.md](./omlx-embedding-quickstart.md) | 添加嵌入模型（5-10 分钟） | 需要语义搜索/RAG 功能 |

---

### 📖 完整文档

| 文档 | 说明 | 详细程度 |
|------|------|----------|
| [mac-omlx-deployment-plan.md](../mac-omlx-deployment-plan.md) | 完整部署方案（6 阶段，26 任务） | ⭐⭐⭐ 详细 |
| [omlx-quick-reference.md](./omlx-quick-reference.md) | 命令行参考 + 常见问题 | ⭐⭐ 实用 |
| [omlx-embedding-models.md](./omlx-embedding-models.md) | 嵌入模型详细指南 | ⭐⭐⭐ 详细 |

---

### 🔧 配置和客户端

| 文档 | 说明 | 目标读者 |
|------|------|----------|
| [omlx-client-configuration.md](./omlx-client-configuration.md) | ThinkBook + 铭凡小主机客户端配置 | ⭐ 必读 |
| [BASELINE.md](../BASELINE.md) | 系统基线（包含 oMLX 配置） | 管理员 |

---

### 📊 对比和选型

| 文档 | 说明 | 适用场景 |
|------|------|----------|
| [mlx-vs-omlx-comparison.md](./mlx-vs-omlx-comparison.md) | MLX vs oMLX 详细对比 | 技术选型 |
| [mlx-flexibility-deep-dive.md](./mlx-flexibility-deep-dive.md) | MLX 灵活性深度分析 | 研究、定制需求 |
| [mac-mlx-deployment-plan.md](../mac-mlx-deployment-plan.md) | MLX 手动部署方案（备选） | 高级用户、研究目的 |

---

## 🎯 快速导航

### 按任务查找

#### 首次部署 oMLX
1. 阅读：[QUICKSTART-OMLX.md](../QUICKSTART-OMLX.md)
2. 执行：5 步部署流程（15-30 分钟）
3. 验证：测试 API 调用

#### 添加嵌入模型
1. 阅读：[omlx-embedding-quickstart.md](./omlx-embedding-quickstart.md)
2. 执行：下载模型 + 重启服务（5-10 分钟）
3. 验证：测试嵌入 API

#### 配置客户端
1. 阅读：[omlx-client-configuration.md](./omlx-client-configuration.md)
2. 选择：ThinkBook 或 铭凡小主机配置
3. 测试：curl/Python 测试连接

#### 故障排除
1. 查看：[omlx-quick-reference.md](./omlx-quick-reference.md) - 常见问题章节
2. 运行：`scripts/omlx-diagnose.sh` 诊断脚本
3. 查看日志：`tail -f /tmp/omlx.log`

---

## 📦 当前部署状态

### M4 Mac mini（服务器）

| 项目 | 状态 | 值 |
|------|------|-----|
| **oMLX 版本** | ✅ 已安装 | v0.2.22 (2026-03-26) |
| **安装方式** | ✅ 已安装 | Homebrew + DMG |
| **服务地址** | ✅ 运行中 | http://0.0.0.0:8000 |
| **API Key** | ✅ 已配置 | `2348` |
| **Web 界面** | ✅ 可访问 | http://localhost:8000/admin/chat |

### 已部署模型

| 模型 | 用途 | 大小 | 状态 |
|------|------|------|------|
| Qwen3.5-0.8B | 通用对话 | 1.71GB | ✅ |
| OmniCoder-9B | 代码生成 | 18.40GB | ✅ |
| GLM-OCR | 视觉/OCR | 2.59GB | ✅ |
| **nomic-embed-4bit** | **文本嵌入** | **0.08GB** | ✅ |

**总计**: 22.78GB / 25.92GB (87.9%)

---

## 🔗 快速链接

### 服务访问

- **Web 管理界面**: http://localhost:8000/admin/chat
- **API 文档**: http://localhost:8000/docs
- **健康检查**: http://localhost:8000/health
- **模型列表**: `curl http://localhost:8000/v1/models -H "Authorization: Bearer 2348"`

### 配置文件

- **oMLX 配置**: `~/.omlx/settings.json`
- **模型目录**: `~/models/`
- **日志文件**: `/tmp/omlx.log` 或 `~/.omlx/logs/`

### 脚本工具

- **诊断脚本**: `scripts/omlx-diagnose.sh`
- **嵌入模型脚本**: `scripts/omlx-add-embedding-model.sh`
- **Python 客户端**: `scripts/omlx-embedding-client.py`

---

## 💡 使用示例

### curl 快速测试

```bash
# 设置变量
export OMLX_URL="http://localhost:8000/v1"
export API_KEY="2348"

# 对话测试
curl ${OMLX_URL}/chat/completions \
  -H "Authorization: Bearer ${API_KEY}" \
  -d '{
    "model": "Qwen3.5-0.8B",
    "messages": [{"role": "user", "content": "你好"}]
  }'

# 嵌入测试
curl ${OMLX_URL}/embeddings \
  -H "Authorization: Bearer ${API_KEY}" \
  -d '{
    "model": "nomic-embed-4bit",
    "input": "测试"
  }'
```

### Python 快速测试

```python
import requests

# 配置
API_URL = "http://localhost:8000/v1"
API_KEY = "2348"

# 对话
response = requests.post(
    f"{API_URL}/chat/completions",
    headers={'Authorization': f'Bearer {API_KEY}'},
    json={
        'model': 'Qwen3.5-0.8B',
        'messages': [{'role': 'user', 'content': '你好'}]
    }
)
print(response.json()['choices'][0]['message']['content'])

# 嵌入
response = requests.post(
    f"{API_URL}/embeddings",
    headers={'Authorization': f'Bearer {API_KEY}'},
    json={
        'model': 'nomic-embed-4bit',
        'input': '测试'
    }
)
print(f"维度: {len(response.json()['data'][0]['embedding'])}")
```

---

## 🎓 学习路径

### 初学者路径

1. **部署 oMLX**
   - 阅读：QUICKSTART-OMLX.md
   - 实践：在 Mac mini 上安装 oMLX
   - 时间：30 分钟

2. **测试基本功能**
   - 阅读：omlx-quick-reference.md（使用示例部分）
   - 实践：curl 测试对话和嵌入
   - 时间：15 分钟

3. **配置客户端**
   - 阅读：omlx-client-configuration.md
   - 实践：在 ThinkBook 上配置 Claude Code
   - 时间：20 分钟

### 进阶路径

1. **添加更多模型**
   - 阅读：omlx-embedding-quickstart.md
   - 实践：下载和配置专用模型
   - 时间：变动（取决于模型大小）

2. **优化性能**
   - 阅读：mac-omlx-deployment-plan.md（性能优化章节）
   - 实践：调整缓存、批处理参数
   - 时间：1 小时

3. **集成应用**
   - 阅读：omlx-client-configuration.md（各语言客户端）
   - 实践：在项目中集成 oMLX API
   - 时间：变动

### 高级路径

1. **深度理解架构**
   - 阅读：mlx-vs-omlx-comparison.md
   - 阅读：mlx-flexibility-deep-dive.md
   - 时间：2 小时

2. **自定义部署**
   - 阅读：mac-mlx-deployment-plan.md
   - 实践：从源码编译和定制
   - 时间：4-8 小时

3. **贡献和扩展**
   - 参与：oMLX GitHub 社区
   - 开发：自定义模型适配器
   - 时间：持续

---

## 🔍 故障排除索引

| 问题 | 文档位置 | 章节 |
|------|----------|------|
| oMLX 无法启动 | omlx-quick-reference.md | 故障排除 → 启动失败 |
| 模型未加载 | omlx-embedding-quickstart.md | 故障排除 → 模型未发现 |
| 网络无法访问 | omlx-client-configuration.md | 故障排除 → 无法连接 |
| API 认证错误 | omlx-quick-reference.md | 故障排除 → 认证问题 |
| 性能问题 | mac-omlx-deployment-plan.md | 性能优化 |
| 内存不足 | omlx-quick-reference.md | 故障排除 → OOM |

---

## 📞 获取帮助

### 官方资源

- **GitHub**: https://github.com/jundot/omlx
- **文档**: https://github.com/jundot/omlx/wiki
- **Issues**: https://github.com/jundot/omlx/issues

### 社区资源

- **Discord**: oMLX 社区（如有）
- **Reddit**: r/LocalLLaMA
- **Hugging Face**: mlx-community

### 本地资源

- **诊断脚本**: `scripts/omlx-diagnose.sh`
- **日志查看**: `tail -f /tmp/omlx.log`
- **配置检查**: `cat ~/.omlx/settings.json`

---

## 📅 更新记录

| 日期 | 版本 | 说明 |
|------|------|------|
| 2026-03-27 | 1.0 | 创建文档索引 |
| 2026-03-27 | 1.1 | 添加嵌入模型配置 |

---

## 📝 待办事项

- [ ] 在 Mac mini 上实际部署验证
- [ ] ThinkBook 客户端实际测试
- [ ] 铭凡小主机 WSL2 + OpenClaw 集成测试
- [ ] 性能基准测试和优化
- [ ] 添加更多模型（多语言、专用领域）
- [ ] 集成向量数据库（ChromaDB/Milvus）
- [ ] 监控和日志系统

---

**文档维护者**: AI Assistant
**最后更新**: 2026-03-27
**状态**: ✅ 初始版本完成，等待实际部署验证
