from config.database import execute_query, execute_query_one
from datetime import datetime, date

class Evento:
    def __init__(self, id=None, nome_evento=None, tipo=None, descricao=None, 
                 data_inicio=None, data_fim=None, horario=None, local=None, 
                 endereco=None, preco=None, capacidade=None, organizador=None, 
                 contato=None, url_imagem=None, data_criacao=None, data_atualizacao=None):
        self.id = id
        self.nome_evento = nome_evento
        self.tipo = tipo
        self.descricao = descricao
        self.data_inicio = data_inicio
        self.data_fim = data_fim
        self.horario = horario
        self.local = local
        self.endereco = endereco
        self.preco = preco
        self.capacidade = capacidade
        self.organizador = organizador
        self.contato = contato
        self.url_imagem = url_imagem
        self.data_criacao = data_criacao
        self.data_atualizacao = data_atualizacao

    @staticmethod
    def get_all():
        """Retorna todos os eventos como objetos"""
        query = "SELECT * FROM eventos ORDER BY data_inicio DESC"
        resultados = execute_query(query)
        return [Evento(**r) for r in resultados] if resultados else []

    @staticmethod
    def get_by_id(evento_id):
        """Retorna um evento pelo ID"""
        query = "SELECT * FROM eventos WHERE id = %s"
        resultado = execute_query_one(query, (evento_id,))
        return Evento(**resultado) if resultado else None

    @staticmethod
    def create(evento_data):
        """Cria um novo evento"""
        query = """
        INSERT INTO eventos (nome_evento, tipo, descricao, data_inicio, data_fim, 
                           horario, local, endereco, preco, capacidade, organizador, 
                           contato, url_imagem)
        VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
        """
        params = (
            evento_data['nome_evento'], evento_data['tipo'], evento_data['descricao'],
            evento_data['data_inicio'], evento_data['data_fim'], evento_data['horario'],
            evento_data['local'], evento_data['endereco'], evento_data['preco'],
            evento_data['capacidade'], evento_data['organizador'], evento_data['contato'],
            evento_data['url_imagem']
        )
        return execute_query(query, params)

    @staticmethod
    def update(evento_id, evento_data):
        """Atualiza um evento"""
        query = """
        UPDATE eventos SET nome_evento = %s, tipo = %s, descricao = %s, 
                          data_inicio = %s, data_fim = %s, horario = %s, 
                          local = %s, endereco = %s, preco = %s, capacidade = %s, 
                          organizador = %s, contato = %s, url_imagem = %s
        WHERE id = %s
        """
        params = (
            evento_data['nome_evento'], evento_data['tipo'], evento_data['descricao'],
            evento_data['data_inicio'], evento_data['data_fim'], evento_data['horario'],
            evento_data['local'], evento_data['endereco'], evento_data['preco'],
            evento_data['capacidade'], evento_data['organizador'], evento_data['contato'],
            evento_data['url_imagem'], evento_id
        )
        return execute_query(query, params)

    @staticmethod
    def delete(evento_id):
        """Deleta um evento"""
        query = "DELETE FROM eventos WHERE id = %s"
        return execute_query(query, (evento_id,))

    @staticmethod
    def search(termo_busca):
        """Busca eventos por termo"""
        query = """
        SELECT * FROM eventos 
        WHERE nome_evento LIKE %s OR descricao LIKE %s OR local LIKE %s OR organizador LIKE %s
        ORDER BY data_inicio DESC
        """
        termo = f"%{termo_busca}%"
        resultados = execute_query(query, (termo, termo, termo, termo))
        return [Evento(**r) for r in resultados] if resultados else []

    @staticmethod
    def filter_by_type(tipo):
        """Filtra eventos por tipo"""
        if tipo == "Todos":
            return Evento.get_all()
        query = "SELECT * FROM eventos WHERE tipo = %s ORDER BY data_inicio DESC"
        resultados = execute_query(query, (tipo,))
        return [Evento(**r) for r in resultados] if resultados else []

    @staticmethod
    def filter_by_status(status):
        """Filtra eventos por status (próximos ou realizados)"""
        hoje = date.today()
        if status == "proximos":
            query = "SELECT * FROM eventos WHERE data_inicio >= %s ORDER BY data_inicio ASC"
            resultados = execute_query(query, (hoje,))
            return [Evento(**r) for r in resultados] if resultados else []
        elif status == "realizados":
            query = "SELECT * FROM eventos WHERE data_fim < %s ORDER BY data_inicio DESC"
            resultados = execute_query(query, (hoje,))
            return [Evento(**r) for r in resultados] if resultados else []
        else:
            return Evento.get_all()

    @staticmethod
    def get_count():
        """Retorna o total de eventos"""
        query = "SELECT COUNT(*) as total FROM eventos"
        result = execute_query_one(query)
        return result['total'] if result else 0

    @staticmethod
    def get_eventos_hoje():
        """Retorna eventos de hoje"""
        hoje = date.today()
        query = "SELECT COUNT(*) as total FROM eventos WHERE data_inicio = %s"
        result = execute_query_one(query, (hoje,))
        return result['total'] if result else 0

    @staticmethod
    def get_locais_unicos():
        """Retorna o número de locais únicos"""
        query = "SELECT COUNT(DISTINCT local) as total FROM eventos"
        result = execute_query_one(query)
        return result['total'] if result else 0

    @staticmethod
    def get_proximos_eventos(limit=5):
        """Retorna os próximos eventos"""
        hoje = date.today()
        query = "SELECT * FROM eventos WHERE data_inicio >= %s ORDER BY data_inicio ASC LIMIT %s"
        resultados = execute_query(query, (hoje, limit))
        return [Evento(**r) for r in resultados] if resultados else []

