import os
import re
import json
import base64
import requests
import datetime
import streamlit as st

st.set_page_config(
    page_title="子ども会 らくらくナビ",
    page_icon="🎈",
    layout="wide"
)

# --------------------------------------------------
# デザイン設定
# --------------------------------------------------
st.markdown("""
<style>
.stApp { background-color: #FFFDF0; }
.custom-title {
    background-color: #FDB849;
    color: white;
    padding: 15px;
    border-radius: 10px;
    text-align: center;
    font-size: 2.2rem;
    font-weight: bold;
    margin-bottom: 2rem;
    box-shadow: 0px 4px 6px rgba(0,0,0,0.1);
}
h1, h2, h3 { color: #333333; }
</style>
<div class="custom-title">🎈 子ども会 らくらくナビ 🎈</div>
""", unsafe_allow_html=True)


# --------------------------------------------------
# 超・強力ファイル自動検索機能
# --------------------------------------------------
def find_actual_file(target_filename):
    if os.path.exists(target_filename):
        return target_filename
    
    def clean_name(s):
        name, ext = os.path.splitext(s)
        name = name.replace('入会', '入学').replace('〇', '').replace('○', '')
        name = re.sub(r'[^a-zA-Z0-9ぁ-んァ-ヶ一-龥]', '', name)
        return name + ext.lower()

    target_clean = clean_name(target_filename)
    
    for f in os.listdir('.'):
        if not os.path.isfile(f): continue
        f_clean = clean_name(f)
        if target_clean in f_clean or f_clean in target_clean:
            return f
            
    if "迎える会" in target_filename:
        for f in os.listdir('.'):
            if "迎える会" in f: return f
            
    return None

def show_download(label, filename):
    actual_file = find_actual_file(filename)
    if actual_file:
        ext = os.path.splitext(actual_file)[1].lower()
        mime_map = {
            ".xlsx": "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
            ".xls": "application/vnd.ms-excel",
            ".docx": "application/vnd.openxmlformats-officedocument.wordprocessingml.document"
        }
        mime = mime_map.get(ext, "application/octet-stream")

        with open(actual_file, "rb") as f:
            st.download_button(
                label=f"📄 {label}",
                data=f,
                file_name=actual_file,
                mime=mime,
                use_container_width=True
            )
    else:
        st.error(f"❌ ファイルが見つかりません。({filename})")

# サイドバー設定
month_list = ["4月", "5月", "6月", "7月", "8月", "9月", "10月", "11月", "12月", "1月", "2月", "3月"]
selected_month = st.sidebar.selectbox("月を選択してください", month_list, index=0)

st.header(f"✨ {selected_month}の予定と必要な準備 🔗")

# --- 月別コンテンツ ---
if selected_month == "4月":
    st.subheader("📌 4月：新年度スタート・学区総会・新入生案内")
    st.write("青崎学区子供会総会への出席、自治会役員への年間行事計画・新役員名簿の提出に加え、新1年生への加入案内を行います。")
    col1, col2 = st.columns([3, 2])
    with col1:
        st.subheader("📝 今月の「やる事」リスト")
        st.checkbox("町内会定例会へ前会長が出席し、新役員案内を配って引き継ぎ完了")
        st.checkbox("自治会から新1年生の名簿（紙）を受け取る")
        st.checkbox("新1年生宅へ加入案内・入会届のポストイン（名簿をもとに訪問）")
        st.checkbox("町内会未加入・他校通学の1年生用に地域掲示板（6ヶ所）へポスター掲示")
        st.checkbox("自治会役員へ年間行事計画と新役員名簿を提出")
        st.checkbox("青崎学区子供会総会への出席（新旧役員・LINE交換）")
        st.checkbox("「新1年生を迎える会」の準備開始（会館予約等）")
    with col2:
        st.subheader("📥 必要な資料・原紙")
        show_download("迎える会案内 (Excel)", "迎える会_案内_原紙.xlsx")
        show_download("入会届 育成版 (Excel)", "入会届○○年度_育成版_新1年・2～6年用_原紙.xlsx")
        show_download("入会届 育成休止版 (Excel)", "入会届○○年度_育成休止版_新1年・2～6年用_原紙.xlsx")
        show_download("年間行事計画・報告 (Excel)", "令和○○年度_行事計画+報告_原紙.xlsx")
        show_download("新役員名簿 (Excel)", "○○年度_子ども会名簿_原紙.xlsx")
    
    st.subheader("💡 ノウハウ＆アドバイス（※画面上で直接編集可能）")
    st.text_area("編集可能なアドバイス欄", value="""* 新1年生案内: 小学校からの情報提供がないため、町内会の総書さんへ「新1年生の回覧が集まったら教えてほしい」と事前にお願いしておくのがコツ！
* ポスター掲示: 町内会未加入の方に向けて、地域の掲示板（6ヶ所）に強力テープでポスターを貼り出します。
* 迎える会の準備: 大原会館の予約は山田さんへTELして用紙提出（当日はカギを受け取る）。新1年生へのプレゼント（約1,000円。例年「折りたたみ傘」が好評！）や、全員用のお菓子を手配しておきます。""", height=160, key="knowhow_4")

