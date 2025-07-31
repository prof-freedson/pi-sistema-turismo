#alteração das configurações do banco de dados e nome do arquivo
import os
from dotenv import load_dotenv
import mysql.connector
from mysql.connector import Error

load_dotenv()
# Carrega as variáveis de ambiente do arquivo .env
def get_db_connection():
    """
    Estabelece conexão com o banco de dados MySQL
    """
    try:
        connection = mysql.connector.connect(
            host=os.getenv('DB_HOST'),
            database=os.getenv('DB_NAME'),
            user=os.getenv('DB_USER'),
            password=os.getenv('DB_PASSWORD'),
            charset=os.getenv('DB_CHARSET'),
            collation=os.getenv('DB_COLLATION')
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

