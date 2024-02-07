from flask import Flask
from flask import request
from flask import render_template

app = Flask(__name__, template_folder = 'app/templates')

@app.route('/')
@app.route('/index.html')
def index():
    return render_template('index.html')

@app.route('/2')
def page_two():
    return 'page_two'

app.run(host='127.0.0.1', port=5000, debug=True)