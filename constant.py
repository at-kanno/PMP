import os

DIFF_JST_FROM_UTC = 9

# データベースのパスを特定
base_path = os.path.dirname(__file__)
#base_path = os.path.dirname(os.path.abspath(__file__))
DATA_FILE = base_path + '/venv/data/users.json'
db_path = base_path + '/exam.sqlite'
form_path = base_path + '/templates'
FILES_DIR = base_path + '/static'

NumOfArea = 3
NumOfCategory = 12

NumOfCategory1 = 4
NumOfCategory2 = 8
NumOfCategory3 = 12
NumOfCheckArea = 12

examType1 = "人(10問)"
examType2 = "プロセス(10問)"
examType3 = "事業環境(10問)"
examType10 = "全領域(10問)"
examType11 = "模擬試験(180問)"
examType12 = "実力試験(180問)"
examType99 = "その他"

examTitle1 = "人：確認問題"
examTitle2 = "プロセス：確認問題"
examTitle3 = "事業環境：確認問題"
examTitle4 = "全領域：確認問題"
examTitle10 = "確認問題（全領域）"
examTitle11 = "模擬試験"
examTitle12 = "実力試験"

abbreviation = ['チーム作り', '評価・パフォーマンス', '交渉・コンフリクト', '協力・サポート', 'プロセス全体','予測的アプローチ',\
                'アジャイル', 'ハイブリッド', 'コンプライアンス', 'ベネフィットと価値 ','外部ビジネス環境の変化', '組織の変更']

PassScore1 = 70
PassScore2 = 75

# 33だが、多めに設定している
categoryCode = "0123456789:;<=>?@ABCDEFGHIJKLMNOPQRSTUVW" \
               + "XYZ[]^`abcdefghijklmnopqrstuvwxyz"

# 出題カテゴリから問題列を生成する
MaxQuestions = 60

categoryNumber = [11, 12, 13, 14, \
                  21, 22, 23, 24, \
                  31, 32, 33, 34]

PASS1_MASSAGE = "おめでとうございます。修了試験の前半合格です。<br>頑張ってこられた成果が出ました。<br>" \
    + "あと１回修了試験の後半があります。<br>それに合格すると、いよいよ本試験（認定試験）です。<br>" \
    +  "あと少しです。がんばってください。"

PASS2_MASSAGE = "おめでとうございます。合格です。<br>頑張ってこられた成果が出ました。<br>" \
    + "修了試験と提出課題の２つをクリアすることで、PeopleCertの本試験を受験することができます。<br>" \
    + "まだ課題を提出していない場合は、提出をお願いします。<br><br>" \
    + "受験要件を満たしたことがアークで確認できましたら、バウチャー（ITIL本試験受験権利コード)を発行します。<br>" \
    + "試験実施機関のPeopleCert社から連絡がありますので、その内容に従い、都合のよい受験日時を予約登録してください。"

FAIL_MESSAGE = "残念ながら、今回合格ラインに達していませんでした。<br>" \
              + "模擬試験に立ち返り、弱い分野を確認して補強するようにしてください。<br>" \
              + "あとひと頑張りです。"


prefec = ["都道府県",
          "北海道",
          "青森県",
          "岩手県",
          "秋田県",
          "山形県",
          "宮城県",
          "福島県",
          "茨城県",
          "栃木県",
          "群馬県",
          "埼玉県",
          "千葉県",
          "東京都",
          "神奈川県",
          "新潟県",
          "富山県",
          "石川県",
          "福井県",
          "山梨県",
          "長野県",
          "岐阜県",
          "静岡県",
          "愛知県",
          "三重県",
          "滋賀県",
          "京都府",
          "大阪府",
          "兵庫県",
          "奈良県",
          "和歌山県",
          "鳥取県",
          "島根県",
          "岡山県",
          "広島県",
          "山口県",
          "徳島県",
          "香川県",
          "愛媛県",
          "高知県",
          "福岡県",
          "佐賀県",
          "長崎県",
          "熊本県",
          "大分県",
          "宮崎県",
          "鹿児島県",
          "沖縄県", ]


return1 = '<form action="makeExam" method="POST">' + \
          '<input type="hidden" name="user_id" value="'
return2 = '" /><button type="submit" class="btn btn-primary btn-block" name="category" value="99">' + \
          '管理画面へ戻る</button><br></p></form>'

return3 = '<div class="buttonwrap" style="display:inline-flex"><form action="summary" >' + \
          '<input type="hidden" name="user_id" value="'
return4 = '" /><button type="submit" style="margin:10px" name="category" value="99">' + \
          'メインメニューへ戻る</button><br></p></form>'

areaname = [
    ["人", 4, "", "", ""],
    ["プロセス", 4, "", "", ""],
    ["事業環境", 4, "", "", ""],
]
practice = [
    ["チーム作り", "評価・パフォーマンス", "交渉・コンフリクト", "協力・サポート"],
    ["プロセス全体", "予測的アプローチ", "アジャイル", "ハイブリッド"],
    ["コンプライアンス", "プロジェクトのベネフィットと価値", "外部ビジネス環境の変化", "組織の変更"],
]

#LOGIN_URL = 'http://54.163.203.19:5000/'
LOGIN_URL = 'http://54.95.74.230:6000/'
PASS3_MASSAGE = 'おめでとうございます。合格です。\n頑張ってこられた成果が出ました。\n\n' \
    + '修了試験と提出課題の２つをクリアすることで、PeopleCertの本試験を受験することができます。\n' \
    + 'まだ課題を提出していない場合は、提出をお願いします。\n\n' \
    + '受験要件を満たしたことがアークで確認できましたら、バウチャー（ITIL本試験受験権利コード)を発行します。\n\n' \
    + '試験実施機関のPeopleCert社から連絡がありますので、その内容に従い、都合のよい受験日時を予約登録してください。'

NEW_ACCOUNT_MESSAGE1 = '模擬試験システムのアカウントを作成しました。\n\n' \
    + '模擬試験システムには、以下のURLからログインしてください。\n  ' + LOGIN_URL + \
    '\nログイン名は、研修お申込み時に記載のメールアドレスです。\n\n初期パスワードは「'
NEW_ACCOUNT_MESSAGE2 = '」です。\nパスワードの変更は、システムの管理画面から可能です。\n\n' + \
    'ご不明な点がございましたら、遠慮なくご連絡ください。'

END_MESSAGE = '\n\n株式会社アーク\nTEL：03-5577-5311\n代表email: ark@gigamall.ne.jp\n' + \
    '\n本メールにご返信いただいても対応できません。\n上記メールアドレスにご連絡ください。'

# 送受信先
cc_email = "at.kanno@icloud.com"
bcc_email = "atsushi.kanno@nifty.com"
#cc_email = "ark@gigamall.ne.jp"
#bcc_email = "miyauchi.ark@gmail.com,kanno@olivenet.co.jp"
from_email = "PMP Exercise System"

cset = 'utf-8'
servername = "smtp.gmail.com"

#
examMode = 1
Area_Base = 741

