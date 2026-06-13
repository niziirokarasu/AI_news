import logging
import requests

logger = logging.getLogger(__name__)

_MAX_CHARS = 1900


def send(webhook_url: str, content: str):
    """Discord Webhook にメッセージを送る。長い場合は分割して送る。"""
    if not webhook_url:
        logger.error("Webhook URLが設定されていません。")
        raise ValueError("Webhook URLが未設定です。.envまたはGitHub Secretsを確認してください。")

    for chunk in _split(content):
        try:
            r = requests.post(webhook_url, json={"content": chunk}, timeout=10)
            r.raise_for_status()
        except requests.exceptions.RequestException as e:
            logger.error(f"Discord通知失敗: {e}")
            raise


def _split(content: str) -> list[str]:
    if len(content) <= _MAX_CHARS:
        return [content]
    chunks, current = [], ""
    for line in content.split("\n"):
        if len(current) + len(line) + 1 > _MAX_CHARS:
            if current:
                chunks.append(current.rstrip())
            current = line + "\n"
        else:
            current += line + "\n"
    if current:
        chunks.append(current.rstrip())
    return chunks


def build_domestic(articles: list[dict]) -> str:
    lines = [f"🇯🇵 **国内AI情報 新着 {len(articles)}件**", ""]
    for a in articles:
        lines.append(f"📰 [{a['title']}]({a['url']})")
        lines.append(f"　　　└ {a['source']}")
        lines.append("")
    return "\n".join(lines).rstrip()


def build_hackernews(articles: list[dict]) -> str:
    lines = [f"🔬 **HackerNews AI 新着 {len(articles)}件**", ""]
    for a in articles:
        lines.append(f"▲ **{a['points']}pts** [{a['title']}]({a['url']})")
    return "\n".join(lines)


def build_international(articles: list[dict]) -> str:
    lines = [f"📰 **海外AI ニュース新着 {len(articles)}件**", ""]
    for a in articles:
        lines.append(f"📌 [{a['title']}]({a['url']})")
        lines.append(f"　　　└ {a['source']}")
        lines.append("")
    return "\n".join(lines).rstrip()
