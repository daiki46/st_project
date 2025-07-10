from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.exc import OperationalError
from config.settings import settings
import time

class Database:
    def __init__(self, retries=6, delay=10):
        self.db_url = settings.DB_URL
        for attempt in range(1, retries + 1):
            try:
                self.engine = create_engine(self.db_url, echo=settings.DEBUG)
                with self.engine.connect() as conn:
                    pass    #スキップ
                print("DB接続に成功しました。")
                break

            except OperationalError as e:
                print(f"DB接続失敗：{e}")
                if attempt < retries:
                    time.sleep(delay)
                else:
                    print("接続に1分間失敗し続けたため処理を中止します。")
                    raise   #例外

        
        self.SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=self.engine)

    def get_session(self):
        return self.SessionLocal()