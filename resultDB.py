from constant import db_path, NumOfCategory, NumOfArea, categoryCode, \
     NumOfCategory1, NumOfCategory2, NumOfCategory3, \
     NumOfCheckArea, Area_Base
from flask import Flask, request, render_template
import sqlite3, os, json
import datetime
import re

class ResultInfo:
    def __init__(self, user_id, exam_id, arealist, answerlist, resultlist):
        self.user_id = user_id
        self.exam_id = exam_id
        self.arealist = arealist
        self.answerlist = answerlist
        self.resultlist = resultlist

# 試験結果を格納する
def putResult(user_id, exam_id, amount, arealist, answerlist, resultlist, correct, rate, usedTime):
    categoryNumber = [0 for i in range(NumOfCategory)]
    categoryScore = [0 for i in range(NumOfCategory)]
    categoryPercent = [0 for i in range(NumOfCategory)]

    areaNumber = [0 for i in range(NumOfArea)]
    areaScore = [0 for i in range(NumOfArea)]
    areaPercent = [0 for i in range(NumOfArea)]

# 領域ごとに採点する
    for i, c in enumerate(arealist):
        if resultlist[i] == '1':
            flag = 1
        else:
            flag = 0
        n = categoryCode.find(c)
        categoryNumber[n] += 1
        categoryScore[n] = categoryScore[n] + flag
        if n < NumOfCategory1:
            areaNumber[0] += 1
            areaScore[0] = areaScore[0] + flag
        elif n < NumOfCategory2:
            areaNumber[1] += 1
            areaScore[1] = areaScore[1] + flag
        else:
            areaNumber[2] += 1
            areaScore[2] = areaScore[2] + flag

    for i in range(NumOfCategory):
        if categoryNumber[i] != 0:
            categoryPercent[i] = categoryScore[i] / categoryNumber[i] * 100

    for i in range(NumOfArea):
        if areaNumber[i] != 0:
            areaPercent[i] = areaScore[i] / areaNumber[i] * 100

    half1 = half2 = 0
    length =  round(len(resultlist)/2)
    for i in range(length):
        if resultlist[i] == '1' :
            half1 += 1
    for i in range(length,len(resultlist)):
        if resultlist[i] == '1':
            half2 += 1
    half1 = half1 / length * 100           # 正答率（前半）
    half2 = half2 / (len(resultlist) - length) * 100  # 正答率（後半）

    res = res_correct = 0

    for i, c in enumerate(answerlist):
        if c != '0' :
            res += 1                              # 解答数
    for i, c in enumerate(resultlist):
        if c == '1' :
            res_correct += 1                     # 正答数
    if res == 0:
        res_ratio = 0
    else:
        res_ratio = res_correct / res * 100          # 解答した問題に対する正答率
    total_time = amount * 90
    remain_time = total_time - usedTime          # 残り時間
    remain_time_rate = remain_time / total_time  # 残り時間の割合

    #    last3_answered                   # 最後の３問への解答数
    #    last3_result                     # 最後の３問の採点結果
    last3_answered = answerlist[-3:]
    last3_result = resultlist[-3:]
    last3 = 0
    for i, c in enumerate(last3_result):
        if c == '1':
            last3 += 1
    last3 = last3 / 3 * 100               # 最後の３問の正答率）

    conn = sqlite3.connect(db_path)
    c = conn.cursor()
    sql = "DROP TABLE RESULT_TABLE;"
    #    c.execute(sql)
    sql = "CREATE TABLE IF NOT EXISTS RESULT_TABLE ( EXAM_ID INTEGER, USER_ID INTEGER, EXAM_TYPE LONG VARCHAR,"\
        + "TOTAL INTEGER, TOTAL_R INTEGER, TOTAL_P FLOAT," \
        + "C1_NUMBER INTEGER, C1_SCORE INTEGER, C1_PERCENT FLOAT," \
        + "C2_NUMBER INTEGER, C2_SCORE INTEGER, C2_PERCENT FLOAT," \
        + "C3_NUMBER INTEGER, C3_SCORE INTEGER, C3_PERCENT FLOAT," \
        + "C4_NUMBER INTEGER, C4_SCORE INTEGER, C4_PERCENT FLOAT," \
        + "C5_NUMBER INTEGER, C5_SCORE INTEGER, C5_PERCENT FLOAT," \
        + "C6_NUMBER INTEGER, C6_SCORE INTEGER, C6_PERCENT FLOAT," \
        + "C7_NUMBER INTEGER, C7_SCORE INTEGER, C7_PERCENT FLOAT," \
        + "C8_NUMBER INTEGER, C8_SCORE INTEGER, C8_PERCENT FLOAT," \
        + "C9_NUMBER INTEGER, C9_SCORE INTEGER, C9_PERCENT FLOAT," \
        + "C10_NUMBER INTEGER, C10_SCORE INTEGER, C10_PERCENT FLOAT," \
        + "C11_NUMBER INTEGER, C11_SCORE INTEGER, C11_PERCENT FLOAT," \
        + "C12_NUMBER INTEGER, C12_SCORE INTEGER, C12_PERCENT FLOAT," \
        + "A1_NUMBER INTEGER, A1_SCORE INTEGER, A1_PERCENT FLOAT," \
        + "A2_NUMBER INTEGER, A2_SCORE INTEGER, A2_PERCENT FLOAT," \
        + "A3_NUMBER INTEGER, A3_SCORE INTEGER, A3_PERCENT FLOAT," \
        + "HALF1 FLOAT, HALF2 FLOAT, RESPONSE INTEGER, CORRECT_RES_RATE FLOAT," \
        + "REMAIN_TIME INTEGER, REMAIN_TIME_RATE FLOAT, LAST3 INTEGER);"
    c.execute(sql)

    sql = "INSERT INTO RESULT_TABLE( USER_ID, EXAM_ID, TOTAL, TOTAL_R, TOTAL_P ";
    for i in range(1,NumOfCategory+1):
        sql = sql + ", C"+ str(i) +"_NUMBER, C"+ str(i) +"_SCORE, C"+ str(i) +"_PERCENT";

    for i in range(1,NumOfArea+1):
        sql = sql + ", A" + str(i) + "_NUMBER, A" + str(i) + "_SCORE, A" + str(i) + "_PERCENT";

    sql = sql + ", HALF1, HALF2, RESPONSE, CORRECT_RES_RATE, REMAIN_TIME, REMAIN_TIME_RATE, LAST3" \
          + ") VALUES (" + str(user_id)  + ", " + str(exam_id) + ", " + str(amount) +", " + str(correct) +", " + str(rate) + " ";
    for i in range(NumOfCategory):
        sql = sql + ", " + str(categoryNumber[i]) + ", " + str(categoryScore[i]) + ", " + str(categoryPercent[i]);

    for i in range(NumOfArea):
        sql = sql + ", " + str(areaNumber[i]) + ", " + str(areaScore[i]) + ", " + str(areaPercent[i]);

    sql = sql + ", " + str(half1) + ", " + str(half2) + ", " + str(res) + ", " + str(res_ratio) + ", "\
          + str(remain_time) + ", " + str(remain_time_rate) + ", " + str(last3) + " )"

    print(sql)
    if c.execute(sql):
        print("Success!")
    else:
        print("Error!")
    conn.commit()

