import os
import re
import streamlit as st

st.set_page_config(
    page_title="子ども会 らくらくナビ",
    page_icon="🎈",
    layout="wide"
)

# --------------------------------------------------
# デザイン設定（柔らかい色合いとオレンジのタイトル帯）
# --------------------------------------------------
st.markdown("""
<style>
/* 全体の背景色を柔らかいクリーム色に */
.stApp {
    background-color: #FFFDF0;
}
/* タイトルのオレンジ帯 */
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
/* 見出しの色を少し柔らかく */
h1, h2, h3 {
    color: #333333;
}
</style>
<div class="custom-title">🎈 子ども会 らくらくナビ 🎈</div>
""", unsafe_allow_html=True)


# --------------------------------------------------
# 超・強力ファイル自動検索機能
# --------------------------------------------------
def find_actual_file(target_filename):
    if os.path.exists(target_filename):
        return target_filename
    
    # 記号（通常 _, 特殊 ‗, スペース等）を完全に無視する処理
    def clean_name(s):
        name, ext = os.path.splitext(s)
        # 表記揺れを統一（入会/入学、〇/○）
        name = name.replace('入会', '入学').replace('〇', '').replace('○', '')
        # 漢字・ひらがな・カタカナ・英数字「以外」の記号をすべて強制消去
        name = re.sub(r'[^a-zA-Z0-9ぁ-んァ-ヶ一-龥]', '', name)
        return name + ext.lower()

    target_clean = clean_name(target_filename)
    
    for f in os.listdir('.'):
        if not os.path.isfile(f): continue
        f_clean = clean_name(f)
        # 記号を抜いた文字の並びが一致すれば正解
        if target_clean in f_clean or f_clean in target_clean:
            return f
            
    # 【最終安全装置】迎える会専用のキーワード検索
    if "迎える会" in target_filename:
        for f in os.listdir('.'):
            if "迎える会" in f: return f
            
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
        st.error(f"❌ ファイルが見つかりません。({filename})")

# サイドバー設定（4月始まり）
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
        st.caption("ボタンを押すとパソコンのエクセル・ワードが直接開きます")
        # 変更点：「お祝い会」を「迎える会」に修正
        show_download("迎える会案内 (Excel)", "迎える会_案内_原紙.xlsx")
        show_download("入会届 育成版 (Excel)", "入会届○○年度_育成版_新1年・2～6年用_原紙.xlsx")
        show_download("入会届 育成休止版 (Excel)", "入会届○○年度_育成休止版_新1年・2～6年用_原紙.xlsx")
        show_download("年間行事計画・報告 (Excel)", "令和○○年度_行事計画+報告_原紙.xlsx")
        show_download("新役員名簿 (Excel)", "○○年度_子ども会名簿_原紙.xlsx")

elif selected_month == "5月":
    st.subheader("📌 5月：新1年生を迎える会・リーダー研修①・球技大会準備")
    st.write("歓迎会、リーダー研修、夏季球技大会の準備、夏フェスの最初の企画話し合いを行います。")
    st.write("【迎える会の記念品について】 迎える会の案内と新加入者を記載した名簿を基に、以下の記念品を用意します。 ・新1年生：名入れ鉛筆 ・1年生以外の新加入者：500円分のクオカード\n\n【夏季球技大会について】 参加については体協からのお願いが来てからとなるため、連絡を待ちます。")
    st.info("💡 記念品代（名入れ鉛筆、クオカード等）の予算確保を忘れずに！")
    
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
        st.caption("ボタンを押すとパソコンのエクセル・ワードが直接開きます")
        # 変更点：「お祝い会」を「迎える会」に修正
        show_download("迎える会案内 (Excel)", "迎える会_案内_原紙.xlsx")
        show_download("迎える会 課題打合せ内容 (Excel)", "ようこそ会_課題打合せ内容_①_原紙.xlsx")
        show_download("子ども会名簿 (Excel)", "○○年度_子ども会名簿_原紙.xlsx")

