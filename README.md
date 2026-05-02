# Agentic Research Assistant

基于多智能体协作的自动化行业研究报告生成系统。
这个项目涉及信息搜集（Search）、分析、撰写报告，可以体现RAG、爬虫工具、多Agent分工（研究员、分析师、撰稿人、审校）、记忆与反思。可以集成多种模型，如用GPT-4做规划，用开源模型做特定嵌入或摘要，展示对模型能力边界的理解，还可加入微调领域报告风格。
## 使用方法
1. 安装依赖：`pip install -r requirements.txt`
2. 在项目根目录创建 `.env` 文件，写入你的 API 密钥（见下方说明）
3. 运行：`python main.py`

## 环境变量
在 `.env` 文件中设置：
OPENAI_API_KEY=你的密钥
TAVILY_API_KEY=你的密钥
