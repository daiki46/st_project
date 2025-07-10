from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.exc import OperationalError
from config.settings import settings
import time

class Database:
    def __init__(self, retries=6, delay=10):
        self.db_url = settings.DB_URL

        # エンジン構築用パラメータを準備
        engine_args = {
            "echo": settings.DEBUG
        }

        # SQLite の場合は専用の connect_args を追加し、
        # リトライ不要とする
        if self.db_url.startswith("sqlite"):
            engine_args["connect_args"] = {"check_same_thread": False}
            retries = 1

        # 接続試行ループ
        for attempt in range(1, retries + 1):
            try:
                self.engine = create_engine(self.db_url, **engine_args)
                with self.engine.connect():
                    pass
                print("DB接続に成功しました。")
                break

            except OperationalError as e:
                print(f"DB接続失敗 (試行 {attempt}/{retries}) ：{e}")
                if attempt < retries:
                    print(f"{delay} 秒後に再試行します…")
                    time.sleep(delay)
                else:
                    print("接続に失敗し続けたため処理を中止します。")
                    raise

        # セッションメーカーを生成
        self.SessionLocal = sessionmaker(
            autocommit=False,
            autoflush=False,
            bind=self.engine
        )

    def get_session(self):
        return self.SessionLocal()
