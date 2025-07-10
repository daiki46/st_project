import streamlit as st
import os

# ファイルアップロード
uploaded_file = st.file_uploader("画像を選択してください", type=["png", "jpg", "jpeg"])
if uploaded_file is not None:
    # Azure App Serviceの保存先ディレクトリ
    save_path = os.path.join("/home/img/", uploaded_file.name)
    with open(save_path, "wb") as file:
        file.write(uploaded_file.getbuffer())
    st.write(f"画像をアップロードしました: {save_path}")