# Configuração do banco de dados
import os
from dotenv import load_dotenv
import mysql.connector

# Carrega variáveis do arquivo .env
load_dotenv()

def get_db_connection():
    return mysql.connector.connect(
        host=os.getenv('HOST'),
        user=os.getenv('USER'),
        password=os.getenv('PASSWORD'),
        database=os.getenv('DATABASE')
    )