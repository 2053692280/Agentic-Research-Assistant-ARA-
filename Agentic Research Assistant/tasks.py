from crewai import Task
from agents import researcher, analyst, writer, reviewer, orchestrator
from crewai import Crew, Process

# ---------- 编排器先行任务：生成大纲和搜索指令 ----------
plan_task = Task(
    description=(
        "用户要求：{topic}\n"
        "请将研究主题拆解为详细的报告大纲（章、节标题），并为研究员生成5-10个核心搜索子主题。\n"
        "输出格式：\n大纲：[...]\n搜索子主题：[...]"
    ),
    expected_output="一个包含大纲和搜索子主题的清晰文档",
    agent=orchestrator
)

# ---------- 研究员任务 ----------
research_task = Task(
    description=(
        "根据以下搜索子主题，结合互联网搜索、爬虫深度抓取和私有知识库，收集所有相关信息。\n"
        "搜索子主题：{search_subtopics}\n"
        "对每条信息，标注来源URL、可信度（高/中/低）。最终汇总为信息池。"
    ),
    expected_output="信息池，每条格式：序号、标题、URL、内容摘要、可信度",
    agent=researcher,
    context=[plan_task]   # 从编排任务获取搜索结果
)

# ---------- 分析师任务 ----------
analysis_task = Task(
    description=(
        "基于提供的信息池，结合报告大纲（{outline}），进行数据分析与归纳。\n"
        "识别关键趋势、矛盾点，并标注每个结论对应的证据来源（引用信息池序号）。\n"
        "如果某一章节数据不足，明确说明需要补充的内容。"
        "输出分为：章节关键发现、数据表格、图表需求（如柱状图、饼图）"
    ),
    expected_output="结构化的分析要点文档，包含证据链接",
    agent=analyst,
    context=[research_task]
)

# ---------- 撰稿任务 ----------
writing_task = Task(
    description=(
        "严格根据以下大纲和对应分析要点，撰写完整的行业研究报告。\n"
        "大纲：{outline}\n"
        "分析要点：\n{analysis_points}\n"
        "要求：\n"
        "1. 采用券商研报风格，常用‘我们判断’、‘值得关注的是’等表述。\n"
        "2. 每个数据点必须插入引用标记，如 [源3-第5段]。\n"
        "3. 图表位置用 {{chart_01}} 占位。\n"
        "4. 最终输出为Markdown格式，包含所有章节。"
    ),
    expected_output="完整报告Markdown初稿",
    agent=writer,
    context=[analysis_task]
)

# ---------- 审校任务 ----------
review_task = Task(
    description=(
        "对以下报告初稿进行严格审校：\n"
        "报告：{draft_report}\n"
        "审校要点：\n"
        "- 用搜索引擎交叉验证关键数据（万元、亿元等单位）\n"
        "- 检查逻辑连贯性、术语一致性\n"
        "- 检查Markdown格式、图表引用\n"
        "输出修改列表，并给出终稿建议。如果问题严重（>2个事实错误），标记为需要重做。"
    ),
    expected_output="审校报告，包含错误清单和终稿建议",
    agent=reviewer,
    context=[writing_task]
)

# ---------- 反思控制任务（由编排器决定） ----------
reflection_task = Task(
    description=(
        "审校结果：{review_result}\n"
        "如果发现严重问题，规划下一步：\n"
        "1. 是否需要研究员补充缺失数据？\n"
        "2. 是否需要分析师重新核对矛盾？\n"
        "3. 是否需要撰稿人重写部分章节？\n"
        "请给出明确的命令：'重返研究' / '重返分析' / '重写段落' 或 '发布'."
    ),
    expected_output="一个决策指令",
    agent=orchestrator,
    context=[review_task]
)