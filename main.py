"""
AI情報 Discord通知Bot

使い方:
  python main.py run                # 新着を取得して通知
  python main.py run --force-notify # 新着がなくても強制通知（テスト用）
"""

import argparse
import logging
import os
import sys

import config
import fetcher_domestic
import fetcher_hackernews
import fetcher_international
from notifier import send, build_domestic, build_hackernews, build_international
from storage import load_seen, save_seen


def setup_logging():
    os.makedirs(config.LOG_DIR, exist_ok=True)
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s [%(levelname)s] %(name)s: %(message)s",
        handlers=[
            logging.FileHandler(config.LOG_PATH, encoding="utf-8"),
            logging.StreamHandler(sys.stdout),
        ],
    )


def _run_channel(name: str, fetcher, webhook_url: str, build_message, force_notify: bool):
    """1チャンネル分の取得・差分チェック・通知を行う。"""
    logger = logging.getLogger(__name__)
    logger.info(f"--- {name} チェック ---")

    articles = fetcher.fetch()
    logger.info(f"{name}: {len(articles)}件取得")

    seen = load_seen(name)

    # 未通知の記事を抽出
    new_articles = [a for a in articles if a["id"] not in seen]
    logger.info(f"{name}: 新着 {len(new_articles)}件")

    # 今回取得した全記事をseenに追加して保存
    for a in articles:
        seen.add(a["id"])
    save_seen(name, seen)

    # 通知対象を決定
    if new_articles:
        to_notify = new_articles[:config.MAX_NOTIFY_PER_RUN]
    elif force_notify and articles:
        logger.info(f"{name}: 新着なし。force_notifyのため最新{config.MAX_NOTIFY_PER_RUN}件を通知します。")
        to_notify = articles[:config.MAX_NOTIFY_PER_RUN]
    else:
        logger.info(f"{name}: 新着なし。通知スキップ。")
        return

    try:
        message = build_message(to_notify)
        send(webhook_url, message)
        logger.info(f"{name}: Discord通知完了（{len(to_notify)}件）")
    except Exception as e:
        logger.error(f"{name}: Discord通知失敗: {e}")


def cmd_run(force_notify: bool = False):
    logger = logging.getLogger(__name__)
    logger.info("=== AI情報チェック開始 ===")

    _run_channel(
        name="domestic",
        fetcher=fetcher_domestic,
        webhook_url=config.DISCORD_WEBHOOK_DOMESTIC,
        build_message=build_domestic,
        force_notify=force_notify,
    )
    _run_channel(
        name="hackernews",
        fetcher=fetcher_hackernews,
        webhook_url=config.DISCORD_WEBHOOK_HACKERNEWS,
        build_message=build_hackernews,
        force_notify=force_notify,
    )
    _run_channel(
        name="international",
        fetcher=fetcher_international,
        webhook_url=config.DISCORD_WEBHOOK_INTERNATIONAL,
        build_message=build_international,
        force_notify=force_notify,
    )

    logger.info("=== AI情報チェック完了 ===")


def main():
    setup_logging()

    parser = argparse.ArgumentParser(description="AI情報 Discord通知Bot")
    subparsers = parser.add_subparsers(dest="command")

    run_parser = subparsers.add_parser("run", help="新着AI情報を取得して通知する")
    run_parser.add_argument(
        "--force-notify",
        action="store_true",
        help="新着がなくても強制通知する（テスト用）",
    )

    args = parser.parse_args()

    if args.command == "run":
        cmd_run(force_notify=args.force_notify)
    else:
        parser.print_help()


if __name__ == "__main__":
    main()
