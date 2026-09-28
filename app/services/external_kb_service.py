import html
import re
from urllib.parse import quote

import httpx


WIKIPEDIA_SEARCH_URL = "https://zh.wikipedia.org/w/api.php"
WIKIPEDIA_SUMMARY_URL = "https://zh.wikipedia.org/api/rest_v1/page/summary/"

HEADERS = {
    "User-Agent": "RAG-KB-Student/0.1 (contact: your-email@example.com)",
    "Accept-Language": "zh-CN,zh;q=0.9",
}


def _clean_html(text: str) -> str:
    text = re.sub(r"<[^>]+>", "", text)
    return html.unescape(text).strip()


async def search_wikipedia(query: str, limit: int = 3) -> list[dict]:
    params = {
        "action": "query",
        "list": "search",
        "srsearch": query,
        "format": "json",
        "srlimit": str(limit),
        "variant": "zh-cn",
    }

    async with httpx.AsyncClient(timeout=15, headers=HEADERS) as client:
        response = await client.get(WIKIPEDIA_SEARCH_URL, params=params)
        response.raise_for_status()
        data = response.json()

        search_items = data.get("query", {}).get("search", [])
        sources = []

        for item in search_items:
            title = item.get("title", "")
            snippet = _clean_html(item.get("snippet", ""))
            page_url = f"https://zh.wikipedia.org/wiki/{quote(title)}"
            text = snippet

            try:
                summary_response = await client.get(
                    f"{WIKIPEDIA_SUMMARY_URL}{quote(title)}"
                , headers=HEADERS)
                if summary_response.status_code == 200:
                    summary_data = summary_response.json()
                    text = summary_data.get("extract") or snippet
            except Exception:
                pass

            sources.append(
                {
                    "title": title,
                    "url": page_url,
                    "text": text,
                }
            )

        return sources