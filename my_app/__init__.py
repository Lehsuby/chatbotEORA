#!flask/bin/python
from flask import Flask, request
import psycopg2
from psycopg2.extensions import ISOLATION_LEVEL_AUTOCOMMIT
import time as ttime
from datetime import datetime
import os
from subprocess import call

con = psycopg2.connect(dbname='db_chatbotEORA', user='tu', host='localhost', password='qwerty')
con.set_isolation_level(ISOLATION_LEVEL_AUTOCOMMIT)
MAIN_DIRECTORY = "/home/lehsuby/PycharmProjects/chatbotEORA/my_app/src"
NICKNAME = "Привет! Меня зовут EORA. Как тебя зовут (введи user_id)?"
START_MESSAGE = "Я помогу отличить кота от хлеба! Объект перед тобой квадратный?"
ITS_BREAD = 'Это хлеб, а не кот! Ешь его!'
ITS_CAT = 'Это кот, а не хлеб! Не ешь его!'
ADD_QUESTION = 'У него есть уши?'
WRONG_EXP = 'Я не понимаю вас'
POSITIVE_ANSWER = ['да', 'конечно', 'ага', 'пожалуй']
NEGATIVE_ANSWER = ['нет', 'нет, конечно', 'ноуп', 'найн']
START_COMMAND = ['/start']
CHECK_USER = """SELECT *
                    FROM public.users
                    WHERE user_id = %s"""
CHECK_MESSANGES = """SELECT *
                        FROM public.answers
                        WHERE user_id = %s
                        ORDER BY time_message"""
INSERT_USER = """INSERT INTO users VALUES (%s)"""
INSERT_MESSAGE = """INSERT INTO answers VALUES (%s,%s,%s,%s,%s)"""
FIND_LAST_STATUS = """SELECT task_status
                        FROM public.answers
                        WHERE time_message=(SELECT MAX(time_message)
                                                FROM public.answers
                                                WHERE user_id = %s)"""
TAG_INPUT_WITH_ID = """</scroll-container></body>
  <div style="float: left;">
  <form action = "/eora/api/" method="get" class="input_message">
    <input type="text" name="msg" required="required">
    <input type="hidden" name="user_id" value=%s>
    <input type="submit" value="Отправить">
  </form>
  </div>
  <div style="float: right;">
  <form action="/eora/api/" method="post" enctype="multipart/form-data" class="input_message">
    <input type="file" name="file" accept="image/jpeg,image/png" required autofocus>
    <input type="hidden" name="user_id" value=%s>
    <input type="submit" value="Отправить на обработку"/>
  </form>
  </div>
  <script type="text/javascript">
  var messageBody = document.querySelector('scroll-container');
    messageBody.scrollTop = messageBody.scrollHeight - messageBody.clientHeight;
</script>"""
TAG_INPUT_WITOUT_ID = """</scroll-container></body>
  <form action = "/eora/api/" method="get" class="input_message" class="input_file">
    <input type="text" name="user_id" required="required">
    <input type="submit" value="Отправить">
  </form>
  <script>
  var messageBody = document.querySelector('scroll-container');
    messageBody.scrollTop = messageBody.scrollHeight - messageBody.clientHeight;
</script>"""
STYLES = """<style>#input_message{
                    display: inline_block;
                    position: fixed; 
                    margin-top: 10px;
                    bottom: 0;
                    }
                    .name_bot{
                    font: bold 2em Arial, Tahome, sans-serif;
                    position: fixed;
                    width: 100%;
                    margin-bottom: 10px; 
                    text-align: center;
                    top: 0;
                    }
                    scroll-container {
                    outline: 2px solid #000;
                    display: block;
                    height: 90%;
                    margin: 50px auto 20px;
                    overflow-y: auto;
                    }
</style>
<script src="https://ajax.googleapis.com/ajax/libs/jquery/2.1.1/jquery.min.js"></script>
<body>
<div class="name_bot">EORA - your personal bot</div>
<scroll-container>
"""
UPLOAD_FILE="""
<form action="/eora/api" method="post" enctype="multipart/form-data"">
    <input type="file" name="file" accept="image/jpeg,image/png" required autofocus>
    <input type="submit" value="Отправить на обработку"/>
</form>"""
app = Flask(__name__)

def get_history(user_id):
    cur = con.cursor()
    cur.execute(CHECK_MESSANGES, [user_id])
    rows = cur.fetchall()
    history = STYLES
    for row in rows:
        if row[4] == 0:
            history = history + row[0] + "<br />" + row[1].strftime("%Y-%m-%d %H:%M") + "<br />"
        else:
            history = history + "<p align='right'>" + row[0] + "<br />" + row[1].strftime(
                "%Y-%m-%d %H:%M") + "</p><br />"
    return history

def get_last_status(user_id):
    cur = con.cursor()
    cur.execute(FIND_LAST_STATUS, [user_id])
    return cur.fetchone()[0]


