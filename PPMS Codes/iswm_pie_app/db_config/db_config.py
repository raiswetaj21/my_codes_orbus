# Database Configuration files

import pyodbc


# AST_MNG database server details
def get_db_connection():
    server = '3.6.47.39'
    database = 'SWMsystem'
    username = 'webadmin'
    password = 'Admin@123!@#'

    conn_str = (
        'DRIVER={ODBC Driver 17 for SQL Server};'
        'SERVER=' + server + ';'
        'DATABASE=' + database + ';'
        'UID=' + username + ';'
        'PWD=' + password
    )
    return pyodbc.connect(conn_str)