elif selected_month == "5月":
    st.subheader("📌 5月：新1年生を迎える会・リーダー研修①・球技大会準備")
    st.write("歓迎会、リーダー研修、夏季球技大会の準備、夏フェスの最初の企画話し合いを行います。")
    col1, col2 = st.columns([3, 2])
    with col1:
        st.subheader("📝 今月の「やる事」リスト")
        st.checkbox("「新1年生を迎える会」の実施（大原会館/公園）")
        st.checkbox("新1年生プレゼント（折りたたみ傘等）とお菓子・おみやげの配布")
        st.checkbox("リーダー研修①の参加者取りまとめ（4・5・6年生）")
        st.checkbox("体協からの夏季球技大会に関する連絡確認＆ポスター掲示（6ヶ所・LINE）")
        st.checkbox("夏フェス企画案の初回話し合い（町内会と合同）")
    with col2:
        st.subheader("📥 必要な資料・原紙")
        show_download("迎える会案内 (Excel)", "迎える会_案内_原紙.xlsx")
        show_download("迎える会 課題打合せ内容 (Excel)", "迎える会_課題打合せ内容_①_原紙.xlsx")
        show_download("子ども会名簿 (Excel)", "○○年度_子ども会名簿_原紙.xlsx")
    
    st.subheader("💡 ノウハウ＆アドバイス（※画面上で直接編集可能）")
    st.text_area("編集可能なアドバイス欄", value="""* 迎える会当日のプログラム: あいさつ ➔ 自己紹介ゲーム ➔ ころがしドッジ ➔ おわりのあいさつ ➔ おみやげ（解散）。
* 雨天時の対応: 雨なら「会館内でゲーム」、晴れなら「公園でドッジボール」（※倉庫に道具あり）。過去には「BBQ」の提案もありました。
* 球技大会案内: 他校（新田小など）に通う町内の子どもたちにも届くよう、地域掲示板6ヶ所にポスターを掲示してLINEでお知らせします。""", height=160, key="knowhow_5")

elif selected_month == "6月":
    st.subheader("📌 6月：夏フェス企画＆予算案・チケット作成・球技大会連絡")
    st.write("夏フェスの企画詳細とチケット作成を進めます。年間予算案の提出も行います。")
    col1, col2 = st.columns([3, 2])
    with col1:
        st.subheader("📝 今月の「やる事」リスト")
        st.checkbox("夏フェスの店舗・景品・人員選考の検討（アンケート実施）")
        st.checkbox("夏フェス用50円チケットの印刷・手分けして切る作業（ハサミ持参！）")
        st.checkbox("年間予算案（決算報告書の案）の提出")
        st.checkbox("体協・育成からの球技大会の連絡をLINEグループへ展開")
        st.checkbox("（要請があれば）球技大会のサポート")
    with col2:
        st.subheader("📥 必要な資料・原紙")
        show_download("店舗・景品・人員選考表 (Excel)", "店舗・景品・人員選考表_原紙.xlsx")
        show_download("決算報告書(予算案) (Excel)", "決算報告書_案+実_原紙.xlsx")
        show_download("夏フェス50円チケット (Excel)", "50円チケット.xlsx")
    
    st.subheader("💡 ノウハウ＆アドバイス（※画面上で直接編集可能）")
    st.text_area("編集可能なアドバイス欄", value="""* アンケート収集: 射的（50円）やフランクフルト、ボールすくいなど、高学年の子どもたちが中心となって出店できるようにアンケートを取って企画をまとめます。
* チケット作業: 50円チケットは量が多いので、役員同士で手分けしてハサミで切っておくと後が楽です！""", height=140, key="knowhow_6")

