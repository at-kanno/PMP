import math
import constant
from constant import db_path, PassScore1, PassScore2, categoryCode, practice, \
     NumOfArea, areaname, return1, return2, return3, return4, DIFF_JST_FROM_UTC, \
     PASS1_MASSAGE, PASS2_MASSAGE, FAIL_MESSAGE, examTitle11
from constant import db_path, examMode
from flask import Flask, session, render_template, request, Blueprint
from users import getStage, setStage, getStatus, rankUp, rankDown, getMailadress
import sqlite3, os
import datetime
from examDB import getQuestion, getQuestions, Question, getCorrectList, makeExam2, saveExam, getExamTYpe
from resultDB import putResult, setTestData, getTestData, getTestID, getTestResult, getStartTime
from mail import sendMail

exec_module = Blueprint("exercise", __name__, static_folder='./static')

# 問題の出題
@exec_module.route('/exercise')
def exercise():
    return_value = [16]

    command = request.args.get("command", "")
    q_no = request.args.get("q_no", "")
    user_id = request.args.get("user_id", "")
    title = request.args.get("title", "")
    exam_id = request.args.get("exam_id", "")
    total = int(request.args.get("total", ""))
    examlist = request.args.get("examlist", "")
    arealist = request.args.get("arealist", "")
    remainTime = int(request.args.get("remainTime", ""))

# 時間情報の獲得
    h = request.args.get("timeHour", "")
    if h == '':
        timeHour = 0
    else:
        timeHour = int(request.args.get("timeHour", ""))
    m = request.args.get("timeMin", "")
    if m == '':
        timeMin = 0
    else:
        timeMin = int(request.args.get("timeMin", ""))
    s = request.args.get("timeSec", "")
    if s == '':
        timeSec = 0
    else:
        timeSec = int(request.args.get("timeSec", ""))

    stime = request.args.get("stime", "")
    Y = request.args.get("Y", "")

    stage = getStage(user_id)
    if (stage != 2 and stage != 3 and stage != 4 and stage != 13 and stage != 23):
        return render_template('error.html',
                               user_id=user_id,
                               error_message='エラーが発生しました。')
    if (stage == 2):
        setStage(user_id, 3)
    if (stage == 4):
        return render_template('error.html',
                               user_id=user_id,
                               error_message='試験が終了してから演習に戻ることはできません。ログインし直してください。')

    qlist = [0 for QuestionList in range(40)]
    selectStr = ["", "", "", ""]
    marklist = {"     "}
    backward = ""
    forward = ""

    if command == 'start':

        if os.name != 'nt':
            now = datetime.datetime.now() + datetime.timedelta(hours=DIFF_JST_FROM_UTC)
        else:
            now = datetime.datetime.now()

        stime = now.strftime("%H:%M:%S")
        sdate = now.strftime("%Y-%m-%d")
        stime = sdate + " " + stime

        q_no = 1
        q = Question
        q = getQuestion(examlist, q_no)

        backward = "disabled"
        answerlist = ""
        marklist = ""
        timeMin = 0
        timeSec = 0
