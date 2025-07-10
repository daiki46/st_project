import os
from dotenv import load_dotenv

# .envの読み込み
load_dotenv()

class Settings:
    DB_URL = os.environ["DB_URL"]
    DEBUG = os.getenv("DEBUG", "False").lower() == "true"

settings = Settings()