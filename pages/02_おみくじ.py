import random
import streamlit as st

image_path = "img/"

st.title("おみくじアプリ")
st.write("ボタンを押しておみくじを引いてね")
if st.button("おみくじを引く"):
    # 乱数を生成（１～１００）して変数に代入
    random_int = random.randint(1, 100)

    # 生成した乱数が90以上の場合は大吉
    if random_int >= 90:
        st.write("大吉")
        st.image(f"{image_path}daikichi.png")

    # 生成した乱数が30以上の場合は中吉
    elif random_int >= 30:
        st.write("中吉")
        st.image(f"{image_path}chukichi.png")

    # それ以外の場合は凶
    else:
        st.write("凶")
        st.image(f"{image_path}kyou.png")   