elif selected_month == "7月":
    st.subheader("📌 7月：夏フェス準備・盆踊り打合せ・ラジオ体操")
    st.write("夏フェスや盆踊りの打合せ、ラジオ体操（1週間のみ）の準備を行います。")
    col1, col2 = st.columns([3, 2])
    with col1:
        st.subheader("📝 今月の「やる事」リスト")
        st.checkbox("夏フェス説明会への参加・サポート（主催は運営委員）")
        st.checkbox("盆踊り打合せへの参加（内容・役割分担の確認）")
        st.checkbox("ラジオ体操のスタンプカード作成・開催ポスター掲示")
        st.checkbox("ラジオ体操の実施（1週間限定！）＆雨天LINE連絡準備")
    with col2:
        st.subheader("📥 必要な資料・原紙")
        show_download("盆踊り打合せ (Excel)", "盆踊り打合せ_原紙.xlsx")
        show_download("ラジオ体操 スタンプカード (Excel)", "ラジオ体操_スタンプカード_2026.xlsx")
        show_download("ラジオ体操 開催ポスター (Excel)", "ラジオ体操_原紙_20230718.xlsx")
    
    st.subheader("💡 ノウハウ＆アドバイス（※画面上で直接編集可能）")
    st.text_area("編集可能なアドバイス欄", value="""* ラジオ体操: 当日はYouTubeでラジオ体操を流します（スピーカーは会館にもあり）。雨天中止の判断は6:00〜6:15頃に子ども会LINEで連絡します。
* 備品手配: 金魚すくい等の「たらい」は町内会から借ります。ダンボールで看板を用意しましょう。""", height=140, key="knowhow_7")

elif selected_month == "8月":
    st.subheader("📌 8月：盆行事＆夏フェス本番")
    st.write("ラジオ体操の締めくくり、夏フェス看板準備、盆行事の準備・本番・片付け、夏フェス本番・片付けを行います。")
    col1, col2 = st.columns([3, 2])
    with col1:
        st.subheader("📝 今月の「やる事」リスト")
        st.checkbox("ラジオ体操最終日のアイスクリーム手配・配布")
        st.checkbox("夏フェスの看板作成（GeminiやChatGPTに作成させる！）")
        st.checkbox("盆行事の準備・当番シフト確認・本番・片付け")
        st.checkbox("夏フェス当日の準備（17:30集合、机・イス運搬）・運営・片付け")
        st.checkbox("盆行事・夏フェスの会計精算（購入関係ファイルに入力）")
    with col2:
        st.subheader("📥 必要な資料・原紙")
        show_download("盆踊り打合せ・シフト (Excel)", "盆踊り打合せ_原紙.xlsx")
        show_download("盆・夏フェス購入関係・会計 (Excel)", "盆・夏フェス購入関係_原紙.xlsx")
    
    st.subheader("💡 ノウハウ＆アドバイス（※画面上で直接編集可能）")
    st.text_area("編集可能なアドバイス欄", value="""* ラジオ体操最終日: 頑張った子どもたちへアイスクリームを用意してね！
* 夏フェス本番: 17:30集合。18:00〜19:00 / 19:00〜20:00の2交代制。高学年の店番に大人の見守り係を配置します。手ふき等をいただいた場合は後日お礼（お返し）を用意し、9月定例会で収支報告をします。""", height=160, key="knowhow_8")

