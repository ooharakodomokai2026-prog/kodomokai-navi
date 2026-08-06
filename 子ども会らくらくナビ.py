import os
import streamlit as st

# 画面表示の設定
st.set_page_config(
    page_title="子ども会 らくらくナビ",
    page_icon="🎈",
    layout="wide"
)

st.title("🎈 子ども会 らくらくナビ 🎈")

# サイドバー（月選択）
selected_month = st.sidebar.selectbox("月を選択してください", [f"{i}月" for i in range(1, 13)], index=3)  # デフォルトで4月を選択

st.header(f"✨ {selected_month}の予定と必要な準備")

# ダウンロードボタン生成関数（ファイル名の完全一致チェック機能付き）
def show_download_button(label, filename):
    if os.path.exists(filename):
        ext = os.path.splitext(filename)[1].lower()
        if ext == ".xlsx":
            mime = "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
        elif ext == ".xls":
            mime = "application/vnd.ms-excel"
        elif ext == ".docx":
            mime = "application/vnd.openxmlformats-officedocument.wordprocessingml.document"
        else:
            mime = "application/octet-stream"

        with open(filename, "rb") as f:
            st.download_button(
                label=f"📄 {label}",
                data=f,
                file_name=filename,
                mime=mime,
                use_container_width=True
            )
    else:
        st.error(f"❌ ファイル「{filename}」がGitHub上に見つかりません。")

# 4月のコンテンツ
if selected_month == "4月":
    st.subheader("📌 4月：新年度スタート・学区総会・新一年生案内")
    st.write("青崎学区子ども会総会への出席、自治会役員への年間行事計画・新役員名簿の提出に加え、新1年生への加入案内を行います。")

    col1, col2 = st.columns([3, 2])

    with col1:
        st.subheader("📝 今月の「やる事」リスト")
        st.checkbox("自治会から新1年生の名簿（紙）を受け取る")
        st.checkbox("新1年生宅へ加入案内・入会届の配布（名簿をもとに訪問）")
        st.checkbox("自治会役員へ年間行事計画と新役員名簿を提出")
        st.checkbox("青崎学区子ども会総会への出席（新旧役員）")
        st.checkbox("新1年生を迎える会の準備開始")

    with col2:
        st.subheader("📥 必要な資料・原紙")
        st.caption("ボタンを押すとファイルがスマホやPCにダウンロードされます")

        # GitHub上の実際のファイル名を指定
        show_download_button("お祝い会・迎える会 案内 (Excel)", "お祝い会‗案内‗原紙.xlsx")
        show_download_button("入会届 育成版 (Excel)", "入学届○○年度‗育成版‗新1年・2～6年用‗原紙.xlsx")
        show_download_button("入会届 育成休止版 (Excel)", "入学届○○年度‗育成休止版‗新1年・2～6年用‗原紙.xlsx")
        show_download_button("年間行事計画・報告 (Excel)", "令和○○年度_行事計画+報告_原紙.xlsx")
        show_download_button("新役員名簿 (Excel)", "○○年度_子ども会名簿_原紙.xlsx")
        show_download_button("総会案内・委任状 (Excel)", "総会案内○○令和年度委任状‗原紙.xlsx")
        show_download_button("総会資料次第 (Word)", "1.総会資料令和○○年度‗次第‗原紙.docx")

# 8月のコンテンツ
elif selected_month == "8月":
    st.subheader("📌 8月：盆行事＆夏フェス本番")
    st.write("夏フェス看板準備、盆行事の準備・本番・片付けを行います。")

    col1, col2 = st.columns([3, 2])

    with col1:
        st.subheader("📝 今月の「やる事」リスト")
        st.checkbox("夏フェスの看板作成（GeminiやChatGPTに作成させる！）")
        st.checkbox("盆行事の準備・当番シフト確認・本番・片付け")
        st.checkbox("夏フェス当日の準備・運営・片付け")
        st.checkbox("盆行事・夏フェスの会計精算")

    with col2:
        st.subheader("📥 必要な資料・原紙")
        show_download_button("盆踊り打合せ_原紙 (Excel)", "盆踊り打合せ_原紙.xlsx")
        show_download_button("盆・夏フェス購入関係_原紙 (Excel)", "盆・夏フェス購入関係_原紙.xlsx")
        
        st.link_button("🌐 Geminiを開く", "https://gemini.google.com/", use_container_width=True)
        st.link_button("🌐 ChatGPTを開く", "https://chat.openai.com/", use_container_width=True)

# その他の月（一覧表示機能付き）
else:
    st.info(f"{selected_month}の個別ガイドは準備中です。")
    st.subheader("📁 保管中の原紙一覧（全月共通）")
    
    show_download_button("子ども会会則 (Word)", "2.向洋大原子ども会会則 〇〇令和.docx")
    show_download_button("ラジオ体操 スタンプカード (Excel)", "ラジオ体操_スタンプカード_2026.xlsx")
    show_download_button("クリスマス会 案内 (Excel)", "クリスマス会案内_原紙.xlsx")
    show_download_button("決算報告書 案+実 (Excel)", "決算報告書_案+実_原紙.xlsx")

st.divider()
st.subheader("✍️ 今月の記録を残す（引き継ぎ用）")
st.text_area("来年度の役員へ残したいメモや反省点", height=120)
