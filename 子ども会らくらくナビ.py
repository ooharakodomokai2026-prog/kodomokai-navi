import os
import re
import json
import base64
import requests
import datetime
import streamlit as st

st.set_page_config(page_title="子ども会 らくらくナビ", page_icon="🎈", layout="wide")

# デザイン設定
st.markdown("""
<style>
.stApp { background-color: #FFFDF0; }
.custom-title {
    background-color: #FDB849; color: white; padding: 15px; border-radius: 10px;
    text-align: center; font-size: 2.2rem; font-weight: bold; margin-bottom: 2rem;
}
</style>
<div class="custom-title">🎈 子ども会 らくらくナビ 🎈</div>
""", unsafe_allow_html=True)

# ★★★ ご自身のGASウェブアプリURL ★★★
GAS_URL = "https://script.google.com/macros/s/AKfycbzhE4SNVf5CbCb0GzMc5BkU9QuiQntbUi_nwjts-xsekXK10aR0BEywRNkx_bJcaHs/exec"

# ファイル自動検索＆ダウンロード機能
def find_actual_file(target_filename):
    if os.path.exists(target_filename): return target_filename
    def clean_name(s):
        name, ext = os.path.splitext(s)
        return re.sub(r'[^a-zA-Z0-9ぁ-んァ-ヶ一-龥]', '', name.replace('入会', '入学').replace('〇', '').replace('○', '')) + ext.lower()
    target_clean = clean_name(target_filename)
    for f in os.listdir('.'):
        if os.path.isfile(f) and (target_clean in clean_name(f) or clean_name(f) in target_clean): return f
    return None

def show_download(label, filename):
    actual_file = find_actual_file(filename)
    if actual_file:
        with open(actual_file, "rb") as f:
            st.download_button(label=f"📄 {label}", data=f, file_name=actual_file, use_container_width=True)

# サイドバー設定
month_list = ["4月", "5月", "6月", "7月", "8月", "9月", "10月", "11月", "12月", "1月", "2月", "3月"]
selected_month = st.sidebar.selectbox("月を選択してください", month_list, index=0)

st.header(f"✨ {selected_month}の予定と必要な準備 🔗")

# デフォルトのノウハウデータ
default_knowhow = {
    "4月": "* 新1年生案内: 小学校からの情報提供がないため、町内会の総書さんへ「新1年生の回覧が集まったら教えてほしい」と事前にお願いしておくのがコツ！\n* ポスター掲示: 町内会未加入の方に向けて、地域の掲示板（6ヶ所）に強力テープでポスターを貼り出します。\n* 迎える会の準備: 大原会館の予約は管理者の山口さんへ用紙提出（当日はカギを受け取る）。新1年生へのプレゼント（約1,000円。例年「名入り鉛筆」「折りたたみ傘」が好評！）や、全員用のお菓子を手配しておきます。",
    "5月": "* 迎える会当日のプログラム: あいさつ ➔ 自己紹介 ➔ ゲーム ➔ おわりのあいさつ ➔ おみやげ（解散）。\n* 雨天時の対応: 雨なら「会館内でゲーム」（※倉庫に道具あり）。過去には「BBQ」の提案もありました。\n* 球技大会案内: 青崎小、新町小の両校に通う町内の子どもたちにも届くよう、地域掲示板6ヶ所にポスターを掲示して子ども会のグループLINEでお知らせします。",
    "8月": "* ラジオ体操最終日: 頑張った子どもたちへアイスクリームやお菓子を用意してね！（歓迎会の時にまとめて購入して配れるようにしておくと楽です）\n* 盆踊りの店舗: 帰省者が多いので出店するなら１店舗。（おすすめはかたぬき屋さん）\n* 夏フェス当日の動き: 16:45集合。17:00〜17:30までは大人対応してもらい、子どもには先に遊んでもらいます。17:30～18:00 / 18:00〜18:30は子どもお手伝い参加。19:00までの残りは大人対応。大人は1時間交代がおすすめ。寄付金等をいただいた場合は後日お礼（お返し）を用意し、9月定例会で収支報告をします。",
    "10月": "* お菓子手配: 秋祭りのお菓子は人数分より多めに用意。10日前までに注文を完了させます。\n* 余ったお菓子: もし秋祭りでお菓子が余ったら（例: 20袋残った等）、11月の映画鑑賞会で子どもたちに配ると喜ばれます！\n* 映画鑑賞会: 会館のプロジェクターを使うため、早めに管理人の山岡さんへ予約をお願いしておきます。"
}

