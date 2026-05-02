from crewai_tools import tool
import requests
from bs4 import BeautifulSoup
from langchain_community.vectorstores import Chroma
from langchain_openai import OpenAIEmbeddings
import os

# ========== 1. 搜索工具（使用Tavily，也可换SerpAPI） ==========
@tool("InternetSearch")
def internet_search(query: str) -> str:
    """Search the internet for recent information. Input: search query string."""
    from tavily import TavilyClient
    client = TavilyClient(api_key=os.getenv("TAVILY_API_KEY"))
    response = client.search(query, search_depth="advanced", max_results=5)
    results = []
    for r in response['results']:
        results.append(f"Title: {r['title']}\nURL: {r['url']}\nContent: {r['content']}\n")
    return "\n---\n".join(results)

# ========== 2. 网页爬虫工具（深度抓取） ==========
@tool("WebScraper")
def web_scraper(url: str) -> str:
    """Scrape and extract main article text from a URL. Input: a valid URL."""
    try:
        headers = {'User-Agent': 'Mozilla/5.0'}
        resp = requests.get(url, headers=headers, timeout=10)
        soup = BeautifulSoup(resp.text, 'html.parser')
        # 简单去噪，提取正文（可按网站定制）
        for script in soup(["script", "style", "nav", "footer", "header"]):
            script.extract()
        text = soup.get_text(separator='\n', strip=True)
        # 截取前8000字符避免token超限
        return text[:8000]
    except Exception as e:
        return f"Scraping error: {str(e)}"

# ========== 3. RAG私有库检索工具 ==========
@tool("PrivateKnowledgeBase")
def private_rag(query: str) -> str:
    """Search internal company reports, white papers. Input: query string."""
    embeddings = OpenAIEmbeddings(model="text-embedding-3-small")
    # 假设已存在持久化的向量库，如果没有则返回空
    persist_dir = "./data/chroma_db"
    if not os.path.exists(persist_dir):
        return "Private knowledge base is empty."
    vectorstore = Chroma(persist_database_directory=persist_dir,
                         embedding_function=embeddings)
    docs = vectorstore.similarity_search(query, k=3)
    return "\n\n".join([d.page_content for d in docs])