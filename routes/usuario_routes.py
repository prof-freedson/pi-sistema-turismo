from flask import Blueprint
from controllers.usuario_controller import (
    listar_usuarios, criar_usuario
)

usuario_bp = Blueprint('usuario', __name__)

@usuario_bp.route('/usuarios', methods=['GET'])
def listar():
    return listar_usuarios()

@usuario_bp.route('/usuarios', methods=['POST'])
def criar():
    return criar_usuario()


