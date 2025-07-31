import mysql.connector
from mysql.connector import Error

def get_db_connection():
    """
    Estabelece conexão com o banco de dados MySQL
    """
    try:
        connection = mysql.connector.connect(
            host='localhost',
            database='encantos_da_ilha',
            user='root',
            password='',
            charset='utf8mb4',
            collation='utf8mb4_unicode_ci'
        )
        return connection
    except Error as e:
        print(f"Erro ao conectar ao MySQL: {e}")
        return None

def execute_query(query, params=None):
    """
    Executa uma query no banco de dados
    """
    connection = get_db_connection()
    if connection is None:
        return None
    
    try:
        cursor = connection.cursor(dictionary=True)
        if params:
            cursor.execute(query, params)
        else:
            cursor.execute(query)
        
        if query.strip().upper().startswith('SELECT'):
            result = cursor.fetchall()
        else:
            connection.commit()
            result = cursor.rowcount
        
        return result
    except Error as e:
        print(f"Erro ao executar query: {e}")
        return None
    finally:
        if connection.is_connected():
            cursor.close()
            connection.close()

def execute_query_one(query, params=None):
    """
    Executa uma query e retorna apenas um resultado
    """
    connection = get_db_connection()
    if connection is None:
        return None
    
    try:
        cursor = connection.cursor(dictionary=True)
        if params:
            cursor.execute(query, params)
        else:
            cursor.execute(query)
        
        result = cursor.fetchone()
        return result
    except Error as e:
        print(f"Erro ao executar query: {e}")
        return None
    finally:
        if connection.is_connected():
            cursor.close()
            connection.close()