import streamlit as st
from datetime import datetime

st.set_page_config(page_title="予約返信文自動生成", layout="wide")

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

st.header("■ 基本情報入力")

col1, col2 = st.columns(2)
with col1:
    name = st.text_input("お名前（様は自動入力）」", "ひろ")
    email = st.text_input("メールアドレス", "hiro@gmail.com")
    tel = st.text_input("電話番号", "080117117")

with col2:
    place = st.selectbox("場所", list(area_fee.keys()))
    date = st.date_input("日付", datetime(2025, 12, 1))
    start_time = st.time_input("開始時刻", datetime.strptime("15:00", "%H:%M"))
    play_time = st.selectbox("プレイ時間（分枠）", list(price_table.keys()))

options = st.multiselect(
    "オプション（複数可）",
    ["乳首舐め", "聖水", "ボンデージ", "AF", "逆AF"]
)

extra_fee_text = st.text_input("特別追加料金（例：撮影1000）", "")
other_text = st.text_input("その他", "")

# 計算
base_price = price_table.get(play_time, 0)
area_price = area_fee.get(place, 0)

extra_price = 0
if "¥" in extra_fee_text or "円" in extra_fee_text:
    extra_price = int("".join(filter(str.isdigit, extra_fee_text)))
elif any(char.isdigit() for char in extra_fee_text):
    extra_price = int("".join(filter(str.isdigit, extra_fee_text)))

total_price = base_price + area_price + extra_price

# 日付整形
weekday_jp = weekday_map[date.strftime("%A")]
date_str = f"{date.month}月{date.day}日"
datetime_label = f"{date_str}（{weekday_jp}）{start_time.strftime('%H:%M')}"

# オプション
option_output = "・".join(options) if options else "なし"

# 特別料金
extra_label = extra_fee_text if extra_fee_text else "なし"

# その他
other_label = other_text if other_text else "なし"


# ========================
# ★ 生成関数
# ========================
def section(text):
    st.code(text, language="markdown")
    return


# ============================================================
# ★★ 【新規・数日前予約】DM①
# ============================================================
dm1 = f"""
ご連絡ありがとうございます。

{date_str}（{weekday_jp}）{start_time.strftime('%H:%M')}〜の{play_time}分枠で、ただいまご予約を仮押さえさせていただいております。

ご予約の確定には、以下のカウンセリングフォームのご記入が必要となります。
お手数をおかけいたしますが、ご確認のうえご記入をお願いいたします。

▶︎カウンセリングフォーム
https://docs.google.com/forms/d/e/1FAIpQLSf0XNC78LSqy8xKGGL6AjlIQGu7Wthi7tbzr-gS2mwqqwcmhw/viewform

カウンセリングフォームへの入力が済みましたら、一度ご連絡頂けましたら幸いです。

お会いできるのを楽しみにしています。

よろしくお願いいたします。
"""

# ============================================================
# ★★ 【新規・数日前予約】DM② カウンセリング後
# ============================================================
dm2 = f"""
カウンセリングフォームへのご記入、ありがとうございました☺️

ご予約を確定させていただきます。

――――――――
【ご予約内容】
{datetime_label}〜（{play_time}分枠）
場所：{place}
オプション：{option_output}
特別追加料金：{extra_label}
その他：{other_label}

合計：¥{total_price:,}
――――――――

★ホテルに到着されましたら
ホテル名とお部屋番号をご連絡ください。

早めにお知らせいただけますと、スムーズにお伺いすることができます。

ご不明な点がございましたら、どうぞお気軽にご連絡ください。

お会いできるのを心より楽しみにしております。
よろしくお願いいたします♡
"""

# ============================================================
# ★★ 【新規・数日前予約】メール①
# ============================================================
mail1 = f"""
件名：仮予約のご案内（要確認）/むぎ茶

{name} 様

ご連絡ありがとうございます。

{date_str}（{weekday_jp}）{start_time.strftime('%H:%M')}〜の{play_time}分枠で、ただいまご予約を仮押さえさせていただいております。

ご予約の確定には、以下のカウンセリングフォームのご記入が必要となります。
お手数をおかけいたしますが、ご確認のうえご記入をお願いいたします。

▶︎カウンセリングフォーム
https://docs.google.com/forms/d/e/1FAIpQLSf0XNC78LSqy8xKGGL6AjlIQGu7Wthi7tbzr-gS2mwqqwcmhw/viewform

カウンセリングフォームへの入力が済みましたら、一度ご連絡頂けましたら幸いです。

お会いできるのを楽しみにしています。

よろしくお願いいたします。

むぎ茶
"""

