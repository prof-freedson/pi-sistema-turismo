
from flask import Blueprint, request, jsonify
from controllers.restaurante_controller import listar_restaurantes, criar_restaurante, atualizar_restaurante, deletar_restaurante

restaurante_bp = Blueprint("restaurante_bp", __name__, url_prefix="/restaurantes")

@restaurante_bp.route("/", methods=["GET"])
def get_restaurantes():
    return listar_restaurantes()

@restaurante_bp.route("/", methods=["POST"])
def post_restaurante():
    dados = request.json
    return criar_restaurante(dados)

@restaurante_bp.route("/<int:id>", methods=["PUT"])
def put_restaurante(id):
    dados = request.json
    return atualizar_restaurante(id, dados)

@restaurante_bp.route("/<int:id>", methods=["DELETE"])
def delete_restaurante(id):
    return deletar_restaurante(id)