elif selected_month == "6月":
    st.subheader("📌 6月：夏フェス企画＆予算案・チケット作成・球技大会連絡")
    st.write("夏フェスの企画詳細とチケット作成を進めます。年間予算案の提出も行います。")
    st.write("【夏季球技大会について】 体協または育成から連絡が来るので、それを子ども会のLINEグループに展開（転送）するだけで基本OKです。要請があった場合のみサポートに入ります。\n\n【夏フェスの準備】 ・店舗、景品、人員の選考表を基に詳細を詰めます。 ・夏フェス用の50円チケットは印刷後、役員で手分けしてハサミで切って作成します！")
    
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
        st.caption("ボタンを押すとパソコンのエクセル・ワードが直接開きます")
        show_download("店舗・景品・人員選考表 (Excel)", "店舗・飲食・人員選考表_原紙.xlsx")
        show_download("決算報告書(予算案) (Excel)", "決算報告書_案+実_原紙.xlsx")
        show_download("夏フェス50円チケット (Excel)", "50円チケット.xlsx")

elif selected_month == "7月":
    st.subheader("📌 7月：夏フェス準備・盆踊り打合せ・ラジオ体操")
    st.write("夏フェスや盆踊りの打合せ、ラジオ体操（1週間のみ）の準備を行います。")
    st.write("【夏フェス説明会について】 主催・進行は「夏フェス運営委員」が行うため、子ども会役員はそのサポートや連絡事項の確認を中心に行います。\n\n【ラジオ体操について】 開催期間は「1週間のみ」です。スタンプカードの作成と、ポスターへの記入・掲示を行います。")
    
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
        st.caption("ボタンを押すとパソコンのエクセル・ワードが直接開きます")
        show_download("盆踊り打合せ (Excel)", "盆踊り打合せ_原紙.xlsx")
        show_download("ラジオ体操 スタンプカード (Excel)", "ラジオ体操_スタンプカード_2026.xlsx")
        show_download("ラジオ体操 開催ポスター (Excel)", "ラジオ体操_原紙_20230718.xlsx")

elif selected_month == "8月":
    st.subheader("📌 8月：盆行事＆夏フェス本番")
    st.write("1ヶ月を通した夏フェス看板準備、盆行事の準備・本番・片付け、夏フェス本番・片付けを行います。")
    st.write("【AIを活用した看板作成】 看板製作のデザインや文言は、ゼロから考えず「Gemini」や「ChatGPT」に作ってもらいましょう！劇的にラクになります。右のリンクボタンからすぐに開けます。\n\n【資料提供とシフトについて】 ・夏フェスの準備、運営、片付けなどの資料は「夏フェス運営委員」から提供されるため、自作しなくてOKです。 ・当番シフトの確認等は、引き続き「盆踊り打合せ」のファイルを使用します。")
    
    col1, col2 = st.columns([3, 2])
    with col1:
        st.subheader("📝 今月の「やる事」リスト")
        st.checkbox("夏フェスの看板作成（GeminiやChatGPTに作成させる！）")
        st.checkbox("盆行事の準備・当番シフト確認・本番・片付け")
        st.checkbox("夏フェス当日の準備・運営・片付け（資料は運営委員から提供）")
        st.checkbox("盆行事・夏フェスの会計精算（購入関係ファイルに入力）")
    with col2:
        st.subheader("📥 必要な資料・原紙")
        st.caption("ボタンを押すとパソコンのエクセル・ワードが直接開きます")
        show_download("盆踊り打合せ・シフト (Excel)", "盆踊り打合せ_原紙.xlsx")
        show_download("盆・夏フェス購入関係・会計 (Excel)", "盆・夏フェス購入関係_原紙.xlsx")
        st.link_button("🌐 Geminiを開く (Google)", "https://gemini.google.com/", use_container_width=True)
        st.link_button("🌐 ChatGPTを開く (OpenAI)", "https://chat.openai.com/", use_container_width=True)

elif selected_month == "9月":
    st.subheader("📌 9月：運動会3町合同会議＆町民運動会")
    st.write("町民運動会に向けた打ち合わせと当日の運営協力を行います。")
    st.write("【町民運動会について】 運動会の参加案内は「体協」から提供されるため、子ども会で作成する必要はありません。提供された案内をもとに、参加メンバーの選考を行います。")
    
    col1, col2 = st.columns([3, 2])
    with col1:
        st.subheader("📝 今月の「やる事」リスト")
        st.checkbox("運動会3町合同会議への出席（大原会館）")
        st.checkbox("体協から提供された運動会案内の配布・周知")
        st.checkbox("参加メンバーの選考（競技種目ファイルを使用）")
        st.checkbox("青崎学区 町民運動会 当日の運営協力")
    with col2:
        st.subheader("📥 必要な資料・原紙")
        st.caption("ボタンを押すとパソコンのエクセル・ワードが直接開きます")
        show_download("競技種目・メンバー選考 (Excel)", "競技種目_原紙.xlsx")

