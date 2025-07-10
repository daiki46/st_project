from db.connection import Database
from datetime import datetime
import pandas as pd
from sqlalchemy import create_engine, text

dt_now = datetime.now()
dt_now = dt_now.strftime('%Y-%m-%d %H:%M:%S')

db = Database()

def exec(query):
    try:
        session = db.get_session()
        # クエリ実行
        session.execute(text(query))
        session.commit()
    finally:
        if not session is None:
            session.rollback()
            session.close()

def delete_table():
    exec("""DELETE FROM dbo.BUNMORI;
         DBCC CHECKIDENT ('dbo.BUNMORI', RESEED, 0);
         """)

def get_pd_yoyakujoukyou():
    query = text("SELECT * FROM BUNMORI")  # 必要に応じて WHERE 句で日付フィルター可
    df = pd.read_sql(query, db.engine)
    return df

def get_pd_aki_yoyakujoukyou():
    query = text("SELECT * FROM BUNMORI WHERE YOYAKUJOKYOU = '空き'")  # 必要に応じて WHERE 句で日付フィルター可
    df = pd.read_sql(query, db.engine)
    return df

def get_update_time():
    query = "SELECT TOP 1 UPDATETIME FROM BUNMORI" 
    try:
        session = db.get_session()
        # クエリ実行
        result = session.execute(text(query)).all()
        return result[0]
    finally:
        if not session is None:
            session.close()
