import os
import re
import streamlit as st

st.set_page_config(
    page_title="子ども会 らくらくナビ",
    page_icon="🎈",
    layout="wide"
)

st.title("🎈 子ども会 らくらくナビ 🎈")

# 超強力ファイル自動検索機能（記号・全角半角・空白の表記ズレを全自動補正）
def find_actual_file(target_filename):
    if os.path.exists(target_filename):
        return target_filename
    
    def normalize(s):
        # 記号や空白を除外して比較用文字列を作成
        return re.sub(r'[^\w\u4e00-\u9fff\u3040-\u309f\u30a0-\u30ff]', '', s).lower()

    target_norm = normalize(target_filename)
    target_ext = os.path.splitext(target_filename)[1].lower()

    for f in os.listdir('.'):
        f_ext = os.path.splitext(f)[1].lower()
        if f_ext == target_ext:
            f_norm = normalize(f)
            if target_norm in f_norm or f_norm in target_norm:
                return f
    return None

# ダウンロードボタン表示関数
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
        st.error(f"❌ ファイル「{filename}」が見つかりません。")

# サイドバー設定（4月始まりの順番に修正）
month_list = ["4月", "5月", "6月", "7月", "8月", "9月", "10月", "11月", "12月", "1月", "2月", "3月"]
selected_month = st.sidebar.selectbox(
    "月を選択してください", 
    month_list, 
    index=0  # デフォルトを4月に設定
)

st.header(f"✨ {selected_month}の予定と必要な準備")

# --- 月別コンテンツ ---

if selected_month == "4月":
    st.subheader("📌 4月：新年度スタート・学区総会・新一年生案内")
    st.write("新年度のスタートです。学区総会への出席、自治会役員への書類提出、新1年生への加入案内を行います。")
    col1, col2 = st.columns([3, 2])
    with col1:
        st.subheader("📝 今月の「やる事」リスト")
        st.checkbox("自治会から新1年生の名簿（紙）を受け取る")
        st.checkbox("新1年生宅へ加入案内・入会届の配布")
        st.checkbox("自治会役員へ年間行事計画と新役員名簿を提出")
        st.checkbox("青崎学区子ども会総会への出席")
        st.checkbox("新1年生を迎える会（お祝い会）の準備開始")
    with col2:
        st.subheader("📥 必要な資料・原紙")
        show_download("お祝い会・迎える会 案内", "お祝い会‗案内‗原紙.xlsx")
        show_download("入会届 (育成版)", "入学届○○年度‗育成版‗新1年・2～6年用‗原紙.xlsx")
        show_download("入会届 (育成休止版)", "入学届○○年度‗育成休止版‗新1年・2～6年用‗原紙.xlsx")
        show_download("年間行事計画・報告", "令和○○年度_行事計画+報告_原紙.xlsx")
        show_download("新役員名簿", "○○年度_子ども会名簿_原紙.xlsx")
        show_download("総会案内・委任状", "総会案内○○令和年度委任状‗原紙.xlsx")
        show_download("総会資料次第 (Word)", "1.総会資料令和○○年度‗次第‗原紙.docx")

elif selected_month == "5月":
    st.subheader("📌 5月：新一年生ようこそ会・育成打合せ")
    st.write("新1年生を迎えるイベントの開催と、今後の課題や行事についての打合せを行います。")
    col1, col2 = st.columns([3, 2])
    with col1:
        st.subheader("📝 今月の「やる事」リスト")
        st.checkbox("ようこそ会（新一年生歓迎会）の最終打合せ・開催")
        st.checkbox("参加者の確認とプレゼント・備品の準備")
        st.checkbox("次月以降のラジオ体操や夏行事の初期相談")
    with col2:
        st.subheader("📥 必要な資料・原紙")
        show_download("ようこそ会 課題打合せ内容", "ようこそ会_課題打合せ内容_①_原紙.xlsx")
        show_download("お祝い会・迎える会 案内", "お祝い会‗案内‗原紙.xlsx")
        show_download("50円チケット (イベント用)", "50円チケット.xlsx")

