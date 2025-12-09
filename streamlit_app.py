# streamlit_app.py
import streamlit as st
from datetime import datetime

# -----------------------------
# 日本語曜日対応
# -----------------------------
weekday_jp = {
    "Mon":"月", "Tue":"火", "Wed":"水", "Thu":"木",
    "Fri":"金", "Sat":"土", "Sun":"日"
}

# -----------------------------
# 料金・オプション設定
# -----------------------------
play_prices = {
    "60": 20000, "90": 25000, "120": 30000, "150": 45000, "180": 55000,
    "210": 65000, "240": 75000, "270": 85000, "300": 95000, "330": 105000,
    "オールナイト": 120000, "特殊料金": 0
}

option_prices = {
    "無し":0, "乳首舐め":2000, "聖水":3000, "ボンデージ":1000,
    "その他の衣装":1000, "局部奉仕":8000, "アナル奉仕":5000, "その他":0
}

# -----------------------------
# 場所料金
# -----------------------------
locations = {
    "新宿(歌舞伎町)/渋谷(道玄坂)/鶯谷": 0,
    "池袋/五反田/錦糸町": 1000,
    "アルファイン": 3000,
    "その他": 0
}

# -----------------------------
# フォーム入力
# -----------------------------
st.title("予約・DM・メール文章生成（非公開用）")

name = st.text_input("名前")
email = st.text_input("メールアドレス（任意）")
phone = st.text_input("電話番号（任意）")
date_str = st.text_input("日付", "2025/12/1")
start_time = st.text_input("開始時刻", "15:00")
location = st.selectbox("場所", options=list(locations.keys()))
play_time = st.selectbox("プレイ時間（分枠）", options=list(play_prices.keys()))
options_selected = st.multiselect("オプション（複数可）", list(option_prices.keys()))
extra_fee = st.number_input("特別追加料金（任意）", min_value=0, step=100, format="%d")
other_text = st.text_input("その他（任意）")

# -----------------------------
# 金額計算
# -----------------------------
play_fee = play_prices.get(play_time, 0)
option_fee = sum(option_prices.get(opt, 0) for opt in options_selected)
location_fee = locations.get(location,0)
total_fee = play_fee + option_fee + extra_fee + location_fee

# -----------------------------
# 予約情報生成
# -----------------------------
def format_options(opts):
    return "・".join(opts) if opts else ""

def reservation_info():
    dt = datetime.strptime(date_str, "%Y/%m/%d")
    weekday = weekday_jp[dt.strftime("%a")]
    lines = [
        "‐‐‐‐‐‐‐‐",
        "【基本情報】",
        f"名前　{name}",
        f"メールアドレス　{email}" if email else "メールアドレス　",
        f"電話番号　{phone}" if phone else "電話番号　",
        f"場所　{location}",
        f"日付　{date_str}（{weekday}）",
        f"開始時刻　{start_time}〜",
        f"プレイ時間（分枠）　{play_time}",
        f"オプション　{format_options(options_selected)}" if options_selected else "オプション　",
        f"特別追加料金　¥{extra_fee}" if extra_fee else "",
        f"その他　{other_text}" if other_text else "",
        "",
        "‐‐‐‐‐‐‐‐",
        "【予約情報】",
        f"{date_str}（{weekday}） {start_time}〜（{play_time}分枠）",
        f"場所：{location}",
    ]
    if options_selected:
        lines.append(f"オプション：{format_options(options_selected)}")
    if extra_fee:
        lines.append(f"特別追加料金　¥{extra_fee}")
    if other_text:
        lines.append(f"その他　{other_text}")
    lines.append(f"合計：¥{total_fee}")
    lines.append("‐‐‐‐‐‐‐‐")
    return "\n".join([line for line in lines if line.strip() != ""])

reservation_text = reservation_info()

# -----------------------------
# DM文章生成
# -----------------------------
def dm_text1():
    dt = datetime.strptime(date_str, "%Y/%m/%d")
    weekday = weekday_jp[dt.strftime("%a")]
    return f"""ご連絡ありがとうございます。

{date_str}（{weekday}）{start_time}〜の{play_time}分枠で、ただいまご予約を仮押さえさせていただいております。

ご予約の確定には、以下のカウンセリングフォームのご記入が必要となります。
お手数をおかけいたしますが、ご確認のうえご記入をお願いいたします。

▶︎カウンセリングフォーム
https://docs.google.com/forms/d/e/1FAIpQLSf0XNC78LSqy8xKGGL6AjlIQGu7Wthi7tbzr-gS2mwqqwcmhw/viewform

ご不明な点がございましたら、どうぞお気軽にご連絡ください。
"""

def dm_text2():
    return f"""カウンセリングフォームへのご記入、ありがとうございました☺️

以下の日時でご予約を確定させていただきます。

{reservation_text}

ご質問や追加のご希望などがありましたら、お気軽にお知らせください。

前日にはこちらから最終確認のご連絡を差し上げます。
なお、当日の無断キャンセルは料金の100%を頂戴しております。
ご変更がある場合は、前日確認の時までにお知らせいただけますと幸いです。

お会いできるのを楽しみにしております。
引き続きよろしくお願いいたします✨
"""

def dm_text3():
    return f"""
いよいよ明日ですね！前日確認のご連絡です。

{reservation_text}

明日ホテルに到着されましたら
★ホテル名とお部屋番号をご連絡ください。

早めにお知らせいただけますと、スムーズにお伺いすることができます。

明日お会いできるのを心より楽しみにしています。

どうぞよろしくお願いいたします！
"""

dm_texts = {
    "DM①最初": dm_text1(),
    "DM②カウンセリング後": dm_text2(),
    "DM③前日確認": dm_text3()
}

# -----------------------------
# メール文章生成
# -----------------------------
mail_texts = {
    "メール①最初": f"件名：仮予約のご案内（{date_str} {start_time}〜）/むぎ茶\n{name} 様\n\n{dm_texts['DM①最初']}\nむぎ茶",
    "メール②カウンセリング後": f"件名：【確定】ご予約についてのご案内（{date_str} {start_time}〜）\n{name} 様\n\n{dm_texts['DM②カウンセリング後']}\nむぎ茶",
    "メール③前日確認": f"件名：前日確認のご案内 /むぎ茶\n{name} 様\n\n{dm_texts['DM③前日確認']}\nむぎ茶"
}

# -----------------------------
# 選択表示
# -----------------------------
pattern = st.selectbox(
    "出力したい文章",
    ["基本情報+予約情報"] + list(dm_texts.keys()) + list(mail_texts.keys())
)

# -----------------------------
# 文章生成・コピー
# -----------------------------
if st.button("文章を生成"):
    if pattern == "基本情報+予約情報":
        text_to_display = reservation_text
    elif pattern in dm_texts:
        text_to_display = dm_texts[pattern]
    else:
        text_to_display = mail_texts[pattern]

    st.text_area("生成文章", value=text_to_display, height=400)
    st.button("コピー", on_click=lambda: st.experimental_set_query_params(copy=text_to_display))
