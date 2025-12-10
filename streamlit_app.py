# streamlit_app.py
import streamlit as st
import streamlit.components.v1 as components
from datetime import datetime

st.set_page_config(page_title="予約・DM・メール自動生成", layout="centered")

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
    inp_play_time = st.selectbox("プレイ時間（分枠）", list(play_prices.keys()), index=2)

with col2:
    inp_date = st.date_input("日付", value=datetime.now().date())
    inp_time = st.time_input("開始時刻", value=datetime.strptime("15:00", "%H:%M").time())
    loc_choice = st.selectbox("場所（選択）", list(location_prices.keys()), index=1)
    loc_extra = 0
    if loc_choice == "その他（特別料金）":
        loc_extra = st.number_input("その他（場所）特別料金（¥）", min_value=0, step=100)

inp_options = st.multiselect("オプション（複数選択可）", list(option_prices.keys()))
option_other_fee = 0
if "その他(特別料金)" in inp_options:
    option_other_fee = st.number_input("オプションのその他（金額 ¥）", min_value=0, step=100)

inp_extra_fee = st.number_input("特別追加料金（任意 ¥）", min_value=0, step=100)
inp_other_text = st.text_input("その他（任意）", value="")

# -----------------------------
# ヘルパー関数
# -----------------------------
def jpy(n):
    return f"¥{int(n):,}"

def format_options(opts):
    fixed = [o for o in opts if o != "その他(特別料金)"]
    if "その他(特別料金)" in opts:
        fixed.append("その他")
    return "・".join(fixed)

def calc_total(play_key, loc_key, loc_extra_val, opts, opt_other_fee, extra_fee_val):
    play_fee = play_prices.get(play_key, 0)
    loc_fee = location_prices.get(loc_key, 0) + (loc_extra_val or 0)
    option_fee = sum(option_prices.get(o, 0) for o in opts) + (opt_other_fee or 0)
    total = play_fee + loc_fee + option_fee + (extra_fee_val or 0)
    return play_fee, loc_fee, option_fee, total

# -----------------------------
# 予約情報生成
# -----------------------------
def make_reservation_info():
    dt = datetime.combine(inp_date, inp_time)
    weekday = weekday_jp[dt.weekday()]
    play_fee, loc_fee, option_fee, total = calc_total(inp_play_time, loc_choice, loc_extra, inp_options, option_other_fee, inp_extra_fee)

    body = []
    body.append("‐‐‐‐‐‐‐‐")
    body.append("【ご予約内容】")
    body.append(f"{dt.strftime('%m月%d日')}（{weekday}） {dt.strftime('%H:%M')}〜（{inp_play_time}分枠）")
    body.append(f"場所：{loc_choice}")

    if inp_options:
        body.append(f"オプション：{format_options(inp_options)}")
    if option_other_fee:
        body.append(f"オプション（その他）　{jpy(option_other_fee)}")
    if inp_extra_fee:
        body.append(f"特別追加料金　{jpy(inp_extra_fee)}")
    if inp_other_text:
        body.append(f"その他　{inp_other_text}")

    body.append("")
    body.append(f"合計：{jpy(total)}")
    body.append("‐‐‐‐‐‐‐‐")
    return "\n".join(body)

# -----------------------------
# 出力 UI
# -----------------------------
st.markdown("---")
st.subheader("■ 出力（料金明細 × テンプレ生成）")

col_fee, col_out = st.columns(2)

# -----------------------------
# ★ カードデザイン料金明細（インデント完全除去版）★
# -----------------------------
with col_fee:
    play_fee, loc_fee, option_fee, total = calc_total(
        inp_play_time, loc_choice, loc_extra, inp_options, option_other_fee, inp_extra_fee
    )

    fee_html = f"""
<div style="background-color:#fff; padding:18px; border-radius:14px;
    border:1px solid #e0e0e0; box-shadow:0 3px 10px rgba(0,0,0,0.12);
    margin-bottom:20px; font-size:16px; line-height:1.6;">

    <div><strong>プレイ料金：</strong> {jpy(play_fee)}</div>

    <div><strong>場所料金：</strong> {jpy(loc_fee)} <span style='color:#666;'>（{loc_choice}）</span></div>

    <div><strong>オプション料金：</strong> {jpy(option_fee)}</div>
"""

    if inp_extra_fee:
        fee_html += f"""
    <div><strong>特別追加料金：</strong> {jpy(inp_extra_fee)}</div>
"""

    fee_html += f"""
    <hr style="margin:14px 0; border-top:1px solid #ddd;">
    <div style="font-size:20px; font-weight:bold; color:#e91e63; text-align:right;">
        合計：{jpy(total)}
    </div>
</div>
"""

    st.markdown(fee_html, unsafe_allow_html=True)

# -----------------------------
# テンプレート生成
# -----------------------------
with col_out:
    st.markdown("### ✉ テンプレート生成")
    choice = st.selectbox(
        "テンプレを選んでください",
        [
            "予約情報",
            "DM①（最初）",
            "DM②（カウンセリング後）",
            "DM③（前日確認）",
            "メール①（最初）",
            "メール②（カウンセリング後）",
            "メール③（前日確認）"
        ]
    )

    if st.button("生成"):
        if choice == "予約情報":
            out_text = make_reservation_info()
        elif choice == "DM①（最初）":
            out_text = make_reservation_info()
        else:
            out_text = make_reservation_info()

        escaped = out_text.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")

        components.html(f"""
        <textarea id='out' style='width:100%;height:320px;'>{escaped}</textarea>
        <button onclick="navigator.clipboard.writeText(document.getElementById('out').value)"
        style="padding:8px 12px; font-size:16px; margin-top:6px;">📋 コピー</button>
        """, height=420)

st.markdown("---")