elif selected_month in ["6月", "7月"]:
    st.subheader(f"📌 {selected_month}：夏休み準備・ラジオ体操・夏フェス打合せ")
    st.write("夏休みに向けたラジオ体操の準備、盆踊り・夏フェスに向けた企画を進めます。")
    col1, col2 = st.columns([3, 2])
    with col1:
        st.subheader("📝 今月の「やる事」リスト")
        st.checkbox("ラジオ体操の開催日程・場所の決定と周知")
        st.checkbox("ラジオ体操スタンプカードの印刷・配布準備")
        st.checkbox("盆踊り・夏フェスの出店（店舗・飲食・人員）選考")
        st.checkbox("助成金提案書の作成（必要な場合）")
    with col2:
        st.subheader("📥 必要な資料・原紙")
        show_download("ラジオ体操 スタンプカード", "ラジオ体操_スタンプカード_2026.xlsx")
        show_download("ラジオ体操 実施案内原紙", "ラジオ体操_原紙_20230718.xlsx")
        show_download("店舗・飲食・人員選考表", "店舗・飲食・人員選考表_原紙.xlsx")
        show_download("健全会助成金提案書", "健全会助成金提案書 (1).xlsx")

elif selected_month == "8月":
    st.subheader("📌 8月：盆行事＆夏フェス本番")
    st.write("夏フェス看板準備、盆行事の準備・当番シフト・本番・片付けを行います。")
    col1, col2 = st.columns([3, 2])
    with col1:
        st.subheader("📝 今月の「やる事」リスト")
        st.checkbox("夏フェス看板作成（GeminiやChatGPTを活用）")
        st.checkbox("盆行事の準備・当番シフト確認・本番・片付け")
        st.checkbox("競技種目や店舗運営の準備")
        st.checkbox("盆行事・夏フェスの会計購入精算")
    with col2:
        st.subheader("📥 必要な資料・原紙")
        show_download("盆踊り打合せ・シフト", "盆踊り打合せ_原紙.xlsx")
        show_download("盆・夏フェス購入関係・会計", "盆・夏フェス購入関係_原紙.xlsx")
        show_download("競技種目 原紙", "競技種目_原紙.xlsx")
        show_download("50円チケット", "50円チケット.xlsx")
        st.link_button("🌐 Geminiを開く (看板作成用)", "https://gemini.google.com/", use_container_width=True)

elif selected_month in ["9月", "10月", "11月"]:
    st.subheader(f"📌 {selected_month}：秋行事・決算中間確認・冬行事準備")
    st.write("上半期の報告や町内への業績見通し報告、冬のクリスマス会に向けた準備を始めます。")
    col1, col2 = st.columns([3, 2])
    with col1:
        st.subheader("📝 今月の「やる事」リスト")
        st.checkbox("町内役員へ上半期の業績見通し報告")
        st.checkbox("秋の地域イベント参加・お手伝い")
        st.checkbox("クリスマス会の企画・予算案作成の開始")
    with col2:
        st.subheader("📥 必要な資料・原紙")
        show_download("業績見通し (町内役員配布用)", "3.R○○年度業績見通し（町内役員へ配布）‗原紙.xls")
        show_download("クリスマス会予算案", "クリスマス会予算案‗原紙.xlsx")
        show_download("クリスマス会案内", "クリスマス会案内_原紙.xlsx")

elif selected_month == "12月":
    st.subheader("📌 12月：クリスマス会本番")
    st.write("子どもたちが楽しみにしているクリスマス会の案内、予算精算、当日の運営を行います。")
    col1, col2 = st.columns([3, 2])
    with col1:
        st.subheader("📝 今月の「やる事」リスト")
        st.checkbox("クリスマス会案内の配布と集計")
        st.checkbox("景品・お菓子・備品の買い出しと予算照合")
        st.checkbox("クリスマス会当日の運営・精算")
    with col2:
        st.subheader("📥 必要な資料・原紙")
        show_download("クリスマス会案内", "クリスマス会案内_原紙.xlsx")
        show_download("クリスマス会予算案", "クリスマス会予算案‗原紙.xlsx")
        show_download("50円チケット", "50円チケット.xlsx")

