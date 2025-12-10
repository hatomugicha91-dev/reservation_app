import streamlit as st
import streamlit.components.v1 as components
from datetime import datetime

st.set_page_config(page_title="予約・DM・メール自動生成", layout="wide")


# -----------------------------
# マスタデータ（料金等）
# -----------------------------
play_prices = {
    "60": 20000,
    "90": 25000,
    "120": 35000,
    "150": 45000,
    "180": 55000,
    "210": 65000,
    "240": 75000,
    "270": 85000,
    "300": 95000,
    "330": 105000,
    "オールナイト": 120000,
    "特殊料金": 0
}

option_prices = {
    "無し": 0,
    "乳首舐め": 2000,
    "聖水": 3000,
    "ボンデージ": 1000,
    "その他の衣装": 1000,
    "局部奉仕": 8000,
    "アナル奉仕": 5000,
    "その他(特別料金)": 0
}

location_prices = {
    "新宿（歌舞伎町）": 0,
    "渋谷（道玄坂）": 0,
    "鶯谷": 0,
    "池袋": 1000,
    "五反田": 1000,
    "錦糸町": 1000,
    "アルファイン": 3000,
    "その他（特別料金）": 0
}

weekday_jp = ["月", "火", "水", "木", "金", "土", "日"]


# -----------------------------
# UI：基本情報入力
# -----------------------------
st.title("予約・DM・メール自動生成ツール")

st.markdown("### ■ 基本情報入力")
col1, col2 = st.columns(2)

with col1:
    inp_name = st.text_input("名前", value="")
    inp_play_time = st.selectbox(
        "プレイ時間（分枠）",
        options=list(play_prices.keys()),
        index=list(play_prices.keys()).index("120")
    )

with col2:
    inp_date = st.date_input("日付", value=datetime.now().date())
    inp_time = st.time_input("開始時刻", value=datetime.strptime("15:00", "%H:%M").time())
    loc_choice = st.selectbox(
        "場所（選択）",
        options=list(location_prices.keys()),
        index=list(location_prices.keys()).index("渋谷（道玄坂）")
    )
    loc_extra = 0
    if loc_choice == "その他（特別料金）":
        loc_extra = st.number_input("その他（場所）特別料金（¥）", min_value=0, step=100, value=0)

inp_options = st.multiselect("オプション（複数選択可）", options=list(option_prices.keys()))
option_other_fee = 0
if "その他(特別料金)" in inp_options:
    option_other_fee = st.number_input("オプションのその他（金額 ¥）", min_value=0, step=100, value=0)

inp_extra_fee = st.number_input("特別追加料金（任意 ¥）", min_value=0, step=100, value=0)
inp_other_text = st.text_input("その他（任意）", value="")

# -----------------------------
# ヘルパー
# -----------------------------
def format_options(opts):
    return "・".join(
        [o for o in opts if o != "その他(特別料金)"] +
        (["その他"] if "その他(特別料金)" in opts else [])
    )

def calc_total(play_key, loc_key, loc_extra_val, opts, opt_other_fee, extra_fee_val):
    play_fee = play_prices.get(play_key, 0)
    loc_fee = location_prices.get(loc_key, 0) + (loc_extra_val or 0)
    option_fee = sum(option_prices.get(o, 0) for o in opts) + (opt_other_fee or 0)
    total = play_fee + loc_fee + option_fee + (extra_fee_val or 0)
    return play_fee, loc_fee, option_fee, total

def jpy(n):
    return f"¥{int(n):,}"


# -----------------------------
# 予約情報（共通）
# -----------------------------
def make_reservation_info():
    dt = datetime.combine(inp_date, inp_time)
    weekday = weekday_jp[dt.weekday()]
    play_fee, loc_fee, option_fee, total = calc_total(
        inp_play_time, loc_choice, loc_extra, inp_options, option_other_fee, inp_extra_fee
    )

    lines = []
    lines.append("‐‐‐‐‐‐‐‐")
    lines.append("【ご予約内容】")
    lines.append(f"{dt.strftime('%m月%d日')}（{weekday}） {dt.strftime('%H:%M')}〜（{inp_play_time}分枠）")
    lines.append(f"場所：{loc_choice}")

    if inp_options:
        lines.append(f"オプション：{format_options(inp_options)}")

    if option_other_fee:
        lines.append(f"オプション（その他）　{jpy(option_other_fee)}")

    if inp_extra_fee:
        lines.append(f"特別追加料金　　{jpy(inp_extra_fee)}")

    if inp_other_text:
        lines.append(f"その他　{inp_other_text}")

    lines.append("")
    lines.append(f"合計：{jpy(total)}")
    lines.append("‐‐‐‐‐‐‐‐")
    return "\n".join(lines)


# -----------------------------
# DM・メールテンプレ（全部あなたの元コード通り）
# -----------------------------
# ※（ここは長いので省略せずそのまま入れてあります）
# すべて元のロジックを保持しています

def make_dm1():
