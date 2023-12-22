from constant import db_path, PassScore1, PassScore2, categoryCode, practice, \
     NumOfArea, areaname, return1, return2, return3, return4, prefec
from flask import Flask, session, render_template, request, jsonify
#from flask_login import LoginManager, UserMixin, login_user, logout_user
import logging
import sqlite3, os, sys
import datetime
#import requests
import re
from datetime import timedelta
from users import check_login, getStage, setStage, getUserList, makePassword, \
    deleteUser, getUserInfo, password_verify, getLoginName, \
    getLoginPassword, getStatus, rankUp, rankDown, getMailadress, checkPeriod, user_module, setPassword
from examDB import getQuestion, getQuestions, Question, \
    makeExam2, saveExam, getCorrectList, stringToButton, getExamlist, \
    getQuestionFromCategory, getQuestionFromNum
from resultDB import putResult, getResult, makeComments, getComment, \
    getUserResultList, getUserResultList1, getUserResultList2, getStartTime
from mail import sendMail
from test import setGrade
from registration import regist_module
from makeExam import exam_module
from exercise import exec_module
from result import result_module
from sql import database_module
from maintenance import maintenance_module

app = Flask(__name__, static_folder='./static')
app.secret_key = '9KStWezD'  # セッション情報を暗号化するための鍵
# 日本語を使えるように
app.config['JSON_AS_ASCII'] = False
books = [{'name': 'EffectivePython', 'price': 3315}, {'name': 'Expert Python Programming', 'price': 3960}]

app.register_blueprint(regist_module)
app.register_blueprint(user_module)
app.register_blueprint(exam_module)
app.register_blueprint(exec_module)
app.register_blueprint(result_module)
app.register_blueprint(maintenance_module)
app.register_blueprint(database_module)

# セッション管理
#login_manager = LoginManager()
#login_manager.init_app(app)

#class User(UserMixin):
#    def __init__(self, uid):
#        self.id = uid

#@login_manager.user_loader
#def load_user(uid):
#    return User(uid)

#@app.before_request
#def before_request():
    # リクエストのたびにセッションの寿命を更新する
#    session.permanent = True
#    app.permanent_session_lifetime = timedelta(minutes=15)
#    session.modified = True
# ここまでがセッション管理

LOGFILE_NAME = "DEBUG.log"
app.logger.setLevel(logging.DEBUG)
log_handler = logging.FileHandler(LOGFILE_NAME)
log_handler.setLevel(logging.DEBUG)
app.logger.addHandler(log_handler)

# ブラウザのメイン画面
@app.route('/')
def index():
    return render_template('login.html',
                           )

# ログアウト処理
@app.route('/logout', methods=['POST'])
def logout():
    user_id = int(request.form['user_id'])
    #    user_id = request.form.get('user_id')
    setStage(user_id, 0)
#    logout_user()  # ログアウト
#    session.pop('login', None)
    return render_template(
        'login.html',
        )

# ユーザー認証
@app.route('/login', methods=['POST'])
def login():
    xid = request.form.get('id')
    pw = request.form.get('pw')
    if xid == '':
        return '<h3>失敗:IDが空です。</h3>'
    # パスワードを照合
    id = xid.lower()
    user_id = check_login(id, pw)
    if user_id == False:
        return '<h3>パスワードが一致しません。</h3>'
    else:
        result = checkPeriod(user_id)
        if result == 99:
            return '<h3>まだ、利用期間が始まっていません。</h3>'
        elif result == 101:
            return '<h3>既に、利用期間が過ぎています。</h3>'
        # セッション管理をFlaskに任せる
#        user = load_user(id)
#        login_user(user)
        session['login'] = id
        setStage(user_id, 1)
        status = getStatus(user_id)
        return render_template('main-menu.html',
                               user_id=user_id,
                               status=status,
                               )



# APIにアクセスがあったとき
@app.route('/api')
def api():
    if not is_login():
        return """
        <h1>ログインしてください</h1>
        <p><a href="/">→ログインする</a></p>
        """

    # パラメータを取得
    q = request.args.get("q", "")

    print('q:' + str(q))

    # データベースから値を取得
    conn = sqlite3.connect(db_path)
    c = conn.cursor()
    c.execute(
        'SELECT Q,A1,A2,A3,A4 FROM knowledge_base WHERE NUMBER=?',
        [q])
    items = c.fetchall()
    conn.close()

    # 結果を入手
    res = []
    for i, r in enumerate(items):
        quest, ans1, ans2, ans3, ans4 = (r[0], r[1], r[2], r[3], r[4])

    return render_template('execExam.html',
                           question=quest,
                           selection1=ans1,
                           selection2=ans2,
                           selection3=ans3,
                           selection4=ans4)