#        timeMin = 59
#        timeSec = 45
        Y = 0

        for i in range(total):
            answerlist = answerlist + "0"
            marklist = marklist + "0"

        # データベースへ開始時間を格納
        conn = sqlite3.connect(db_path)
        c = conn.cursor()
        sql = 'UPDATE EXAM_TABLE SET START_TIME = "' + stime + '" WHERE EXAM_ID = ' + exam_id + ";"
        c.execute(sql)
        conn.commit()
        conn.close()

        return render_template('exercise.html',
                               user_id=user_id,
                               exam_id=exam_id,
                               total=total,
                               examlist=examlist,
                               arealist=arealist,
                               q_no=q_no,
                               question=q.q,
                               selection1=q.a1,
                               selection2=q.a2,
                               selection3=q.a3,
                               selection4=q.a4,
                               selectStr=selectStr,
                               marklist=marklist,
                               answerlist=answerlist,
                               backward=backward,
                               forward=forward,
                               timeHour=timeHour,
                               timeMin=timeMin,
                               timeSec=timeSec,
                               remainTime=remainTime,
                               title=title,
                               Y=Y,
                               )

    elif command == 'next':
        q_no = (int)(request.args.get("q_no", ""))
        marklist = request.args.get("marklist", "")
        answerlist = request.args.get("answerlist", "")

        q_no += 1
        q = getQuestion(examlist, q_no)

        if (q_no >= total):
            forward = "disabled"

        return render_template('exercise.html',
                               user_id=user_id,
                               exam_id=exam_id,
                               total=total,
                               examlist=examlist,
                               arealist=arealist,
                               q_no=q_no,
                               question=q.q,
                               selection1=q.a1,
                               selection2=q.a2,
                               selection3=q.a3,
                               selection4=q.a4,
                               selectStr=selectStr,
                               marklist=marklist,
                               answerlist=answerlist,
                               backward=backward,
                               forward=forward,
                               timeHour=timeHour,
                               timeMin=timeMin,
                               timeSec=timeSec,
                               remainTime=remainTime,
                               title=title,
                               Y=Y,
                               )

    elif command == 'previous':
        q_no = (int)(request.args.get("q_no", ""))
        marklist = request.args.get("marklist", "")
        answerlist = request.args.get("answerlist", "")

        q_no -= 1
        q = getQuestion(examlist, q_no)

        if (q_no == 1):
            backward = "disabled"

        return render_template('exercise.html',
                               user_id=user_id,
                               exam_id=exam_id,
                               total=total,
                               examlist=examlist,
                               arealist=arealist,
                               q_no=q_no,
                               question=q.q,
                               selection1=q.a1,
                               selection2=q.a2,
                               selection3=q.a3,
                               selection4=q.a4,
                               selectStr=selectStr,
                               marklist=marklist,
                               answerlist=answerlist,
                               backward=backward,
                               forward=forward,
                               timeHour=timeHour,
                               timeMin=timeMin,
                               timeSec=timeSec,
                               remainTime=remainTime,
                               title=title,
                               Y=Y,
                               )

    elif command == 'move':
        q_no = (int)(request.args.get("q_no", ""))
        marklist = request.args.get("marklist", "")
        answerlist = request.args.get("answerlist", "")

        q = getQuestion(examlist, q_no)

        if (q_no == 1):
            backward = "disabled"
        if (q_no == total):
            forward = "disabled"

        return render_template('exercise.html',
                               user_id=user_id,
                               exam_id=exam_id,
                               total=total,
                               examlist=examlist,
                               arealist=arealist,
                               q_no=q_no,
                               question=q.q,
                               selection1=q.a1,
                               selection2=q.a2,
                               selection3=q.a3,
                               selection4=q.a4,
                               selectStr=selectStr,
                               marklist=marklist,
                               answerlist=answerlist,
                               backward=backward,
                               forward=forward,
                               timeHour=timeHour,
                               timeMin=timeMin,
                               timeSec=timeSec,
                               remainTime=remainTime,
                               title=title,
                               Y=Y,
                               )

    elif (command == 'finish') or (command == 'timeout'):
        #   終了

        answerlist = request.args.get("answerlist", "")
        examlist = request.args.get("examlist", "")
        correctlist = getCorrectList(examlist)
        correct = 0
        resultlist = ""
        for i, c in enumerate(answerlist):
            if (c == correctlist[i]):
                correct += 1
                resultlist = resultlist + "1"
            else:
                resultlist = resultlist + "0"

        # デバックのためのコード
        # 正解数を35にする
        # correct = 35

        # データベースへ試験結果を格納
        conn = sqlite3.connect(db_path)
        c = conn.cursor()
        rate = round((correct / total * 100), 1)
        usedTime = int(timeSec) + int(timeMin) * 60 + int(timeHour) * 3600
        usedTime1 = int(usedTime / 3600)
        usedTime2 = int(usedTime / 60)
        usedTime2 = usedTime2 - (usedTime1 * 60)
        usedTime3 = usedTime % 60
        if total == 10:
            total_time = 13 * 60
        elif total == 18:
            total_time = 23 * 60
        else:
            total_time = 230 * 60

        sql = "UPDATE EXAM_TABLE SET ANSWERLIST = \'" + str(answerlist) + "\', RESULTLIST = \'" + str(resultlist) + "\', SCORE = " + str(correct) + ", USED_TIME = " \
              + str(usedTime) + ", TOTAL_TIME = " + str(total_time) + ", RATE = " + str(rate) \
              + " WHERE EXAM_ID = " + exam_id + ";"
        print(sql)
        c.execute(sql)

        sql = "SELECT START_TIME, EXAM_TYPE FROM EXAM_TABLE WHERE EXAM_ID = " + exam_id + ";"
        c.execute(sql)
        items = c.fetchall()
        stime = items[0][0]
        type = items[0][1]
        conn.commit()
        conn.close()

        putResult(user_id, exam_id, total, arealist, answerlist, resultlist, correct, rate, usedTime)

        stage = getStage(user_id)
        test_id = 0
        if(examMode==1 and total==constant.MaxQuestions):
            if stage == 3:
                setStage(user_id, 13)
                stime = getStartTime(exam_id)
                setTestData(user_id, exam_id, exam_id, usedTime, 1, stime)
                test_id = exam_id
                amount = constant.MaxQuestions
                type = getExamTYpe(exam_id)
