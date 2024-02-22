import sqlite3

added_products = 0
deleted_products = 0


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
    id INTEGER PRIMARY KEY,
    date_upd TEXT,
    vsego INTEGER,
    insert_product INTEGER,
    delete_product INTEGER)
    ''')
    
    cursor.execute('INSERT INTO tStat(vsego) VALUES (0)')
    cursor.execute('DELETE FROM tStat WHERE id > 1')
                     
    connection.commit()
    connection.close()
    

#добавляет очередную запись и ставит статус 'ok'   
def add_product(db_folder:str, name:str, link:str, price:int):
    global added_products
    added_products += 1 #учитывает количество прибавок в базе для статистики
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
    connection = sqlite3.connect(db_folder + 'sql_base.db')
    cursor = connection.cursor()
    query = 'SELECT * FROM tProduct WHERE name = ? AND link = ?'
    cursor.execute(query, (name, link))
    record = cursor.fetchone()
    connection.close()
    
    if record == None: 
        add_product(db_folder, name, link, price)
    else:
        key = record[0]
        update_record(db_folder, key, price)
    
        
#меняет флаг всех записей в базе на 'need_check'    
def erase_sverka(db_folder):
    connection = sqlite3.connect(db_folder + 'sql_base.db')
    cursor = connection.cursor()
    cursor.execute('UPDATE tProduct SET sverka = ? WHERE sverka = ?', ('need_check', 'ok'))
    connection.commit()
    connection.close()
    
    
#удаляет записи со статусом 'need_check', возвращает количество удалённых
def erase_unchecked(db_folder):
    global deleted_products
    deleted_products +=1 #для статистики удалено продуктов
    connection = sqlite3.connect(db_folder + 'sql_base.db')
    cursor = connection.cursor()
    query = 'DELETE FROM tProduct WHERE sverka = ?'
    cursor.execute(query, ('need_check',))
    connection.commit()
    connection.close()
    

#выдача статистики из tStat
def read_stat(db_folder):
    connection = sqlite3.connect(db_folder+'sql_base.db')
    cursor = connection.cursor()
    query = 'SELECT * FROM tStat WHERE id = 1'
    cursor.execute(query)
    stat = cursor.fetchall()
    connection.close()
    return stat


#запись статистики в tStat
def write_stat(db_folder, date, total, inserted, deleted):
    connection = sqlite3.connect(db_folder+'sql_base.db')
    cursor = connection.cursor()
    query = ''' UPDATE tStat 
                SET date_upd = ?,
                    vsego = ?,
                    insert_product = ?,
                    delete_product = ?
                WHERE id = 1'''
    cursor.execute(query, (date, total, inserted, deleted,))
    connection.commit()
    connection.close()
    

if __name__ == "__main__": #при импорте модуля не выполняется
    #ans = read_records('./parser4510/', 1, 5)
    #print(ans)
    #write_stat('./parser4510/', '15_10_25', 1,2,3)
    #check_base('./parser4510/')
    #added_products += 1
    #print(read_stat('./parser4510/'))
    pass