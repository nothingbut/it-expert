# TXT章节智能识别

## 快速使用

### 1. 准备环境
```bash
pip install openai sklearn-crfsuite jieba tqdm
```

### 2. 启动oMLX（确保Qwen2.5-0.5B已加载）
```bash
curl http://localhost:8000/v1/models -H "Authorization: Bearer 2348"
```

### 3. 放入小说文件
```bash
cp your_novels/*.txt novels/
```

### 4. 运行主动学习
```bash
python active_learning.py
```

## 工作流程

1. **LLM标注** → 自动标注10本初始样本
2. **CRF训练** → 训练轻量模型
3. **主动学习** → 只标注困难样本
4. **持续优化** → 自动迭代提升

## 输出

- `annotations/*.json` - 标注数据
- `models/crf_iter*.pkl` - 训练模型
- `output/` - 提取章节

## 参数调整

编辑 `active_learning.py`:
- `uncertainty_threshold`: 不确定性阈值(默认0.3)
- `initial_size`: 初始标注数量(默认10)
