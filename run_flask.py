from flask import Flask
from flask import request
from flask import render_template
import sql_module as sm

app = Flask(__name__, template_folder = 'app/templates', static_folder = 'app/static')
main_folder = './parser4510/'


@app.route('/')
@app.route('/index.html')
def index():
    stat_value = sm.read_stat(main_folder)
    product_value = create_table_products(1,50)
    return render_template('index.html', stat = stat_value, products = product_value)

@app.route('/products')
@app.route('/products.html')
def products():
    value = create_table_products(1,200)
    return render_template('products.html', value=value)


@app.route('/stat')
@app.route('/stat.html')
def create_table_stat():
    value = sm.read_stat(main_folder)
    print(type(value))
    print(type(value[0]))
    print(value[0][0])
    print(value[0][1])
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