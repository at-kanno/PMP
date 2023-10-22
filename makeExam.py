from constant import db_path, examTitle1, examTitle2, examTitle3, examTitle4, \
     examTitle10, examTitle11, examTitle12, abbreviation
from flask import Flask, session, render_template, request, Blueprint
import sqlite3, os
from users import getStage, setStage, getStatus
from examDB import makeExam2, getQuestionFromCategory, getQuestionFromNum, saveExam, getCorrectList

exam_module = Blueprint("exam", __name__, static_folder='./static')

# 基本概念を選択
@exam_module.route('/makeExam', methods=['POST'])
def makeExam():
    user_id = request.form.get('user_id')
    stage = getStage(user_id)
    #    if(stage != 1 and stage !=2):
    #        return """
    #        <h1>異常を検出しました。<br>
    #        ログインし直してください。</h1>
    #        <p><a href="/">→ログインする</a></p>
    #        """
    if (stage == 1):
        setStage(user_id, 2)

    if not is_login():
        return """
        <h1>ログインしてください</h1>
        <p><a href="/">→ログインする</a></p>
        """
    if request.method == 'POST':
        category = request.form['category']
        print('category=' + str(category))

        level = 1
        if (category == '01'):
            status = getStatus(user_id)
            return render_template('main-menu.html',
                                   user_id=user_id,
                                   status=status,
                                   )
        elif (category == '60'):
            amount = 18
            title = examTitle10
            examlist, arealist = makeExam2(user_id, amount, int(category), level, 1380, '')
        elif (category == '70'):
            amount = 60
#            title = examTitle11
            title = examTitle11 + '（第１セクション）'
            examlist, arealist = makeExam2(user_id, amount, int(category), level, 13800, '')
        elif (category == '80'):
            amount = 60
#            title = examTitle12
            title = examTitle12 + '（第１セクション）'
            examlist, arealist = makeExam2(user_id, amount, int(category), level, 13800, '')
        elif (category == '10'):
            amount = 10
            title = examTitle1
            examlist, arealist = makeExam2(user_id, amount, int(category), level, 780, '')
        elif (category == '20'):
            amount = 10
            title = examTitle2
            examlist, arealist = makeExam2(user_id, amount, int(category), level, 780, '')
        elif (category == '30'):
            amount = 10
            title = examTitle3
            examlist, arealist = makeExam2(user_id, amount, int(category), level, 780, '')
        elif (category == '40'):
            amount = 10
            title = examTitle4
            examlist, arealist = makeExam2(user_id, amount, int(category), level, 780, '')
        elif (category == '81' or category == '82' or category == '83' \
              or category == '84' or category == '85' or category == '86'\
              or category == '87' or category == '88' or category == '89'\
              or category == '90' or category == '91' or category == '92'):
            amount = 10
            examlist, arealist = makeExam2(user_id, amount, int(category), level, 780, '')
        else:
            setStage(user_id, 9)
            return render_template('admin.html', user_id=int(user_id))
        try:
            exam_id = saveExam(user_id, category, level, amount, examlist, arealist)
            # for debug
            correctlist = getCorrectList(examlist)
            return render_template('startExam.html',
                                   user_id=user_id,
                                   exam_id=exam_id,
                                   total=amount,
                                   examlist=examlist,
                                   arealist=arealist,
                                   title=title,
                                   correctlist=correctlist,
                                   )
        except:
            return "Error...."
    else:
        return 'Fail'


