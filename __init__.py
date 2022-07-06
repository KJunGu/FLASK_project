from flask import Flask, render_template, request, url_for, session, redirect
from datetime import datetime
import sqlite3




app = Flask(__name__)
app.secret_key = "super secret key"

@app.before_request
def before_request():
    scheme = request.headers.get('X-Forwarded-Proto')
    if scheme and scheme == 'http' and request.url.startswith('http://'):
        url = request.url.replace('http://', 'https://', 1)
        code = 301
        return redirect(url, code=code)

@app.route("/")
def mainpage():
    if session:
        conn = sqlite3.connect('temp.db')
        cur = conn.cursor()
        cur.execute("SELECT NAME FROM user WHERE ID = '%s'" %session['ID'])
        userid = cur.fetchall()
        cur.execute("SELECT * FROM user WHERE ID = '%s'" %session['ID'])
        asdf = cur.fetchall()
        print(session['ID'])
        print(asdf)
        return render_template("main.html", userid=userid)
    else:
        return render_template("main.html")

@app.route("/admin")
def admin():
    conn = sqlite3.connect('temp.db')
    cur = conn.cursor()
    cur.execute("SELECT * FROM user")
    userInfo = cur.fetchall()
    userLen = len(userInfo)
    return render_template("관리자.html", userInfo=userInfo, userLen=userLen)

@app.route("/login")
def loginpage():
    return render_template("login.html")

@app.route("/register")
def register():
    return render_template("회원가입.html")

#####################################로그인, 회원가입 기능##########################################
@app.route("/sign-up-proc/", methods=['POST'])
def signupproc():
    ID = request.form['ID']
    PSW = request.form['PSW']
    PSW_repeat = request.form['PSW_repeat']
    NAME = request.form['NAME']
    EMAIL = request.form['EMAIL']
    QUESTION = request.form['question']

    conn = sqlite3.connect('temp.db')
    cur = conn.cursor()

    if PSW == PSW_repeat:
        cur.execute("SELECT ID FROM user WHERE ID = '%s'" %ID)
        chk_id = cur.fetchall()
        if chk_id == []:
            sql = "INSERT INTO user(ID, PSW, NAME, EMAIL, QUESTION) VALUES(?, ?, ?, ?, ?)"
            cur.execute(sql, (ID, PSW, NAME, EMAIL, QUESTION))
            conn.commit()
            
            return '''<script>alert("회원가입이 완료되었습니다."); window.location.href="/";</script>'''

        else:
            return '''<script>alert("이미 존재하는 계정입니다.");history.go(-1);</script>'''
    else:
        return '''<script>alert("비밀번호가 맞지 않습니다.");history.go(-1);</script>'''

@app.route("/sign-in-proc/", methods=['POST'])
def signinproc():
    conn = sqlite3.connect('temp.db')
    cur = conn.cursor()
    ID = request.form['ID']
    PSW = request.form['PSW']

    cur.execute("SELECT ID FROM user WHERE ID = '%s'" %ID)
    chk_id = cur.fetchall()

    if chk_id == []:
        return '''<script>alert("존재하지 않는 계정입니다.");history.go(-1);</script>'''
    
    elif chk_id[0][0] == "admin":
        return redirect('/admin')
    else:
        cur.execute("SELECT PSW FROM user WHERE ID = '%s'" %ID)
        chk_psw = cur.fetchall()
        print(chk_psw, PSW)
        if PSW == chk_psw[0][0]:          # 자료형이 같은지 확인해야함
            session['ID'] = ID
            cur.execute("SELECT NAME FROM USER WHERE ID = '%s'" %ID)
            chk_name = cur.fetchall()
            cur.execute("SELECT NAME FROM user WHERE ID = '%s'" %session['ID'])
            userid = cur.fetchall()
            return render_template("main.html", userid=userid)
        else:
            return '''<script>alert("비밀번호가 맞지 않습니다.");history.go(-1);</script>'''

@app.route("/findid")
def findid():
    return render_template("아이디 찾기.html")

@app.route("/findpw")
def findpw():
    return render_template("비밀번호 찾기.html")

@app.route("/findid_", methods=['POST'])
def findid_():
    NAME = request.form['NAME']
    EMAIL = request.form['EMAIL']
    conn = sqlite3.connect('temp.db')
    cur = conn.cursor()
    cur.execute("SELECT NAME, EMAIL FROM user WHERE NAME = '%s' and EMAIL = '%s'" %(NAME, EMAIL))
    chk_id = cur.fetchall()
    print(chk_id)
    if chk_id == []:
        return '''<script>alert("이름 또는 이메일이 맞지 않습니다.");history.go(-1);</script>'''
    else:
        cur.execute(f"SELECT ID FROM user WHERE NAME = '{NAME}' and EMAIL = '{EMAIL}'")
        asdf = cur.fetchall()

        return f'''<script>alert("회원님의 아이디는 {asdf[0][0]}입니다.");window.location.href="/login";</script>'''


################################################################################################

@app.route("/logout", methods=['GET'])
def logout():
    session.pop('ID', None)
    return redirect('/')