def prediction(name_file, user_id):
    f = open('src/%s_logfile_1.txt' % user_id, 'w')
    call_string = "python scripts/label_image.py --image src/%s" % (name_file)
    call(call_string, stdout=f, shell=True)
    with open('src/%s_logfile_1.txt' % user_id, 'r') as f:
        data = f.readlines()
    cat = data[3]
    cat = float(cat[12:19])
    bread = data[4]
    bread = float(bread[13:20])
    os.remove("src/%s_logfile_1.txt" % user_id)
    os.remove("src/%s" % name_file)
    if cat > bread:
        return ITS_CAT
    else:
        return ITS_BREAD

@app.route('/eora/api/', methods = ['GET','POST'])
def get_bot_response():
    cur = con.cursor()
    t = datetime.fromtimestamp(ttime.time())
    if request.method == 'POST':
        static_file = request.files['file']
        full_name_file = static_file.filename
        name_file = full_name_file.replace(' ', '')
        static_file.save("src/"+name_file)
        user_id = request.form['user_id'].strip()
        answer = prediction(name_file,user_id)
        cur.execute(INSERT_MESSAGE, (full_name_file, t.strftime("%Y-%m-%d %H:%M:%S.%f"), user_id, 0, '1'))
        t = datetime.fromtimestamp(ttime.time())
        cur.execute(INSERT_MESSAGE, (answer, t.strftime("%Y-%m-%d %H:%M:%S.%f"), user_id, 0, '0'))
        history = get_history(user_id) + TAG_INPUT_WITH_ID % (user_id, user_id)
        return history
    elif not request.args.get('msg'):
        if not request.args.get('user_id'):
            history = get_history("") + NICKNAME + TAG_INPUT_WITOUT_ID
            return history
        else:
            user_id = request.args.get('user_id').strip()
            cur.execute(CHECK_USER, [user_id])
            if (cur.rowcount == 0):
                cur.execute(INSERT_USER, [user_id])
                message = "Привет, " + user_id + "!!! " + START_MESSAGE
                cur.execute(INSERT_MESSAGE, (message,t.strftime("%Y-%m-%d %H:%M:%S.%f"),user_id,0,'0'))
                history = get_history(user_id) + TAG_INPUT_WITH_ID % (user_id,user_id)
                return history
            else:
                message = "И снова здравствуй, " + user_id + "!!! " + START_MESSAGE
                cur.execute(INSERT_MESSAGE, (message, t.strftime("%Y-%m-%d %H:%M:%S.%f"), user_id, 0, '0'))
                history = get_history(user_id) + TAG_INPUT_WITH_ID % (user_id,user_id)
                return history
    else:
        user_id = request.args.get('user_id').strip()
        last_status = get_last_status(user_id)
        print(last_status)
        message = request.args.get('msg').strip().lower()
        cur.execute(INSERT_MESSAGE, (message, t.strftime("%Y-%m-%d %H:%M:%S.%f"), user_id, last_status, '1'))
        history = get_history(user_id)
        t = datetime.fromtimestamp(ttime.time())

        if message in START_COMMAND:
            cur.execute(INSERT_MESSAGE, (START_MESSAGE, t.strftime("%Y-%m-%d %H:%M:%S.%f"), user_id, 0, '0'))
            history += START_MESSAGE + "<br />" + t.strftime("%Y-%m-%d %H:%M")
        elif last_status == 2:
            cur.execute(INSERT_MESSAGE, (WRONG_EXP, t.strftime("%Y-%m-%d %H:%M:%S.%f"), user_id, 2, '0'))
            history += WRONG_EXP + "<br />" + t.strftime("%Y-%m-%d %H:%M")
        elif message in POSITIVE_ANSWER:
            if last_status == 0:
                cur.execute(INSERT_MESSAGE, (ADD_QUESTION, t.strftime("%Y-%m-%d %H:%M:%S.%f"), user_id, 1, '0'))
                history += ADD_QUESTION + "<br />" + t.strftime("%Y-%m-%d %H:%M")
            elif last_status == 1:
                cur.execute(INSERT_MESSAGE, (ITS_CAT, t.strftime("%Y-%m-%d %H:%M:%S.%f"), user_id, 2, '0'))
                history += ITS_CAT + "<br />" + t.strftime("%Y-%m-%d %H:%M")
        elif message in NEGATIVE_ANSWER:
            if last_status == 0:
                cur.execute(INSERT_MESSAGE, (ITS_CAT, t.strftime("%Y-%m-%d %H:%M:%S.%f"), user_id, 2, '0'))
                history += ITS_CAT + "<br />" + t.strftime("%Y-%m-%d %H:%M")
            elif last_status == 1:
                cur.execute(INSERT_MESSAGE, (ITS_BREAD, t.strftime("%Y-%m-%d %H:%M:%S.%f"), user_id, 2, '0'))
                history += ITS_BREAD + "<br />" + t.strftime("%Y-%m-%d %H:%M")
        else:
            cur.execute(INSERT_MESSAGE, (WRONG_EXP, t.strftime("%Y-%m-%d %H:%M:%S.%f"), user_id, last_status, '0'))
            history += WRONG_EXP + "<br />" + t.strftime("%Y-%m-%d %H:%M")
        history += TAG_INPUT_WITH_ID % (user_id,user_id)
        return history

if __name__ == "__main__":
    app.run(debug=False)