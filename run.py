from flask import Flask, render_template, request, session, redirect, url_for, jsonify
import databaes
app = Flask(__name__)
app.config.from_object('config')  # 读取配置文件


@app.route('/')
def index():
    results = databaes.query_all('select * from t_article_type')
    #try:
    #    return render_template('index.html', username=session['username'], typies=results)
    #except KeyError:
    #    return render_template('index.html', typies=results)
    return render_template('index.html', typies=results)

@app.route('/list_article', methods={'POST', 'GET'})
def list_article():
    # page_num =
    if request.method == 'GET':
        type_id = request.args.get('typeId')
        print('**********', type_id)
        results = databaes.query_all('select * from t_article_type')
        return render_template('list_article.html', typies=results, nowTypeid=type_id)
    else:
        now_type_id = request.form.get('typeId')
        print('---------', now_type_id)
        if now_type_id != '0':
            sql = 'select art.*, type.* from ' \
                  't_article art, t_article_type type ' \
                  'where art.type_id=type.type_id '\
                  'and type.type_id=%s'
            articles = databaes.query_all(sql, (now_type_id,))
            # print(type_id)
            # print(articles)
            return jsonify(articles)
        else:
            sql_2 = 'select art.*, type.* from ' \
                  't_article art, t_article_type type ' \
                  'where art.type_id=type.type_id '
            articles = databaes.query_all(sql_2)
            print('/////////', articles)
            return jsonify(articles)

@app.route('/login',  methods=['POST', 'GET'])
def login():
    if request.method == 'GET':
        return render_template('login.html')
    else:
        username = request.form.get('username')
        password = request.form.get('password')
        art_id = request.form.get('id')
        result = databaes.query_one('select * from t_user where username=%s and password=%s', (username, password))
        if result:
            session['username'] = username
            session['userId'] = result['user_id']
            if not art_id:
                return redirect(url_for('index'))
            else:
                return 'ok'
        else:
            if not art_id:
                return render_template('login.html', error='用户名或密码错误')
            else:
                return 'not'

@app.route('/login_admin',  methods=['POST', 'GET'])
def login_admin():
    if request.method == 'GET':
        return render_template('admin_login.html')
    else:
        username = request.form.get('username')
        password = request.form.get('password')
        result = databaes.query_one('select * from t_admin where admin_name=%s and admin_password=%s', (username, password))
        if result:
            session['username'] = username
            try:
                session['userId'] = result['user_id']
            except KeyError:
                session['userId'] = result['admin_id']
            return redirect('/mgr_article')
        else:
            return '<script>alert(\'用户名或密码错误\')</script>'


@app.route('/logout')
def logout():
    session.pop('username')
    return redirect(url_for('index'))
    pass

@app.route('/regist', methods=['POST', 'GET'])
def regist():
    if request.method == 'GET':
        return render_template('regist.html')
    else:
        username = request.form.get('username')
        password = request.form.get('password')
        confirm_pass = request.form.get('passwordconfirm')
        email = request.form.get('email')

        if username == '':
            return render_template('regist.html', email=email, error='用户名不能为空')
        elif password != confirm_pass:
            return render_template('regist.html', email=email, error='密码不一致')
        elif len(password) < 6:
            return render_template('regist.html', email=email, error='密码太短')
        sql = "insert into t_user(username, password, email) values(%s, %s, %s)"
        row = databaes.update(sql, (username, password, email))
        if row > 0:
            return redirect(url_for('index'))
        else:
            return '注册失败'

@app.route('/check_name')
def check_name():
    # 接数据
    name = request.args.get('uname')
    # 连数据库
    result = databaes.query_one('select * from t_user where username=%s', (name,))
    # 返回结果
    # print(result)
    if result:
        return 'fail'
    else:
        return 'success'

