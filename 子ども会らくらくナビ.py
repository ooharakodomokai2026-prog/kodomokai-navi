import os
import re
import json
import base64
import requests
import datetime
import streamlit as st

st.set_page_config(page_title="子ども会 らくらくナビ", page_icon="🎈", layout="wide")

# --------------------------------------------------
# デザイン設定
# --------------------------------------------------
st.markdown("""
<style>
.stApp { background-color: #FFFDF0; }
.custom-title {
    background-color: #FDB849; color: white; padding: 15px; border-radius: 10px;
    text-align: center; font-size: 2.2rem; font-weight: bold; margin-bottom: 2rem;
    box-shadow: 0px 4px 6px rgba(0,0,0,0.1);
}
h1, h2, h3 { color: #333333; }
</style>
<div class="custom-title">🎈 子ども会 らくらくナビ 🎈</div>
""", unsafe_allow_html=True)

# ★★★ 正しいGASウェブアプリURL ★★★
GAS_URL = "https://script.google.com/macros/s/AKfycbzhE4SNVf5CbCf0GzMc5BkU9QuiQntbUi_nwjts-xsekXK10aR0BEywRNkx_bJcaHs/exec"

# --------------------------------------------------
# 超・強力ファイル自動検索機能
# --------------------------------------------------
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
    else:
        st.error(f"❌ ファイルが見つかりません: {filename}")

# サイドバー設定
month_list = ["4月", "5月", "6月", "7月", "8月", "9月", "10月", "11月", "12月", "1月", "2月", "3月"]
selected_month = st.sidebar.selectbox("月を選択してください", month_list, index=0)

st.header(f"✨ {selected_month}の予定と必要な準備 🔗")