# 試験結果を抽出する
def getResult(exam_id):

    categoryNumber = [0 for i in range(NumOfCategory+1)]
    categoryScore = [0 for i in range(NumOfCategory+1)]
    categoryPercent = [0 for i in range(NumOfCategory+1)]

    areaNumber = [0 for i in range(NumOfArea)]
    areaScore = [0 for i in range(NumOfArea)]
    areaPercent = [0 for i in range(NumOfArea)]

    conn = sqlite3.connect(db_path)
    c = conn.cursor()
    sql = "SELECT * FROM RESULT_TABLE WHERE EXAM_ID = " + str(exam_id) + ";"
    print(sql)
    if c.execute(sql):
        print("Success!")
    else:
        print("Error!")
    items = c.fetchall()
    user_id = items[0][1]
    total = items[0][3]
    correct = items[0][4]
    rate = items[0][5]

    for i in range(NumOfCategory+1):
        a = items[0][i * 3 + 6]
        b = items[0][i * 3 + 7]

        categoryNumber[i] = int(a)
        categoryScore[i] = int(b)
        if categoryNumber[i] != 0:
            categoryPercent[i] = categoryScore[i] / categoryNumber[i] * 100

    for i in range(NumOfArea):
        areaNumber[i] = items[0][i*3+42]    # 42 = 6 + (12 x 3)
        areaScore[i] = items[0][i*3+43]
        areaPercent[i] = items[0][i*3+44]

    return categoryNumber, categoryScore, categoryPercent, areaNumber, \
           areaScore, areaPercent

#   コメントIDからコメントを得る
def getComment(cid):

    conn = sqlite3.connect(db_path)
    c = conn.cursor()
    sql = "SELECT  COMMENT FROM COMMENTS_TABLE" \
          + " WHERE COMMENT_ID = " + str(cid) + ";"
    c.execute(sql)
    items = c.fetchall()
    conn.close()

    return items[0][0]

