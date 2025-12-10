# streamlit_app.py
import streamlit as st
import streamlit.components.v1 as components
from datetime import datetime

st.set_page_config(page_title="予約・DM・メール自動生成", layout="wide")

# -----------------------------
# マスタデータ（料金等）
# -----------------------------
play_prices = {
    "60": 20000, "90": 25000, "120": 35000, "150": 45000, "180": 55000,
    "210": 65000, "240": 75000, "270": 85000, "300": 95000, "330": 105000,
    "オールナイト": 120000, "特殊料金": 0
}

option_prices = {
    "無し": 0, "乳首舐め": 2000, "聖水": 3000, "ボンデージ": 1000,
    "その他の衣装": 1000, "局部奉仕": 8000, "アナル奉仕": 5000, "その他(特別料金)": 0
}

location_prices = {
    "新宿(歌舞伎町)/渋谷(道玄坂)/鶯谷": 0,
    "池袋/五反田/錦糸町": 1000,
    "アルファイン": 3000,
    "その他（特別料金）": 0
}

weekday_jp = ["月", "火", "水", "木", "金", "土", "日"]

# -----------------------------
# UI（左：入力 / 右：出力）
# -----------------------------
st.title("予約・DM・メール自動生成ツール")

left, right = st.columns([1, 1.4])

with left:
    st.markdown("### ■ 基本情報（入力）")
    inp_name = st.text_input("名前", value="")  # 名前のみ（メール・電話は削除）

    st.markdown("### ■ 予約情報（入力）")
    inp_date = st.date_input("日付", value=datetime.now().date())
    inp_time = st.time_input("開始時刻", value=datetime.strptime("15:00", "%H:%M").time())
    inp_play_time = st.selectbox("プレイ時間（分枠）", options=list(play_prices.keys()), index=list(play_prices.keys()).index("120"))
    loc_choice = st.selectbox("場所（選択）", options=list(location_prices.keys()), index=list(location_prices.keys()).index("新宿(歌舞伎町)/渋谷(道玄坂)/鶯谷"))
    loc_extra = 0
    if loc_choice == "その他（特別料金）":
        loc_extra = st.number_input("その他（場所）特別料金（¥）", min_value=0, step=100, value=0)

    inp_options = st.multiselect("オプション（複数可）", options=list(option_prices.keys()))
    option_other_fee = 0
    if "その他(特別料金)" in inp_options:
        option_other_fee = st.number_input("オプションのその他（金額 ¥）", min_value=0, step=100, value=0)

    inp_extra_fee = st.number_input("特別追加料金（任意 ¥）", min_value=0, step=100, value=0)
    inp_other_text = st.text_input("その他（任意）", value="")

    # Form reflect button to explicitly apply inputs (optional)
    if st.button("入力を反映"):
        st.experimental_rerun()

# -----------------------------
# 計算・整形ヘルパー
# -----------------------------
def format_options(opts):
    # 表示用：その他(特別料金)を「その他」に置換
    return "・".join([o for o in opts if o != "その他(特別料金)"] + (["その他"] if "その他(特別料金)" in opts else []))

def calc_total():
    play_fee = play_prices.get(inp_play_time, 0)
    loc_fee = location_prices.get(loc_choice, 0) + (loc_extra or 0)
    option_fee = sum(option_prices.get(o, 0) for o in inp_options) + (option_other_fee or 0)
    total = play_fee + loc_fee + option_fee + (inp_extra_fee or 0)
    return play_fee, loc_fee, option_fee, total

def jpy(n):
    return f"¥{int(n):,}"

def make_reservation_info():
    dt = datetime.combine(inp_date, inp_time)
    weekday = weekday_jp[dt.weekday()]
    play_fee, loc_fee, option_fee, total = calc_total()
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
# DM / メールテンプレ（通常）
# -----------------------------
def make_dm1():
    dt = datetime.combine(inp_date, inp_time)
    weekday = weekday_jp[dt.weekday()]
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

def make_mail1():
    dt = datetime.combine(inp_date, inp_time)
    weekday = weekday_jp[dt.weekday()]
    subject = f"件名：仮予約のご案内（{dt.strftime('%Y/%m/%d')} {dt.strftime('%H:%M')}〜）/むぎ茶"
    header = f"{inp_name} 様\n\n" if inp_name else ""
    return f"""{subject}

{header}{make_dm1()}

むぎ茶
"""

def make_mail2():
    dt = datetime.combine(inp_date, inp_time)
    weekday = weekday_jp[dt.weekday()]
    subject = f"件名：【確定】ご予約についてのご案内（{dt.strftime('%Y/%m/%d')} {dt.strftime('%H:%M')}〜）"
    header = f"{inp_name} 様\n\n" if inp_name else ""
    return f"""{subject}

{header}{make_dm2()}

むぎ茶
"""

