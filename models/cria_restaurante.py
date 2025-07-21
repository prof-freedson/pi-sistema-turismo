from config.db import get_db_connection

def cria_restaurante(nome, descricao, tipo_cozinha, horario_funcionamento, faixa_preco, capacidade, avaliacao, imagem, reservas, delivery, estacionamento, fone_1, fone_2, rua, numero, bairro, cidade, estado ):
    conn = get_db_connection()
    cursor = conn.cursor()

    try:
        # 1. Insere endereço
        cursor.execute("""
            INSERT INTO endereco (rua, numero, bairro, cidade, estado)
            VALUES (%s, %s, %s, %s, %s)
        """, (rua, numero, bairro, cidade, estado))
        id_end = cursor.lastrowid

        # 2. Insere telefone
        cursor.execute("""
            INSERT INTO telefone (fone_1, fone_2) VALUES (%s, %s)
        """, (fone_1, fone_2))
        id_tel = cursor.lastrowid

        # 3. Insere restaurante
        cursor.execute("""
            INSERT INTO restaurantes (nome, descricao, tipo_cozinha, horario_funcionamento, faixa_preco, capacidade, avaliacao, imagem, reservas, delivery, estacionamento, id_end, id_tel)
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
        """, (nome, descricao, tipo_cozinha, horario_funcionamento, faixa_preco, capacidade, avaliacao, imagem, reservas, delivery, estacionamento, id_end, id_tel))

        conn.commit()
    finally:
        cursor.close()
        conn.close()


