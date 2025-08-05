from config.database import execute_query, execute_query_one
import hashlib

class Administrador:
    def __init__(self, id=None, nome=None, email=None, senha=None):
        self.id = id
        self.nome = nome
        self.email = email
        self.senha = senha

    @staticmethod
    def get_all():
        """Retorna todos os administradores"""
        query = "SELECT id, nome, email, data_criacao FROM administradores ORDER BY nome ASC"
        return execute_query(query)

    @staticmethod
    def get_by_id(admin_id):
        """Retorna um administrador pelo ID"""
        query = "SELECT id, nome, email, data_criacao FROM administradores WHERE id = %s"
        return execute_query_one(query, (admin_id,))

    @staticmethod
    def get_by_email(email):
        """Retorna um administrador pelo email"""
        query = "SELECT * FROM administradores WHERE email = %s"
        return execute_query_one(query, (email,))

    @staticmethod
    def create(admin_data):
        """Cria um novo administrador"""
        # Hash da senha
        senha_hash = hashlib.sha256(admin_data['senha'].encode()).hexdigest()
        
        query = "INSERT INTO administradores (nome, email, senha) VALUES (%s, %s, %s)"
        params = (admin_data['nome'], admin_data['email'], senha_hash)
        return execute_query(query, params)

    @staticmethod
    def update(admin_id, admin_data):
        """Atualiza um administrador"""
        if 'senha' in admin_data and admin_data['senha']:
            # Se há nova senha, fazer hash
            senha_hash = hashlib.sha256(admin_data['senha'].encode()).hexdigest()
            query = "UPDATE administradores SET nome = %s, email = %s, senha = %s WHERE id = %s"
            params = (admin_data['nome'], admin_data['email'], senha_hash, admin_id)
        else:
            # Se não há nova senha, não atualizar
            query = "UPDATE administradores SET nome = %s, email = %s WHERE id = %s"
            params = (admin_data['nome'], admin_data['email'], admin_id)
        
        return execute_query(query, params)

    @staticmethod
    def delete(admin_id):
        """Deleta um administrador"""
        query = "DELETE FROM administradores WHERE id = %s"
        return execute_query(query, (admin_id,))

    @staticmethod
    def authenticate(email, senha):
        """Autentica um administrador"""
        senha_hash = hashlib.sha256(senha.encode()).hexdigest()
        query = "SELECT id, nome, email FROM administradores WHERE email = %s AND senha = %s"
        return execute_query_one(query, (email, senha_hash))

    @staticmethod
    def email_exists(email):
        """Verifica se o email já existe"""
        query = "SELECT COUNT(*) as count FROM administradores WHERE email = %s"
        result = execute_query_one(query, (email,))
        return result['count'] > 0 if result else False

