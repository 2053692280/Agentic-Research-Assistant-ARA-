import json
from datetime import datetime

class MemoryStore:
    def __init__(self, file_path="long_term_memory.json"):
        self.file_path = file_path
        try:
            with open(file_path, 'r') as f:
                self.mem = json.load(f)
        except:
            self.mem = {"tasks": [], "lessons": [], "style_notes": []}

    def add_task_record(self, topic, outcome, notes):
        self.mem["tasks"].append({
            "topic": topic,
            "time": datetime.now().isoformat(),
            "outcome": outcome,
            "notes": notes
        })
        self._save()

    def add_lesson(self, lesson):
        self.mem["lessons"].append(lesson)
        self._save()

    def get_recent_lessons(self, k=3):
        return self.mem["lessons"][-k:]

    def _save(self):
        with open(self.file_path, 'w') as f:
            json.dump(self.mem, f, indent=2, ensure_ascii=False)

# 全局记忆实例
memory = MemoryStore()