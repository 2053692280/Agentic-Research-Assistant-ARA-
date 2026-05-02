import os
from crewai import Crew, Process
from agents import orchestrator, researcher, analyst, writer, reviewer
from tasks import plan_task, research_task, analysis_task, writing_task, review_task, reflection_task
from memory import memory

# 设置API密钥（请替换为你的真实密钥或环境变量）
os.environ["OPENAI_API_KEY"] = "your-openai-api-key"
os.environ["TAVILY_API_KEY"] = "your-tavily-api-key"

def run_report(topic: str):
    print(f"🚀 开始生成报告：{topic}\n")

    # 1. 编排器规划
    crew_plan = Crew(
        agents=[orchestrator],
        tasks=[plan_task],
        process=Process.sequential,
        verbose=True
    )
    plan_result = crew_plan.kickoff(inputs={"topic": topic})
    # 从结果中解析大纲和搜索子主题（这里简化，直接用字符串）
    outline = plan_result.raw  # 实际应解析，这里假设包含大纲描述
    search_subtopics = plan_result.raw  # 在生产环境中你会做更精细的提取

    print("📋 大纲生成完毕，开始研究...\n")

    # 2. 研究 -> 分析 -> 撰写 -> 审校 顺序执行
    crew_main = Crew(
        agents=[researcher, analyst, writer, reviewer],
        tasks=[research_task, analysis_task, writing_task, review_task],
        process=Process.sequential,
        verbose=True,
        memory=True,  # CrewAI内建短期记忆
        planning=True  # 允许计划
    )
    inputs = {
        "topic": topic,
        "search_subtopics": search_subtopics,
        "outline": outline,
        "analysis_points": "",  # 将在分析任务产出后填入
        "draft_report": ""      # 将在撰写任务后填入
    }
    main_result = crew_main.kickoff(inputs=inputs)
    draft_report = main_result.raw   # 中间环节的最终输出应为审校后的报告

    # 3. 审校后决定是否需要反思循环
    print("\n🔍 审校结果检查中...")
    reflection_crew = Crew(
        agents=[orchestrator],
        tasks=[reflection_task],
        process=Process.sequential,
        verbose=True
    )
    decision = reflection_crew.kickoff(inputs={"review_result": draft_report})
    print(f"编排器决策：{decision}")

    # 4. 简单模拟：如果决策包含"发布"，保存报告
    if "发布" in str(decision):
        final_report = draft_report
        with open(f"report_{topic[:10]}.md", "w") as f:
            f.write(final_report)
        print("✅ 报告已生成并保存！")
        memory.add_task_record(topic, "success", "完整流程完成。")
    else:
        print("⚠️ 报告需要修改，可在实际系统中注入循环。")
        memory.add_lesson(f"主题'{topic}'第一次审校未通过，需人工干预。")

if __name__ == "__main__":
    topic = "2024年中国AI制药行业深度研究报告"
    run_report(topic)