@app.route("/form")
def form():
    if session:
        conn = sqlite3.connect('temp.db')
        cur = conn.cursor()
        cur.execute("SELECT NAME FROM user WHERE ID = '%s'" %session['ID'])
        userid = cur.fetchall()
        return render_template("form.html", userid=userid)
    else:
        return '''<script>alert("로그인 해주세요"); window.location.href="/login";</script>'''

@app.route("/form/add", methods=['GET','POST'])
def form_add():
    TITLE = request.form['title']
    CONTENTS = request.form['contents']
    uploaded_files = request.files["file1"]
    
    if session == {}:
        return '''<script>alert("로그인 해주세요"); window.location.href="/login";</script>'''
    else:
        conn = sqlite3.connect("temp.db")
        cur = conn.cursor()
        cur.execute("SELECT NAME FROM user WHERE ID = '%s'" %session['ID'])
        userid = cur.fetchall()
        cur.execute(f"INSERT INTO board(TITLE, CONTENTS, TIME, NAME) values('{TITLE}', '{CONTENTS}', '{datetime.now()}', '{userid[0][0]}')")
        cur.execute("SELECT seq FROM board")
        board_seq = cur.fetchall()
        imgname = board_seq[len(board_seq)-1][0]
        conn.commit()
        uploaded_files.save("static/images/{}.jpeg".format(imgname))
        return '''<script>alert("글이 저장되었습니다.");window.location.href="/gesipan";</script>'''

@app.route("/gesipan")
def gesipan():
    conn = sqlite3.connect("temp.db")
    cur = conn.cursor()
    if session == {}:
        cur.execute("SELECT * FROM board")
        gesi = cur.fetchall()
        len_seq = len(gesi)
        return render_template("게시판.html", len_seq=len_seq, gesi=gesi)
    else:    
        cur.execute("SELECT NAME FROM user WHERE ID = '%s'" %session['ID'])
        userid = cur.fetchall()
        cur.execute("SELECT * FROM board")
        gesi = cur.fetchall()
        len_seq = len(gesi)
        print(gesi)
        return render_template("게시판.html", len_seq=len_seq, gesi=gesi, userid=userid)

@app.route("/update/<uid>", methods=["GET","POST"])
def update(uid):
    if request.method == "POST":
        TITLE = request.form['title']
        CONTENTS = request.form['contents']
        uploaded_files = request.files["file1"]
        print(uid)
        conn = sqlite3.connect("temp.db")
        cur = conn.cursor()
        cur.execute("SELECT * FROM board;")
        board_seq = cur.fetchall()
        seq = board_seq[int(uid)][0]
        cur.execute(f"UPDATE board SET TITLE='{TITLE}', CONTENTS='{CONTENTS}' WHERE seq = {seq}")
        conn.commit()
        uploaded_files.save("static/images/{}.jpeg".format(seq))
        return '''<script>alert("글이 저장되었습니다.");window.location.href="/gesipan";</script>'''


    else:
        conn = sqlite3.connect("temp.db")
        cur = conn.cursor()
        cur.execute("SELECT NAME FROM user WHERE ID = '%s'" %session['ID'])
        userid = cur.fetchall()
        return render_template("formtest.html",userid=userid,uid=uid)

@app.route("/delete/<uid>")
def delete(uid):
    conn = sqlite3.connect("temp.db")
    cur = conn.cursor()
    cur.execute("SELECT * FROM board;")
    board_seq = cur.fetchall()
    seq = board_seq[int(uid)][0]
    print(uid,seq)
    cur.execute(f"DELETE FROM board WHERE seq = {seq}")
    conn.commit()
    return '''<script>alert("글이 삭제되었습니다.");window.location.href="/gesipan";</script>'''

@app.route("/mypage")
def mypage():
    conn = sqlite3.connect('temp.db')
    cur = conn.cursor()
    cur.execute("SELECT * FROM user WHERE ID = '%s'" %session['ID'])
    userid = cur.fetchall()
    return render_template("마이페이지.html", userid=userid)

@app.route("/article/<seq>")
def article(seq):
    conn = sqlite3.connect("temp.db")
    cur = conn.cursor()
    if session == {}:
        cur.execute("SELECT * FROM board")
        gesi = cur.fetchall()
        len_seq = len(gesi)
        return render_template("testtest.html", len_seq=len_seq, gesi=gesi, seq=int(seq))
    else:
        print(session['ID'])
        cur.execute("SELECT NAME FROM user WHERE ID = '%s'" %session['ID'])
        userid = cur.fetchall()
        cur.execute("SELECT * FROM board")
        gesi = cur.fetchall()
        len_seq = len(gesi)
        print(gesi)
        print(gesi[int(seq)-1][4])
        print(userid)
        return render_template("testtest.html", len_seq=len_seq, gesi=gesi, seq=int(seq), userid=userid)

@app.route("/userDel/<seq>")
def userDel(seq):
    conn = sqlite3.connect("temp.db")
    cur = conn.cursor()
    cur.execute("SELECT * FROM user;")
    userdel = cur.fetchall()
    cur.execute(f"DELETE FROM user WHERE ID = '{userdel[int(seq)][0]}'")
    conn.commit()
    return '''<script>alert("회원정보가 삭제되었습니다.");window.location.href="/admin";</script>'''

if __name__ == "__main__":
    app.run(host='127.0.0.1', port=5000, debug=True)
    