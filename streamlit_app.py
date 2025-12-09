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

import streamlit.components.v1 as components

# -----------------------------
# 生成関数
# -----------------------------
def make_basic_info():
    lines = [
        "【基本情報】",
        f"名前　{name}",
    ]
    if email:
        lines.append(f"メールアドレス　{email}")
    if tel:
        lines.append(f"電話番号　{tel}")
    lines += [
        f"場所　{full_place}",
        f"日付　{date_str}（{weekday}）",
        f"開始時刻　{start_time.strftime('%H:%M')}～",
        f"プレイ時間（分）　{play_time}",
        f"オプション（複数可）　{option_list}" if options else "",
        special_fee_block.strip(),
        other_block.strip()
    ]
    return "\n".join([l for l in lines if l])

def make_reservation_info():
    lines = [
        "‐‐‐‐‐‐‐‐",
        "【ご予約内容】",
        f"{date_str}（{weekday}） {start_time.strftime('%H:%M')}～（{play_time}分枠）",
        f"場所：{full_place}",
        f"オプション：{option_list}" if options else "",
        special_fee_block.strip(),
        other_block.strip(),
        "",
        f"合計：¥{total:,}",
        "‐‐‐‐‐‐‐‐"
    ]
    return "\n".join([l for l in lines if l])

# -----------------------------
# DM / メールテンプレート
# -----------------------------
def make_dm1():
    return f"""ご連絡ありがとうございます。

{date_str}（{weekday}） {start_time.strftime('%H:%M')}〜の{play_time}分枠で、ただいまご予約を仮押さえさせていただいております。

ご予約確定にはカウンセリングフォームのご記入が必要です。
▶︎フォーム
https://docs.google.com/forms/d/e/1FAIpQLSf0XNC78LSqy8xKGGL6AjlIQGu7Wthi7tbzr-gS2mwqqwcmhw/viewform
"""

def make_dm2():
    return f"""カウンセリングフォームへのご記入ありがとうございました☺️

以下の日時でご予約を確定しました。

{make_reservation_info()}

前日確認のご連絡を差し上げます。
当日無断キャンセルは100%料金を頂戴します。
"""

def make_dm3():
    return f"""前日確認のご連絡です。

{make_reservation_info()}

ホテルに到着されましたらお部屋番号をご連絡ください。
"""

def make_mail1():
    subject = f"件名：仮予約のご案内（{date_str} {start_time.strftime('%H:%M')}〜）/むぎ茶"
    return f"""{subject}

{name} 様

{make_dm1()}

むぎ茶
"""

def make_mail2():
    # ←ここを修正：件名を固定で入れる
    subject = "件名：本日のご予約確定のご案内/むぎ茶"
    return f"""{subject}

{name} 様

{make_dm2()}

むぎ茶
"""

def make_mail3():
    subject = "件名：前日確認のご案内 /むぎ茶"
    return f"""{subject}

{name} 様

{make_dm3()}

むぎ茶
"""

# -----------------------------
# 出力選択
# -----------------------------
choice = st.selectbox("出力するテンプレを選択してください", options=[
    "基本情報",
    "予約情報",
    "DM①（最初）",
    "DM②（カウンセリング後）",
    "DM③（前日確認）",
    "メール①（最初）",
    "メール②（カウンセリング後）",
    "メール③（前日確認）"
])

if st.button("生成"):
    if choice == "基本情報":
        out_text = make_basic_info()
    elif choice == "予約情報":
        out_text = make_reservation_info()
    elif choice == "DM①（最初）":
        out_text = make_dm1()
    elif choice == "DM②（カウンセリング後）":
        out_text = make_dm2()
    elif choice == "DM③（前日確認）":
        out_text = make_dm3()
    elif choice == "メール①（最初）":
        out_text = make_mail1()
    elif choice == "メール②（カウンセリング後）":
        out_text = make_mail2()  # 件名修正済み
    else:
        out_text = make_mail3()

    # コピー用HTML
    escaped = out_text.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")
    html = f"""
<div>
<textarea id="out" style="width:100%;height:320px;">{escaped}</textarea><br/>
<button id="copybtn" style="padding:8px 12px; font-size:16px;">📋 コピー</button>
<span id="copystatus" style="margin-left:10px;"></span>
</div>
<script>
const btn = document.getElementById('copybtn');
btn.addEventListener('click', () => {{
  const textarea = document.getElementById('out');
  navigator.clipboard.writeText(textarea.value).then(() => {{
    const s = document.getElementById('copystatus');
    s.textContent = ' コピーしました ✔';
    setTimeout(()=> s.textContent='', 2000);
  }});
}});
</script>
"""
    components.html(html, height=420)

st.caption("※特別料金は任意で入力できます。")