# --- GASから保存済みノウハウを取得 ---
current_knowhow_text = default_knowhow.get(selected_month, "")
try:
    res = requests.post(GAS_URL, data=json.dumps({"action": "getKnowhow", "month": selected_month}), headers={"Content-Type": "application/json"}, timeout=5)
    if res.status_code == 200:
        fetched_data = res.json()
        if fetched_data.get("result") == "success" and fetched_data.get("text"):
            current_knowhow_text = fetched_data.get("text")
except Exception:
    pass

# 月別やる事＆原紙
st.subheader("📝 タスク＆資料")
col1, col2 = st.columns([3, 2])
with col1:
    st.checkbox("今月のメイン業務・確認事項")
    st.checkbox("資料作成・関係各所への連絡")
with col2:
    show_download("年間行事計画・報告 (Excel)", "令和○○年度_行事計画+報告_原紙.xlsx")

st.divider()

# --- 編集＆保存可能なノウハウ欄 ---
st.subheader("💡 ノウハウ＆アドバイス（自由編集・永久保存可能）")
edited_text = st.text_area("文章を書き換えて下の「保存ボタン」を押すと、永久に最新状態が記録されます！", value=current_knowhow_text, height=180)

if st.button("💾 この月のノウハウを更新・保存する", use_container_width=True):
    with st.spinner("Googleクラウドへ永久保存中..."):
        try:
            save_res = requests.post(GAS_URL, data=json.dumps({"action": "saveKnowhow", "month": selected_month, "text": edited_text}), headers={"Content-Type": "application/json"}, timeout=10)
            
            if save_res.status_code == 200:
                try:
                    result_json = save_res.json()
                    if result_json.get("result") == "success":
                        st.success(f"🎉 {selected_month}のノウハウを永久保存しました！次回以降もこの文章が表示されます。")
                    else:
                        st.error(f"保存処理エラー: {result_json.get('error')}")
                except Exception:
                    st.error("❌ GASからの返答がJSON形式ではありません。GASのアクセス権限が「全員(Anyone)」になっているか確認してください。")
            else:
                st.error(f"通信エラー (Status: {save_res.status_code})")
        except Exception as e:
            st.error(f"エラーが発生しました: {e}")

st.divider()

# ファイル提出機能
st.subheader("📤 資料提出（自動整理）")
uploaded_file = st.file_uploader("ドラッグ＆ドロップで提出", key="uploader")
if uploaded_file and st.button("✨ このファイルを提出する ✨", use_container_width=True):
    with st.spinner("送信中..."):
        JST = datetime.timezone(datetime.timedelta(hours=+9), 'JST')
        now = datetime.datetime.now(JST)
        nendo = now.year - 1 if now.month <= 3 else now.year
        
        payload = {
            "fileName": uploaded_file.name, "mimeType": uploaded_file.type or "application/octet-stream",
            "fileData": base64.b64encode(uploaded_file.read()).decode('utf-8'),
            "year": str(nendo), "month": selected_month
        }
        res = requests.post(GAS_URL, data=json.dumps(payload), headers={"Content-Type": "application/json"})
        if res.status_code == 200 and res.json().get("result") == "success":
            st.success(f"🎉 提出完了！【{selected_month}提出】{uploaded_file.name}")
        else:
            st.error("提出に失敗しました。GASの設定を確認してください。")
