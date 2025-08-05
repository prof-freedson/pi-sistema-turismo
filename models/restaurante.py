from config.database import execute_query, execute_query_one

class Restaurante:
    def __init__(self, id=None, nome_restaurante=None, tipo_culinaria=None, 
                 descricao=None, endereco=None, bairro=None, telefone=None, 
                 horario_funcionamento=None, faixa_preco=None, capacidade=None, 
                 url_imagem=None, aceita_reservas=False, tem_delivery=False, 
                 tem_estacionamento=False):
        self.id = id
        self.nome_restaurante = nome_restaurante
        self.tipo_culinaria = tipo_culinaria
        self.descricao = descricao
        self.endereco = endereco
        self.bairro = bairro
        self.telefone = telefone
        self.horario_funcionamento = horario_funcionamento
        self.faixa_preco = faixa_preco
        self.capacidade = capacidade
        self.url_imagem = url_imagem
        self.aceita_reservas = aceita_reservas
        self.tem_delivery = tem_delivery
        self.tem_estacionamento = tem_estacionamento

    @staticmethod
    def get_all():
        """Retorna todos os restaurantes"""
        query = "SELECT * FROM restaurantes ORDER BY nome_restaurante ASC"
        return execute_query(query)

    @staticmethod
    def get_by_id(restaurante_id):
        """Retorna um restaurante pelo ID"""
        query = "SELECT * FROM restaurantes WHERE id = %s"
        return execute_query_one(query, (restaurante_id,))

    @staticmethod
    def create(restaurante_data):
        """Cria um novo restaurante"""
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
        """Atualiza um restaurante"""
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
        """Deleta um restaurante"""
        query = "DELETE FROM restaurantes WHERE id = %s"
        return execute_query(query, (restaurante_id,))

    @staticmethod
    def search(termo_busca):
        """Busca restaurantes por termo"""
        query = """
        SELECT * FROM restaurantes 
        WHERE nome_restaurante LIKE %s OR descricao LIKE %s OR bairro LIKE %s OR endereco LIKE %s
        ORDER BY nome_restaurante ASC
        """
        termo = f"%{termo_busca}%"
        return execute_query(query, (termo, termo, termo, termo))

    @staticmethod
    def filter_by_culinaria(tipo_culinaria):
        """Filtra restaurantes por tipo de culinária"""
        if tipo_culinaria == "Todas":
            return Restaurante.get_all()
        query = "SELECT * FROM restaurantes WHERE tipo_culinaria = %s ORDER BY nome_restaurante ASC"
        return execute_query(query, (tipo_culinaria,))

    @staticmethod
    def filter_by_preco(faixa_preco):
        """Filtra restaurantes por faixa de preço"""
        if faixa_preco == "Todas":
            return Restaurante.get_all()
        query = "SELECT * FROM restaurantes WHERE faixa_preco = %s ORDER BY nome_restaurante ASC"
        return execute_query(query, (faixa_preco,))

    @staticmethod
    def get_count():
        """Retorna o total de restaurantes"""
        query = "SELECT COUNT(*) as total FROM restaurantes"
        result = execute_query_one(query)
        return result['total'] if result else 0