@app.route('/admin', methods=['GET', 'POST'])
def admin():
    command = request.form.get('command')
    user_id = int(request.form.get('user_id'))
    id = request.form.get('id')

    if command != '10' and command != '20' and command != '30' and command != '30':
        id = request.form.get('id')
        flag = 'command' + str(id)
        command = request.form.get(flag)
        if command == 'True':
            deleteUser(id)
        command = '10'

    if command == '10':
        # ページ番号を得る

        user_list = [0 for i in range(100)]
        user_list = getUserList()

        return render_template('list.html',
                               user_id=user_id,
                               user_list=user_list,
                               command=command,
                               )

        s = '<div>'
        for i, r in enumerate(user_list):
            s += '<div class="item" style="display:inline-flex">'
            s += '[' + str(r[0]) + ']'
            s += '' + r[1] + ' : '
            s += '<table><td style="display:inline-flex">'
            s += '<form action="display" method="POST" >'
            s += '<input type="hidden" name = "user_id" value = "' + str(user_id) + '" / >'
            s += '<button type="submit" name="id" style="margin:1;" value="'
            s += str(r[0]) + '">表示</button>'
            s += '</form>'
            # アカウント削除
            s += '<form action="delete" method="POST" >'
            s += '<button type="submit" name = "free_button" style="margin:1;" '
            s += 'value = "free_button" onclick="confirmBooking(' + str(r[0]) + ')">削除</button>'
            s += '<input type="hidden" name="user_id" value = ' + str(user_id) + '" / >'
            s += '<input type="hidden" id = "userInput" name = "userInput" / >'
            s += '</form>'
            # パスワード設定
            s += '<form action="setpassword" method="POST" >'
            s += '<input type="hidden" name = "user_id" value = ' + str(user_id) + '" / >'
            s += '<button type="submit" name="id" style="margin:1;" value="'
            s += str(r[0]) + '">パスワード</button>'
            s += '</form>'
            s += '</td></table></div>'
        s += '</div>'

        return '''
            <html><meta charset="utf-8">
            <script>
                function confirmBooking(elem) {
                    if(confirm('Are you sure you want to book this slot?') == true) {
                    //elem = 1;
                        alert("its done: " + elem);
                        document.getElementById("userInput").value = "True";
                        }
                    else {
                        document.getElementById("userInput").value = "False";
                        return 0;
                        }
                }

            function deleteAlert(id) {
                var x = confirm(id + "：削除してもよいですか？");
                var y = 'dflag' + id
                if (x)
                   alert('Yes:' + y);
                else {
                   alert('No:' + y);
                   history.back();
                } 
            }

            </script>
            <meta name="viewport"
               content="width=device-width, initial-scale=1">
            <link rel="stylesheet" href="static/pure-min.css">
            <style> .item { border: 1px solid silver;
                            background-color: #f0f0ff;
                            padding: 1px; margin: 1px; } </style>
            <body><h3 style="text-align:center;">ユーザ・リスト</h3>
            ''' + return1 + user_id + return2 + s + '<br></body>' \
               + return1 + user_id + return2 + '</html>'

    elif command == '20':

        n = 0
        result_list = [0 for i in range(100)]
        result_list, n = getUserResultList(user_id)

        return render_template('history.html',
                               user_id=user_id,
                               result_list=result_list,
                               n=n,
                               )

    elif command == '40':
        user_list = [0 for i in range(100)]
        user_list = getUserList()

        result_list = [0 for i in range(100)]
        result_list = getUserResultList(user_id)


    else:
        return render_template('registration.html',
                               user_id=user_id)
        return 'NO request'


@app.route('/delete', methods=['POST'])
def delete():
    user_id = request.form.get('user_id')
    id = request.form.get('id')
    name = 'userInput' + str(user_id)
    userInput = request.form.get(name)
    if id != 0:
        deleteUser(id)

    limit = 3
    user_list = [0 for i in range(100)]
    user_list = getUserList()

    s = '<div>'
    for i, r in enumerate(user_list):
        s += '<div class="item" style="display:inline-flex">'
        s += '[' + str(r[0]) + ']'
        s += '' + r[1] + ' : '
        s += '<table><td style="display:inline-flex">'
        s += '<form action="display" method="POST" >'
        s += '<input type="hidden" name = "user_id" value = "' + str(user_id) + '" / >'
        s += '<button type="submit" name="id" style="margin:1;" value="'
        s += str(r[0]) + '">表示</button>'
        s += '</form>'
        # アカウント削除
        s += '<form action="delete" method="POST" >'
        s += '<button type="submit" name="delete_id" style="margin:1;" value="'
        s += str(r[0]) + '" onclick="deleteAlert(\'' + str(r[0]) + '\')">削除</button>'
        s += '<input type="hidden" name="user_id" value = ' + str(user_id) + '" / >'
        s += '<input type="hidden" name = "dflag' + str(r[0]) + '" value = "1" / >'
        s += '</form>'
        # パスワード設定
        s += '<form action="setpassword" method="POST" >'
        s += '<input type="hidden" name = "user_id" value = ' + str(user_id) + '" / >'
        s += '<button type="submit" name="id" style="margin:1;" value="'
        s += str(r[0]) + '">パスワード</button>'
        s += '</form>'
        s += '</td></table></div>'
    s += '</div>'

    return '''
            <html><meta charset="utf-8">
            <script>
            function deleteAlert(id) {
                var x = confirm(id + "：削除してもよいですか？");
                var y = 'dflag' + id
                if (x)
                   z = document.getElementsByName(y).value;
                   alert('Yes:' + z);
                else {
                   z = document.getElementsByName(y).value;
                   alert('No:' + z);
                   document.getElementsByName(y).value = 0;
                } 
            }
            </script>
            <meta name="viewport"
               content="width=device-width, initial-scale=1">
            <link rel="stylesheet" href="static/pure-min.css">
            <style> .item { border: 1px solid silver;
                            background-color: #f0f0ff;
                            padding: 1px; margin: 1px; } </style>
            <body><h3 style="text-align:center;">ユーザ・リスト</h3>
            ''' + return1 + user_id + return2 + s + '<br></body>' \
           + return1 + user_id + return2 + '</html>'

