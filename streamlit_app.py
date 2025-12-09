import streamlit as st
from datetime import datetime

st.set_page_config(page_title="予約返信文 自動生成", layout="wide")

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
price_table = {
    60: 20000,
    90: 25000,
    120: 30000,
    150: 45000,
    180: 55000,
    210: 65000,
    240: 75000
}

# 地域料金
area_fee = {
    "新宿(歌舞伎町)/渋谷(道玄坂)/鶯谷": 0,
    "池袋/五反田/錦糸町": 1000,
    "アルファイン": 3000,
    "その他": 0
}

# UI
st.title("予約返信文 自動生成ツール")

# ----------------------------------------------------
# 基本情報
# ----------------------------------------------------
st.header("■ 基本情報")
col1, col2 = st.columns(2)

with col1:
    name = st.text_input("お名前（様は自動付与）", "ひろ")
    email = st.text_input("メールアドレス（任意）", "")
with col2:
    tel = st.text_input("電話番号（任意）", "")

# ----------------------------------------------------
# 予約情報
# ----------------------------------------------------
st.header("■ 予約情報")
col1, col2 = st.columns(2)

with col1:
    place = st.selectbox("場所", list(area_fee.keys()))
    date = st.date_input("日付")
with col2:
    start_time = st.time_input("開始時間", datetime.strptime("15:00", "%H:%M"))
    play_time = st.selectbox("プレイ時間（分）", list(price_table.keys()))

options = st.multiselect(
    "オプション",
    ["乳首舐め", "聖水", "ボンデージ", "AF", "逆AF"]
)

extra_fee_text = st.text_input("特別料金（任意）", "")
other_text = st.text_input("その他（任意）", "")

# ----------------------------------------------------
# 計算
# ----------------------------------------------------
base_price = price_table[play_time]
area_price = area_fee[place]

extra_price = 0
if any(ch.isdigit() for ch in extra_fee_text):
    extra_price = int("".join(filter(str.isdigit, extra_fee_text)))

total_price = base_price + area_price + extra_price

weekday_jp = weekday_map[date.strftime("%A")]
date_str = f"{date.month}月{date.day}日"

datetime_label = f"{date_str}（{weekday_jp}）{start_time.strftime('%H:%M')}"

option_output = "・".join(options) if options else "なし"
extra_label = extra_fee_text if extra_fee_text else "なし"
other_label = other_text if other_text else "なし"


# ----------------------------------------------------
# メッセージ生成関数
# ----------------------------------------------------
def show(text):
    st.code(text, language="markdown")


# =====================================================
# 新規予約 DM①
# =====================================================
dm1 = f"""
ご連絡ありがとうございます。

{datetime_label}〜の{play_time}分枠で、ただいまご予約を仮押さえさせていただいております。

ご予約の確定には、以下カウンセリングフォームのご記入が必要となります。
お手数ですが、ご確認のうえご記入ください。

▶︎カウンセリングフォーム
https://docs.google.com/forms/d/e/1FAIpQLSf0XNC78LSqy8xKGGL6AjlIQGu7Wthi7tbzr-gS2mwqqwcmhw/viewform

入力が完了しましたら、一度ご連絡ください。

よろしくお願いいたします☺️
"""

# =====================================================
# 新規予約 DM②
# =====================================================
dm2 = f"""
カウンセリングフォームのご記入、ありがとうございました☺️

ご予約を確定させていただきます。

――――――――
【ご予約内容】
{datetime_label}
場所：{place}
オプション：{option_output}
特別料金：{extra_label}
その他：{other_label}
合計：¥{total_price:,}
――――――――

ホテルに到着されましたら、お部屋番号をご連絡ください。

よろしくお願いいたします♡
"""

# =====================================================
# 新規 メール①
# =====================================================
mail1 = f"""
件名：仮予約のご案内（要確認）/むぎ茶

{name} 様

ご連絡ありがとうございます。

{datetime_label}〜の{play_time}分枠で、ただいま仮予約となっております。

ご予約確定には以下のカウンセリングフォームのご入力が必要です。

▶︎カウンセリングフォーム
https://docs.google.com/forms/d/e/1FAIpQLSf0XNC78LSqy8xKGGL6AjlIQGu7Wthi7tbzr-gS2mwqqwcmhw/viewform

入力が完了しましたらご連絡いただけますと幸いです。

よろしくお願いいたします。

むぎ茶
"""

# =====================================================
# 新規 メール②
# =====================================================
mail2 = f"""
件名：ご予約確定のご案内/むぎ茶

{name} 様

カウンセリングフォームのご記入、ありがとうございました。

ご予約を確定いたしました。

――――――――
【ご予約内容】
{datetime_label}
場所：{place}
オプション：{option_output}
特別料金：{extra_label}
その他：{other_label}
合計：¥{total_price:,}
――――――――

ご不明点があればお気軽にご連絡ください。

むぎ茶
"""

# =====================================================
# 当日予約 DM①
# =====================================================
today_dm1 = f"""
ご連絡ありがとうございます。

本日 {datetime_label}〜の{play_time}分枠で仮予約いたしました。

以下フォームの入力をもってご予約確定となります。
（2時間前までに入力がない場合はキャンセル扱いとなります）

▶︎カウンセリングフォーム
https://docs.google.com/forms/d/e/1FAIpQLSf0XNC78LSqy8xKGGL6AjlIQGu7Wthi7tbzr-gS2mwqqwcmhw/viewform

入力が完了しましたらご連絡ください。
"""

# =====================================================
# 当日予約 DM②
# =====================================================
today_dm2 = f"""
カウンセリングフォームのご記入ありがとうございました☺️

本日のご予約を確定いたします。

――――――――
【ご予約内容】
{datetime_label}
場所：{place}
オプション：{option_output}
特別料金：{extra_label}
その他：{other_label}
合計：¥{total_price:,}
――――――――

ホテルに着きましたら、お部屋番号をご連絡ください♡
"""

# =====================================================
# ★ 当日予約 メール②（件名だけ修正）
# =====================================================
today_mail2 = f"""
件名：本日のご予約確定のご案内/むぎ茶

{name} 様

カウンセリングフォームのご記入、ありがとうございました。

本日のご予約を確定いたしました。

――――――――
【ご予約内容】
{datetime_label}
場所：{place}
オプション：{option_output}
特別料金：{extra_label}
その他：{other_label}
合計：¥{total_price:,}
――――――――

ホテルに到着されましたら、お部屋番号をご連絡ください。

むぎ茶
"""

# ----------------------------------------------------
# 出力タブ
# ----------------------------------------------------
tabs = st.tabs([
    "新規 DM①", "新規 DM②", "新規 メール①", "新規 メール②",
    "当日 DM①", "当日 DM②", "当日 メール②"
])

messages = [
    dm1, dm2, mail1, mail2,
    today_dm1, today_dm2, today_mail2
]

for tab, content in zip(tabs, messages):
    with tab:
        show(content)
