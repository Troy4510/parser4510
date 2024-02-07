from flask import Flask
from flask import request
from flask import render_template

app = Flask(__name__, template_folder = 'app/templates')

@app.route('/')
@app.route('/index.html')
def index():
    return render_template('index.html', data1 = 'one111', data2 = 'two222', data3 = 'three333')

@app.route('/2')
def page_two():
    return 'page_two'

app.run(host='1c.k-desk.ru', port=88, debug=True)