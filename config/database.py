import os
import sys
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import mysql.connector
from mysql.connector import Error
from dotenv import load_dotenv

# Carrega variáveis de ambiente do arquivo .env
load_dotenv()
port=os.getenv('DB_PORT', 3306)  # Padrão para MySQL é 3306, mas pode ser alterado
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
            port=port,
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
        cursor.execute(query, params) if params else cursor.execute(query)

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
        cursor.execute(query, params) if params else cursor.execute(query)

        return cursor.fetchone()
    except Error as e:
        print(f"Erro ao executar query: {e}")
        return None
    finally:
        if connection.is_connected():
            cursor.close()
            connection.close()