# コメント文を作成する
def makeComments(exam_id):

    categoryNumber = [0 for i in range(NumOfCategory)]
    categoryScore = [0 for i in range(NumOfCategory)]
    categoryPercent = [0 for i in range(NumOfCategory)]

    areaNumber = [0 for i in range(NumOfArea)]
    areaScore = [0 for i in range(NumOfArea)]
    areaPercent = [0 for i in range(NumOfArea)]

    result_data = [0 for i in range(9)]

    area, score, percent, user_id, half1, half2, res, correct_rate, \
    remain_time, remain_time_rate, last3 = getResultData(exam_id)

    conn = sqlite3.connect(db_path)
    c = conn.cursor()
    sql = 'SELECT TOTAL_TIME, USED_TIME, RESULTLIST, AREALIST, START_TIME'\
        ' FROM EXAM_TABLE WHERE EXAM_ID = ' + str(exam_id)
    c.execute(sql)
    items = c.fetchall()
    total_time = items[0][0]
    used_time = items[0][1]
    resultlist = items[0][2]
    arealist = items[0][3]
    start_time = items[0][4]

    sql = 'SELECT TOTAL, TOTAL_P, TOTAL_R,'\
          'A1_NUMBER, A1_SCORE, A1_PERCENT,'\
          'A2_NUMBER , A2_SCORE, A2_PERCENT,'\
          'A3_NUMBER , A3_SCORE , A3_PERCENT'\
          ' FROM RESULT_TABLE WHERE EXAM_ID = ' + str(exam_id)
    c.execute(sql)
    items = c.fetchall()

    total = items[0][0]
    total_p = items[0][1]
    total_r = items[0][2]

    for i in range(NumOfArea):
        areaNumber[i] = items[0][i*3+3]
        areaScore[i] = items[0][i*3+4]
        areaPercent[i] = items[0][i*3+5]

    sql = 'SELECT C1_NUMBER , C1_SCORE , C1_PERCENT,'\
          'C2_NUMBER , C2_SCORE , C2_PERCENT ,'\
          'C3_NUMBER , C3_SCORE , C3_PERCENT ,'\
          'C4_NUMBER , C4_SCORE , C4_PERCENT ,'\
          'C5_NUMBER , C5_SCORE , C5_PERCENT ,'\
          'C6_NUMBER , C6_SCORE , C6_PERCENT ,'\
          'C7_NUMBER , C7_SCORE , C7_PERCENT ,'\
          'C8_NUMBER , C8_SCORE , C8_PERCENT ,'\
          'C9_NUMBER , C9_SCORE , C9_PERCENT ,'\
          'C10_NUMBER , C10_SCORE , C10_PERCENT ,'\
          'C11_NUMBER , C11_SCORE , C11_PERCENT ,'\
          'C12_NUMBER , C12_SCORE , C12_PERCENT '\
          ' FROM RESULT_TABLE WHERE EXAM_ID = ' + str(exam_id)
    c.execute(sql)
    items = c.fetchall()

# なぜ、NumOfCategory-1)
    for i in range(NumOfCategory):
        a = items[0][i * 3]
        b = items[0][i * 3 + 1]

        categoryNumber[i] = int(a)
        categoryScore[i] = int(b)
        if categoryNumber[i] != 0:
            categoryPercent[i] = categoryScore[i] / categoryNumber[i] * 100

    weakArea = [0 for i in range(NumOfArea)]
    weakCategory = [0 for i in range(NumOfCheckArea)]
    weakAreaList1 = ""
    weakAreaList2 = ""
    weakCategoryList1 = ""
    weakCategoryList2 = ""

#
    for i in range(NumOfCheckArea):
        if categoryNumber[i] != 0:
            if categoryPercent[i] == 0:
                weakCategory[i] = 1
                if( weakCategoryList1 != ""):
                    weakCategoryList1 = ',' + weakCategoryList1 + str(i)
                else:
                    weakCategoryList1 = weakCategoryList1 + str(i)
            elif categoryPercent[i] < 50:
                weakCategory[i] = 2
                if( weakCategoryList2 != ""):
                    weakCategoryList2 = ',' + weakCategoryList2 + str(i)
                else:
                    weakCategoryList2 = weakCategoryList2 + str(i)
            else:
                weakCategory[i] = 0

    n = 0
    for i in range(NumOfArea):
        if areaNumber[i] != 0:
            areaPercent[i] = areaScore[i] / areaNumber[i]
            if areaPercent[i] == 0:
                weakArea[i] = 1
                n += 1
                weakAreaList1 = weakAreaList1 + str(i)
            elif areaPercent[i] < 50:
                weakArea[i] = 2
                weakAreaList2 = weakAreaList2 + str(i)
            else:
                weakArea[i] = 0

# 選択された領域を明かにする
    select = 0
    j = 0
    for i in range(NumOfArea):
        if areaNumber[i] != 0:
            j += 1
            select = i+1
