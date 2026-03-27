"""LLM自动标注工具"""
from openai import OpenAI
from typing import List, Dict
import json
from tqdm import tqdm

class LLMAnnotator:
    def __init__(self, model: str = "Qwen2.5-0.5B-Instruct"):
        self.client = OpenAI(base_url="http://localhost:8000/v1", api_key="2348")
        self.model = model
        self.prompt_template = """分析文本，判断哪些行是章节标题。
只输出0或1列表，用逗号分隔。1=章节标题，0=非章节。

文本：
{text}

标注："""

    def annotate_batch(self, lines: List[str], batch_size: int = 10) -> List[int]:
        annotations = []
        for i in tqdm(range(0, len(lines), batch_size), desc="标注中"):
            batch = lines[i:i + batch_size]
            text = '\n'.join([f"{j+1}. {line.strip()}" for j, line in enumerate(batch)])

            try:
                response = self.client.chat.completions.create(
                    model=self.model,
                    messages=[{"role": "user", "content": self.prompt_template.format(text=text)}],
                    max_tokens=50, temperature=0.1
                )
                result = response.choices[0].message.content.strip()
                labels = [int(x.strip()) for x in result.split(',')]
                annotations.extend([1 if x > 0 else 0 for x in labels[:len(batch)]])
            except:
                annotations.extend([0] * len(batch))
        return annotations

    def annotate_file(self, file_path: str, output_path: str = None) -> Dict:
        with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
            lines = f.readlines()

        annotations = self.annotate_batch(lines)
        data = {
            'file_path': file_path,
            'lines': [line.strip() for line in lines],
            'annotations': annotations,
            'chapter_count': sum(annotations)
        }

        if output_path:
            with open(output_path, 'w', encoding='utf-8') as f:
                json.dump(data, f, ensure_ascii=False, indent=2)

        print(f"✅ {file_path}: {len(lines)}行, {sum(annotations)}章节")
        return data
