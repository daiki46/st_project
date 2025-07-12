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
    exec("DELETE FROM BUNMORI;")
    exec("UPDATE sqlite_sequence SET seq = 0 WHERE name = 'BUNMORI';")
        

def get_pd_yoyakujoukyou():
    query = text("SELECT * FROM BUNMORI")  # 必要に応じて WHERE 句で日付フィルター可
    df = pd.read_sql(query, db.engine)
    return df

def get_pd_aki_yoyakujoukyou():
    query = text("SELECT * FROM BUNMORI WHERE YOYAKUJOKYOU = '空き'")  # 必要に応じて WHERE 句で日付フィルター可
    df = pd.read_sql(query, db.engine)
    return df

def get_update_time():
    query = """SELECT UPDATETIME FROM BUNMORI
ORDER BY UPDATETIME DESC
LIMIT 1;
"""
    try:
        session = db.get_session()
        # クエリ実行
        result = session.execute(text(query)).all()
        return result[0]
    finally:
        if not session is None:
            session.close()

def get_question(q_id: int):
    query = text("SELECT question, answer FROM t_questions WHERE id = :q_id")
    try:
        session = db.get_session()
        result = session.execute(query, {"q_id": q_id}).fetchone()
        return result if result else None
    finally:
        if session is not None:
            session.close()

def exec_query_list(query_list):
    for q in query_list:
        print(f'実行されるクエリ：{q}')
        exec(q)
        