elif selected_month == "9月":
    st.subheader("📌 9月：子ども商店収支報告＆運動会3町合同会議＆町民運動会")
    st.write("夏フェスの決算報告と、町民運動会に向けた打ち合わせ・当日の運営協力を行います。")
    col1, col2 = st.columns([3, 2])
    with col1:
        st.subheader("📝 今月の「やる事」リスト")
        st.checkbox("子ども商店の収支報告書を作成し、9月定例会で報告")
        st.checkbox("寄付（御寄付）をいただいた方へ菓子折りとお礼状を届ける")
        st.checkbox("運動会3町合同会議への出席（大原会館／大原町・本町・中町）")
        st.checkbox("体協から提供された運動会案内の配布・周知＆参加メンバー選考")
        st.checkbox("役員・手伝い用のお弁当発注（中学生や保護者の人数もカウントして14個程度）")
        st.checkbox("青崎学区 町民運動会 当日の運営協力")
    with col2:
        st.subheader("📥 必要な資料・原紙")
        show_download("競技種目・メンバー選考 (Excel)", "競技種目_原紙.xlsx")
    
    st.subheader("💡 ノウハウ＆アドバイス（※画面上で直接編集可能）")
    st.text_area("編集可能なアドバイス欄", value="""* 御寄付のお礼: 御寄付をいただいた方には、必ず後日「菓子折り」と「お礼状」をお渡しするのがマナーです！
* 運動会のお弁当: 当日手伝ってくれる中学生や保護者の人数もカウントして、お弁当やお茶をしっかり発注しておきましょう。""", height=140, key="knowhow_9")

elif selected_month == "10月":
    st.subheader("📌 10月：秋祭り準備・お菓子手配・クリスマス会企画開始")
    st.write("秋祭りの準備と、クリスマス会の企画を開始します。")
    col1, col2 = st.columns([3, 2])
    with col1:
        st.subheader("📝 今月の「やる事」リスト")
        st.checkbox("自治会からの秋祭り案内・法被指示（紙）の受け取り")
        st.checkbox("秋祭り用お菓子の手配（250円×60袋＝15,000円。10日前までに注文！）")
        st.checkbox("子ども用ハッピの準備・のぼり設置（5箇所）")
        st.checkbox("大原神社秋祭りのサポート")
        st.checkbox("11月映画鑑賞会用プロジェクター手配（大原会館山岡さんへ依頼）")
        st.checkbox("クリスマス会の企画・予算案作成の開始")
    with col2:
        st.subheader("📥 必要な資料・原紙")
        show_download("クリスマス会 予算案 (Excel)", "クリスマス会予算案_原紙.xlsx")
        show_download("クリスマス会 案内 (Excel)", "クリスマス会案内_原紙.xlsx")
    
    st.subheader("💡 ノウハウ＆アドバイス（※画面上で直接編集可能）")
    st.text_area("編集可能なアドバイス欄", value="""* お菓子手配: 秋祭りのお菓子は60袋用意。10日前までに注文を完了させます。
* 余ったお菓子: もし秋祭りでお菓子が余ったら（例: 20袋残った等）、11月の映画鑑賞会で子どもたちに配ると喜ばれます！
* 映画鑑賞会: 会館のプロジェクターを使うため、早めに管理人の山岡さんへ予約をお願いしておきます。""", height=160, key="knowhow_10")

elif selected_month == "11月":
    st.subheader("📌 11月：映画鑑賞会・クリスマス会詳細決定＆三世代交流ふれあい広場")
    st.write("映画鑑賞会の実施、三世代交流のお手伝い、クリスマス会の詳細を決定させていきます。")
    col1, col2 = st.columns([3, 2])
    with col1:
        st.subheader("📝 今月の「やる事」リスト")
        st.checkbox("映画鑑賞会のお知らせをLINEで配信・実施（あまりのお菓子配布）")
        st.checkbox("三世代交流ふれあい広場の参加・お手伝い（各町より役員2名参加）")
        st.checkbox("クリスマス会の工作（サンタ帽子等）の試作・ゲーム選定")
        st.checkbox("クリスマス会のケーキ（ピープル等）・プレゼント手配")
        st.checkbox("クリスマス会の予算案・案内文の完成")
    with col2:
        st.subheader("📥 必要な資料・原紙")
        show_download("クリスマス会 予算案 (Excel)", "クリスマス会予算案_原紙.xlsx")
        show_download("クリスマス会 案内 (Excel)", "クリスマス会案内_原紙.xlsx")
    
    st.subheader("💡 ノウハウ＆アドバイス（※画面上で直接編集可能）")
    st.text_area("編集可能なアドバイス欄", value="""* 三世代交流: 育成から連絡が来ます。お昼のお弁当（うどん等）は育成側で用意してくれます。
* クリスマス会準備: 子どもたちにサンタ帽子作りなどの工作をさせる場合は、11月中に役員で試作しておきます。ケーキも早めに予約しましょう。""", height=140, key="knowhow_11")

