from app import app
from models.restaurante import Restaurante

with app.app_context():
    restaurantes = Restaurante.query.all()
    for r in restaurantes:
        print(f"{r.id} - {r.nome} - {r.endereco}")
