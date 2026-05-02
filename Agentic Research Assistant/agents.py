from crewai import Agent
from models import orchestator_llm, researcher_llm, analyst_llm, writer_planner_llm, writer_base_llm, reviewer_llm
from tools import internet_search, web_scraper, private_rag

# 注意：CrewAI中Agent的tools参数接受工具列表
# 我们将三个工具全部给研究员，分析师只给RAG，撰稿人和审校没有直接工具。

researcher = Agent(
    role='研究员',
    goal='针对研究主题，全面收集互联网与私有库的信息，产出信息池（每条信息含来源、内容、可信度评分）',
    backstory="你是一名资深行业研究员，擅长设计搜索策略、识别高质量信息源。",
    tools=[internet_search, web_scraper, private_rag],
    llm=researcher_llm,
    verbose=True
)

analyst = Agent(
    role='分析师',
    goal='将信息池转化为结构化的分析要点，识别趋势、矛盾，并给出图表建议',
    backstory="你是一名行业分析师，擅长数据提取、统计和逻辑归纳。",
    tools=[private_rag],  # 也可直接调用RAG补充数据
    llm=analyst_llm,
    verbose=True
)

writer = Agent(
    role='撰稿人',
    goal='根据分析要点和大纲，撰写专业、风格统一的行业研究报告（Markdown格式）',
    backstory="你是资深研报撰写人，文风客观严谨，善用行业术语。",
    llm=writer_base_llm,       # 实际撰写用微调模型
    function_calling_llm=writer_planner_llm,  # 控制逻辑用GPT-4
    verbose=True
)

reviewer = Agent(
    role='审校',
    goal='逐项检查报告：事实准确性、逻辑连贯性、格式规范，并输出修改意见',
    backstory="你是一名严格的编辑，确保报告零错误。",
    llm=reviewer_llm,
    verbose=True
)

# 编排器用单独Agent指导全局
orchestrator = Agent(
    role='编排器',
    goal='理解用户需求，拆解研究大纲，分派任务，监控进度，决定是否启动反思循环',
    backstory="你是项目管理者，协调多Agent协作完成高质量报告。",
    llm=orchestrator_llm,
    verbose=True
)