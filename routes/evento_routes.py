from flask import Blueprint
from controllers.evento_controller import (
    listar_eventos, criar_evento, atualizar_evento, deletar_evento
)

evento_bp = Blueprint('evento', __name__)

@evento_bp.route('/eventos', methods=['GET'])
def listar():
    return listar_eventos()

@evento_bp.route('/eventos', methods=['POST'])
def criar():
    return criar_evento()

@evento_bp.route('/eventos/<int:id>', methods=['PUT'])
def atualizar(id):
    return atualizar_evento(id)

@evento_bp.route('/eventos/<int:id>', methods=['DELETE'])
def deletar(id):
    return deletar_evento(id)