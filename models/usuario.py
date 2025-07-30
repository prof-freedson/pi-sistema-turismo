from config.database import execute_query, execute_query_one
import hashlib

class Usuario:
    def __init__(self, id=None, nome=None, email=None, senha=None):
        self.id = id
        self.nome = nome
        self.email = email
        self.senha = senha

    @staticmethod
    def get_all():
        """Retorna todos os usuários"""
        query = "SELECT id, nome, email, data_criacao FROM usuarios ORDER BY nome ASC"
        return execute_query(query)

    @staticmethod
    def get_by_id(usuario_id):
        """Retorna um usuário pelo ID"""
        query = "SELECT id, nome, email, data_criacao FROM usuarios WHERE id = %s"
        return execute_query_one(query, (usuario_id,))

    @staticmethod
    def get_by_email(email):
        """Retorna um usuário pelo email"""
        query = "SELECT * FROM usuarios WHERE email = %s"
        return execute_query_one(query, (email,))

    @staticmethod
    def create(usuario_data):
        """Cria um novo usuário"""
        # Hash da senha
        senha_hash = hashlib.sha256(usuario_data['senha'].encode()).hexdigest()
        
        query = "INSERT INTO usuarios (nome, email, senha) VALUES (%s, %s, %s)"
        params = (usuario_data['nome'], usuario_data['email'], senha_hash)
        return execute_query(query, params)

    @staticmethod
    def update(usuario_id, usuario_data):
        """Atualiza um usuário"""
        if 'senha' in usuario_data and usuario_data['senha']:
            # Se há nova senha, fazer hash
            senha_hash = hashlib.sha256(usuario_data['senha'].encode()).hexdigest()
            query = "UPDATE usuarios SET nome = %s, email = %s, senha = %s WHERE id = %s"
            params = (usuario_data['nome'], usuario_data['email'], senha_hash, usuario_id)
        else:
            # Se não há nova senha, não atualizar
            query = "UPDATE usuarios SET nome = %s, email = %s WHERE id = %s"
            params = (usuario_data['nome'], usuario_data['email'], usuario_id)
        
        return execute_query(query, params)

    @staticmethod
    def delete(usuario_id):
        """Deleta um usuário"""
        query = "DELETE FROM usuarios WHERE id = %s"
        return execute_query(query, (usuario_id,))

    @staticmethod
    def authenticate(email, senha):
        """Autentica um usuário"""
        senha_hash = hashlib.sha256(senha.encode()).hexdigest()
        query = "SELECT id, nome, email FROM usuarios WHERE email = %s AND senha = %s"
        return execute_query_one(query, (email, senha_hash))

    @staticmethod
    def email_exists(email):
        """Verifica se o email já existe"""
        query = "SELECT COUNT(*) as count FROM usuarios WHERE email = %s"
        result = execute_query_one(query, (email,))
        return result['count'] > 0 if result else False