# ============================================================
# ★★ 【新規・数日前予約】メール② カウンセリング後
# ============================================================
mail2 = f"""
件名：ご予約確定のご案内/むぎ茶

{name} 様

カウンセリングフォームへのご記入、ありがとうございました☺️

ご予約を確定させていただきます。

――――――――
【ご予約内容】
{datetime_label}〜（{play_time}分枠）
場所：{place}
オプション：{option_output}
特別追加料金：{extra_label}
その他：{other_label}

合計：¥{total_price:,}
――――――――

★ホテルに到着されましたら
ホテル名とお部屋番号をご連絡ください。

早めにお知らせいただけますと、スムーズにお伺いすることができます。

ご不明な点がございましたら、どうぞお気軽にご連絡ください。

お会いできるのを心より楽しみにしております。
よろしくお願いいたします♡

むぎ茶
"""


# ============================================================
# ★★【当日予約】DM① 最初
# ============================================================
today_dm1 = f"""
ご連絡ありがとうございます。

本日{date_str}（{weekday_jp}）{start_time.strftime('%H:%M')}〜の{play_time}分枠で、ただいまご予約を仮押さえさせていただいております。

ご予約の確定には、以下のカウンセリングフォームのご記入が必要となります。
お手数をおかけいたしますが、ご確認のうえご記入をお願いいたします。

（プレイ予定の２時間前までにご入力が無ければ、キャンセル扱いとなります。）

▶︎カウンセリングフォーム
https://docs.google.com/forms/d/e/1FAIpQLSf0XNC78LSqy8xKGGL6AjlIQGu7Wthi7tbzr-gS2mwqqwcmhw/viewform

カウンセリングフォームへの入力が済みましたら、一度ご連絡頂けましたら幸いです。

お会いできるのを楽しみにしています。

よろしくお願いいたします。
"""

# ============================================================
# ★★【当日予約】DM② カウンセリング後
# ============================================================
today_dm2 = f"""
カウンセリングフォームへのご記入、ありがとうございました☺️

本日のご予約を確定させていただきます。

――――――――
【ご予約内容】
{datetime_label}〜（{play_time}分枠）
場所：{place}
オプション：{option_output}
特別追加料金：{extra_label}
その他：{other_label}

合計：¥{total_price:,}
――――――――

★ホテルに到着されましたら
ホテル名とお部屋番号をご連絡ください。

早めにお知らせいただけますと、スムーズにお伺いすることができます。

ご不明な点がございましたら、どうぞお気軽にご連絡ください。

お会いできるのを心より楽しみにしております。
よろしくお願い致します♡
"""

# ============================================================
# ★★【当日予約】メール① 最初
# ============================================================
today_mail1 = f"""
件名：仮予約のご案内（要確認）/むぎ茶

{name} 様

ご連絡ありがとうございます。

本日{date_str}（{weekday_jp}）{start_time.strftime('%H:%M')}〜の{play_time}分枠で、ただいまご予約を仮押さえさせていただいております。

ご予約の確定には、以下のカウンセリングフォームのご記入が必要となります。
お手数をおかけいたしますが、ご確認のうえご記入をお願いいたします。

（プレイ予定の２時間前までにご入力が無ければ、キャンセル扱いとなります。）

▶︎カウンセリングフォーム
https://docs.google.com/forms/d/e/1FAIpQLSf0XNC78LSqy8xKGGL6AjlIQGu7Wthi7tbzr-gS2mwqqwcmhw/viewform

カウンセリングフォームへの入力が済みましたら、一度ご連絡頂けましたら幸いです。

お会いできるのを楽しみにしています。

よろしくお願いいたします。

むぎ茶
"""

# ============================================================
# ★★【当日予約】メール② カウンセリング後（件名追加）
# ============================================================
today_mail2 = f"""
件名：本日のご予約確定のご案内/むぎ茶

{name} 様

カウンセリングフォームへのご記入、ありがとうございました☺️

本日のご予約を確定させていただきます。

――――――――
【ご予約内容】
{datetime_label}〜（{play_time}分枠）
場所：{place}
オプション：{option_output}
特別追加料金：{extra_label}
その他：{other_label}

合計：¥{total_price:,}
――――――――

★ホテルに到着されましたら
ホテル名とお部屋番号をご連絡ください。

早めにお知らせいただけますと、スムーズにお伺いすることができます。

ご不明な点がございましたら、どうぞお気軽にご連絡ください。

お会いできるのを心より楽しみにしております。
よろしくお願い致します♡

むぎ茶
"""

# ----------------------------
# 出力
# ----------------------------
st.header("生成メッセージ")

tabs = st.tabs([
    "新規 DM①", "新規 DM②",
    "新規 メール①", "新規 メール②",
    "当日 DM①", "当日 DM②",
    "当日 メール①", "当日 メール②"
])

sections = [
    dm1, dm2,
    mail1, mail2,
    today_dm1, today_dm2,
    today_mail1, today_mail2
]

for tab, msg in zip(tabs, sections):
    with tab:
        section(msg)
