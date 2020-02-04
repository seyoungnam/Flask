import os
from flask import Flask, request, render_template, Markup, flash, redirect, url_for, make_response, abort, jsonify
from werkzeug.utils import secure_filename

app = Flask(__name__)

@app.route('/')
def index():
    return 'index'

@app.route('/hello/')
@app.route('/hello/<name>')
def hello(name=None):
    return render_template('hello.html', name=name)

@app.route('/markup/')
def markup():
    return Markup('<strong>Hello %s!</strong>') % '<blink>hacker</blink>'

#The Request Object
@app.route('/login', methods=['POST', 'GET'])
def login():
    error = None
    if request.method == 'POST':
        if valid_login(request.form['username'],
                       request.form['password']):
            return log_the_user_in(request.form['username'])
        else:
            error = 'Invalid username/password'
    # the code below is executed if the request method
    # was GET or the credentials were invalid
    return render_template('login.html', error=error)

# 추가로 작성해서 넣은 코드1
def valid_login(username, password):
    if username == 'seyoung' and password == '1234':
        return True
    else:
        return False

# 추가로 작성해서 넣은 코드2
def log_the_user_in(username):
    return render_template('hello.html', name=username)


# Uploads
UPLOAD_FOLDER = 'uploads'
ALLOWED_EXTENSIONS = {'txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif'}
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/upload', methods=['GET', 'POST'])
def upload_file():
    if request.method == 'POST':
        # check if the post request has the file part
        if 'file' not in request.files:
            flash('No file part')
            return redirect(request.url)
        file = request.files['file']
        # if user does not select file, browser also
        # submit an empty part without filename
        if file.filename == '':
            flash('No selected file')
            return redirect(request.url)
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            return render_template('upload.html', filename=filename)
    return '''
    <!doctype html>
    <title>Upload new File</title>
    <h1>Upload new File</h1>
    <form action="/upload" method=post enctype=multipart/form-data>
      <input type=file name=file>
      <input type=submit value=Upload>
    </form>
    '''


# Cookies
# Storing Cookies
@app.route('/store')
def store_cookies():
    resp = make_response(render_template('hello.html'))
    resp.set_cookie('username', 'seyoung')
    resp.set_cookie('theme', 'blue')
    resp.set_cookie('imgage', 'image example')
    return resp

# Reading Cookies
@app.route('/read')
def read_cookies():
    username = request.cookies.get('username')
    print(username)
    return Markup("<h2>불러온 쿠키값: %s</h2>" % username)



# Redirects and Errors

@app.route('/redirect')
def redirectFunction():
    return redirect(url_for('test_redirect'))

@app.route('/test_redirect')
def test_redirect():
    abort(401)
    this_is_never_executed()

@app.errorhandler(401)
def access_denied(error):
    return render_template('access_denied.html'), 401

@app.errorhandler(404)
def page_not_found(error):
    return render_template('page_not_found.html'), 404

# APIs with JSON
@app.route("/me")
def me_api():
    user = get_current_user()
    print("user.username : ", user.username)
    return {
        "username": user.username,
        "theme": user.theme,
        "image": user.image
        # "image": url_for("user_image", filename=user.image)
    }

class get_current_user():
    def __init__(self):
        self.username = 'nsy'
        self.theme = 'blue'
        self.image = 'pics.jpg'
    
# jsonify() 활용
# @app.route("/users")
# def users_api():
#     users = get_all_users()
#     return jsonify([user.to_jason() for user in users])

# class get_all_users():
#     def __init__(self):
#         self.user1 = '영수'
#         self.user2 = '동진'
#         self.user3 = '지현'
#         self.user4 = '수영'
    
#     def to_jason(self):
#         return [self.user1, self.user2, self.user3, self.user4]

# https://pythonise.com/series/learning-flask/working-with-json-in-flask
# json 데이터 받아오기
@app.route("/json", methods=["POST"])
def json_example():
    req = request.get_json()
    print(req)
    return "Thanks!", 200

# is_json을 통해 json 데이터인지 확인
@app.route("/jsonCheck", methods=["POST"])
def json_example2():
    if request.is_json:
        req = request.get_json()
        print(req)
        return "JSON received!", 200
    else:
        return "Request was not JSON", 400

# from flask import jsonify, make_response
@app.route("/jsonify", methods=["POST"])
def json_example3():
    if request.is_json:
        req = request.get_json()
        response_body = {
            "message": "JSON received!",
            "sender": req.get("name")
        }
        res = make_response(jsonify(response_body), 200)
        return res
    else:
        return make_response(jsonify({"message": "Request body must be JSON"}), 400)