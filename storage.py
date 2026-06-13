"""
通知済み記事IDのJSON保存・読み込み。

data/seen_{name}.json に記事のURL/IDを保存して、
次回実行時に「既読かどうか」を判定するために使う。
"""

import json
import logging
from pathlib import Path

logger = logging.getLogger(__name__)

_BASE_DIR = Path(__file__).parent
_DATA_DIR = _BASE_DIR / "data"
_MAX_SEEN = 1000  # これを超えたら古いものを削除


def load_seen(name: str) -> set[str]:
    """通知済みIDのセットを返す。ファイルがなければ空セット。"""
    path = _DATA_DIR / f"seen_{name}.json"
    if not path.exists():
        return set()
    try:
        with open(path, encoding="utf-8") as f:
            return set(json.load(f))
    except (json.JSONDecodeError, OSError) as e:
        logger.error(f"seen_{name}.json 読み込み失敗: {e}")
        return set()


def save_seen(name: str, seen: set[str]):
    """通知済みIDを保存する。上限を超えたら古い分を切り捨てる。"""
    _DATA_DIR.mkdir(parents=True, exist_ok=True)
    seen_list = list(seen)
    if len(seen_list) > _MAX_SEEN:
        seen_list = seen_list[-_MAX_SEEN:]
    path = _DATA_DIR / f"seen_{name}.json"
    try:
        with open(path, "w", encoding="utf-8") as f:
            json.dump(seen_list, f, ensure_ascii=False, indent=2)
    except OSError as e:
        logger.error(f"seen_{name}.json 保存失敗: {e}")
        raise
