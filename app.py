from flask import Flask
from flask_cors import CORS
import os
import sys 
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from dotenv import load_dotenv
load_dotenv()
from config.database import get_db_connection
from controllers.evento_controller import EventoController
from controllers.restaurante_controller import RestauranteController
from controllers.dashboard_controller import DashboardController
from controllers.auth_controller import AuthController
from controllers.geochat_controller import GeoChatController
from models.restaurante import Restaurante  # opcional se quiser usar em utilitários
from werkzeug.utils import secure_filename  # opcional se quiser usar em utilitários




# 🔧 Inicializa o Flask antes de tudo
app = Flask(__name__)

# 📁 Pasta onde imagens serão armazenadas
app.config['UPLOAD_FOLDER'] = os.path.join('static', 'img')

# 🔑 Chave para sessões
app.secret_key = 'encantos_da_ilha_secret_key_2025'

# 📷 Extensões permitidas para imagens
app.config['ALLOWED_EXTENSIONS'] = {'png', 'jpg', 'jpeg', 'gif'}

# 🌍 Libera CORS para acesso externo
CORS(app)

# 🚀 Instancia os controllers
evento_controller = EventoController()
restaurante_controller = RestauranteController()
dashboard_controller = DashboardController()
auth_controller = AuthController()
geochat_controller = GeoChatController()

# 🔗 Importa as rotas (define todas as URLs da aplicação)
from routes.web import *

# 🚪 Ponto de entrada da aplicação
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)