# j = 1 でなければ、全領域を指定しているはず
    if j != 1:
        select = 0

    if total_p >= 90:
        cid =500
    elif total_p >= 75:
        cid = 501
    elif total_p >= 65:
        cid = 502
    elif total_p >= 40:
        cid = 503
    elif total_p >= 20:
        cid = 504
    elif correct_rate < 60:
        cid = 510
    else:
        cid = 505

    comment = "<br>" + getComment(cid) + "<br>"

# 残り時間の量で試験への取り組みを判別する
    if remain_time_rate > 0.5:
        cid = 511
        comment = comment + getComment(cid) + "<br>"
# 最後の３問の成績で試験への取り組みを判別する
    if last3 == 0:
        cid = 520
        comment = comment + getComment(cid) + "<br>"
# 前半と後半の成績の差で試験への取り組みを判別する
    if half1 - half2 > 50:
        cid = 521
        comment = comment + getComment(cid) + "<br>"
# 解答数をベースとした正答率で理解度を判別する
    if correct_rate >=85:
        cid = 514
        comment = comment + getComment(cid) + "<br>"
    elif correct_rate > 70:
        cid = 513
        comment = comment + getComment(cid) + "<br>"

    if correct_rate < 30:
        cid = 512
        comment = comment + getComment(cid) + "<br>"

#   解答結果の分析とコメント選択
#   全領域選択の場合
    if total == 60 or total == 18:
#   すべての領域で 50 % 以下の正答率の場合
        if areaPercent[0] < 50 and areaPercent[1] < 50 and areaPercent[2] < 50 :
            cid = 538
#   全領域で 80 % 以上、正解している場合
        elif areaPercent[0] > 80 and areaPercent[1] > 80 and areaPercent[2] > 80 :
            cid = 590
#   50 % 以下の正答率の領域があった場合
        elif areaPercent[0] < 50 or areaPercent[1] < 50 or areaPercent[2] < 50 :
#   かつ、80 % 以上の正答率の領域もある場合
            if areaPercent[0] > 80 or areaPercent[1] > 80 or areaPercent[2] > 80 :
                cid = 591
#   かつ、80 % 　以上正答した領域がない場合
            else:
                cid = 537
#   すべての領域が 50 % 以上の正答率であり、80 % を超える領域もある場合
        elif areaPercent[0] > 80 or areaPercent[1] > 80 or areaPercent[2] > 80 :
            cid = 592
# すべての領域が 50 % 以上、79 % 以下の正答率である場合
        else:
            cid = 594
#   各領域の正答率から判断した分析結果をコメントする
        comment = comment + getComment(cid) + "<br><br>"

#   弱点を指摘する
        list = ""
        if (cid == 537 or cid == 538 or cid == 591) and n != 0:

            j = 0
            for i, n in enumerate(weakArea) :
                if n == 1:
                    if j != 0:
                        list = list + '、'
                    list = list + '「' + getComment(Area_Base + i) + '」'
                    j += 1
            list = list + getComment(539)
        comment = comment + list
        comment = comment + "<BR>"

#   出題領域を選択している場合
    else:
        if select != 0 :
            cid = (Area_Base-1) + select
            comment = comment + '「' + getComment(cid) + '」'
            cid = 589
            comment = comment + getComment(cid) + "<BR>"

        #   不得意領域を指摘する
        m = 0
        list = ""
        for i in range(NumOfCheckArea):
            if weakCategory[i] == 1:
                if m != 0:
                    list = list + "、"
                m = m + 1
                list = list + '「' + getComment(710 + i) + '」'
        #   不得意領域がない場合
        if m == 0:
            cid = 595
            comment = comment + getComment(cid)
        else:
            comment = comment + list + getComment(539)
    comment = comment + "<BR>"
    return comment

def getResultData(exam_id):

    area = [0 for i in range(NumOfArea+NumOfCategory+3)]
    score = [0 for i in range(NumOfArea+NumOfCategory+3)]
    percent = [0 for i in range(NumOfArea+NumOfCategory+3)]

    conn = sqlite3.connect(db_path)
    c = conn.cursor()
    sql = "SELECT * FROM RESULT_TABLE WHERE EXAM_ID = " + str(exam_id)
    c.execute(sql)
    items = c.fetchall()

    user_id = items[0][1]
    area[NumOfArea+NumOfCategory] = items[0][3]
    score[NumOfArea+NumOfCategory] = items[0][4]
    percent[NumOfArea+NumOfCategory] = items[0][5]
    for i in range(NumOfArea+NumOfCategory):
        area[i]= items[0][i*3+6]
        score[i]= items[0][i*3+7]
        percent[i]= items[0][i*3+8]
    half1 = items[0][(NumOfArea+NumOfCategory)*3+6]
    half2 = items[0][(NumOfArea+NumOfCategory)*3+7]
    res = items[0][(NumOfArea+NumOfCategory)*3+8]
    correct_rate = items[0][(NumOfArea+NumOfCategory)*3+9]
    remain_time = items[0][(NumOfArea+NumOfCategory)*3+10]
    remain_time_rate = items[0][(NumOfArea+NumOfCategory)*3+11]
    last3 = items[0][(NumOfArea+NumOfCategory)*3+12]

    conn.close()
    return area, score, percent, user_id, half1, half2, res, correct_rate, \
           remain_time, remain_time_rate, last3

