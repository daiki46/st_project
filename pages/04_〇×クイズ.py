import random
import streamlit as st
import mysql.connector

image_path = "img/"

def get_question(aaa):
    conn = mysql.connector.connect(
        host='localhost',
        user='root',
        password='daiki0907',
        database='marubatu_db'
    )
    cursor = conn.cursor()
    cursor.execute("SELECT question, answer FROM t_questions WHERE id = %s", (aaa,))
    result = cursor.fetchone()
    cursor.close()
    conn.close()
    return result  # (question, answer)


st.title("〇×クイズ")
st.write("〇か×で答えてね😘")
if st.button("スタート"):
    

    # 乱数を生成（１～5）して変数に代入
    random_int = random.randint(1, 5)

    # データベースに接続して問題を取得
    mondai = get_question(random_int)
    if mondai:
        st.write(f"問題ID: {random_int}")
        st.write(f"問題: {mondai[0]}")  # 質問文
        st.write(f"答え（あとで確認用）: {mondai[1]}")  # 正解（非表示にしたい場合は後から切り替えも可能）
    else:
        st.write("問題が見つかりませんでした🥲")


    # # 生成した乱数が90以上の場合は大吉
    # if random_int >= 90:
    #    st.write("大吉")
    #    st.image(f"{image_path}daikichi.png")

    # # 生成した乱数が30以上の場合は中吉
    # elif random_int >= 30:
    #     st.write("中吉")
    #     st.image(f"{image_path}chukichi.png")

    # # それ以外の場合は凶
    # else:
    #     st.write("凶")
    #     st.image(f"{image_path}kyou.png")   




        
