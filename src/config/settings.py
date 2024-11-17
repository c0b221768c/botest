import os
from pathlib import Path

from dotenv import load_dotenv

load_dotenv(dotenv_path=Path(__file__).resolve().parent.parent / ".env")


class Settings:
    # Discord Bot Token
    DISCORD_TOKEN = os.getenv("DISCORD_TOKEN")

    # データベース設定 (Heroku Postgres)
    DATABASE_URL = os.getenv("DATABASE_URL")

    # キャッシュ設定
    CACHE_TIMEOUT = int(os.getenv("CACHE_TIMEOUT", 600))  # デフォルトは10分

    # その他の設定
    DEBUG = os.getenv("DEBUG", "false").lower() in ("true", "1", "yes")


settings = Settings()
print(settings.DISCORD_TOKEN)
