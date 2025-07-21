from config.db import get_db_connection

def atualizar_restaurante(id_restaurante, nome, descricao, tipo_cozinha, horario_funcionamento, faixa_preco, capacidade, avaliacao, imagem, reservas, delivery, estacionamento, fone_1, fone_2, rua, numero, bairro, cidade, estado):
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)

    try:
        # Busca IDs relacionados
        cursor.execute("SELECT id_end, id_tel FROM restaurantes WHERE id_restaurante = %s", (id_restaurante,))
        dados = cursor.fetchone()
        if not dados:
            return False

        id_end = dados["id_end"]
        id_tel = dados["id_tel"]

        # Atualiza endereço
        cursor.execute("""
            UPDATE endereco
            SET rua=%s, numero=%s, bairro=%s, cidade=%s, estado=%s
            WHERE id_end=%s
        """, (rua, numero, bairro, cidade, estado, id_end))

        # Atualiza telefone
        cursor.execute("""
            UPDATE telefone SET tel_1=%s, tel_2=%s WHERE id_tel=%s
        """, (fone_1, fone_2, id_tel))

        # Atualiza nome do restaurante
        cursor.execute("""
            UPDATE restaurantes SET nome=%s, descricao=%s, tipo_cozinha=%s, horario_funcionamento=%s, faixa_preco=%s, capacidade=%s, avaliacao=%s, imagem=%s, reservas=%s, delivery=%s, estacionamento=%s WHERE id_restaurante=%s
        """, (nome, descricao, tipo_cozinha, horario_funcionamento, faixa_preco, capacidade, avaliacao, imagem, reservas, delivery, estacionamento, id_restaurante))

        conn.commit()
        return True
    finally:
        cursor.close()
        conn.close()