# 全ての月を網羅したデフォルトのノウハウデータ
default_knowhow = {
    "4月": "* 新1年生案内: 小学校からの情報提供がないため、町内会の総書さんへ「新1年生の回覧が集まったら教えてほしい」と事前にお願いしておくのがコツ！\n* ポスター掲示: 町内会未加入の方に向けて、地域の掲示板（6ヶ所）に強力テープでポスターを貼り出します。\n* 迎える会の準備: 大原会館の予約は管理者の山口さんへ用紙提出（当日はカギを受け取る）。新1年生へのプレゼント（約1,000円。例年「名入り鉛筆」「折りたたみ傘」が好評！）や、全員用のお菓子を手配しておきます。",
    "5月": "* 迎える会当日のプログラム: あいさつ ➔ 自己紹介 ➔ ゲーム ➔ おわりのあいさつ ➔ おみやげ（解散）。\n* 雨天時の対応: 雨なら「会館内でゲーム」（※倉庫に道具あり）。過去には「BBQ」の提案もありました。\n* 球技大会案内: 青崎小、新町小の両校に通う町内の子どもたちにも届くよう、地域掲示板6ヶ所にポスターを掲示して子ども会のグループLINEでお知らせします。",
    "6月": "* アンケート収集: 射的（50円）やフランクフルト、ボールすくいなど、高学年の子どもたちが中心となって出店できるようにアンケートを取って企画をまとめます。\n* チケット作業: 50円チケットは量が多いので、役員同士で手分けしてハサミで切っておくと後が楽です！",
    "7月": "* ラジオ体操: 当日はYouTubeでラジオ体操を流します（スピーカーは会館にもあり）。雨天中止の判断は6:00〜6:15頃に子ども会LINEで連絡します。\n* 備品手配: 金魚すくい等の「たらい」は町内会から借ります。ダンボールで看板を用意しましょう。",
    "8月": "* ラジオ体操最終日: 頑張った子どもたちへアイスクリームやお菓子を用意してね！（歓迎会の時にまとめて購入して配れるようにしておくと楽です）\n* 盆踊りの店舗: 帰省者が多いので出店するなら１店舗。（おすすめはかたぬき屋さん）\n* 夏フェス当日の動き: 16:45集合。17:00〜17:30までは大人対応してもらい、子どもには先に遊んでもらいます。17:30～18:00 / 18:00〜18:30は子どもお手伝い参加。19:00までの残りは大人対応。大人は1時間交代がおすすめ。寄付金等をいただいた場合は後日お礼（お返し）を用意し、9月定例会で収支報告をします。",
    "9月": "* 御寄付のお礼: 御寄付をいただいた方には、必ず後日「菓子折り」と「お礼状」をお渡しするのがマナーです！\n* 運動会のお弁当: 当日手伝ってくれる中学生や保護者の人数もカウントして、お弁当やお茶をしっかり発注しておきましょう。",
    "10月": "* お菓子手配: 秋祭りのお菓子は人数分より多めに用意。10日前までに注文を完了させます。\n* 余ったお菓子: もし秋祭りでお菓子が余ったら（例: 20袋残った等）、11月の映画鑑賞会で子どもたちに配ると喜ばれます！\n* 映画鑑賞会: 会館のプロジェクターを使うため、早めに管理人の山岡さんへ予約をお願いしておきます。",
    "11月": "* 三世代交流: 育成から連絡が来ます。お昼のお弁当（うどん等）は育成側で用意してくれます。\n* クリスマス会準備: 子どもたちにサンタ帽子作りなどの工作をさせる場合は、11月中に役員で試作しておきます。ケーキも早めに予約しましょう。",
    "12月": "* クリスマス会当日の流れ: ボードゲーム ➔ サンタ帽子工作 ➔ ケーキデコレーション＆実食 ➔ サンタ＆トナカイからプレゼント登場！ ➔ 片付け。",
    "1月": "* 6年生の記念品: 予算は3,000円程度（例: QUOカードなど）。1月中に6年生本人に希望を聞いて手配しておきます。\n* 送る会の飲食: ケーキや軽食（お好み焼き等）の手配を進めます。",
    "2月": "* 総会案内: 欠席者向けに委任状を添えて事前に配布・回収します。\n* アンケート: 行事の良かった点・改善点をアンケートで回収し、次年度へ引き継ぎます。\n* 引き継ぎ: この「らくらくナビ」自体が引き継ぎマニュアルです！",
    "3月": "* 会計監査: 会則上、監査は前会長に依頼するのがスムーズです。\n* 紙の印刷物: 子ども会役員間はLINEで共有するため印刷不要ですが、LINEを使っていない町内会役員さん（年配の方等）向けには紙で印刷して準備しておきます。\n* 総会資料のコツ: 各イベントが終わるたびに行事報告書へ日付をこまめにメモしておくと、3月の総会資料作成が劇的にラクになります！"
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

# 月別タスク＆ダウンロード資料の定義
st.subheader("📝 タスク＆資料")
col1, col2 = st.columns([3, 2])

with col1:
    st.subheader("📝 今月の「やる事」リスト")
    if selected_month == "4月":
        st.checkbox("町内会定例会へ前会長が出席し、新役員案内を配って引き継ぎ完了")
        st.checkbox("自治会から新1年生の名簿（紙）を受け取る")
        st.checkbox("新1年生宅へ加入案内・入会届のポストイン（名簿をもとに訪問）")
        st.checkbox("町内会未加入・他校通学の1年生用に地域掲示板（6ヶ所）へポスター掲示")
        st.checkbox("自治会役員へ年間行事計画と新役員名簿を提出")
        st.checkbox("青崎学区子供会総会への出席（新旧役員・LINE交換）")
        st.checkbox("「新1年生を迎える会」の準備開始（会館予約等）")
    elif selected_month == "5月":
        st.checkbox("「新1年生を迎える会」の実施（大原会館/公園）")
        st.checkbox("新1年生プレゼント（折りたたみ傘等）とお菓子・おみやげの配布")
        st.checkbox("リーダー研修①の参加者取りまとめ（4・5・6年生）")
        st.checkbox("体協からの夏季球技大会に関する連絡確認＆ポスター掲示（6ヶ所・LINE）")
        st.checkbox("夏フェス企画案の初回話し合い（町内会と合同）")
    elif selected_month == "6月":
        st.checkbox("夏フェスの店舗・景品・人員選考の検討（アンケート実施）")
        st.checkbox("夏フェス用50円チケットの印刷・手分けして切る作業（ハサミ持参！）")
        st.checkbox("年間予算案（決算報告書の案）の提出")
        st.checkbox("体協・育成からの球技大会の連絡をLINEグループへ展開")
        st.checkbox("（要請があれば）球技大会のサポート")
    elif selected_month == "7月":
        st.checkbox("夏フェス説明会への参加・サポート（主催は運営委員）")
        st.checkbox("盆踊り打合せへの参加（内容・役割分担の確認）")
        st.checkbox("ラジオ体操のスタンプカード作成・開催ポスター掲示")
        st.checkbox("ラジオ体操の実施（1週間限定！）＆雨天LINE連絡準備")
    elif selected_month == "8月":
        st.checkbox("ラジオ体操最終日のアイスクリーム手配・配布")
        st.checkbox("夏フェスの看板作成（GeminiやChatGPTに作成させる！）")
        st.checkbox("盆行事の準備・当番シフト確認・本番・片付け")
        st.checkbox("夏フェス当日の準備（16:45集合、机・イス運搬）・運営・片付け")
        st.checkbox("盆行事・夏フェスの会計精算（購入関係ファイルに入力）")
    elif selected_month == "9月":
        st.checkbox("子ども商店の収支報告書を作成し、9月定例会で報告")
        st.checkbox("寄付（御寄付）をいただいた方へ菓子折りとお礼状を届ける")
        st.checkbox("運動会3町合同会議への出席（大原会館／大原町・本町・中町）")
        st.checkbox("体協から提供された運動会案内の配布・周知＆参加メンバー選考")
        st.checkbox("役員・手伝い用のお弁当発注（中学生や保護者の人数もカウントして14個程度）")
        st.checkbox("青崎学区 町民運動会 当日の運営協力")
    elif selected_month == "10月":
        st.checkbox("自治会からの秋祭り案内・法被指示（紙）の受け取り")
        st.checkbox("秋祭り用お菓子の手配（人数分より多めに用意！10日前までに注文）")
        st.checkbox("子ども用ハッピの準備・のぼり設置（5箇所）")
        st.checkbox("大原神社秋祭りのサポート")
        st.checkbox("11月映画鑑賞会用プロジェクター手配（大原会館山岡さんへ依頼）")
        st.checkbox("クリスマス会の企画・予算案作成の開始")
    elif selected_month == "11月":
        st.checkbox("映画鑑賞会のお知らせをLINEで配信・実施（あまりのお菓子配布）")
        st.checkbox("三世代交流ふれあい広場の参加・お手伝い（各町より役員2名参加）")
        st.checkbox("クリスマス会の工作（サンタ帽子等）の試作・ゲーム選定")
        st.checkbox("クリスマス会のケーキ（ピープル等）・プレゼント手配")
        st.checkbox("クリスマス会の予算案・案内文の完成")
    elif selected_month == "12月":
        st.checkbox("クリスマス会本番の実施＆1年間お疲れ様会")
        st.checkbox("クリスマス会予算案ファイルに「実績」を入力する")
        st.checkbox("大原会館の大掃除参加（自治会からの案内待ち／合同大掃除）")
        st.checkbox("広島ジュニアマリンバアンサンブルコンサート引率")
        st.checkbox("来期役員募集案内の作成（テンプレート活用）と全世帯配布")
    elif selected_month == "1月":
        st.checkbox("来期役員募集案内を全世帯のポストへ投函（ポストイン）")
        st.checkbox("育成からの冬季スポーツに関する連絡を待ち、LINEへ展開")
        st.checkbox("6年生へ卒業記念品（3,000円分QUOカード等）の希望ヒアリング")
        st.checkbox("「6年生を送る会」のケーキ・お好み焼き等の予約・手配")
    elif selected_month == "2月":
        st.checkbox("冬季スポーツフェスタ本番（楠那小 / 南区スポーツセンター）")
        st.checkbox("青崎学区防災訓練フェアへの協力")
        st.checkbox("子ども会総会開催のお知らせ（委任状付き）の作成・配布")
        st.checkbox("「6年生を送る会」プログラム作成（挨拶➔ルール➔食事➔ビンゴ等）")
        st.checkbox("1年間の振り返り「ご意見アンケート」の実施・回収")
        st.checkbox("新旧役員引き継ぎ＆会計監査の実施")
    elif selected_month == "3月":
        st.checkbox("「6年生を送る会」の実施")
        st.checkbox("会計監査の実施（前会長へ監査を依頼）")
        st.checkbox("総会資料（次第・会則・事業報告・会計報告）をまとめホッチキス留め")
        st.checkbox("「大原町子供会総会」の開催（大原会館）＆新役員へ挨拶依頼")
        st.checkbox("更新者の年会費を先に集金しておく（集金袋・案内の手配）")
        st.checkbox("町内会組長さんへ新1年生案内回覧の手配（3/20頃までに渡す）")
        st.checkbox("LINE不使用の町内会役員向けに新役員案内を紙で印刷準備")
        st.checkbox("新会長・新会計へ完全引き継ぎ完了")

with col2:
    st.subheader("📥 必要な資料・原紙")
    if selected_month == "4月":
        show_download("迎える会案内 (Excel)", "迎える会_案内_原紙.xlsx")
        show_download("入会届 育成版 (Excel)", "入会届○○年度_育成版_新1年・2～6年用_原紙.xlsx")
        show_download("入会届 育成休止版 (Excel)", "入会届○○年度_育成休止版_新1年・2～6年用_原紙.xlsx")
        show_download("年間行事計画・報告 (Excel)", "令和○○年度_行事計画+報告_原紙.xlsx")
        show_download("新役員名簿 (Excel)", "○○年度_子ども会名簿_原紙.xlsx")
    elif selected_month == "5月":
        show_download("迎える会案内 (Excel)", "迎える会_案内_原紙.xlsx")
        show_download("迎える会 課題打合せ内容 (Excel)", "迎える会_課題打合せ内容_①_原紙.xlsx")
        show_download("子ども会名簿 (Excel)", "○○年度_子ども会名簿_原紙.xlsx")
    elif selected_month == "6月":
        show_download("店舗・景品・人員選考表 (Excel)", "店舗・景品・人員選考表_原紙.xlsx")
        show_download("決算報告書(予算案) (Excel)", "決算報告書_案+実_原紙.xlsx")
        show_download("夏フェス50円チケット (Excel)", "50円チケット.xlsx")
    elif selected_month == "7月":
        show_download("盆踊り打合せ (Excel)", "盆踊り打合せ_原紙.xlsx")
        show_download("ラジオ体操 スタンプカード (Excel)", "ラジオ体操_スタンプカード_2026.xlsx")
        show_download("ラジオ体操 開催ポスター (Excel)", "ラジオ体操_原紙_20230718.xlsx")
    elif selected_month == "8月":
        show_download("盆踊り打合せ・シフト (Excel)", "盆踊り打合せ_原紙.xlsx")
        show_download("盆・夏フェス購入関係・会計 (Excel)", "盆・夏フェス購入関係_原紙.xlsx")
    elif selected_month == "9月":
        show_download("競技種目・メンバー選考 (Excel)", "競技種目_原紙.xlsx")
    elif selected_month in ["10月", "11月"]:
        show_download("クリスマス会 予算案 (Excel)", "クリスマス会予算案_原紙.xlsx")
        show_download("クリスマス会 案内 (Excel)", "クリスマス会案内_原紙.xlsx")
    elif selected_month == "12月":
        show_download("クリスマス会 予算案・実績 (Excel)", "クリスマス会予算案_原紙.xlsx")
        show_download("クリスマス会 案内 (Excel)", "クリスマス会案内_原紙.xlsx")
    elif selected_month == "1月":
        st.info("📁 今月はパソコンで開く決まった資料（様式）はありません。")
    elif selected_month == "2月":
        show_download("6年生さんを送る会 案+実績 (Excel)", "6年生さんを送る会案+実績_原紙.xlsx")
    elif selected_month == "3月":
        show_download("年間行事計画・報告 (Excel)", "令和○○年度_行事計画+報告_原紙.xlsx")
        show_download("決算報告書_案+実 (Excel)", "決算報告書_案+実_原紙.xlsx")
        show_download("子ども会会則 (Word)", "2.向洋大原子ども会会則 令和〇〇.docx")
        show_download("子供会総会 議案書・事業報告書 (Word)", "1.総会資料令和○○年度‗次第‗原紙.docx")
        show_download("6年生さんを送る会 案+実績 (Excel)", "6年生さんを送る会案+実績_原紙.xlsx")

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
                    st.error("❌ 返答形式エラーです。GASのデプロイでアクセス権限が「全員(Anyone)」になっているか確認してください。")
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
