import streamlit as st
from datetime import datetime

st.set_page_config(page_title="予約文自動生成", layout="wide")

# 日本語曜日
weekday_map = {
    "Monday": "月",
    "Tuesday": "火",
    "Wednesday": "水",
    "Thursday": "木",
    "Friday": "金",
    "Saturday": "土",
    "Sunday": "日"
}

# 料金表
price_list = {
    60: 20000,
    90: 25000,
    120: 30000,
    150: 45000,
    180: 55000,
    210: 65000,
    240: 75000
}

# 場所ごとの料金
place_fee = {
    "新宿(歌舞伎町)/渋谷(道玄坂)/鶯谷": 0,
    "池袋/五反田/錦糸町": 1000,
    "アルファイン": 3000
}

# UI レイアウト
st.title("✨ 予約文 自動生成アプリ（完成版）✨")

st.subheader("■ 基本情報")
name = st.text_input("お名前")
email = st.text_input("メールアドレス（任意）")
tel = st.text_input("電話番号（任意）")

place = st.selectbox("場所", list(place_fee.keys()))
date = st.date_input("日付")
start_time = st.time_input("開始時間")
play_time = st.selectbox("プレイ時間（分）", list(price_list.keys()))

options = st.multiselect(
    "オプション（複数可）",
    ["乳首舐め", "ボンデージ", "聖水", "逆聖水", "３P", "パウダーM"]
)

special_fee = st.text_input("特別料金（任意入力例：撮影1000）")
other = st.text_area("その他")

st.write("---")

# 予約情報の生成
date_str = date.strftime("%Y/%m/%d")
weekday = weekday_map[date.strftime("%A")]

full_place = place
option_list = "・".join(options) if options else "なし"

# 特別料金ブロック
special_fee_block = f"特別追加料金　　{special_fee}\n" if special_fee else ""
other_block = f"その他　{other}\n" if other else ""

# 合計計算
base_price = price_list[play_time]
place_price = place_fee[place]
option_price = 2000 * len(options)
special_price = 0

if special_fee:
    nums = [int(s) for s in special_fee.replace("¥", "").replace(",", "") if s.isdigit()]
    if nums:
        special_price = nums[0]

total = base_price + place_price + option_price + special_price