def getUserResultList(user_id):

    n = 0
    userlist = []
    conn = sqlite3.connect(db_path)
    c = conn.cursor()

    sql = 'SELECT USER_TABLE.LASTNAME, AMOUNT, SCORE,'\
       'RATE, START_TIME, EXAM_TYPE, '\
       'USER_TABLE.MAIL_ADR FROM EXAM_TABLE INNER JOIN USER_TABLE ON '\
       'EXAM_TABLE.USER_ID = USER_TABLE.USER_ID '
    sql = sql + 'where USER_TABLE.USER_ID = ' + str(user_id) + \
          ' AND EXAM_TYPE != "修了試験(40問)" and score != ""'

    try:
        c.execute(sql)
        items = c.fetchall()
        n = len(items)
        conn.close()
        return items, n
    except sqlite3.Error as e:
        print('sqlite3.Error occurred:', e.args[0])
        conn.close()
        return False, n


def getStartTime(exam_id):

    conn = sqlite3.connect(db_path)
    c = conn.cursor()
    sql = 'SELECT START_TIME FROM EXAM_TABLE where EXAM_ID = ' + str(exam_id)
    try:
        c.execute(sql)
        items = c.fetchall()

        conn.close()
        return items[0][0]
    except sqlite3.Error as e:
        print('sqlite3.Error occurred:', e.args[0])
        conn.close()
        return False

def getUserResultList1(user_id):

    userlist = []
    n = 0
    conn = sqlite3.connect(db_path)
    c = conn.cursor()

    sql = 'SELECT USER_TABLE.LASTNAME, USER_TABLE.STATUS, AMOUNT, SCORE,'\
       'RATE, START_TIME, EXAM_TYPE, '\
       'USER_TABLE.MAIL_ADR FROM EXAM_TABLE INNER JOIN USER_TABLE ON '\
       'EXAM_TABLE.USER_ID = USER_TABLE.USER_ID '
    sql = sql + 'where USER_TABLE.USER_ID = ' + str(user_id) + \
          ' AND EXAM_TYPE = "模擬試験(40問)" and score != ""'

    try:
        c.execute(sql)
        items = c.fetchall()
        n = len(items)
        conn.close()
        return items, n
    except sqlite3.Error as e:
        print('sqlite3.Error occurred:', e.args[0])
        conn.close()
        return False, n

def getUserResultList2(user_id):

    n = 0
    userlist = []
    conn = sqlite3.connect(db_path)
    c = conn.cursor()

    sql = 'SELECT USER_TABLE.LASTNAME, USER_TABLE.STATUS, '\
       'RATE, START_TIME, EXAM_TYPE, '\
       'USER_TABLE.MAIL_ADR FROM EXAM_TABLE INNER JOIN USER_TABLE ON '\
       'EXAM_TABLE.USER_ID = USER_TABLE.USER_ID '
    sql = sql + 'where USER_TABLE.USER_ID = ' + str(user_id) + \
          ' AND EXAM_TYPE = "修了試験(40問)" and score != ""'

    try:
        c.execute(sql)
        items = c.fetchall()
        n = len(items)
        conn.close()
        return items, n
    except sqlite3.Error as e:
        print('sqlite3.Error occurred:', e.args[0])
        conn.close()
        return False, n

def setTestData(user_id, test_id, exam_id, used_time, number, stime):

    conn = sqlite3.connect(db_path)
    c = conn.cursor()
    sql = "DROP TABLE TEST_TABLE;"
    # c.execute(sql)
    sql = "CREATE TABLE IF NOT EXISTS TEST_TABLE ( USER_ID INTEGER, "\
        + "TEST_ID INTEGER, USED_TIME1 INTEGER," \
        + "EXAM_ID2 INTEGER, USED_TIME2 INTEGER," \
        + "EXAM_ID3 INTEGER, USED_TIME3 INTEGER," \
        + "STIME TIME);"
    try:
        c.execute(sql)
    except sqlite3.Error as e:
        print('sqlite3.Error occurred:', e.args[0])
        conn.close()
        return False

    if number == 1:
        sql = "INSERT INTO TEST_TABLE ( USER_ID, "\
            + "TEST_ID, USED_TIME1, USED_TIME2, USED_TIME3, STIME) VALUES (" + str(user_id) + ", "\
            + str(test_id) + ", " + str(used_time) + ", \'"\
            + str(stime) + "\', 0, 0 );"
    elif number == 2:
        sql = "UPDATE TEST_TABLE SET EXAM_ID2 = "\
            + str(exam_id) + ", USED_TIME2 = " + str(used_time) \
            + " WHERE TEST_ID = " + str(test_id) + ";"
    elif number == 3:
        sql = "UPDATE TEST_TABLE SET EXAM_ID3 = "\
            + str(exam_id) + ", USED_TIME3 = " + str(used_time) \
            + " WHERE TEST_ID = " + str(test_id) + ""
    else:
        conn.close()
        return False

    try:
        c.execute(sql)
        conn.commit()
        conn.close()
        return test_id
    except sqlite3.Error as e:
        print('sqlite3.Error occurred:', e.args[0])
        conn.close()
        return False

