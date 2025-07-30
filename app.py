from flask import Flask, render_template, request, redirect, url_for, flash, session, jsonify
from flask_cors import CORS
import mysql.connector
from datetime import datetime, date
import os
from config.database import get_db_connection
from controllers.evento_controller import EventoController
from controllers.restaurante_controller import RestauranteController
from controllers.dashboard_controller import DashboardController
from controllers.auth_controller import AuthController

app = Flask(__name__)
app.secret_key = 'encantos_da_ilha_secret_key_2025'

# Configurar CORS para permitir requisições de qualquer origem
CORS(app)

# Inicializar controllers
evento_controller = EventoController()
restaurante_controller = RestauranteController()
dashboard_controller = DashboardController()
auth_controller = AuthController()

# Importar rotas
from routes.web import *

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