# 基本概念を選択
@exam_module.route('/makeExam3', methods=['POST'])
def makeExam3():

    user_id = request.form.get('user_id')
    command = request.form.get('command')

    if command == 'exit':
        status = getStatus(user_id)
        return render_template('main-menu.html',
                               user_id=user_id,
                               status=status,
                               )

    category = request.form['category']

    if command == 'check' or command == 'timeout':
        crct = int(request.form.get('crct'))
        num = request.form.get('num')
        ans = int(request.form.get('answer'))
        cid = request.form.get('cid')
        permutation = request.form.get('permutation')
        if ans == 9:
            correct = '選択がなされませんでした。'
        elif ans - 1 == crct:
            correct = '正解です。'
        else:
            correct = '誤りです。'

        q, a1, a2, a3, a4, cid = getQuestionFromNum(num, permutation)

        conn = sqlite3.connect(db_path)
        c = conn.cursor()
        sql = "SELECT  COMMENT FROM COMMENTS_TABLE" \
              + " WHERE COMMENT_ID = " + str(cid) + ";"
        if c.execute(sql):
            print("Success!")
        else:
            print("Error!")
        items = c.fetchall()
        comment = items[0][0]

        area = request.form.get('area')
        return render_template('analysis2.html',
                               user_id=user_id,
                               q=q,
                               a1=a1,
                               a2=a2,
                               a3=a3,
                               a4=a4,
                               correct=correct,
                               comment=comment,
                               answer="ABCD"[crct],
                               category=category,
                               area=area,
                               )
    else:
        stage = getStage(user_id)
        if (stage == 1):
            setStage(user_id, 2)

        if not is_login():
            return """
            <h1>ログインしてください</h1>
            <p><a href="/">→ログインする</a></p>
            """

        #        category = request.form['category']
        print('category=' + str(category))

# １問１答の処理（91:FND,92:CDS,93:DSV,94:HVIT,95:DPI）
        if (category == '81'):
            q, a1, a2, a3, a4, crct, cid, num, permutation = getQuestionFromCategory(11, 11)
        elif (category == '82'):
            q, a1, a2, a3, a4, crct, cid, num, permutation = getQuestionFromCategory(12, 12)
        elif (category == '83'):
            q, a1, a2, a3, a4, crct, cid, num, permutation = getQuestionFromCategory(13, 13)
        elif (category == '84'):
            q, a1, a2, a3, a4, crct, cid, num, permutation = getQuestionFromCategory(14, 14)
        elif (category == '85'):
            q, a1, a2, a3, a4, crct, cid, num, permutation = getQuestionFromCategory(21, 21)
        elif (category == '86'):
            q, a1, a2, a3, a4, crct, cid, num, permutation = getQuestionFromCategory(22, 22)
        elif (category == '87'):
            q, a1, a2, a3, a4, crct, cid, num, permutation = getQuestionFromCategory(23, 23)
        elif (category == '88'):
            q, a1, a2, a3, a4, crct, cid, num, permutation = getQuestionFromCategory(24, 24)
        elif (category == '89'):
            q, a1, a2, a3, a4, crct, cid, num, permutation = getQuestionFromCategory(31, 31)
        elif (category == '90'):
            q, a1, a2, a3, a4, crct, cid, num, permutation = getQuestionFromCategory(32, 32)
        elif (category == '91'):
            q, a1, a2, a3, a4, crct, cid, num, permutation = getQuestionFromCategory(33, 33)
        elif (category == '92'):
            q, a1, a2, a3, a4, crct, cid, num, permutation = getQuestionFromCategory(34, 34)
# 第2メニュー
        elif (category == '5'):
            setStage(user_id, 1)
            status = getStatus(user_id)
            return render_template('main-menu1.html',
                                   user_id=user_id,
                                   status=status,
                                   )
        elif (category == '6'):
            setStage(user_id, 1)
            status = getStatus(user_id)
            return render_template('main-menu2.html',
                                   user_id=user_id,
                                   status=status,
                                   )
        elif (category == '7'):
            setStage(user_id, 1)
            status = getStatus(user_id)
            return render_template('main-menu3.html',
                                   user_id=user_id,
                                   status=status,
                                   )
        elif (category == '8'):
            setStage(user_id, 1)
            status = getStatus(user_id)
            return render_template('main-menu4.html',
                                   user_id=user_id,
                                   status=status,
                                   )
# メインメニューに戻る
        else:
            setStage(user_id, 1)
            status = getStatus(user_id)
            return render_template('main-menu.html',
                                   user_id=user_id,
                                   status=status,
                                   )

    n = int(category) - 81
    return render_template('exercise2.html',
                           user_id=user_id,
                           question=q,
                           selection1=a1,
                           selection2=a2,
                           selection3=a3,
                           selection4=a4,
                           timeMin=0,
                           timeSec=0,
                           selectStr="",
                           crct=crct,
                           cid=cid,
                           num=num,
                           permutation=permutation,
                           category=category,
                           area=abbreviation[n] # 領域（エリア）名：constant.pyで定義
                           )

# ログインしているか調べる
@exam_module.route('/is_login')
def is_login():
    if 'login' in session:
        return "on"
    else:
        return "off"
    return 'login' in session