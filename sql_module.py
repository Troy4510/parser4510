import sqlite3

def create_base(way1:str):
    connection = sqlite3.connect(way1 + 'tamaris.db')
    connection.close()
    print('base create complete')

def sm_test():
    print('test_ok')