import os
import re
import streamlit as st
from google.oauth2 import service_account
from googleapiclient.discovery import build
from googleapiclient.http import MediaIoBaseUpload

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
    st.write("【加入案内の手順】 4月の早い時期に、自治会から「自治会に入っている新1年生」の紙の名簿をもらえます。その名簿をもとに、各ご家庭へ加入案内（迎える会の案内や入会届）を配布しに行きます。")
    col1, col2 = st.columns([3, 2])
    with col1:
        st.subheader("📝 今月の「やる事」リスト")
        st.checkbox("自治会から新1年生の名簿（紙）を受け取る")
        st.checkbox("新1年生宅へ加入案内・入会届の配布（名簿をもとに訪問）")
        st.checkbox("自治会役員へ年間行事計画と新役員名簿を提出")
        st.checkbox("青崎学区子供会総会への出席（新旧役員）")
        st.checkbox("新1年生を迎える会の準備開始")
    with col2:
        st.subheader("📥 必要な資料・原紙")
        show_download("迎える会案内 (Excel)", "迎える会_案内_原紙.xlsx")
        show_download("入会届 育成版 (Excel)", "入会届○○年度_育成版_新1年・2～6年用_原紙.xlsx")
        show_download("入会届 育成休止版 (Excel)", "入会届○○年度_育成休止版_新1年・2～6年用_原紙.xlsx")
        show_download("年間行事計画・報告 (Excel)", "令和○○年度_行事計画+報告_原紙.xlsx")
        show_download("新役員名簿 (Excel)", "○○年度_子ども会名簿_原紙.xlsx")

elif selected_month == "5月":
    st.subheader("📌 5月：新1年生を迎える会・リーダー研修①・球技大会準備")
    st.write("歓迎会、リーダー研修、夏季球技大会の準備、夏フェスの最初の企画話し合いを行います。")
    col1, col2 = st.columns([3, 2])
    with col1:
        st.subheader("📝 今月の「やる事」リスト")
        st.checkbox("新加入者への記念品手配（名入れ鉛筆・QUOカード）")
        st.checkbox("「新1年生を迎える会」の実施（大原会館/公園）")
        st.checkbox("リーダー研修①の参加者取りまとめ（4・5・6年生）")
        st.checkbox("体協からの夏季球技大会に関する連絡確認")
        st.checkbox("夏フェス企画案の初回話し合い（町内会と合同）")
    with col2:
        st.subheader("📥 必要な資料・原紙")
        show_download("迎える会案内 (Excel)", "迎える会_案内_原紙.xlsx")
        show_download("迎える会 課題打合せ内容 (Excel)", "迎える会_課題打合せ内容_①_原紙.xlsx")
        show_download("子ども会名簿 (Excel)", "○○年度_子ども会名簿_原紙.xlsx")

elif selected_month == "6月":
    st.subheader("📌 6月：夏フェス企画＆予算案・チケット作成・球技大会連絡")
    st.write("夏フェスの企画詳細とチケット作成を進めます。年間予算案の提出も行います。")
    col1, col2 = st.columns([3, 2])
    with col1:
        st.subheader("📝 今月の「やる事」リスト")
        st.checkbox("夏フェスの店舗・景品・人員選考の検討")
        st.checkbox("夏フェス用50円チケットの印刷・手分けして切る作業（ハサミ持参！）")
        st.checkbox("年間予算案（決算報告書の案）の提出")
        st.checkbox("体協・育成からの球技大会の連絡をLINEグループへ展開")
        st.checkbox("（要請があれば）球技大会のサポート")
    with col2:
        st.subheader("📥 必要な資料・原紙")
        show_download("店舗・景品・人員選考表 (Excel)", "店舗・景品・人員選考表_原紙.xlsx")
        show_download("決算報告書(予算案) (Excel)", "決算報告書_案+実_原紙.xlsx")
        show_download("夏フェス50円チケット (Excel)", "50円チケット.xlsx")

elif selected_month == "7月":
    st.subheader("📌 7月：夏フェス準備・盆踊り打合せ・ラジオ体操")
    st.write("夏フェスや盆踊りの打合せ、ラジオ体操（1週間のみ）の準備を行います。")
    col1, col2 = st.columns([3, 2])
    with col1:
        st.subheader("📝 今月の「やる事」リスト")
        st.checkbox("夏フェス説明会への参加・サポート（主催は運営委員）")
        st.checkbox("盆踊り打合せへの参加（内容・役割分担の確認）")
        st.checkbox("ラジオ体操のスタンプカード作成")
        st.checkbox("ラジオ体操の開催ポスター作成・掲示")
        st.checkbox("ラジオ体操の実施（1週間限定！）")
    with col2:
        st.subheader("📥 必要な資料・原紙")
        show_download("盆踊り打合せ (Excel)", "盆踊り打合せ_原紙.xlsx")
        show_download("ラジオ体操 スタンプカード (Excel)", "ラジオ体操_スタンプカード_2026.xlsx")
        show_download("ラジオ体操 開催ポスター (Excel)", "ラジオ体操_原紙_20230718.xlsx")