#                title = examTitle11 + '（第２セクション）'
                title = type[0:4] + '（第２セクション）'
                level = 1
                category = '70'
                examlist, arealist = makeExam2(user_id, amount, int(category), level, 13800-usedTime, '')
                exam_id = saveExam(user_id, category, level, amount, examlist, arealist)
                # for debug
                correctlist = getCorrectList(examlist)
                remain_time = 230 * 60 - usedTime
                remain_time1 = int(remain_time / 3600)
                remain_time2 = int(remain_time / 60)
                remain_time2 = remain_time2 - (remain_time1 * 60)
                remain_time3 = remain_time % 60

                return render_template('sleepExam.html',
                                       user_id=user_id,
                                       exam_id=exam_id,
                                       total=amount,
                                       examlist=examlist,
                                       arealist=arealist,
                                       timeHour=timeHour,
                                       timeMin=timeMin,
                                       timeSec=timeSec,
                                       title=title,
                                       correctlist=correctlist,
                                       test_id=test_id,
                                       usedTime1=usedTime1,
                                       usedTime2=usedTime2,
                                       usedTime3=usedTime3,
                                       remainTime=remain_time,
                                       remainTime1=remain_time1,
                                       remainTime2=remain_time2,
                                       remainTime3=remain_time3,
                                       sleep=1,
                                       )
            elif stage == 13:
                setStage(user_id, 23)
                try:
                    test_id = getTestID(user_id)
#                    test_id = int(exam_id) - 1
                    stime = getStartTime(exam_id)
                    setTestData(user_id, test_id, exam_id, usedTime, 2, stime)

                    items = getTestData(user_id, test_id)
                    usedTime = usedTime + items[0][0]
                    usedTime1 = int(usedTime / 3600)
                    usedTime2 = int(usedTime / 60)
                    usedTime2 = usedTime2 - (usedTime1 * 60)
                    usedTime3 = usedTime % 60

                    remain_time = 230 * 60 - usedTime
                    remain_time1 = int(remain_time / 3600)
                    remain_time2 = int(remain_time / 60)
                    remain_time2 = remain_time2 - (remain_time1 * 60)
                    remain_time3 = remain_time % 60

                    amount = constant.MaxQuestions
                    type = getExamTYpe(exam_id)
#                    title = examTitle11 + '（第３セクション）'
                    title = type[0:4] + '（第３セクション）'
                    level = 1
                    category = '70'
                    examlist, arealist = makeExam2(user_id, amount, int(category), level, 13800-usedTime, '')
                    exam_id = saveExam(user_id, category, level, amount, examlist, arealist)
                    # for debug
                    correctlist = getCorrectList(examlist)
                    return render_template('sleepExam.html',
                                       user_id=user_id,
                                       exam_id=exam_id,
                                       total=amount,
                                       examlist=examlist,
                                       arealist=arealist,
                                       timeHour=timeHour,
                                       timeMin=timeMin,
                                       timeSec=timeSec,
                                       title=title,
                                       correctlist=correctlist,
                                       test_id=test_id,
                                       usedTime1=usedTime1,
                                       usedTime2=usedTime2,
                                       usedTime3=usedTime3,
                                       remainTime=remain_time,
                                       remainTime1=remain_time1,
                                       remainTime2=remain_time2,
                                       remainTime3=remain_time3,
                                       sleep=2,
                                       )
                except:
                    return "Error...."
            elif stage == 23:
                setStage(user_id, 4)
                try:
                    test_id = getTestID(user_id)
