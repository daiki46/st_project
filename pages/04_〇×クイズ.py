import random
import streamlit as st
import sqlite3
from pathlib import Path
from config.settings import settings
from db import db_logic

st.title("〇×クイズ")
st.write("〇か×で答えてね😘")

if st.button("スタート"):
    random_int = random.randint(1, 10)
    mondai = db_logic.get_question(random_int)

    if mondai:
        st.write(f"問題ID: {random_int}")
        st.write(f"問題: {mondai[0]}")
        if st.button("答えを見る"):
            st.write(f"答え: {mondai[1]}")
    else:
        st.error("問題が見つかりませんでした🥲")
