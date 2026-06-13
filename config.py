import os
from dotenv import load_dotenv

load_dotenv()

DISCORD_WEBHOOK_DOMESTIC      = os.getenv("DISCORD_WEBHOOK_DOMESTIC", "")
DISCORD_WEBHOOK_HACKERNEWS    = os.getenv("DISCORD_WEBHOOK_HACKERNEWS", "")
DISCORD_WEBHOOK_INTERNATIONAL = os.getenv("DISCORD_WEBHOOK_INTERNATIONAL", "")

# 1回の実行で通知する最大件数（チャンネルごと）
MAX_NOTIFY_PER_RUN = int(os.getenv("MAX_NOTIFY_PER_RUN", "5"))

# HackerNews の最低ポイント数（これ未満は無視）
MIN_HN_POINTS = int(os.getenv("MIN_HN_POINTS", "10"))

LOG_DIR  = "logs"
LOG_PATH = "logs/app.log"
