from flask import Flask
from flask import request
from flask import render_template
import sql_module as sm

app = Flask(__name__, template_folder = 'app/templates')
main_folder = './parser4510/'


@app.route('/')
@app.route('/index.html')
def index():
    return render_template('index.html', data1 = 'one111', data2 = 'two222', data3 = 'three333')

@app.route('/products')
@app.route('/products.html')
def products():
    value = create_table_products(1,200)
    return render_template('products.html', value=value)


@app.route('/stat')
@app.route('/stat.html')
def create_table_stat():
    value = create_table_stat()
    return render_template('stat.html', value=value)


def create_table_products(key, end):
    records_value =()
    records_value = sm.read_records(main_folder, key, end)
    #print(records_value)
    return records_value


def create_table_stat():
    value = sm.read_stat(main_folder)
    return value


#create_table_products(1,10)
app.run(host='127.0.0.1', port=5050, debug=True)
print(sm.added_products)
sm.added_products +=1
print(sm.added_products)