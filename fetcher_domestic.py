"""
国内AI情報フェッチャー。

取得元：
  - ITmedia AI+  (AI専門フィード、フィルタ不要)
  - Gigazine      (全記事フィード、AIキーワードでフィルタ)

フィードのURLや追加先は FEEDS リストを編集してください。
"""

import feedparser
import logging

logger = logging.getLogger(__name__)

# AIと判定するキーワード（Gigazineフィルタ用）
_AI_KEYWORDS = [
    "AI", "人工知能", "ChatGPT", "Claude", "Gemini", "GPT", "LLM",
    "機械学習", "生成AI", "ディープラーニング", "deep learning",
    "OpenAI", "Anthropic", "画像生成", "自然言語処理", "大規模言語モデル",
    "Copilot", "Stable Diffusion", "Midjourney",
]

FEEDS = [
    {
        "url": "https://rss.itmedia.co.jp/rss/2.0/aiplus.xml",
        "source": "ITmedia AI+",
        "filter": False,   # AI専門なのでキーワードフィルタ不要
    },
    {
        "url": "https://gigazine.net/news/rss_2.0/",
        "source": "Gigazine",
        "filter": True,    # 全記事フィードなのでキーワードフィルタあり
    },
]


def _is_ai_related(title: str, summary: str = "") -> bool:
    text = (title + " " + summary)
    return any(kw.lower() in text.lower() for kw in _AI_KEYWORDS)


def fetch() -> list[dict]:
    """国内AI記事リストを返す。"""
    articles = []
    for feed_info in FEEDS:
        try:
            feed = feedparser.parse(feed_info["url"])
            for entry in feed.entries:
                title = entry.get("title", "").strip()
                url   = entry.get("link", "").strip()
                if not title or not url:
                    continue
                summary = entry.get("summary", "")
                if feed_info["filter"] and not _is_ai_related(title, summary):
                    continue
                articles.append({
                    "id":     url,
                    "title":  title,
                    "url":    url,
                    "source": feed_info["source"],
                })
        except Exception as e:
            logger.error(f"国内RSS取得失敗 ({feed_info['source']}): {e}")

    return articles
