import streamlit as st
import pandas as pd
from datetime import date, timedelta
from db import db_logic

# 状態をアイコン付きに変換（任意）
def status_icon(status):
    return "🟢 空き" if status == "空き" else "🔴 予約"

st.title("🎾 テニスコート 週間予約表")

# 📅 表示する週の開始日
start_date = st.date_input("週の開始日を選択", value=date.today())
end_date = start_date + timedelta(days=6)

st.caption(f"表示対象：{start_date} 〜 {end_date}")

# データ取得
update_time = db_logic.get_update_time()
df = db_logic.get_pd_yoyakujoukyou()
df["FROMDT"] = pd.to_datetime(df["FROMDT"])
df["TODT"] = pd.to_datetime(df["TODT"])
df["日付"] = df["FROMDT"].dt.date
df["時間帯"] = df["FROMDT"].dt.strftime("%H:%M") + "〜" + df["TODT"].dt.strftime("%H:%M")

# 空きのみ
aki_df = db_logic.get_pd_aki_yoyakujoukyou()
aki_df["FROMDT"] = pd.to_datetime(aki_df["FROMDT"])
aki_df["TODT"] = pd.to_datetime(aki_df["TODT"])
aki_df["日付"] = aki_df["FROMDT"].dt.date
aki_df["時間帯"] = aki_df["FROMDT"].dt.strftime("%H:%M") + "〜" + aki_df["TODT"].dt.strftime("%H:%M")

# フィルター処理
filtered = df[(df["日付"] >= start_date) & (df["日付"] <= end_date)]
aki_filtered = aki_df[(aki_df["日付"] >= start_date) & (aki_df["日付"] <= end_date)]


filtered["表示"] = filtered["YOYAKUJOKYOU"].apply(status_icon)
aki_filtered["表示"] = aki_filtered["YOYAKUJOKYOU"].apply(status_icon)

# 🔄 ピボットテーブルで視覚的に
pivot = filtered.pivot_table(
    index=["COURTNO", "時間帯"],
    columns="日付",
    values="表示",
    aggfunc="first",
    fill_value="ー"
)
aki_pivot = aki_filtered.pivot_table(
    index=["COURTNO", "時間帯"],
    columns="日付",
    values="表示",
    aggfunc="first",
    fill_value="ー"
)

display_mode = st.radio("表示を選択", ("すべて表示", "空きのみ表示"))
st.write("空きのみ表示の意味なくね？なんかいい具合に改修予定")

# 表示
if display_mode == "すべて表示":
    st.dataframe(pivot, use_container_width=True)
elif display_mode == "空きのみ表示":
    st.dataframe(aki_pivot, use_container_width=True)

# タプルからdatetimeオブジェクトを抽出
str_dt = update_time[0]  # タプルの最初の要素を取得

# フォーマット変換
str_dt = str_dt.strftime("%Y-%m-%d %H:%M:%S")

st.write(f"最終更新日時：{str_dt}")