elif selected_month == "12月":
    st.subheader("📌 12月：大掃除・クリスマス会本番・来期役員募集")
    st.write("いよいよクリスマス会本番です！終了後に予算の実績を入力します。")
    col1, col2 = st.columns([3, 2])
    with col1:
        st.subheader("📝 今月の「やる事」リスト")
        st.checkbox("クリスマス会本番の実施＆1年間お疲れ様会")
        st.checkbox("クリスマス会予算案ファイルに「実績」を入力する")
        st.checkbox("大原会館の大掃除参加（自治会からの案内待ち／合同大掃除）")
        st.checkbox("広島ジュニアマリンバアンサンブルコンサート引率")
        st.checkbox("来期役員募集案内の作成（テンプレート活用）と全世帯配布")
    with col2:
        st.subheader("📥 必要な資料・原紙")
        show_download("クリスマス会 予算案・実績 (Excel)", "クリスマス会予算案_原紙.xlsx")
        show_download("クリスマス会 案内 (Excel)", "クリスマス会案内_原紙.xlsx")
    
    st.subheader("💡 ノウハウ＆アドバイス（※画面上で直接編集可能）")
    st.text_area("編集可能なアドバイス欄", value="""* クリスマス会当日の流れ: ボードゲーム ➔ サンタ帽子工作 ➔ ケーキデコレーション＆実食 ➔ サンタ＆トナカイからプレゼント登場！ ➔ 片付け。""", height=120, key="knowhow_12")

elif selected_month == "1月":
    st.subheader("📌 1月：来期役員募集・6年生を送る会準備・冬季スポーツ連絡")
    st.write("来期役員募集チラシの投函、6年生を送る会の準備を開始します。")
    col1, col2 = st.columns([3, 2])
    with col1:
        st.subheader("📝 今月の「やる事」リスト")
        st.checkbox("来期役員募集案内を全世帯のポストへ投函（ポストイン）")
        st.checkbox("育成からの冬季スポーツに関する連絡を待ち、LINEへ展開")
        st.checkbox("6年生へ卒業記念品（3,000円分QUOカード等）の希望ヒアリング")
        st.checkbox("「6年生を送る会」のケーキ・お好み焼き等の予約・手配")
    with col2:
        st.subheader("📥 必要な資料・原紙")
        st.info("📁 今月はパソコンで開く決まった資料（様式）はありません。")
    
    st.subheader("💡 ノウハウ＆アドバイス（※画面上で直接編集可能）")
    st.text_area("編集可能なアドバイス欄", value="""* 6年生の記念品: 予算は3,000円程度（例: QUOカードなど）。1月中に6年生本人に希望を聞いて手配しておきます。
* 送る会の飲食: ケーキや軽食（お好み焼き等）の手配を進めます。""", height=140, key="knowhow_1")

elif selected_month == "2月":
    st.subheader("📌 2月：スポーツフェスタ本番・引継ぎ＆会計監査・6年生を送る会準備")
    st.write("スポーツフェスタ本番、防災訓練、新旧役員引き継ぎ、総会案内配布を進めます。")
    col1, col2 = st.columns([3, 2])
    with col1:
        st.subheader("📝 今月の「やる事」リスト")
        st.checkbox("冬季スポーツフェスタ本番（楠那小 / 南区スポーツセンター）")
        st.checkbox("青崎学区防災訓練フェアへの協力")
        st.checkbox("子ども会総会開催のお知らせ（委任状付き）の作成・配布")
        st.checkbox("「6年生を送る会」プログラム作成（挨拶➔ルール➔食事➔ビンゴ等）")
        st.checkbox("1年間の振り返り「ご意見アンケート」の実施・回収")
        st.checkbox("新旧役員引き継ぎ＆会計監査の実施")
    with col2:
        st.subheader("📥 必要な資料・原紙")
        show_download("6年生さんを送る会 案+実績 (Excel)", "6年生さんを送る会案+実績_原紙.xlsx")
    
    st.subheader("💡 ノウハウ＆アドバイス（※画面上で直接編集可能）")
    st.text_area("編集可能なアドバイス欄", value="""* 総会案内: 欠席者向けに委任状を添えて事前に配布・回収します。
* アンケート: 行事の良かった点・改善点をアンケートで回収し、次年度へ引き継ぎます。
* 引き継ぎ: この「らくらくナビ」自体が引き継ぎマニュアルです！""", height=160, key="knowhow_2")

