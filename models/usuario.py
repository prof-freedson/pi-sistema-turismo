from sqlalchemy import Column, Integer, String, Enum
from config.database import Base

class Usuario(Base):
    __tablename__ = "usuarios"
    
    id = Column(Integer, primary_key=True)
    nome = Column(String(100), nullable=False)
    email = Column(String(100), nullable=False, unique=True)
    senha = Column(String(255), nullable=False)
    tipo = Column(Enum("admin", "usuario"), default="usuario")
