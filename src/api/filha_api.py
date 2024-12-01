from flask import Blueprint, request, jsonify
from flasgger import swag_from
from criptoData.dao.filha_dao import FilhaDAO
from criptoData.dados.filha import Filha

filha_api = Blueprint("filha_api", __name__)
filha_dao = FilhaDAO()

@filha_api.route("/filha", methods=["POST"])
@swag_from({
    "responses": {
        200: {"description": "Filha inserida com sucesso."}
    }
})
def inserir_filha():
    """Insere um novo registro na tabela `filha`."""
    data = request.get_json()
    nome = data.get("nome")
    idMae = data.get("idMae")
    if not nome or not idMae:
        return jsonify({"error": "Nome e idMae são obrigatórios."}), 400
    filha_dao.inserir(Filha(nome=nome, idMae=idMae))
    return jsonify({"message": "Filha inserida com sucesso."})

@filha_api.route("/filha/<int:id>", methods=["PUT"])
@swag_from({
    "responses": {
        200: {"description": "Filha alterada com sucesso."},
        404: {"description": "Filha não encontrada."}
    }
})
def alterar_filha(id):
    """Altera um registro na tabela `filha`."""
    data = request.get_json()
    novo_nome = data.get("nome")
    if not novo_nome:
        return jsonify({"error": "Nome é obrigatório."}), 400
    filhas = filha_dao.consultar()
    if not any(filha.id == id for filha in filhas):
        return jsonify({"error": "Filha não encontrada."}), 404
    filha_dao.alterar(id, novo_nome)
    return jsonify({"message": "Filha alterada com sucesso."})

@filha_api.route("/filha", methods=["GET"])
@swag_from({
    "responses": {
        200: {"description": "Lista de filhas retornada com sucesso."}
    }
})
def consultar_filha():
    """Consulta todas as filhas."""
    filhas = filha_dao.consultar()
    return jsonify([filha.__dict__ for filha in filhas])

@filha_api.route("/filha/<int:id>", methods=["DELETE"])
@swag_from({
    "responses": {
        200: {"description": "Filha excluída com sucesso."},
        404: {"description": "Filha não encontrada."}
    }
})
def excluir_filha(id):
    """Exclui logicamente um registro na tabela `filha`."""
    filhas = filha_dao.consultar()
    if not any(filha.id == id for filha in filhas):
        return jsonify({"error": "Filha não encontrada."}), 404
    filha_dao.excluir(id)
    return jsonify({"message": "Filha excluída com sucesso."})