# -----------------------------
# 当日予約テンプレ（参考文面に準拠）
# -----------------------------
def make_dm_today1():
    dt = datetime.combine(inp_date, inp_time)
    weekday = weekday_jp[dt.weekday()]
    return f"""ご連絡ありがとうございます。 

本日{dt.strftime('%m月%d日')}（{weekday}） {dt.strftime('%H:%M')}〜の{inp_play_time}分枠で、ただいまご予約を仮押さえさせていただいております。

ご予約の確定には、以下のカウンセリングフォームのご記入が必要となります。 
お手数をおかけいたしますが、ご確認のうえご記入をお願いいたします。 

（プレイ予定の２時間前までにご入力が無ければ、キャンセル扱いとなります。）

▶︎カウンセリングフォーム 
https://docs.google.com/forms/d/e/1FAIpQLSf0XNC78LSqy8xKGGL6AjlIQGu7Wthi7tbzr-gS2mwqqwcmhw/viewform 

カウンセリングフォームへの入力が済みましたら、一度ご連絡頂けましたら幸いです。

お会いできるのを楽しみにしています。

よろしくお願いいたします。
"""

def make_dm_today2():
    return f"""カウンセリングフォームへのご記入、ありがとうございました☺️

本日のご予約を確定させていただきます。

{make_reservation_info()}

★ホテルに到着されましたら 
ホテル名とお部屋番号をご連絡ください。 

早めにお知らせいただけますと、スムーズにお伺いすることができます。 

ご不明な点がございましたら、どうぞお気軽にご連絡ください。 

お会いできるのを心より楽しみにしております。 
よろしくお願い致します♡
"""

def make_mail_today1():
    dt = datetime.combine(inp_date, inp_time)
    weekday = weekday_jp[dt.weekday()]
    subject = "件名： 仮予約のご案内（要確認）/むぎ茶"
    header = f"{inp_name} 様\n\n" if inp_name else ""
    return f"""{subject}

{header}ご連絡ありがとうございます。 

本日{dt.strftime('%m月%d日')}（{weekday}） {dt.strftime('%H:%M')}〜の{inp_play_time}分枠で、ただいまご予約を仮押さえさせていただいております。

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

def make_mail_today2():
    subject = "件名：本日のご予約確定のご案内/むぎ茶"
    header = f"{inp_name} 様\n\n" if inp_name else ""
    return f"""{subject}

{header}カウンセリングフォームへのご記入、ありがとうございました☺️

本日のご予約を確定させていただきます。

{make_reservation_info()}

★ホテルに到着されましたら 
ホテル名とお部屋番号をご連絡ください。 

早めにお知らせいただけますと、スムーズにお伺いすることができます。 

ご不明な点がございましたら、どうぞお気軽にご連絡ください。 

お会いできるのを心より楽しみにしております。 
よろしくお願い致します♡


むぎ茶
"""

# -----------------------------
# 出力選択（右カラム）
# -----------------------------
with right:
    st.markdown("### ■ 生成・出力")
    choice = st.selectbox("出力するテンプレを選択してください", options=[
        "予約情報",
        "DM①（最初）",
        "DM②（カウンセリング後）",
        "メール①（最初）",
        "メール②（カウンセリング後）",
        "【当日予約】DM①最初",
        "【当日予約】DM②カウンセリング後",
        "【当日予約】メール①最初",
        "【当日予約】メール②カウンセリング後"
    ])

    if st.button("文章を生成"):
        if choice == "予約情報":
            out_text = make_reservation_info()
        elif choice == "DM①（最初）":
            out_text = make_dm1()
        elif choice == "DM②（カウンセリング後）":
            out_text = make_dm2()
        elif choice == "メール①（最初）":
            out_text = make_mail1()
        elif choice == "メール②（カウンセリング後）":
            out_text = make_mail2()
        elif choice == "【当日予約】DM①最初":
            out_text = make_dm_today1()
        elif choice == "【当日予約】DM②カウンセリング後":
            out_text = make_dm_today2()
        elif choice == "【当日予約】メール①最初":
            out_text = make_mail_today1()
        else:
            out_text = make_mail_today2()

        # safe-escape
        escaped = out_text.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")
        html = f"""
<div>
  <textarea id="out" style="width:100%;height:380px;">{escaped}</textarea><br/>
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
      setTimeout(()=> s.textContent = '', 2000);
    }});
  }});
</script>
"""
        components.html(html, height=460)

st.markdown("---")
st.caption("※場所の「その他（特別料金）」を選んだ場合、場所追加料金の入力を行ってください。特別追加料金は任意で入力できます。")