@app.route('/display', methods=['POST'])
def display():
    user_info = [0 for i in range(100)]

    user_id = int(request.form.get('user_id'))
    id = request.form.get('id')
    command = request.form.get('command')
    if command == 'delete':
        deleteUser()
    elif command == 'password':
        setPassword()
    elif command == 'rankdown':
        rankDown(id)
        return render_template('success.html',
                               user_id=user_id,
                               message="修了試験［実力確認］を受けられるように設定しました。",
                               )
    elif command == 'rankup':
        rankUp(id, 0, 0)
        user_list = [0 for i in range(100)]
        user_list = getUserList()
        return render_template('success.html',
                               user_id=user_id,
                               message="模擬試験が受けられるように設定しました。",
                               )
    elif command == 'list':
        n = 0
        result_list = [0 for i in range(100)]
        result_list, n = getUserResultList(id)

        s = '<div>'

        return render_template('list2.html',
                               user_id=user_id,
                               result_list=result_list,
                               n=n,
                               )
    elif command == 'status':
        status = getStatus(id)
        if status < 10:
            grade = 'グレード１：基本機能だけ利用できます。'
        elif status < 24:
            grade = 'グレード２：模擬試験が利用できます。'
        elif status < 31:
            grade = 'グレード３：模擬試験と修了試験が利用できます。'
        elif status == 31:
            grade = 'グレード３+：次の修了試験でもう一度70点以上を獲得すると修了です。'
        else:
            grade = 'グレード４：修了しました。'

        result_list1 = [0 for i in range(100)]
        result_list1, n = getUserResultList1(id)
        result_list2 = [0 for i in range(100)]
        result_list2, m = getUserResultList2(id)

        return render_template('status.html',
                               user_id=user_id,
                               grade=grade,
                               result_list1=result_list1,
                               result_list2=result_list2,
                               n=n,
                               m=m,
                               )

    else:
        user_info = getUserInfo(id)

        lastname = user_info[0][0]
        firstname = user_info[0][1]
        lastyomi = user_info[0][2]
        firstyomi = user_info[0][3]
        tel1 = user_info[0][4]
        tel2 = user_info[0][5]
        tel3 = user_info[0][6]
        zip1 = user_info[0][7]
        zip2 = user_info[0][8]
        company = user_info[0][9]
        department = user_info[0][10]
        prefecture = user_info[0][11]
        city = user_info[0][12]
        town = user_info[0][13]
        building = user_info[0][14]
        mail_adr = user_info[0][15]
        status = user_info[0][16]
        beginDate = user_info[0][17]
        endDate = user_info[0][18]
        if beginDate != '0':
            beginDate = beginDate + 'T00:00'
        if endDate != '0':
            endDate = endDate + 'T23:59'

        error_no = 0

        return render_template('display.html',
                               lastname=lastname,
                               firstname=firstname,
                               lastyomi=lastyomi,
                               firstyomi=firstyomi,
                               tel1=tel1,
                               tel2=tel2,
                               tel3=tel3,
                               company=company,
                               department=department,
                               zip1=zip1,
                               zip2=zip2,
                               prefecture=prefecture,
                               prefec=prefec,
                               city=city,
                               town=town,
                               building=building,
                               mail_adr=mail_adr,
                               beginDate=beginDate,
                               endDate=endDate,
                               user_id=user_id,
                               id=id,
                               error_no=error_no,
                               )


# ユーザー認証
@app.route('/sendMsg', methods=['POST'])
def sendMsg():
    user_id = request.form.get('user_id')
    mail_from = request.form.get('mail_from')
    mail_to = request.form.get('mail_to')
    message = request.form.get('massage')

    user_id = 13;

    userInfo = ["", "", ""]
    userInfo = getMailadress(user_id)
    username = str(userInfo[0][0]) + " " + str(userInfo[0][1])
    to_email = str(userInfo[0][2])
    sendMail(username, to_email, "合格です！")

#    result = sendMail(mail_from, mail_to, message)
    result = sendMail("staff@olivenet.co.jp", "kanno@olivenet.co.jp", "合格です！")
    if result:
        return 'Success!'
    else:
        return 'Error!'

# ユーザー認証
@app.route('/setData', methods=['POST'])
def setData():
    user_id = request.form.get('user_id')
    grade = request.form.get('grade')

    if setGrade(grade):
        return 'Success!'
    else:
        return 'Error!'


# if __name__ == '__main__':
#    app.run(host='0.0.0.0', port=80, debug=True)

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')