def getTestData(user_id, test_id):

    conn = sqlite3.connect(db_path)
    c = conn.cursor()

    sql = "SELECT USED_TIME1, USED_TIME2, USED_TIME3 FROM TEST_TABLE "\
        + "WHERE TEST_ID = " + str(test_id) + ";"

    try:
        c.execute(sql)
        items = c.fetchall()
        conn.close()
        return items
    except sqlite3.Error as e:
        print('sqlite3.Error occurred:', e.args[0])
        conn.close()
        return False


def getTestID(user_id):

    conn = sqlite3.connect(db_path)
    c = conn.cursor()

    sql = "SELECT MAX(TEST_ID) FROM TEST_TABLE "\
        + "WHERE USER_ID = " + str(user_id) + ";"

    try:
        c.execute(sql)
        items = c.fetchall()
        n = len(items)
        conn.close()
        if n < 1:
            return False
        else:
            return items[0][0]
    except sqlite3.Error as e:
        print('sqlite3.Error occurred:', e.args[0])
        conn.close()
        return False

def getTestResult(test_id):

    conn = sqlite3.connect(db_path)
    c = conn.cursor()

    sql = "SELECT EXAM_ID2, EXAM_ID3, USED_TIME1, USED_TIME2, USED_TIME3 FROM TEST_TABLE "\
        + "WHERE TEST_ID = " + str(test_id) + ";"

    try:
        c.execute(sql)
        items = c.fetchall()
        n = len(items)
        if n < 1:
            return False
        exam2 = items[0][0]
        exam3 = items[0][1]
        time1 = items[0][2]
        time2 = items[0][3]
        time3 = items[0][4]

        sql = "SELECT TOTAL, TOTAL_R, TOTAL_P FROM RESULT_TABLE " \
            + "WHERE EXAM_ID = " + str(test_id) + ";"
        c.execute(sql)
        items = c.fetchall()
        n = len(items)
        if n < 1:
            return False
        total1 = items[0][0]
        score1 = items[0][1]
        percentage1 = items[0][2]

        sql = "SELECT TOTAL, TOTAL_R, TOTAL_P FROM RESULT_TABLE " \
            + "WHERE EXAM_ID = " + str(exam2) + ";"
        c.execute(sql)
        items = c.fetchall()
        n = len(items)
        if n < 1:
            return False
        total2 = items[0][0]
        score2 = items[0][1]
        percentage2 = items[0][2]

        sql = "SELECT TOTAL, TOTAL_R, TOTAL_P FROM RESULT_TABLE " \
            + "WHERE EXAM_ID = " + str(exam3) + ";"
        c.execute(sql)
        items = c.fetchall()
        n = len(items)
        if n < 1:
            return False
        total3 = items[0][0]
        score3 = items[0][1]
        percentage3 = items[0][2]

        sql = "SELECT EXAM_TYPE FROM EXAM_TABLE " \
            + "WHERE EXAM_ID = " + str(test_id) + ";"
        c.execute(sql)
        items = c.fetchall()
        n = len(items)
        if n < 1:
            return False
        type = items[0][0]

        return test_id, exam2, exam3, time1, time2, time3, total1, score1, percentage1, \
            total2, score2, percentage2, total3, score3, percentage3, type
    except sqlite3.Error as e:
        print('sqlite3.Error occurred:', e.args[0])
        conn.close()
        return False