elif selected_month == "10月":
    st.subheader("📌 10月：秋祭り準備・お菓子手配・クリスマス会企画開始")
    st.write("秋祭りの準備と、クリスマス会の企画を開始します。")
    st.write("【リーダー研修について】 本来は育成から連絡が来ますが、現在は「休会中」となっています。\n\n【秋祭りについて】 ・秋祭りの準備資料や法被の案内などは、自治会側から「紙」で来ます。パソコンのデータ（様式）はないため、紙が来たらそれに従って準備を進めればOKです。 ・お祭りに参加する子どもたちに向けて、お菓子（300～500円程度）を用意します。\n\n【クリスマス会の準備】 ・12月に向けて、10月からパソコンで予算案や案内文の作成をスタートします。")
    st.info("💡 秋祭りに参加する子どもたちへのお菓子代（1人300～500円程度）の予算を確保しておきましょう！")
    
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
        st.caption("ボタンを押すとパソコンのエクセル・ワードが直接開きます")
        show_download("クリスマス会 予算案 (Excel)", "クリスマス会予算案_原紙.xlsx")
        show_download("クリスマス会 案内 (Excel)", "クリスマス会案内_原紙.xlsx")

elif selected_month == "11月":
    st.subheader("📌 11月：クリスマス会詳細決定＆三世代交流ふれあい広場")
    st.write("10月に引き続き、クリスマス会の打ち合わせを行い、詳細を決定させていきます。")
    st.write("【三世代交流ふれあい広場について】 体協から依頼と資料が来るため、その内容に従って参加・協力します。子ども会側で新たに作成する資料・様式はありません。")
    st.info("💡 クリスマス会の景品や備品の買い出しに向けて、予算の最終確認を！")
    
    col1, col2 = st.columns([3, 2])
    with col1:
        st.subheader("📝 今月の「やる事」リスト")
        st.checkbox("クリスマス会の打ち合わせ・詳細の決定")
        st.checkbox("クリスマス会の予算案・案内文の完成（10月と同じファイルを使用）")
        st.checkbox("体協からの三世代交流ふれあい広場の資料確認")
        st.checkbox("三世代交流ふれあい広場の参加・お手伝い（青崎小）")
    with col2:
        st.subheader("📥 必要な資料・原紙")
        st.caption("ボタンを押すとパソコンのエクセル・ワードが直接開きます")
        show_download("クリスマス会 予算案 (Excel)", "クリスマス会予算案_原紙.xlsx")
        show_download("クリスマス会 案内 (Excel)", "クリスマス会案内_原紙.xlsx")

elif selected_month == "12月":
    st.subheader("📌 12月：大掃除・クリスマス会本番・来期役員募集")
    st.write("いよいよクリスマス会本番です！終了後に予算の実績を入力します。")
    st.write("【大原会館の大掃除について】 大掃除の案内は「自治会」から来ますので、案内が来てから参加準備をします。\n\n【来期役員募集について】 案内文は画面下部の「コピー用テンプレート」を使って作成・案内してください。")
    st.info("💡 クリスマス会が終わったら、忘れないうちに予算案のエクセルに「実績額」を入力しましょう！")
    
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
        st.caption("ボタンを押すとパソコンのエクセル・ワードが直接開きます")
        show_download("クリスマス会 予算案・実績 (Excel)", "クリスマス会予算案_原紙.xlsx")
        show_download("クリスマス会 案内 (Excel)", "クリスマス会案内_原紙.xlsx")
        
    st.divider()
    st.subheader("📋 【コピー用】来期役員募集テンプレート")
    st.info("右上のコピーボタン（重なった四角のアイコン）を押して、LINEやWordに貼り付けて自由にお使いください！")
    template_text = """令和〇年度 大原町子ども会 新役員募集のお知らせ

保護者の皆様
日頃は、子ども会の活動にご理解とご協力をいただき、誠にありがとうございます。

さて、いよいよ今年度も残りわずかとなりました。
来年度に向けて、大原町子ども会の新役員を募集いたします！
子どもたちの笑顔と地域交流のために、できる範囲で一緒に楽しく活動しませんか？

「役員って難しそう…」と思う方もいらっしゃるかもしれませんが、今年度の役員がしっかり引き継ぎを行い、前例のデータ（この「らくらくナビ」など！）もバッチリ揃っていますのでご安心ください！

【募集役職】
・会長
・副会長
・会計

【回答締切】
〇月〇日（〇）まで

自薦・他薦は問いません。少しでも興味がある方、質問がある方は、現会長（〇〇）またはLINEグループまでお気軽にご連絡ください。
皆様からの温かいお声がけをお待ちしております！"""
    st.code(template_text, language="text")

