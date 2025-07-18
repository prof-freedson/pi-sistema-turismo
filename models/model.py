# model.py
# model.py
from config.db import get_db_connection

class TodosEventos:
    # Lista todos os eventos cadastrados
    @staticmethod
    def listar_todos():
        conn = get_db_connection()
        cursor = conn.cursor(dictionary=True)
        cursor.execute('SELECT * FROM eventos')
        eventos = cursor.fetchall()
        cursor.close()
        conn.close()
        return eventos
    
     # Busca eventos
    @staticmethod
    def buscar_por_id(id_pac):
        conn = get_db_connection()
        cursor = conn.cursor(dictionary=True)
        cursor.execute('SELECT * FROM eventos WHERE id = %s', (id,))
        evento = cursor.fetchone()
        cursor.close()
        conn.close()
        return evento

    # Cria um novo evento
    @staticmethod
    def criar(nome,tipo, descricao, data_inicio, data_fim, horario, local, endereco, preco, capacidade, organizador, contato, imagem_url):
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute('INSERT INTO eventos (nome, tipo, descricao, data_inicio, data_fim, horario, local, endereco, preco, capacidade, organizador, contato, imagem_url) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)',
                       (nome,tipo, descricao, data_inicio, data_fim, horario, local, endereco, preco, capacidade, organizador, contato, imagem_url))

        conn.commit()
        cursor.close()
        conn.close()
