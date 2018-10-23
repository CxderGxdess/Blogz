from flask import Flask, request, redirect, render_template
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['DEBUG'] = True
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://Blogz:2kidsandablog@localhost:8889/blogz'
app.config['SQLALCHEMY_ECHO'] = True
db = SQLAlchemy(app)

class Blog(db.Model):

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(120))
    body = db.Column(db.String(240))

    def __init__(self, title, body):
        self.title = title

class User(db.Model):

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(240))
    password = db.Column(db.String(20))




blogs = []    

@app.route('/', methods = ['POST', 'GET'])
def index():
     
    if request.method == 'POST':
        blog = request.form['blog']
        blogs.append(blog)

    return render_template('blog.html',title="Blogz", blogs=blogs)

@app.route('/blog', methods=['GET'])
def blog():
    if request.args:
        id = request.args.get('id')
        query = Blog.query.get(id)
        return render_template('single_post.html', post=query)
    else:
        query = Blog.query.all()
        return render_template('blog.html', blog=query)


@app.route('/newpost', methods=['POST', 'GET'])
def newpost():
    if request.method == 'POST':
        title = request.form['title']
        body = request.form['body']
        title_error=''
        body_error=''
        if not title:
            title_error = "You Must Enter a Title For Your Post!"
        if not body:
            body_error = "You Must Enter A Body For Your Entry!"
        if not title_error and not body_error:
            new = Blog(title,body)
            db.session.add(new)
            db.session.commit()
            return redirect('./blog?id='+ str(new.id))

@app.route('/signup', methods=['GET','POST'])

@app.route('/login', methods=['GET','POST'])

@app.route('logout', methods=['POST'])



        return render_template('new_post.html',title_error=title_error, body_error=body_error, title=title, body=body)
    else:
        return render_template('new_post.html')


if __name__ == '__main__':    
    app.run()