elif selected_month == "1月":
    st.subheader("📌 1月：冬季スポーツ連絡・待機")
    st.write("冬季スポーツに関しては「育成」から連絡が来ます。連絡が来たら、子ども会のLINEグループに展開（転送）するだけでOKです！")
    st.write("1月は特に子ども会としての大きな作業・イベントはありません。パソコンを開く必要もない月です。ゆっくりお過ごしください。")
    st.info("💡 1月は特に作業がありません！役員の皆様もゆっくりお正月をお過ごしください。")
    
    col1, col2 = st.columns([3, 2])
    with col1:
        st.subheader("📝 今月の「やる事」リスト")
        st.checkbox("育成からの冬季スポーツに関する連絡を待つ")
        st.checkbox("連絡が来たらLINEグループに展開（転送）する")
    with col2:
        st.subheader("📥 必要な資料・原紙")
        st.info("📁 今月はパソコンで開く決まった資料（様式）はありません。")

elif selected_month == "2月":
    st.subheader("📌 2月：スポーツフェスタ本番・引継ぎ＆会計監査・総会準備")
    st.write("スポーツフェスタ本番、防災訓練、新旧役員引き継ぎ、総会準備を進める最も重要な月です。")
    
    col1, col2 = st.columns([3, 2])
    with col1:
        st.subheader("📝 今月の「やる事」リスト")
        st.checkbox("冬季スポーツフェスタ本番（楠那小 / 南区スポーツセンター）")
        st.checkbox("青崎学区防災訓練フェアへの協力")
        st.checkbox("新旧役員引き継ぎ＆会計監査の実施")
        st.checkbox("年度末の総会資料・決算報告書の作成準備")
    with col2:
        st.subheader("📥 必要な資料・原紙")
        st.caption("ボタンを押すとパソコンのエクセル・ワードが直接開きます")
        show_download("子ども会 決算報告書フォーマット (Excel)", "決算報告書_案+実_原紙.xlsx")
        show_download("新旧役員引き継ぎチェックリスト (Word)", "新旧役員引き継ぎチェックリスト.docx")

elif selected_month == "3月":
    st.subheader("📌 3月：大原町子供会総会")
    st.write("大原町子供会総会を開催し、1年間の締めくくりと新年度役員へ引き継ぎを行います。")
    
    col1, col2 = st.columns([3, 2])
    with col1:
        st.subheader("📝 今月の「やる事」リスト")
        st.checkbox("役員評議員会への出席")
        st.checkbox("大原町子供会総会の開催（大原会館）")
        st.checkbox("新会長・新会計への完全に引き継ぎ完了")
    with col2:
        st.subheader("📥 必要な資料・原紙")
        st.caption("ボタンを押すとパソコンのエクセル・ワードが直接開きます")
        show_download("子供会総会 議案書・事業報告書 (Word)", "1.総会資料令和○○年度_次第_原紙.docx")

st.divider()

# --- 共通フッター（引き継ぎメモ＆支出合計） ---
st.subheader("✍️ 今月の記録を残す（引き継ぎ用）")
st.text_area(f"{selected_month}の引き継ぎメモ", height=120)
st.number_input(f"{selected_month}の支出合計（円）", min_value=0, step=1)
