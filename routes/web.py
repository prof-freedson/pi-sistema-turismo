from app import app, evento_controller, restaurante_controller, dashboard_controller, auth_controller
from flask import render_template, request, flash

# 🏠 Rota principal - Página do Visitante
@app.route('/', methods=['GET'])
def visitante_principal():
    eventos = evento_controller.listar_publicos()
    restaurantes = restaurante_controller.listar_publicos()
    return render_template('visitante.html', eventos=eventos, restaurantes=restaurantes)



# 📊 Rota do Dashboard
@app.route('/dashboard')
def dashboard():
    return dashboard_controller.index()

# 🔐 Rotas de Autenticação
@app.route('/login', methods=['GET'])
def login_form():
    return auth_controller.login_form()

@app.route('/login', methods=['POST'])
def login():
    return auth_controller.login()

@app.route('/logout')
def logout():
    return auth_controller.logout()

@app.route('/cadastro-usuario', methods=['GET'])
def register_usuario_form():
    return auth_controller.register_usuario_form()

@app.route('/cadastro-usuario', methods=['POST'])
def register_usuario():
    return auth_controller.register_usuario()

@app.route('/cadastro-admin', methods=['GET'])
def register_admin_form():
    return auth_controller.register_admin_form()

@app.route('/cadastro-admin', methods=['POST'])
def register_admin():
    return auth_controller.register_admin()

# 🎭 Rotas de Eventos
@app.route('/eventos')
def eventos():
    return evento_controller.index()

@app.route('/eventos/<int:evento_id>')
def evento_show(evento_id):
    return evento_controller.show(evento_id)

@app.route('/eventos/novo', methods=['GET'])
def evento_create():
    return evento_controller.create()

@app.route('/eventos/novo', methods=['POST'])
def evento_store():
    return evento_controller.store()

@app.route('/eventos/<int:evento_id>/editar', methods=['GET'])
def evento_edit(evento_id):
    return evento_controller.edit(evento_id)

@app.route('/eventos/<int:evento_id>/editar', methods=['POST'])
def evento_update(evento_id):
    return evento_controller.update(evento_id)

@app.route('/eventos/<int:evento_id>/deletar', methods=['POST'])
def evento_delete(evento_id):
    return evento_controller.delete(evento_id)

# 🍽️ Rotas de Restaurantes
@app.route('/restaurantes')
def restaurantes():
    return restaurante_controller.index()

@app.route('/restaurantes/<int:restaurante_id>')
def restaurante_show(restaurante_id):
    return restaurante_controller.show(restaurante_id)

@app.route('/restaurantes/novo', methods=['GET'])
def restaurante_create():
    return restaurante_controller.create()

@app.route('/restaurantes/novo', methods=['POST'])
def restaurante_store():
    return restaurante_controller.store()

@app.route('/restaurantes/<int:restaurante_id>/editar', methods=['GET'])
def restaurante_edit(restaurante_id):
    return restaurante_controller.edit(restaurante_id)

@app.route('/restaurantes/<int:restaurante_id>/editar', methods=['POST'])
def restaurante_update(restaurante_id):
    return restaurante_controller.update(restaurante_id)

@app.route('/restaurantes/<int:restaurante_id>/deletar', methods=['POST'])
def restaurante_delete(restaurante_id):
    return restaurante_controller.delete(restaurante_id)
