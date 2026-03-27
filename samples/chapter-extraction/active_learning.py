"""主动学习流程"""
from llm_annotator import LLMAnnotator
from crf_trainer import ChapterCRFTrainer
import glob, os

class ActiveLearningPipeline:
    def __init__(self, uncertainty_threshold: float = 0.3):
        self.annotator = LLMAnnotator()
        self.trainer = ChapterCRFTrainer()
        self.threshold = uncertainty_threshold
        self.iteration = 0

    def run(self, novel_files: list, initial_size: int = 10):
        """主动学习主流程"""
        os.makedirs('annotations', exist_ok=True)
        os.makedirs('models', exist_ok=True)

        # 第一轮：标注初始样本
        print(f"\n🔄 第{self.iteration+1}轮：标注{initial_size}个初始样本")
        for file in novel_files[:initial_size]:
            output = f"annotations/{os.path.basename(file)}.json"
            self.annotator.annotate_file(file, output)

        # 训练初始模型
        annotation_files = glob.glob('annotations/*.json')
        self.trainer.train(annotation_files)
        self.trainer.save(f'models/crf_iter{self.iteration}.pkl')
        self.iteration += 1

        # 主动学习循环
        for file in novel_files[initial_size:]:
            # 预测不确定性
            uncertainty = self._calculate_uncertainty(file)

            print(f"\n📊 {os.path.basename(file)}: 不确定性={uncertainty:.2f}")

            if uncertainty > self.threshold:
                print(f"  → 触发标注（不确定性>{self.threshold}）")
                output = f"annotations/{os.path.basename(file)}.json"
                self.annotator.annotate_file(file, output)

                # 重新训练
                annotation_files = glob.glob('annotations/*.json')
                self.trainer.train(annotation_files)
                self.trainer.save(f'models/crf_iter{self.iteration}.pkl')
                self.iteration += 1
            else:
                print(f"  → 跳过（不确定性<{self.threshold}）")

        print(f"\n✅ 主动学习完成，总迭代{self.iteration}轮")

    def _calculate_uncertainty(self, file_path: str) -> float:
        """计算预测不确定性"""
        with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
            lines = f.readlines()

        # 提取特征并预测
        X = []
        for i, line in enumerate(lines):
            prev = lines[i-1].strip() if i > 0 else ""
            next = lines[i+1].strip() if i < len(lines)-1 else ""
            X.append(self.trainer.extract_features(line.strip(), i, len(lines), prev, next))

        # 预测边际概率
        marginals = self.crf.predict_marginals([X])[0]
        uncertainties = [1 - max(m.values()) for m in marginals]
        return sum(uncertainties) / len(uncertainties)

if __name__ == "__main__":
    pipeline = ActiveLearningPipeline(uncertainty_threshold=0.3)
    novel_files = glob.glob('novels/*.txt')
    pipeline.run(novel_files, initial_size=5)
