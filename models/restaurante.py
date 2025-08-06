from config.database import execute_query, execute_query_one

class Restaurante:
    def __init__(self, **kwargs):
        self.id = kwargs.get('id')
        self.nome_restaurante = kwargs.get('nome_restaurante')
        self.tipo_culinaria = kwargs.get('tipo_culinaria')
        self.descricao = kwargs.get('descricao')
        self.endereco = kwargs.get('endereco')
        self.bairro = kwargs.get('bairro')
        self.telefone = kwargs.get('telefone')
        self.horario_funcionamento = kwargs.get('horario_funcionamento')
        self.faixa_preco = kwargs.get('faixa_preco')
        self.capacidade = kwargs.get('capacidade')
        self.url_imagem = kwargs.get('url_imagem')
        self.aceita_reservas = kwargs.get('aceita_reservas', False)
        self.tem_delivery = kwargs.get('tem_delivery', False)
        self.tem_estacionamento = kwargs.get('tem_estacionamento', False)
        self.data_criacao = kwargs.get('data_criacao')
        self.data_atualizacao = kwargs.get('data_atualizacao')



    @staticmethod
    def get_all():
        """Retorna todos os restaurantes como objetos"""
        query = "SELECT * FROM restaurantes ORDER BY nome_restaurante ASC"
        resultados = execute_query(query)
        return [Restaurante(**r) for r in resultados]  # Transformação em objetos

    @staticmethod
    def get_by_id(restaurante_id):
        query = "SELECT * FROM restaurantes WHERE id = %s"
        resultado = execute_query_one(query, (restaurante_id,))
        return Restaurante(**resultado) if resultado else None

    @staticmethod
    def create(restaurante_data):
        query = """
        INSERT INTO restaurantes (nome_restaurante, tipo_culinaria, descricao, endereco, 
                                bairro, telefone, horario_funcionamento, faixa_preco, 
                                capacidade, url_imagem, aceita_reservas, tem_delivery, 
                                tem_estacionamento)
        VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
        """
        params = (
            restaurante_data['nome_restaurante'], restaurante_data['tipo_culinaria'],
            restaurante_data['descricao'], restaurante_data['endereco'],
            restaurante_data['bairro'], restaurante_data['telefone'],
            restaurante_data['horario_funcionamento'], restaurante_data['faixa_preco'],
            restaurante_data['capacidade'], restaurante_data['url_imagem'],
            restaurante_data.get('aceita_reservas', False),
            restaurante_data.get('tem_delivery', False),
            restaurante_data.get('tem_estacionamento', False)
        )
        return execute_query(query, params)

    @staticmethod
    def update(restaurante_id, restaurante_data):
        query = """
        UPDATE restaurantes SET nome_restaurante = %s, tipo_culinaria = %s, 
                              descricao = %s, endereco = %s, bairro = %s, 
                              telefone = %s, horario_funcionamento = %s, 
                              faixa_preco = %s, capacidade = %s, url_imagem = %s, 
                              aceita_reservas = %s, tem_delivery = %s, 
                              tem_estacionamento = %s
        WHERE id = %s
        """
        params = (
            restaurante_data['nome_restaurante'], restaurante_data['tipo_culinaria'],
            restaurante_data['descricao'], restaurante_data['endereco'],
            restaurante_data['bairro'], restaurante_data['telefone'],
            restaurante_data['horario_funcionamento'], restaurante_data['faixa_preco'],
            restaurante_data['capacidade'], restaurante_data['url_imagem'],
            restaurante_data.get('aceita_reservas', False),
            restaurante_data.get('tem_delivery', False),
            restaurante_data.get('tem_estacionamento', False),
            restaurante_id
        )
        return execute_query(query, params)

    @staticmethod
    def delete(restaurante_id):
        query = "DELETE FROM restaurantes WHERE id = %s"
        return execute_query(query, (restaurante_id,))

    @staticmethod
    def search(termo_busca):
        query = """
        SELECT * FROM restaurantes 
        WHERE nome_restaurante LIKE %s OR descricao LIKE %s OR bairro LIKE %s OR endereco LIKE %s
        ORDER BY nome_restaurante ASC
        """
        termo = f"%{termo_busca}%"
        resultados = execute_query(query, (termo, termo, termo, termo))
        return [Restaurante(**r) for r in resultados]

    @staticmethod
    def filter_by_culinaria(tipo_culinaria):
        if tipo_culinaria == "Todas":
            return Restaurante.get_all()
        query = "SELECT * FROM restaurantes WHERE tipo_culinaria = %s ORDER BY nome_restaurante ASC"
        resultados = execute_query(query, (tipo_culinaria,))
        return [Restaurante(**r) for r in resultados]

    @staticmethod
    def filter_by_preco(faixa_preco):
        if faixa_preco == "Todas":
            return Restaurante.get_all()
        query = "SELECT * FROM restaurantes WHERE faixa_preco = %s ORDER BY nome_restaurante ASC"
        resultados = execute_query(query, (faixa_preco,))
        return [Restaurante(**r) for r in resultados]

    @staticmethod
    def get_count():
        query = "SELECT COUNT(*) as total FROM restaurantes"
        result = execute_query_one(query)
        return result['total'] if result else 0
