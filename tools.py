from langchain.tools import tool 
import requests
from bs4 import BeautifulSoup
from tavily import TavilyClient
import os 
from dotenv import load_dotenv
from rich import print
import json
load_dotenv()

tavily = TavilyClient(api_key=os.getenv("TAVILY_API_KEY"))

@tool
def web_search(query : str) -> str:
    """Search the web for recent and reliable information on a topic . Returns Titles , URLs and snippets."""
    results = tavily.search(query=query,max_results=5)

    out = []

    for r in results['results']:
        out.append(
            f"Title: {r['title']}\nURL: {r['url']}\nSnippet: {r['content'][:300]}\n"
        )
    
    return "\n----\n".join(out)

@tool
def scrape_url(url: str) -> str:
    """Scrape and return clean text content from a given URL for deeper reading."""
    try:
        resp = requests.get(url, timeout=8, headers={"User-Agent": "Mozilla/5.0"})
        soup = BeautifulSoup(resp.text, "html.parser")
        for tag in soup(["script", "style", "nav", "footer"]):
            tag.decompose()
        return soup.get_text(separator=" ", strip=True)[:3000]
    except Exception as e:
        return f"Could not scrape URL: {str(e)}"

import json

@tool
def latest_news() -> str:
    """Fetch the latest news from the past 24 hours from different categories such as business, technology, politics, environment and trading."""

    results = tavily.search(
        query=(
            "latest important news from different categories: "
            "business, technology, politics, environment, trading, "
            "science and AI"
        ),
        topic="news",
        time_range="day",
        max_results=6
    )

    out = []

    for r in results["results"]:
        out.append({
            "title": r.get("title", ""),
            "url": r.get("url", ""),
            "source": r.get("source", "Web"),
            "category": "LATEST",
            "summary": r.get("content", "")[:500]
        })

    return json.dumps(out, ensure_ascii=False)

