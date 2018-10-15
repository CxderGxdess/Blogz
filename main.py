from flask import Flask, request, redirect, render_template

app = Flask(__name__)
app.config['DEBUG'] = True

tasks = []

@app.route('/', methods=['POST', 'GET'])
def index():
    
    if request.methon == 'POST':
        task = request.form['task']
        task.append(task)

    return render_template()

    
app.run()