#                    test_id = int(exam_id) - 2
                    stime = getStartTime(exam_id)
                    setTestData(user_id, test_id, exam_id, usedTime, 3, stime)
                    items = getTestData(user_id, test_id)
                except:
                    return "Error...."
            else:
                return "Error...."
        else:
            setStage(user_id, 4)

        flag = 0
        old_status = getStatus(user_id)

        # ユーザのステータスを更新
        if rate >= PassScore2 and total == 40:
            status, flag = rankUp(user_id, 2, type)
        elif rate >= PassScore1 and total == 40:
            status, flag = rankUp(user_id, 1, type)

        if old_status == 31 and type == '修了試験(40問)' and rate < PassScore2: # 75%を越えなければ、始めからやり直し
            rankDown(user_id)
            flag = 4
        # 修了試験で合格点を取った場合
        if flag == 3:
            userInfo = ["", "", ""]
            userInfo = getMailadress(user_id)
            username = str(userInfo[0][0]) + " " + str(userInfo[0][1])
            to_email = str(userInfo[0][2])
            if old_status == 31 and type == '修了試験(40問)':
                sendMail(username, to_email, "合格です。")
        # 修了試験受験時のメッセージ
        if old_status >= 30 and type == '修了試験(40問)':
            if rate < PassScore2:
                if old_status >= 40:
                    message = "不合格でした。"
                else:
                    message = FAIL_MESSAGE
            elif old_status == 30:
                message = PASS1_MASSAGE
            elif old_status == 31:
                message = PASS2_MASSAGE
            else:
                message = "合格です。おめでとうございます。"

            return render_template('finish2.html',
                               user_id=user_id,
                               title=title,
                               message=message,
                               )
        # 通常試験時のメッセージ
        elif test_id == 0:
            return render_template('finish.html',
                               user_id=user_id,
                               exam_id=exam_id,
                               total=total,
                               examlist=examlist,
                               arealist=arealist,
                               answerlist=answerlist,
                               resultlist=resultlist,
                               correct=correct,
                               rate=rate,
                               timeHour=timeHour,
                               timeMin=timeMin,
                               timeSec=timeSec,
                               stime=stime,
                               stage=stage,
                               title=title,
                               flag=flag,
                               )
        else:
            test_id, exam2, exam3, time1, time2, time3, total1, score1, percentage1, \
                total2, score2, percentage2, total3, score3, percentage3, type = getTestResult(test_id)
#            return_value = int[16]
#            return_value = getTestResult(test_id)

            # test_id = (int)(return_value[0])
            # exam2 = (int)(return_value[1])
            # exam3 = (int)(return_value[2])
            # time1 = (int)(return_value[3])
            # time2 = (int)(return_value[4])
            # time3 = (int)(return_value[5])
            # total1 = (int)(return_value[6])
            # score1 = (int)(return_value[7])
            # percentage1 = (float)(return_value[8])
            # total2 = (int)(return_value[9])
            # score2 = (int)(return_value[10])
            # percentage2 = (float)(return_value[11])
            # total3 = (int)(return_value[12])
            # score3 = (int)(return_value[13])
            # percentage3 = (float)(return_value[14])
            # type = (str)(return_value[15])

            time1h = int(time1 / 3600)
            time1m = int(time1 / 60)
            time1m = time1m - (time1h * 60)
            time1s = time1 % 60
            if(time1h==0):
                time1Str = str(time1m) + "分" + str(time1s) + "秒"
            else:
                time1Str = str(time1h) + "時間" + str(time1m) + "分" + str(time1s) + "秒"

            time2h = int(time2 / 3600)
            time2m = int(time2 / 60)
            time2m = time2m - (time2h * 60)
            time2s = time2 % 60
            if(time2h==0):
                time2Str = str(time2m) + "分" + str(time2s) + "秒"
            else:
                time2Str = str(time2h) + "時間" + str(time2m) + "分" + str(time2s) + "秒"

            time3h = int(time3 / 3600)
            time3m = int(time3 / 60)
            time3m = time3m - (time3h * 60)
            time3s = time3 % 60
            if(time3h==0):
                time3Str = str(time3m) + "分" + str(time3s) + "秒"
            else:
                time3Str = str(time3h) + "時間" + str(time3m) + "分" + str(time3s) + "秒"

            timeT = time1 + time2 + time3
            timeTh = int(timeT / 3600)
            timeTm = int(timeT / 60)
            timeTm = timeTm - (timeTh * 60)
            timeTs = timeT % 60
            if(timeTh==0):
                timeTStr = str(timeTm) + "分" + str(timeTs) + "秒"
            else:
                timeTStr = str(timeTh) + "時間" + str(timeTm) + "分" + str(timeTs) + "秒"

            return render_template('summary.html',
                               user_id=user_id,
                               test_id=test_id,
                               exam1=test_id,
                               exam2=exam2,
                               exam3=exam3,
                               time1=time1,
                               time2=time2,
                               time3=time3,
                               total1=total1,
                               score1=score1,
                               percentage1=percentage1,
                               total2=total2,
                               score2=score2,
                               percentage2=percentage2,
                               total3=total3,
                               score3=score3,
                               percentage3=percentage3,
                               flag=0,
                               comments="",
                               time1Str= time1Str,
                               time2Str= time2Str,
                               time3Str= time3Str,
                               timeTStr= timeTStr,
                               title=type,
                               )