else:  # 1月, 2月, 3月
    st.subheader(f"📌 {selected_month}：年度末決算・次年度引き継ぎ準備")
    st.write("1年の締めくくりです。決算報告書の作成、会則の確認、次期役員への引き継ぎ準備を進めます。")
    col1, col2 = st.columns([3, 2])
    with col1:
        st.subheader("📝 今月の「やる事」リスト")
        st.checkbox("決算報告書（案・実績）の作成")
        st.checkbox("子ども会会則の確認・改定案（必要な場合）")
        st.checkbox("新役員へのファイル・資料の引き継ぎ準備")
    with col2:
        st.subheader("📥 必要な資料・原紙")
        show_download("決算報告書 (案+実)", "決算報告書_案+実_原紙.xlsx")
        show_download("子ども会会則 (Word)", "2.向洋大原子ども会会則 〇〇令和.docx")
        show_download("子ども会名簿原紙", "○○年度_子ども会名簿_原紙.xlsx")

st.divider()

# --- 全資料アーカイブ（全21ファイルを常時ダウンロード可能） ---
with st.expander("📁 アップロード済み 全資料保管庫（クリックで開く）"):
    st.caption("どの月からでも、保管されている全21個のファイルをダウンロードできます。")
    arc_col1, arc_col2 = st.columns(2)
    
    with arc_col1:
        show_download("1. 総会資料次第 (Word)", "1.総会資料令和○○年度‗次第‗原紙.docx")
        show_download("2. 子ども会会則 (Word)", "2.向洋大原子ども会会則 〇〇令和.docx")
        show_download("3. 業績見通し (Excel)", "3.R○○年度業績見通し（町内役員へ配布）‗原紙.xls")
        show_download("4. 50円チケット (Excel)", "50円チケット.xlsx")
        show_download("5. 子ども会名簿 (Excel)", "○○年度_子ども会名簿_原紙.xlsx")
        show_download("6. クリスマス会予算案 (Excel)", "クリスマス会予算案‗原紙.xlsx")
        show_download("7. クリスマス会案内 (Excel)", "クリスマス会案内_原紙.xlsx")
        show_download("8. ラジオ体操スタンプカード (Excel)", "ラジオ体操_スタンプカード_2026.xlsx")
        show_download("9. ラジオ体操案内原紙 (Excel)", "ラジオ体操_原紙_20230718.xlsx")
        show_download("10. 行事計画+報告 (Excel)", "令和○○年度_行事計画+報告_原紙.xlsx")
        show_download("11. 入学届(育成休止版) (Excel)", "入学届○○年度‗育成休止版‗新1年・2～6年用‗原紙.xlsx")

    with arc_col2:
        show_download("12. 入学届(育成版) (Excel)", "入学届○○年度‗育成版‗新1年・2～6年用‗原紙.xlsx")
        show_download("13. 健全会助成金提案書 (Excel)", "健全会助成金提案書 (1).xlsx")
        show_download("14. 店舗・飲食・人員選考表 (Excel)", "店舗・飲食・人員選考表_原紙.xlsx")
        show_download("15. 決算報告書 (Excel)", "決算報告書_案+実_原紙.xlsx")
        show_download("16. 盆・夏フェス購入関係 (Excel)", "盆・夏フェス購入関係_原紙.xlsx")
        show_download("17. 盆踊り打合せ (Excel)", "盆踊り打合せ_原紙.xlsx")
        show_download("18. 競技種目 (Excel)", "競技種目_原紙.xlsx")
        show_download("19. 総会案内委任状 (Excel)", "総会案内○○令和年度委任状‗原紙.xlsx")
        show_download("20. ようこそ会課題打合せ (Excel)", "ようこそ会_課題打合せ内容_①_原紙.xlsx")
        show_download("21. お祝い会案内 (Excel)", "お祝い会‗案内‗原紙.xlsx")

st.divider()
st.subheader("✍️ 今月の記録を残す（引き継ぎ用）")
st.text_area("来年度の役員へ残したいメモや反省点", height=120)