@app.route('/article', methods=['POST', 'GET'])
def article():
    article_id_1 = request.args.get('articleId')
    article_id = request.form.get('articleId')
    types = databaes.query_all('select * from t_article_type')
    sql = 'select art.*, type.type_name from ' \
          't_article art, t_article_type type ' \
          'where art.type_id=type.type_id ' \
          'and art.article_id=%s'
    article = databaes.query_one(sql, (article_id_1,))
    sql2 = "select comm.*, usr.username,usr.portrait from t_comment comm, t_user usr " \
           "where comm.user_id=usr.user_id " \
           "and comm.article_id=%s"
    comments = databaes.query_all(sql2, (article_id_1,))
    comments_num = len(comments)
    if request.method == 'GET':
        return render_template('article.html', article_id=article_id_1, comments_num=comments_num, comments=comments, types=types, article=article)
        # print('************', jsonify(article, comments, types))
        # return render_template('article.html', allinfo=jsonify(article, comments, types))
        # return jsonify(article, comments, types)
    else:
        article = databaes.query_one(sql, (article_id,))
        # print(jsonify(article))
        return jsonify(article)

@app.route('/get_articles')
def get_articles():
    page_num = int(request.args.get('pageNum'))

    sql = 'select art.*, type.type_name ' \
          'from t_article art, t_article_type type ' \
          'where art.type_id=type.type_id ' \
          'limit %s, 3'

    result = databaes.query_all(sql, (page_num * 3))

    return jsonify(result)

@app.route('/check_login')
def check_login():
    username = session.get('username')
    if username:
        return 'ok'
    else:
        return 'not_ok'

@app.route('/mgr_comment')
def mgr_comment():
    sql = 'select art.article_id, art.title, com.*, usr.username ' \
          'from t_article art, t_comment com, t_user usr ' \
          'where com.article_id = art.article_id ' \
          'and com.user_id = usr.user_id'
    result = databaes.query_all(sql)
    print(result)
    return render_template('mgr_comment.html', results=result)

@app.route('/mgr_article')
def mge_article():
    sql = 'select art.*, type.type_name ' \
          'from t_article art, t_article_type type ' \
          'where art.type_id=type.type_id '
    result = databaes.query_all(sql)
    return render_template('mgr_article.html', articles=result)

@app.route('/delete_article')
def delete_article():
    article_id = request.args.get('articleId')
    row = databaes.update('delete from t_article where article_id=%s', (article_id,))
    if row > 0:
        return redirect('/mgr_article')
    else:
        return '删除失败'

@app.route('/delete_articles')
def delete_articles():
    article_ids = request.args.get('articleIds')
    print(article_ids)
    sql = 'delete from t_article where article_id in ('+article_ids+')'
    row = databaes.update(sql)
    if row > 0:
        return 'ok'
    else:
        return 'false'

@app.route('/edit_article', methods=['POST', 'GET'])
def edit_article():
    if request.method == 'POST':
        title = request.form.get('title')
        article = request.form.get('article')
        type = request.form.get('type')
        sql = 'insert into t_article(title, content, type_id) values(%s, %s, %s)'
        row = databaes.update(sql, (title, article, type))
        if row > 0:
            return 'ok'
        else:
            return 'error'
    else:
        types = databaes.query_all('select * from t_article_type')
        return render_template('edit_article.html', types=types)

@app.route('/change_article', methods=['POST', 'GET'])
def change_article():
    if request.method == 'GET':
        article_id = request.args.get('articleId')
        show = request.args.get('show')
        sql = 'select art.*, type.type_name from ' \
              't_article art, t_article_type type ' \
              'where art.type_id=type.type_id ' \
              'and art.article_id=%s'
        article = databaes.query_one(sql, (article_id,))
        types = databaes.query_all('select * from t_article_type')
        if show:
            return jsonify(article)
        return render_template('change_article.html', article=article, types=types)
    else:
        article_id = request.form.get('articleId')
        title = request.form.get('title')
        article = request.form.get('article')
        type = request.form.get('type')
        print(type)
        print(article)
        sql = 'update t_article set title=%s, content=%s, type_id=%s where article_id=%s'
        row = databaes.update(sql, (title, article, type, article_id))
        print(row)
        if row > 0:
            return 'ok'
        else:
            return 'error'

@app.route('/comment', methods=['POST'])
def comment():
    comment_text = request.form.get('commentText')
    user_id = request.form.get('userId')
    article_id = request.form.get('articleId')

    sql = 'insert into t_comment(content, user_id, article_id) values(%s, %s, %s)'
    row = databaes.update(sql, (comment_text, user_id, article_id))
    if row > 0:
        return 'ok'
    else:
        return 'no'

@app.route('/who_am_I')
def my_data():

    return render_template('who_am_I.html')



if __name__ == '__main__':
    app.run()