elif selected_month == "3月":
    st.subheader("📌 3月：大原町子供会総会・6年生さんを送る会・会計監査")
    st.write("「6年生さんを送る会」の実施と、大原町子供会総会を開催し、1年間の締めくくりと新年度役員へ引き継ぎを行います。")
    col1, col2 = st.columns([3, 2])
    with col1:
        st.subheader("📝 今月の「やる事」リスト")
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
        show_download("年間行事計画・報告 (Excel)", "令和○○年度_行事計画+報告_原紙.xlsx")
        show_download("決算報告書_案+実 (Excel)", "決算報告書_案+実_原紙.xlsx")
        show_download("子ども会会則 (Word)", "2.向洋大原子ども会会則 令和〇〇.docx")
        show_download("子供会総会 議案書・事業報告書 (Word)", "1.総会資料令和○○年度‗次第‗原紙.docx")
        show_download("6年生さんを送る会 案+実績 (Excel)", "6年生さんを送る会案+実績_原紙.xlsx")
    
    st.subheader("💡 ノウハウ＆アドバイス（※画面上で直接編集可能）")
    st.text_area("編集可能なアドバイス欄", value="""* 会計監査: 会則上、監査は前会長に依頼するのがスムーズです。
* 紙の印刷物: 子ども会役員間はLINEで共有するため印刷不要ですが、LINEを使っていない町内会役員さん（年配の方等）向けには紙で印刷して準備しておきます。
* 総会資料のコツ: 各イベントが終わるたびに行事報告書へ日付をこまめにメモしておくと、3月の総会資料作成が劇的にラクになります！""", height=160, key="knowhow_3")

st.divider()

# --- 共通フッター ---
st.subheader("✍️ 今月の記録を残す（引き継ぎ用）")
st.text_area(f"{selected_month}の引き継ぎメモ", height=120)
st.number_input(f"{selected_month}の支出合計（円）", min_value=0, step=1)

st.divider()

# --- ファイル提出機能 ---
st.subheader("📤 完成した資料を提出する（自動保管）")
st.info("役員さんが作成したファイルを選択して、「提出する」ボタンを押してください。自動的に『今年度』のフォルダへ『【〇月提出】ファイル名』の形式で整理され保管されます！")

uploaded_file = st.file_uploader("ここにファイルをドラッグ＆ドロップ、または選択してください", key="uploader")

if uploaded_file is not None:
    if st.button("✨ このファイルを提出する ✨", use_container_width=True):
        with st.spinner("安全なGoogleドライブに自動仕分け中...⏳"):
            try:
                # ★★★ ここにWebアプリのURLを貼り付けてください ★★★
                GAS_URL = "https://script.google.com/macros/s/AKfycbzhE4SNVf5CbCf0GzMc5BkU9QuiQntbUi_nwjts-xsekXK10aR0BEywRNkx_bJcaHs/exec"

                file_bytes = uploaded_file.read()
                file_b64 = base64.b64encode(file_bytes).decode('utf-8')
                
                # ----------------------------------------------------
                # ★ 年度計算ロジック（1〜3月は「前の年」を「今年度」とする）
                # ----------------------------------------------------
                JST = datetime.timezone(datetime.timedelta(hours=+9), 'JST')
                now = datetime.datetime.now(JST)
                
                nendo = now.year
                if now.month <= 3:
                    nendo -= 1
                
                # 送信するデータのまとめ
                payload = {
                    "fileName": uploaded_file.name,
                    "mimeType": uploaded_file.type or "application/octet-stream",
                    "fileData": file_b64,
                    "year": str(nendo),         # 1〜3月は前年の数字が送られる
                    "month": selected_month     # サイドバーで選んでいる月
                }

                res = requests.post(GAS_URL, data=json.dumps(payload), headers={"Content-Type": "application/json"})
                result_data = res.json()

                if result_data.get("result") == "success":
                    st.success(f"🎉 提出完了！「【{selected_month}提出】{uploaded_file.name}」を「{nendo}年」フォルダに自動保管しました！")
                else:
                    st.error(f"❌ 提出に失敗しました: {result_data.get('error')}")
            except Exception as e:
                st.error(f"❌ エラーが発生しました。（詳細: {e}）")
