# Database Configuration files

import pyodbc


# AST_MNG database server details
def get_db_connection():
    server = '192.168.0.100'
    database = 'AST_MNG'
    username = 'sa'
    password = 'scs@123'

    conn_str = (
        'DRIVER={ODBC Driver 17 for SQL Server};'
        'SERVER=' + server + ';'
        'DATABASE=' + database + ';'
        'UID=' + username + ';'
        'PWD=' + password
    )
    return pyodbc.connect(conn_str)