elif selected_month == "8月":
    st.subheader("📌 8月：盆行事＆夏フェス本番")
    st.write("1ヶ月を通した夏フェス看板準備、盆行事の準備・本番・片付け、夏フェス本番・片付けを行います。")
    col1, col2 = st.columns([3, 2])
    with col1:
        st.subheader("📝 今月の「やる事」リスト")
        st.checkbox("夏フェスの看板作成（GeminiやChatGPTに作成させる！）")
        st.checkbox("盆行事の準備・当番シフト確認・本番・片付け")
        st.checkbox("夏フェス当日の準備・運営・片付け（資料は運営委員から提供）")
        st.checkbox("盆行事・夏フェスの会計精算（購入関係ファイルに入力）")
    with col2:
        st.subheader("📥 必要な資料・原紙")
        show_download("盆踊り打合せ・シフト (Excel)", "盆踊り打合せ_原紙.xlsx")
        show_download("盆・夏フェス購入関係・会計 (Excel)", "盆・夏フェス購入関係_原紙.xlsx")

elif selected_month == "9月":
    st.subheader("📌 9月：運動会3町合同会議＆町民運動会")
    st.write("町民運動会に向けた打ち合わせと当日の運営協力を行います。")
    col1, col2 = st.columns([3, 2])
    with col1:
        st.subheader("📝 今月の「やる事」リスト")
        st.checkbox("運動会3町合同会議への出席（大原会館）")
        st.checkbox("体協から提供された運動会案内の配布・周知")
        st.checkbox("参加メンバーの選考（競技種目ファイルを使用）")
        st.checkbox("青崎学区 町民運動会 当日の運営協力")
    with col2:
        st.subheader("📥 必要な資料・原紙")
        show_download("競技種目・メンバー選考 (Excel)", "競技種目_原紙.xlsx")

elif selected_month == "10月":
    st.subheader("📌 10月：秋祭り準備・お菓子手配・クリスマス会企画開始")
    st.write("秋祭りの準備と、クリスマス会の企画を開始します。")
    col1, col2 = st.columns([3, 2])
    with col1:
        st.subheader("📝 今月の「やる事」リスト")
        st.checkbox("自治会からの秋祭り案内・法被指示（紙）の受け取り")
        st.checkbox("秋祭りの準備・法被などの対応（紙の指示に従う）")
        st.checkbox("参加する子ども向けのお菓子手配（300～500円程度）")
        st.checkbox("大原神社秋祭りのサポート")
        st.checkbox("クリスマス会の企画・予算案作成の開始")
    with col2:
        st.subheader("📥 必要な資料・原紙")
        show_download("クリスマス会 予算案 (Excel)", "クリスマス会予算案_原紙.xlsx")
        show_download("クリスマス会 案内 (Excel)", "クリスマス会案内_原紙.xlsx")

elif selected_month == "11月":
    st.subheader("📌 11月：クリスマス会詳細決定＆三世代交流ふれあい広場")
    st.write("10月に引き続き、クリスマス会の打ち合わせを行い、詳細を決定させていきます。")
    col1, col2 = st.columns([3, 2])
    with col1:
        st.subheader("📝 今月の「やる事」リスト")
        st.checkbox("クリスマス会の打ち合わせ・詳細の決定")
        st.checkbox("クリスマス会の予算案・案内文の完成（10月と同じファイルを使用）")
        st.checkbox("体協からの三世代交流ふれあい広場の資料確認")
        st.checkbox("三世代交流ふれあい広場の参加・お手伝い（青崎小）")
    with col2:
        st.subheader("📥 必要な資料・原紙")
        show_download("クリスマス会 予算案 (Excel)", "クリスマス会予算案_原紙.xlsx")
        show_download("クリスマス会 案内 (Excel)", "クリスマス会案内_原紙.xlsx")

elif selected_month == "12月":
    st.subheader("📌 12月：大掃除・クリスマス会本番・来期役員募集")
    st.write("いよいよクリスマス会本番です！終了後に予算の実績を入力します。")
    col1, col2 = st.columns([3, 2])
    with col1:
        st.subheader("📝 今月の「やる事」リスト")
        st.checkbox("クリスマス会本番の実施＆1年間お疲れ様会")
        st.checkbox("クリスマス会予算案ファイルに「実績」を入力する")
        st.checkbox("大原会館の大掃除参加（自治会からの案内待ち）")
        st.checkbox("広島ジュニアマリンバアンサンブルコンサート引率")
        st.checkbox("来期役員募集案内の作成（テンプレート活用）と配布")
    with col2:
        st.subheader("📥 必要な資料・原紙")
        show_download("クリスマス会 予算案・実績 (Excel)", "クリスマス会予算案_原紙.xlsx")
        show_download("クリスマス会 案内 (Excel)", "クリスマス会案内_原紙.xlsx")

