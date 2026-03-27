# AI 辅助应用示例代码

## 📁 目录结构

```
samples/
├── navigation/              # 应用内智能导航
│   ├── navigation_assistant.py
│   └── examples/
└── chapter-extraction/      # TXT章节识别
    ├── llm_annotator.py
    ├── crf_trainer.py
    ├── active_learning.py
    ├── annotations/         # 标注数据
    ├── models/             # 训练模型
    ├── novels/             # 小说文件
    └── output/             # 输出结果
```

## 🚀 快速开始

### 1. 智能导航

```bash
cd samples/navigation
python navigation_assistant.py
```

### 2. 章节识别

```bash
cd samples/chapter-extraction

# 放入小说文件到 novels/
# 运行主动学习
python active_learning.py
```

## 📖 详细文档

完整文档：[docs/ai-assistant-solutions.md](../docs/ai-assistant-solutions.md)
