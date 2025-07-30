
from sqlalchemy import Column, Integer, String, Text, Date, Time, DECIMAL, Enum
from config.database import Base

class Evento(Base):
    __tablename__ = "eventos"
    
    id = Column(Integer, primary_key=True)
    nome = Column(String(100), nullable=False)
    tipo = Column(Enum("Show", "Evento", "Festival", "Teatro", "Exposição"), nullable=False)
    descricao = Column(Text)
    data_inicio = Column(Date)
    data_fim = Column(Date)
    horario = Column(Time)
    local = Column(String(100))
    endereco = Column(String(200))
    preco = Column(DECIMAL(10,2))
    capacidade = Column(Integer)
    organizador = Column(String(100))
    contato = Column(String(100))
    url_imagem = Column(String(255))