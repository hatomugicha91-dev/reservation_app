import streamlit as st
from datetime import datetime

st.set_page_config(page_title="DM & メール自動生成ツール", layout="wide")

# -------------------------
# 日本語の曜日
# -------------------------
weekday_jp = ["月", "火", "水", "木", "金", "土", "日"]

def format_datetime(dt):
    """日本語曜日つき日時整形"""
    w = weekday_jp[dt.weekday()]
    return dt.strftime(f"%m/%d（{w}）%H:%M")

# -------------------------
# プルダウン選択肢
# -------------------------
AREA_OPTIONS = [
    "新宿（歌舞伎町）", "渋谷（道玄坂）", "鶯谷",
    "池袋", "五反田", "錦糸町", "アルファイン"
]

# -------------------------
# UI：タイトル
# -------------------------
st.title("DM & メール自動生成ツール（改良版）")

# -------------------------
# 入力フォーム
# -------------------------
st.subheader("■ 入力欄")

col1, col2 = st.columns(2)

with col1:
    name = st.text_input("お客様の名前（例：ひろ 様）")
    date = st.date_input("日付")
    time = st.time_input("開始時間")
    duration = st.selectbox("コース時間", ["60分", "90分", "120分", "150分", "180分", "210分", "240分"])

with col2:
    area = st.selectbox("場所（プルダウン復活）", AREA_OPTIONS)
    option = st.text_input("特別料金など（任意・空欄OK）")
    extra = f"＋{option}" if option else ""

# 合体した日時
dt = datetime.combine(date, time)
dt_str = format_datetime(dt)

# -------------------------
# 出力テンプレ生成関数
# -------------------------
def dm_1():
    return f"""
{name}

ご連絡ありがとうございます☺️

【ご予約内容】
{date.month}月{date.day}日（{weekday_jp[date.weekday()]}） {time.strftime("%H:%M")}〜  
{duration}枠  
場所：{area}{extra}

どうぞよろしくお願いいたします。
"""

def dm_2():
    return f"""
{name}

こちらこそありがとうございます！

【ご予約内容】
{date.month}月{date.day}日（{weekday_jp[date.weekday()]}) {time.strftime("%H:%M")}〜  
{duration}枠  
場所：{area}{extra}

それでは当日、お待ちしております☺️
"""

def dm_3():
    return f"""
{name}

ご連絡ありがとうございます。

【ご予約内容】
{date.month}月{date.day}日（{weekday_jp[date.weekday()]}） {time.strftime("%H:%M")}〜  
{duration}枠  
場所：{area}{extra}

どうぞよろしくお願いいたします。
"""

# メールテンプレ
def mail_1():
    return f"""
{name}

ご予約ありがとうございます。

【ご予約内容】
日時：{dt_str}
コース：{duration}
場所：{area}{extra}

何かご不明点ございましたらお気軽にご連絡ください。
"""

# -------------------------
# 出力欄
# -------------------------
st.subheader("■ 生成されたテンプレート")

tabs = st.tabs(["DM①（丁寧）", "DM②（柔らかめ）", "DM③（シンプル）", "メール①"])

templates = [dm_1(), dm_2(), dm_3(), mail_1()]

for tab, text in zip(tabs, templates):
    with tab:
        st.text_area("内容", text, height=250)
        st.button("コピーする", type="primary", key=text, on_click=lambda t=text: st.session_state.__setitem__("copy", t))
        if "copy" in st.session_state and st.session_state["copy"] == text:
            st.success("コピーしました ✔")

