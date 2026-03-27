# BASELINE.md OpenClaw 更新清单

> **日期**: 2026-03-27
> **原因**: OpenClaw v2026.3.24 重大升级，安装方式变更
> **参考**: openclaw-installation-plan-updated.md

## 📝 需要更新的位置

### 1. 第44行 - D盘空间分配
```
旧：- WSL2 + OpenClaw (计划): 40-55G
新：- WSL2 + OpenClaw (计划): ~17GB（Node.js方式更轻量）
```

### 2. 第196行 - 软件清单
```
旧：| OpenClaw | - | ~/projects/openclaw | ⬜ 未安装 |
新：| OpenClaw | v2026.3.24 | npm global | ⬜ 未安装 |
```

### 3. 第302-335行 - 整个部署项目章节
**需要完全重写**，关键变化：
- ❌ 删除：Docker 相关步骤
- ❌ 删除：腾讯 ClawBot SDK（官方已移除）
- ✅ 添加：Node.js 24 安装
- ✅ 添加：`openclaw onboard --install-daemon`
- ✅ 更新：3步安装流程

新的步骤概要：
```
阶段1: WSL2准备（如已安装跳过）
阶段2: Node.js 24 安装
阶段3: OpenClaw 安装（npm global）
阶段4: 配置引导（openclaw onboard）
阶段5: 连接 oMLX
```

### 4. 第396-419行 - 配置参数
```
旧：Docker compose 配置
新：~/.openclaw/config.yaml 配置

更新为：
### OpenClaw 配置（v2026.3.24）
配置文件位置: ~/.openclaw/config.yaml

models:
  providers:
    - id: omlx-local
      type: openai
      baseURL: http://192.168.x.x:8000/v1
      apiKey: "2348"

数据目录: ~/.openclaw/workspace/
日志目录: ~/.openclaw/logs/
```

### 5. 第449行 - 端口配置
```
旧：| OpenClaw | 8080 | 8080 | TCP | ⬜ 未配置 |
新：| OpenClaw Gateway | 18789 | 18789 | TCP | ⬜ 未配置 |
备注：默认端口从8080改为18789
```

### 6. 第486-490行 - 网络拓扑图
```
更新端口号：8080 → 18789
更新说明：OpenClaw Gateway (port 18789)
```

### 7. 新增章节（建议插入第302行之前）
```markdown
#### OpenClaw 版本信息
- **当前版本**: v2026.3.24（2026-03-25发布）
- **安装方式**: npm global + onboard wizard
- **需要**: Node.js 24（推荐）或 22.16+
- **文档**: openclaw-installation-plan-updated.md
- **官方文档**: https://docs.openclaw.ai/start/getting-started
```

## 🎯 更新优先级

**P0 - 必须更新**：
- 第302-335行（部署项目 - 核心变化）
- 第396-419行（配置参数 - 格式变化）

**P1 - 重要更新**：
- 第449行（端口号）
- 第44行（空间估算）

**P2 - 可选更新**：
- 第486-490行（网络拓扑图）
- 第196行（软件清单）

## 📚 参考文档

- **新安装文档**: openclaw-installation-plan-updated.md
- **旧文档（已过时）**: openclaw-installation-plan.md
- **官方发布说明**: https://github.com/openclaw/openclaw/releases/tag/v2026.3.24

## ✅ 更新后验证

更新完成后，确认：
- [ ] 所有端口号统一为 18789
- [ ] 删除所有 Docker 相关内容
- [ ] 删除腾讯 ClawBot 相关内容
- [ ] 添加 Node.js 要求
- [ ] 更新安装步骤为3步流程
- [ ] 更新配置文件路径和格式

---

**创建时间**: 2026-03-27
**预计完成时间**: 15-20分钟
