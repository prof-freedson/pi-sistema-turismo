from sqlalchemy import Column, Integer, String, Text, Boolean, Enum
from config.database import Base

class Restaurante(Base):
    __tablename__ = "restaurantes"
    
    id = Column(Integer, primary_key=True)
    nome = Column(String(100), nullable=False)
    tipo_culinaria = Column(Enum("Brasileira", "Maranhense", "Italiana", "Japonesa", "Mexicana", "Francesa"), nullable=False)
    descricao = Column(Text)
    endereco = Column(String(200))
    bairro = Column(String(100))
    telefone = Column(String(20))
    horario_funcionamento = Column(String(100))
    faixa_preco = Column(Enum("$", "$$", "$$$", "$$$$"), nullable=False)
    capacidade = Column(Integer)
    aceita_reservas = Column(Boolean, default=False)
    tem_delivery = Column(Boolean, default=False)
    tem_estacionamento = Column(Boolean, default=False)
    url_imagem = Column(String(255))
