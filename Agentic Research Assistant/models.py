import os
from langchain_openai import ChatOpenAI
from crewai import LLM

# 中央编排器 – 使用最强模型
orchestrator_llm = LLM(
    model="openai/gpt-4o",
    temperature=0.2
)

# 研究员 – 主要用性价比高的模型做搜索query和结果筛选
researcher_llm = LLM(
    model="openai/gpt-4o-mini",
    temperature=0.1
)

# 分析师 – 关键推理用GPT-4，批量提取可用本地开源模型（这里用Ollama模拟）
analyst_llm = LLM(
    model="openai/gpt-4o-mini",   # 主推理，也可切为 gpt-4o 用于矛盾分析
    temperature=0.0
)
# 模拟开源模型端点（通过Ollama，需要本地安装并运行）
# 你可以改为实际地址
local_llm = LLM(
    model="ollama/qwen2.5:14b",  # 用于初稿撰写
    base_url="http://localhost:11434",
    temperature=0.3
)

# 撰稿人 – 基座用微调后的本地模型，编排用GPT-4
writer_base_llm = local_llm   # 实际环境下指向你微调好的模型
writer_planner_llm = LLM(model="openai/gpt-4o", temperature=0.4)

# 审校 – 用能力强且客观的模型
reviewer_llm = LLM(model="openai/gpt-4o-mini", temperature=0.0)