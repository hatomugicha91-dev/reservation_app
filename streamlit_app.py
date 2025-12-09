# streamlit_app.py
import streamlit as st
import streamlit.components.v1 as components
from datetime import datetime

st.set_page_config(page_title="予約・DM・メール自動生成", layout="centered")

# -----------------------------
# マスタデータ（料金等）
# -----------------------------
play_prices = {
    "60": 20000, "90": 25000, "120": 30000, "150": 45000, "180": 55000,
    "210": 65000, "240": 75000, "270": 85000, "300": 95000, "330": 105000,
    "オールナイト": 120000, "特殊料金": 0
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

# -----------------------------
# 曜日表記（日本語）
# -----------------------------
weekday_jp = ["月", "火", "水", "木", "金", "土", "日"]

# -----------------------------
# UI：フォーム（基本情報）
# -----------------------------
st.title("予約・DM・メール自動生成ツール")

st.markdown("### ■ 基本情報入力")
with st.form(key="info_form"):
    col1, col2 = st.columns(2)
    with col1:
        inp_name = st.text_input("名前", value="")
        inp_email = st.text_input("メールアドレス（任意）", value="")
        inp_phone = st.text_input("電話番号（任意）", value="")
        inp_play_time = st.selectbox("プレイ時間（分枠）", options=list(play_prices.keys()), index=list(play_prices.keys()).index("120"))
    with col2:
        inp_date = st.date_input("日付", value=datetime.now().date())
        inp_time = st.time_input("開始時刻", value=datetime.strptime("15:00", "%H:%M").time())
        loc_choice = st.selectbox("場所（選択）", options=list(location_prices.keys()), index=list(location_prices.keys()).index("渋谷（道玄坂）"))
        loc_extra = 0
        if loc_choice == "その他（特別料金）":
            loc_extra = st.number_input("その他（場所）特別料金（¥）", min_value=0, step=100, value=0)
        inp_options = st.multiselect("オプション（複数選択可）", options=list(option_prices.keys()))
        option_other_fee = 0
        if "その他(特別料金)" in inp_options:
            option_other_fee = st.number_input("オプションのその他（金額 ¥）", min_value=0, step=100, value=0)
        inp_extra_fee = st.number_input("特別追加料金（任意 ¥）", min_value=0, step=100, value=0)
        inp_other_text = st.text_input("その他（任意）", value="")
    submitted = st.form_submit_button("フォームに反映")

# -----------------------------
# ヘルパー：金額計算・表示整形
# -----------------------------
def format_options(opts):
    return "・".join([o for o in opts if o != "その他(特別料金)"] + (["その他"] if "その他(特別料金)" in opts else []))

def calc_total(play_key, loc_key, loc_extra_val, opts, opt_other_fee, extra_fee_val):
    play_fee = play_prices.get(play_key, 0)
    loc_fee = location_prices.get(loc_key, 0) + (loc_extra_val or 0)
    option_fee = sum(option_prices.get(o, 0) for o in opts) + (opt_other_fee or 0)
    total = play_fee + loc_fee + option_fee + (extra_fee_val or 0)
    return play_fee, loc_fee, option_fee, total

def jpy(n):
    return f"¥{int(n):,}"

# -----------------------------
# 生成テキスト作成
# -----------------------------
def make_basic_info():
    dt = datetime.combine(inp_date, inp_time)
    weekday = weekday_jp[dt.weekday()]
    play_minutes = inp_play_time
    opt_text = format_options(inp_options)
    lines = [
        "【基本情報】",
        f"名前　{inp_name}"
    ]
    if inp_email:
        lines.append(f"メールアドレス　{inp_email}")
    if inp_phone:
        lines.append(f"電話番号　{inp_phone}")
    lines.extend([
        f"場所　{loc_choice}",
        f"日付　{dt.strftime('%Y/%m/%d')}（{weekday}）",
        f"開始時刻　{dt.strftime('%H:%M')}～",
        f"プレイ時間（分枠）　{play_minutes}"
    ])
    if opt_text:
        lines.append(f"オプション（複数可）　{opt_text}")
    if inp_extra_fee:
        lines.append(f"特別追加料金　　{jpy(inp_extra_fee)}")
    if inp_other_text:
        lines.append(f"その他　{inp_other_text}")
    return "\n".join(lines)

def make_reservation_info():
    dt = datetime.combine(inp_date, inp_time)
    weekday = weekday_jp[dt.weekday()]
    play_fee, loc_fee, option_fee, total = calc_total(inp_play_time, loc_choice, loc_extra, inp_options, option_other_fee, inp_extra_fee)
    lines = [
        "‐‐‐‐‐‐‐‐",
        "【ご予約内容】",
        f"{dt.month}月{dt.day}日（{weekday}） {dt.strftime('%H:%M')}〜（{inp_play_time}分枠）",
        f"場所：{loc_choice}"
    ]
    if inp_options:
        lines.append(f"オプション：{format_options(inp_options)}")
    if option_other_fee:
        lines.append(f"オプション（その他）　{jpy(option_other_fee)}")
    if inp_extra_fee:
        lines.append(f"特別追加料金　　{jpy(inp_extra_fee)}")
    if inp_other_text:
        lines.append(f"その他　{inp_other_text}")
    lines.append(f"\n合計：{jpy(total)}")
    lines.append("‐‐‐‐‐‐‐‐")
    return "\n".join(lines)

# -----------------------------
# DM / メールテンプレ作成
# -----------------------------
def make_dm1():
    dt = datetime.combine(inp_date, inp_time)
    weekday = weekday_jp[dt.weekday()]  # 日本語に変更
    return f"""ご連絡ありがとうございます。

{dt.strftime('%Y/%m/%d')}（{weekday}） {dt.strftime('%H:%M')}〜の{inp_play_time}分枠で、ただいまご予約を仮押さえさせていただいております。

ご予約の確定には、以下のカウンセリングフォームのご記入が必要となります。
お手数をおかけいたしますが、ご確認のうえご記入をお願いいたします。

▶︎カウンセリングフォーム
https://docs.google.com/forms/d/e/1FAIpQLSf0XNC78LSqy8xKGGL6AjlIQGu7Wthi7tbzr-gS2mwqqwcmhw/viewform

ご不明な点がございましたら、どうぞお気軽にご連絡ください。
"""

def make_dm2():
    return f"""カウンセリングフォームへのご記入、ありがとうございました☺️

以下の日時でご予約を確定させていただきます。

{make_reservation_info()}

ご質問や追加のご希望などがありましたら、お気軽にお知らせください。

前日にはこちらから最終確認のご連絡を差し上げます。
なお、当日の無断キャンセルは料金の100%を頂戴しております。
ご変更がある場合は、前日確認の時までにお知らせいただけますと幸いです。

お会いできるのを楽しみにしております。
引き続きよろしくお願いいたします✨
"""

def make_dm3():
    return f"""いよいよ明日ですね！前日確認のご連絡です。

{make_reservation_info()}

当日ホテルに到着されましたら
★ホテル名とお部屋番号をご連絡ください。

早めにお知らせいただけますと、スムーズにお伺いすることができます。

明日お会いできるのを心より楽しみにしています。

どうぞよろしくお願いいたします！
"""

def make_mail1():
    subject = f"件名：仮予約のご案内（{inp_date.strftime('%Y/%m/%d')} {inp_time.strftime('%H:%M')}〜）/むぎ茶"
    header = f"{inp_name} 様" if inp_name else ""
    return f"""{subject}

{header}

{make_dm1()}

むぎ茶
"""

def make_mail2():
    subject = f"件名：【確定】ご予約についてのご案内（{inp_date.strftime('%Y/%m/%d')} {inp_time.strftime('%H:%M')}〜）"
    header = f"{inp_name} 様" if inp_name else ""
    return f"""{subject}

{header}

{make_dm2()}

むぎ茶
"""

def make_mail3():
    subject = f"件名：前日確認のご案内 /むぎ茶"
    header = f"{inp_name} 様" if inp_name else ""
    return f"""{subject}

{header}

{make_dm3()}

むぎ茶
"""

# -----------------------------
# 出力選択 UI
# -----------------------------
st.markdown("---")
st.subheader("■ 出力選択")

choice = st.selectbox("出力するテンプレを選択してください",
                      options=[
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
        out_text = make_mail2()
    else:
        out_text = make_mail3()

    escaped = out_text.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")
    html = f"""
    <div>
      <textarea id="out" style="width:100%;height:320px;">{escaped}</textarea><br/>
      <button onclick="navigator.clipboard.writeText(document.getElementById('out').value)" style="padding:8px 12px; font-size:16px;">📋 コピー</button>
      <span id="copystatus" style="margin-left:10px;"></span>
    </div>
    <script>
      const btn = document.querySelector('button');
      btn.addEventListener('click', () => {{
        const s=document.getElementById('copystatus');
        s.textContent=' コピーしました ✔';
        setTimeout(()=>s.textContent='',2000);
      }});
    </script>
    """
    components.html(html, height=420)

st.markdown("---")
st.caption("※「その他（特別料金）」選択時は、場所の追加料金を入力してください。特別追加料金は任意で入力できます。")