# 問題の出題
@exec_module.route('/getback')
def getBaack():

    user_id = int(request.args.get("user_id", ""))
    test_id = int(request.args.get("test_id", ""))

    test_id, exam2, exam3, time1, time2, time3, total1, score1, percentage1, \
     total2, score2, percentage2, total3, score3, percentage3, type = getTestResult(test_id)

#    return_value = getTestResult(test_id)
#    test_id = (int)(return_value[0])
#    exam2 = (int)(return_value[1])
#    exam3 = (int)(return_value[2])
#    time1 = (int)(return_value[3])
#    time2 = (int)(return_value[4])
#    time3 = (int)(return_value[5])
#    total1 = (int)(return_value[6])
#    score1 = (int)(return_value[7])
#    percentage1 = (float)(return_value[8])
#    total2 = (int)(return_value[9])
#    score2 = (int)(return_value[10])
#    percentage2 = (float)(return_value[11])
#    total3 = (int)(return_value[12])
#    score3 = (int)(return_value[13])
#    percentage3 = (float)(return_value[14])
#    type = (str)(return_value[15])

    time1h = int(time1 / 3600)
    time1m = int(time1 / 60)
    time1m = time1m - (time1h * 60)
    time1s = time1 % 60
    if (time1h == 0):
        time1Str = str(time1m) + "分" + str(time1s) + "秒"
    else:
        time1Str = str(time1h) + "時間" + str(time1m) + "分" + str(time1s) + "秒"

    time2h = int(time2 / 3600)
    time2m = int(time2 / 60)
    time2m = time2m - (time2h * 60)
    time2s = time2 % 60
    if (time2h == 0):
        time2Str = str(time2m) + "分" + str(time2s) + "秒"
    else:
        time2Str = str(time2h) + "時間" + str(time2m) + "分" + str(time2s) + "秒"

    time3h = int(time3 / 3600)
    time3m = int(time3 / 60)
    time3m = time3m - (time3h * 60)
    time3s = time3 % 60
    if (time3h == 0):
        time3Str = str(time3m) + "分" + str(time3s) + "秒"
    else:
        time3Str = str(time3h) + "時間" + str(time3m) + "分" + str(time3s) + "秒"

    timeT = time1 + time2 + time3
    timeTh = int(timeT / 3600)
    timeTm = int(timeT / 60)
    timeTm = timeTm - (timeTh * 60)
    timeTs = timeT % 60
    if (timeTh == 0):
        timeTStr = str(timeTm) + "分" + str(timeTs) + "秒"
    else:
        timeTStr = str(timeTh) + "時間" + str(timeTm) + "分" + str(timeTs) + "秒"

    return render_template('finish3.html',
                           user_id=user_id,
                           test_id=test_id,
                           exam1=test_id,
                           exam2=exam2,
                           exam3=exam3,
                           time1=time1,
                           time2=time2,
                           time3=time3,
                           total1=total1,
                           score1=score1,
                           percentage1=percentage1,
                           total2=total2,
                           score2=score2,
                           percentage2=percentage2,
                           total3=total3,
                           score3=score3,
                           percentage3=percentage3,
                           flag=0,
                           comments="",
                           time1Str=time1Str,
                           time2Str=time2Str,
                           time3Str=time3Str,
                           timeTStr=timeTStr,
                           title=type,
                           )
