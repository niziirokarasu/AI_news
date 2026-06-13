"""
海外AI ニュースフェッチャー。

AI専門のRSSフィードを取得する（キーワードフィルタ不要）。

取得元：
  - TechCrunch AI
  - VentureBeat AI
  - The Verge AI

フィードを追加・変更する場合は FEEDS リストを編集してください。
"""

import feedparser
import logging

logger = logging.getLogger(__name__)

FEEDS = [
    {
        "url": "https://techcrunch.com/category/artificial-intelligence/feed/",
        "source": "TechCrunch",
    },
    {
        "url": "https://venturebeat.com/category/ai/feed/",
        "source": "VentureBeat",
    },
    {
        "url": "https://www.theverge.com/ai-artificial-intelligence/rss/index.xml",
        "source": "The Verge",
    },
]


def fetch() -> list[dict]:
    """海外AI ニュース記事リストを返す。"""
    articles = []
    for feed_info in FEEDS:
        try:
            feed = feedparser.parse(feed_info["url"])
            for entry in feed.entries:
                title = entry.get("title", "").strip()
                url   = entry.get("link", "").strip()
                if not title or not url:
                    continue
                articles.append({
                    "id":     url,
                    "title":  title,
                    "url":    url,
                    "source": feed_info["source"],
                })
        except Exception as e:
            logger.error(f"海外RSS取得失敗 ({feed_info['source']}): {e}")

    return articles