elif selected_month == "1月":
    st.subheader("📌 1月：冬季スポーツ連絡・待機")
    st.write("1月は特に子ども会としての大きな作業・イベントはありません。ゆっくりお過ごしください。")
    col1, col2 = st.columns([3, 2])
    with col1:
        st.subheader("📝 今月の「やる事」リスト")
        st.checkbox("育成からの冬季スポーツに関する連絡を待つ")
        st.checkbox("連絡が来たらLINEグループに展開（転送）する")
    with col2:
        st.subheader("📥 必要な資料・原紙")
        st.info("📁 今月はパソコンで開く決まった資料（様式）はありません。")

elif selected_month == "2月":
    st.subheader("📌 2月：スポーツフェスタ本番・引継ぎ＆会計監査・6年生を送る会準備")
    st.write("スポーツフェスタ本番、防災訓練、新旧役員引き継ぎを進めつつ、3月の「6年生さんを送る会」の準備をスタートする重要な月です。")
    col1, col2 = st.columns([3, 2])
    with col1:
        st.subheader("📝 今月の「やる事」リスト")
        st.checkbox("冬季スポーツフェスタ本番（楠那小 / 南区スポーツセンター）")
        st.checkbox("青崎学区防災訓練フェアへの協力")
        st.checkbox("新旧役員引き継ぎ＆会計監査の実施")
        st.checkbox("6年生さんを送る会の企画・準備スタート（案内作成・記念品手配など）")
        st.checkbox("年度末の総会資料・決算報告書の作成準備")
    with col2:
        st.subheader("📥 必要な資料・原紙")
        show_download("6年生さんを送る会 案+実績 (Excel)", "6年生さんを送る会案+実績_原紙.xlsx")
        st.info("💡 【引き継ぎについて】\nこの「らくらくナビ」自体が引き継ぎマニュアルです！")

elif selected_month == "3月":
    st.subheader("📌 3月：大原町子供会総会・6年生さんを送る会")
    st.write("「6年生さんを送る会」の実施と、大原町子供会総会を開催し、1年間の締めくくりと新年度役員へ引き継ぎを行います。")
    col1, col2 = st.columns([3, 2])
    with col1:
        st.subheader("📝 今月の「やる事」リスト")
        st.checkbox("6年生さんを送る会の実施")
        st.checkbox("役員評議員会への出席")
        st.checkbox("大原町子供会総会の開催（大原会館）")
        st.checkbox("新会長・新会計への完全に引き継ぎ完了")
    with col2:
        st.subheader("📥 必要な資料・原紙")
        show_download("年間行事計画・報告 (Excel)", "令和○○年度_行事計画+報告_原紙.xlsx")
        show_download("決算報告書_案+実 (Excel)", "決算報告書_案+実_原紙.xlsx")
        show_download("子ども会会則 (Word)", "2.向洋大原子ども会会則 令和〇〇.docx")
        show_download("子供会総会 議案書・事業報告書 (Word)", "1.総会資料令和○○年度‗次第‗原紙.docx")
        show_download("6年生さんを送る会 案+実績 (Excel)", "6年生さんを送る会案+実績_原紙.xlsx")

st.divider()

# --- 共通フッター ---
st.subheader("✍️ 今月の記録を残す（引き継ぎ用）")
st.text_area(f"{selected_month}の引き継ぎメモ", height=120)
st.number_input(f"{selected_month}の支出合計（円）", min_value=0, step=1)

st.divider()

# --- ファイル提出機能 ---
st.subheader("📤 完成した資料を提出する（自動保管）")
st.info("役員さんが作成したファイルを選択して、「提出する」ボタンを押してください。Googleドライブに自動保管されます！")

uploaded_file = st.file_uploader("ここにファイルをドラッグ＆ドロップ、または選択してください", key="uploader")

if uploaded_file is not None:
    if st.button("✨ このファイルを提出する ✨", use_container_width=True):
        with st.spinner("Googleドライブに転送中です...⏳"):
            try:
                # 辞書データの取得と安全なキー指定
                creds_dict = dict(st.secrets["google_credentials"])

                credentials = service_account.Credentials.from_service_account_info(
                    creds_dict,
                    scopes=["https://www.googleapis.com/auth/drive"]
                )

                service = build('drive', 'v3', credentials=credentials)

                FOLDER_ID = "1l9SzYOf0p4W08Wmv7x8f1kpSArjMAjmx"

                file_metadata = {
                    'name': uploaded_file.name,
                    'parents': [FOLDER_ID]
                }
                media = MediaIoBaseUpload(uploaded_file, mimetype=uploaded_file.type, resumable=True)

                service.files().create(body=file_metadata, media_body=media, fields='id').execute()

                st.success(f"🎉 提出完了！「{uploaded_file.name}」を共有フォルダに自動保管しました！")
            except Exception as e:
                st.error(f"❌ エラーが発生しました。設定を確認してください。（詳細: {e}）")