# コメント文を作成する
def makeTestComments(exam1, exam2, exam3, used_time):

    categoryNumber = [0 for i in range(NumOfCategory)]
    categoryScore = [0 for i in range(NumOfCategory)]
    categoryPercent = [0 for i in range(NumOfCategory)]

    areaNumber = [0 for i in range(NumOfArea)]
    areaScore = [0 for i in range(NumOfArea)]
    areaPercent = [0 for i in range(NumOfArea)]

    result_data = [0 for i in range(9)]

    conn = sqlite3.connect(db_path)
    c = conn.cursor()
    sql = 'SELECT START_TIME FROM EXAM_TABLE WHERE EXAM_ID = ' + str(exam1)
    c.execute(sql)
    items = c.fetchall()
    total_time = 230 * 60
    start_time = items[0][0]
    remain_time = total_time - used_time
    remain_time_rate = remain_time / total_time * 100

    # Category ごとの結果を抽出する

    sql = 'SELECT TOTAL, TOTAL_P, A1_NUMBER, A1_SCORE, '\
          'A2_NUMBER , A2_SCORE, A3_NUMBER , A3_SCORE, '\
          'C1_NUMBER, C1_SCORE, C2_NUMBER, C2_SCORE, '\
          'C3_NUMBER, C3_SCORE, C4_NUMBER, C4_SCORE, C5_NUMBER, C5_SCORE, '\
          'C6_NUMBER ,C6_SCORE, C7_NUMBER, C7_SCORE, C8_NUMBER, C8_SCORE, '\
          'C9_NUMBER ,C9_SCORE, C10_NUMBER, C10_SCORE, C11_NUMBER, C11_SCORE ,'\
          'C12_NUMBER, C12_SCORE '\
          ' FROM RESULT_TABLE WHERE EXAM_ID = ' + str(exam1)
    c.execute(sql)
    items = c.fetchall()
    total = items[0][0]
    total_p = items[0][1]
    half1 = total_p / total * 100  # exam1 のresult を前半の結果とする

# Category の正解率を算出する
    for i in range(NumOfArea):
        areaNumber[i] = items[0][i*2+2]
        areaScore[i] = items[0][i*2+3]
    for i in range(NumOfCategory):
        categoryNumber[i] = int(items[0][i*2] + 8)
        categoryScore[i] = int(items[0][i*2 + 1] + 9)

    sql = 'SELECT TOTAL, TOTAL_P, A1_NUMBER, A1_SCORE, '\
          'A2_NUMBER , A2_SCORE, A3_NUMBER , A3_SCORE, '\
          'C1_NUMBER, C1_SCORE, C2_NUMBER, C2_SCORE, '\
          'C3_NUMBER, C3_SCORE, C4_NUMBER, C4_SCORE, C5_NUMBER, C5_SCORE, ' \
          'C6_NUMBER ,C6_SCORE, C7_NUMBER, C7_SCORE, C8_NUMBER, C8_SCORE, ' \
          'C9_NUMBER ,C9_SCORE, C10_NUMBER, C10_SCORE, C11_NUMBER, C11_SCORE,' \
          'C12_NUMBER, C12_SCORE ' \
          ' FROM RESULT_TABLE WHERE EXAM_ID = ' + str(exam2)
    c.execute(sql)
    items = c.fetchall()
    half2 = items[0][1] / items[0][0] * 100  # exam2 のresult を後半の結果とする
    total = total + items[0][0]
    total_p = total_p + items[0][1]

    # Category の正解率を算出する
    for i in range(NumOfArea):
        areaNumber[i] = areaNumber[i] + items[0][i*2+2]
        areaScore[i] = areaScore[i] + items[0][i*2+3]
    for i in range(NumOfCategory):
        categoryNumber[i] = categoryNumber[i] + int(items[0][i*2 + 8])
        categoryScore[i] = categoryScore[i] + int(items[0][i*2 + 9])

    sql = 'SELECT TOTAL, TOTAL_P, A1_NUMBER, A1_SCORE, '\
          'A2_NUMBER , A2_SCORE, A3_NUMBER , A3_SCORE, '\
          'C1_NUMBER, C1_SCORE, C2_NUMBER, C2_SCORE, '\
          'C3_NUMBER, C3_SCORE, C4_NUMBER, C4_SCORE, C5_NUMBER, C5_SCORE, ' \
          'C6_NUMBER ,C6_SCORE, C7_NUMBER, C7_SCORE, C8_NUMBER, C8_SCORE, ' \
          'C9_NUMBER ,C9_SCORE, C10_NUMBER, C10_SCORE, C11_NUMBER, C11_SCORE,' \
          'C12_NUMBER, C12_SCORE ' \
          ' FROM RESULT_TABLE WHERE EXAM_ID = ' + str(exam3)
    c.execute(sql)
    items = c.fetchall()
    last3 = items[0][1] / items[0][0] * 100  # exam3 のresult を最後の結果とする
    total = total + items[0][0]
    total_p = total_p + items[0][1]
    total_r = total_p / total * 100
    correct_rate = total_r

    # Category の正解率を算出する
    for i in range(NumOfArea):
        areaNumber[i] = areaNumber[i] + items[0][i*2+2]
        areaScore[i] = areaScore[i] + items[0][i*2+3]
        areaPercent[i] = areaScore[i] / areaNumber[i] * 100
    for i in range(NumOfCategory):
        categoryNumber[i] = categoryNumber[i] + int(items[0][i*2 + 8])
        categoryScore[i] = categoryScore[i] + int(items[0][i*2 + 9])
        categoryPercent[i] = categoryScore[i] / categoryNumber[i] * 100

    weakArea = [0 for i in range(NumOfArea)]
    weakCategory = [0 for i in range(NumOfCheckArea)]
    weakAreaList1 = ""
    weakAreaList2 = ""
    weakCategoryList1 = ""
    weakCategoryList2 = ""
