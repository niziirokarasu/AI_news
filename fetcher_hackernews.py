"""
HackerNews AI情報フェッチャー。

Algolia HN API を使って AI関連の最新ストーリーを取得する。
APIキー不要・無料。

MIN_HN_POINTS 未満のポイントのストーリーは通知しない（低品質フィルタ）。
"""

import requests
import logging

import config

logger = logging.getLogger(__name__)

_API_URL = "https://hn.algolia.com/api/v1/search"

_QUERY = "AI | LLM | ChatGPT | Claude | Gemini | OpenAI | Anthropic"


def fetch() -> list[dict]:
    """HackerNews のAI関連ストーリーをポイント降順で返す。

    search_by_date（直近のみ）ではなく search（関連度・ポイント順）を使う。
    seen機構で既通知を除外するため、常にトップ30を取得しても重複しない。
    """
    try:
        response = requests.get(
            _API_URL,
            params={
                "query": _QUERY,
                "tags": "story",
                "hitsPerPage": 30,
            },
            timeout=15,
        )
        response.raise_for_status()
        data = response.json()
    except Exception as e:
        logger.error(f"HackerNews API取得失敗: {e}")
        return []

    articles = []
    for hit in data.get("hits", []):
        title  = hit.get("title", "").strip()
        hn_id  = hit.get("objectID", "")
        points = hit.get("points") or 0

        if not title or not hn_id:
            continue
        if points < config.MIN_HN_POINTS:
            continue

        # 外部URLがあればそちらを、なければHNのスレッドURLを使う
        url = hit.get("url") or f"https://news.ycombinator.com/item?id={hn_id}"

        articles.append({
            "id":     hn_id,
            "title":  title,
            "url":    url,
            "source": "HackerNews",
            "points": points,
        })

    articles.sort(key=lambda x: x["points"], reverse=True)
    return articles
