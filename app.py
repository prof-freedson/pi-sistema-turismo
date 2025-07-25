# App Projeto Integrador
from flask import Flask
from routes.evento_routes import evento_bp
from routes.restaurante_routes import restaurante_bp
from routes.usuario_routes import usuario_bp

app = Flask(__name__)

# Registro dos blueprints com prefixos opcionais
app.register_blueprint(evento_bp)
app.register_blueprint(restaurante_bp)
app.register_blueprint(usuario_bp)

@app.route('/')
def home():
    return 'API Encantos da Ilha funcionando!'

if __name__ == '__main__':
    app.run(debug=True)

print("Rotas registradas:")
for rule in app.url_map.iter_rules():
    print(rule)
