import sqlite3

added_products = 0
deleted_products = 0
updated_products = 0


#проверяет, создана ли база и при отсутствии создаёт базу+таблицы в ней
def check_base(db_folder:str):
    print('[sm.check_base]')
    connection = sqlite3.connect(db_folder + 'sql_base.db')
    cursor = connection.cursor()
    
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS tProduct (
    id INTEGER PRIMARY KEY,
    name TEXT,
    link TEXT,
    price INTEGER,
    sverka TEXT
    )
    ''')
    
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS tStat (
    date_upd TEXT,
    vsego INTEGER,
    insert_product INTEGER,
    delete_product INTEGER
    ) 
    ''')
    
    connection.commit()
    connection.close()
    

#добавляет очередную запись и ставит статус 'ok'   
def add_product(db_folder:str, name:str, link:str, price:int):
    connection = sqlite3.connect(db_folder + 'sql_base.db')
    cursor = connection.cursor()
    query = 'INSERT INTO tProduct (name, link, price, sverka) VALUES (?, ?, ?, ?)'
    cursor.execute(query, (name, link, price, 'ok'))
    connection.commit()
    connection.close()


#обновляет флаг на 'ok' и обновляет цену (даже если она не менялась)
def update_record(db_folder, id, price):
    connection = sqlite3.connect(db_folder + 'sql_base.db')
    cursor = connection.cursor()
    query = 'UPDATE tProduct SET price = ? WHERE id = ?'
    cursor.execute(query, (price, id))
    query = 'UPDATE tProduct SET sverka = ? WHERE id = ?'
    cursor.execute(query, ('ok', id))
    connection.commit()
    connection.close()
    #query = 'UPDATE tProduct SET sverka = ? WHERE sverka = ?', ('ok', 'need_check')


#возвращает количество записей в базе
def counter(db_folder):
    connection = sqlite3.connect(db_folder + 'sql_base.db')
    cursor = connection.cursor()
    cursor.execute('SELECT MAX(id) FROM tProduct')
    #'SELECT COUNT(*) FROM tProduct'
    read_count = cursor.fetchone()
    connection.close()
    counter = read_count[0]
    #print(type(counter))
    #counter = counter.replace('(','')
    #counter = counter.replace(',)','')
    #counter = int(counter)
    return(counter)


#извлекает запись из базы по PRIMARY_KEY
def read_record(db_folder, key):
    record = ()
    connection = sqlite3.connect(db_folder + 'sql_base.db')
    cursor = connection.cursor()
    query = 'SELECT * FROM tProduct WHERE id = ?'
    cursor.execute(query, key)
    record = cursor.fetchone()
    connection.close()
    #print(record)
    return record


#извлекает несколько записей из базы по PRIMARY_KEY
def read_records(db_folder, key, end):
    records = ()
    connection = connection = sqlite3.connect(db_folder + 'sql_base.db')
    cursor = connection.cursor()
    query = 'SELECT * FROM tProduct WHERE id >= ? AND id <= ?'
    cursor.execute(query, (str(key), str(end)))
    records = cursor.fetchall()
    connection.close()
    #print(records)
    return records


#проверяет есть ли запись в базе и обновляет/добавляет её
def check_record(db_folder, name, link, price):
    #added_products, updated_products
    connection = sqlite3.connect(db_folder + 'sql_base.db')
    cursor = connection.cursor()
    query = 'SELECT * FROM tProduct WHERE name = ? AND link = ?'
    cursor.execute(query, (name, link))
    record = cursor.fetchone()
    connection.close()
    if record == None: 
        add_product(db_folder, name, link, price)
        #return 'added'
        #added_products += 1
    else:
        key = record[0]
        update_record(db_folder, key, price)
        #return 'updated'
        #updated_products += 1
    
        
#меняет флаг всех записей в базе на 'need_check'    
def erase_sverka(db_folder):
    connection = sqlite3.connect(db_folder + 'sql_base.db')
    cursor = connection.cursor()
    cursor.execute('UPDATE tProduct SET sverka = ? WHERE sverka = ?', ('need_check', 'ok'))
    connection.commit()
    connection.close()
    
    
#удаляет записи со статусом 'need_check'
def erase_unchecked(db_folder):
    #deleted_products
    connection = sqlite3.connect(db_folder + 'sql_base.db')
    cursor = connection.cursor()
    query = 'DELETE FROM tProduct WHERE sverka = ?'
    cursor.execute(query, 'need_check')
    connection.commit()
    connection.close()
    

#ans = read_records('./parser4510/', 1, 5)
#print(ans)