#
    for i in range(NumOfCheckArea):
        if categoryNumber[i] != 0:
            if categoryPercent[i] == 0:
                weakCategory[i] = 1
                if( weakCategoryList1 != ""):
                    weakCategoryList1 = ',' + weakCategoryList1 + str(i)
                else:
                    weakCategoryList1 = weakCategoryList1 + str(i)
            elif categoryPercent[i] < 50:
                weakCategory[i] = 2
                if( weakCategoryList2 != ""):
                    weakCategoryList2 = ',' + weakCategoryList2 + str(i)
                else:
                    weakCategoryList2 = weakCategoryList2 + str(i)
            else:
                weakCategory[i] = 0

    n = 0
    for i in range(NumOfArea):
        if areaNumber[i] != 0:
            areaPercent[i] = areaScore[i] / areaNumber[i]
            if areaPercent[i] == 0:
                weakArea[i] = 1
                n += 1
                weakAreaList1 = weakAreaList1 + str(i)
            elif areaPercent[i] < 50:
                weakArea[i] = 2
                weakAreaList2 = weakAreaList2 + str(i)
            else:
                weakArea[i] = 0

    if total_p >= 90:
        cid =500
    elif total_p >= 75:
        cid = 501
    elif total_p >= 65:
        cid = 502
    elif total_p >= 40:
        cid = 503
    elif total_p >= 20:
        cid = 504
    elif correct_rate < 60:
        cid = 510
    else:
        cid = 505

    comment = "<br>" + getComment(cid) + "<br>"

# 残り時間の量で試験への取り組みを判別する
    if remain_time_rate > 0.5:
        cid = 511
        comment = comment + getComment(cid) + "<br>"
# 最後の３問の成績で試験への取り組みを判別する
    if last3 == 0:
        cid = 520
        comment = comment + getComment(cid) + "<br>"
# 前半と後半の成績の差で試験への取り組みを判別する
    if half1 - half2 > 50:
        cid = 521
        comment = comment + getComment(cid) + "<br>"
# 解答数をベースとした正答率で理解度を判別する
    if correct_rate >=85:
        cid = 514
        comment = comment + getComment(cid) + "<br>"
    elif correct_rate > 70:
        cid = 513
        comment = comment + getComment(cid) + "<br>"

    if correct_rate < 30:
        cid = 512
        comment = comment + getComment(cid) + "<br>"

#   解答結果の分析とコメント選択
#   すべての領域で 50 % 以下の正答率の場合
        if areaPercent[0] < 50 and areaPercent[1] < 50 and areaPercent[2] < 50 :
            cid = 538
#   全領域で 80 % 以上、正解している場合
        elif areaPercent[0] > 80 and areaPercent[1] > 80 and areaPercent[2] > 80 :
            cid = 590
#   50 % 以下の正答率の領域があった場合
        elif areaPercent[0] < 50 or areaPercent[1] < 50 or areaPercent[2] < 50 :
#   かつ、80 % 以上の正答率の領域もある場合
            if areaPercent[0] > 80 or areaPercent[1] > 80 or areaPercent[2] > 80 :
                cid = 591
#   かつ、80 % 　以上正答した領域がない場合
            else:
                cid = 537
#   すべての領域が 50 % 以上の正答率であり、80 % を超える領域もある場合
        elif areaPercent[0] > 80 or areaPercent[1] > 80 or areaPercent[2] > 80 :
            cid = 592
# すべての領域が 50 % 以上、79 % 以下の正答率である場合
        else:
            cid = 594
#   各領域の正答率から判断した分析結果をコメントする
        comment = comment + getComment(cid) + "<br><br>"

#   弱点を指摘する
        list = ""
        if (cid == 537 or cid == 538 or cid == 591) and n != 0:

            j = 0
            for i, n in enumerate(weakArea) :
                if n == 1:
                    if j != 0:
                        list = list + '、'
                    list = list + '「' + getComment(Area_Base + i) + '」'
                    j += 1
            list = list + getComment(539)
        comment = comment + list
        comment = comment + "<BR>"

    comment = comment + "<BR>"
    return comment

