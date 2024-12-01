from flask import Blueprint, request, jsonify
from flasgger import swag_from
from dao.mae_dao import MaeDAO
from criptoData.dados.mae import Mae

mae_api = Blueprint("mae_api", __name__)
mae_dao = MaeDAO()

@mae_api.route("/mae", methods=["POST"])
@swag_from({
    "responses": {
        200: {"description": "Mãe inserida com sucesso."}
    }
})
def inserir_mae():
    """Insere um novo registro na tabela `mae`."""
    data = request.get_json()
    nome = data.get("nome")
    if not nome:
        return jsonify({"error": "Nome é obrigatório."}), 400
    mae_dao.inserir(Mae(nome=nome))
    return jsonify({"message": "Mãe inserida com sucesso."})

@mae_api.route("/mae/<int:id>", methods=["PUT"])
@swag_from({
    "responses": {
        200: {"description": "Mãe alterada com sucesso."},
        404: {"description": "Mãe não encontrada."}
    }
})
def alterar_mae(id):
    """Altera um registro na tabela `mae`."""
    data = request.get_json()
    novo_nome = data.get("nome")
    if not novo_nome:
        return jsonify({"error": "Nome é obrigatório."}), 400
    maes = mae_dao.consultar()
    if not any(mae.id == id for mae in maes):
        return jsonify({"error": "Mãe não encontrada."}), 404
    mae_dao.alterar(id, novo_nome)
    return jsonify({"message": "Mãe alterada com sucesso."})

@mae_api.route("/mae", methods=["GET"])
@swag_from({
    "responses": {
        200: {"description": "Lista de mães retornada com sucesso."}
    }
})
def consultar_mae():
    """Consulta todas as mães."""
    maes = mae_dao.consultar()
    return jsonify([mae.__dict__ for mae in maes])

@mae_api.route("/mae/<int:id>", methods=["DELETE"])
@swag_from({
    "responses": {
        200: {"description": "Mãe excluída com sucesso."},
        404: {"description": "Mãe não encontrada."}
    }
})
def excluir_mae(id):
    """Exclui logicamente um registro na tabela `mae`."""
    maes = mae_dao.consultar()
    if not any(mae.id == id for mae in maes):
        return jsonify({"error": "Mãe não encontrada."}), 404
    mae_dao.excluir(id)
    return jsonify({"message": "Mãe excluída com sucesso."})
