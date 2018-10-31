from flask import Flask, request, redirect, render_template, session, flash
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['DEBUG'] = True
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://Blogz:2kidsandablog@localhost:8889/blogz'
app.config['SQLALCHEMY_ECHO'] = True
db = SQLAlchemy(app)
app.secret_key = 'jazzy44:john:316'

class Blog(db.Model):

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(120))
    body = db.Column(db.String(240))
    owner_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)

    def __init__(self, title, body, owner):
        self.title = title
        self.body = body
        self.owner = owner

class User(db.Model):

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(240), unique=True)
    password = db.Column(db.String(20))
    blogs = db.relationship('Blog', backref='owner')

    def __init__(self, username, password):
        self.username = username
        self.password = password


@app.route('/login', methods=['GET','POST'])
def login():

    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        user = User.query.filter_by(username=username).first()

        if user and user.password == password:
            session['username'] = username
            flash("Logged in")
            return redirect('/newpost')
        else:
            flash('User password incorrect, or user does not exist', 'error')
    
    return render_template('login.html')

@app.before_request
def require_login():
    allowed_routes = ['index','login', 'list_blogs', 'signup', 'logout']

    if request.endpoint not in allowed_routes and 'username' not in session:
        return redirect('/login')

@app.route('/blog', methods=['GET'])
def blog():

    
    blog_id = request.args.get('id')
    blog_user = request.args.get('user')

    if blog_id:
        blog_post = Blog.query.get(blog_id)
        return render_template('blog_entry.html', blog_post=blog_post)

    if blog_user:
        user = User.query.filter_by(username=blog_user).first()
        blog_post = Blog.query.filter_by(owner=user).all()
        return render_template('singleUser.html', blog_post=blog_post, username=blog_user)

    else:
        blog_post = Blog.query.all()
        return render_template('blog.html', title="Build a Blog", blog_post=blog_post) 


@app.route('/signup', methods=['GET','POST'])
def signup():

    if request.method == "POST":
        username = request.form['username']
        pwd = request.form['password']
        verify = request.form['verify']

        username_error = ''
        password1_error = ''
        password2_error = ''
        error_check = False

        user = User.query.filter_by(username=username).first()
        if user != None:
            print(user.username)

        if user != None:
            if user.username == username:
                username_error = 'Username already exists'
                error_check = True

        elif username == '':
            username_error = 'Thats not a valid Username'
            error_check = True

        elif ' ' in username:
            username_error = 'Username cannot contain a space'
            error_check = True

        elif len(username) < 3 or len(username) > 20:
            username_error = 'Username must be between 3 and 20 characters long'
            error_check = True

        if pwd == '':
            password1_error = 'Thats not a valid Password'
            error_check = True

        elif ' ' in pwd:
            password1_error = 'Password cannot contain a space'
            error_check = True

        elif len(pwd) < 3 or len(pwd) > 20:
            password1_error = 'Password must be between 3 and 20 characters long'
            error_check = True

        if not (pwd == verify):
            password1_error = 'Passwords dont match'
            password2_error = 'Passwords dont match'
            error_check = True

        if error_check == True:
            return render_template('signup.html', username_error = username_error, password1_error = password1_error, password2_error = password2_error)
        else:
            new_user = User(username, pwd)
            db.session.add(new_user)
            db.session.commit()
            session['username'] = username
            return redirect('/newpost')

    return render_template('signup.html')    


@app.route('/newpost', methods=['POST', 'GET'])
def newpost():

    owner = User.query.filter_by(username=session['username']).first()
    title_error = ""
    body_error = ""

    if request.method == 'POST' :
        title = request.form['title']
        body = request.form['body']

        if len(title) == 0:
            title_error = "Invalid title"
            
        if len(body) == 0:
            body_error = "Invalid body"

        if len(title) != 0 and len(body) !=  0:
            blog_post = Blog(title, body, owner)
            db.session.add(blog_post)
            db.session.commit()
            id = blog_post.id
            return redirect('/blog?id={0}'.format(id))
     
        else:
            return render_template("new_post.html",
            title=title,
            body=body,
            title_error=title_error,
            body_error=body_error )

    return render_template('new_post.html')


@app.route('/blog', methods=['GET'])
def list_blogs():
    blog_id = request.args.get('id')
    blog_user = request.args.get('user')

    if blog_user:
        user = User.query.filter_by(username=blog_user).first()
        blog_post = Blog.query.filter_by(owner=user).all()
        return render_template('singleUser.html', blog_post=blog_post, username=blog_user)

    elif blog_id:
        blog_post = Blog.query.get(blog_id)
        return render_template('blog_entry.html', blog_post=blog_post)
    else:
        blogs = Blog.query.all()
        return render_template('blog.html',  title="Blogz", blog_post=blogs_post)


@app.route('/logout')       
def logout():
    
    del session['username']
    return redirect('/blog')

@app.route('/')
def index():
    users = User.query.all()
    return render_template('index.html', users=users)        




if __name__ == '__main__':    
    app.run()