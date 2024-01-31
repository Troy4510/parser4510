import sqlite3

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
    
    
def add_product(db_folder:str, name:str, link:str, price:int):
    connection = sqlite3.connect(db_folder + 'sql_base.db')
    cursor = connection.cursor()
    query = 'INSERT INTO tProduct (name, link, price, sverka) VALUES (?, ?, ?, ?)'
    cursor.execute(query, (name, link, price, 'ok',))
    connection.commit()
    connection.close()