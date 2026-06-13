import os

from flask import Flask, jsonify, request

from medalert.services import validate_time_format
from medalert.db_services import (
    add_medication_db,
    list_medications_db,
    mark_as_taken_db,
    remove_medication_db,
)

app = Flask(__name__)


@app.route("/")
def home():
    return jsonify({
        "project": "MedAlert CLI",
        "status": "online",
        "message": "Deploy ativo no Render",
        "endpoints": {
            "listar": "GET /medicamentos",
            "adicionar": "POST /medicamentos",
            "marcar_tomado": "PATCH /medicamentos/<id>/tomar",
            "remover": "DELETE /medicamentos/<id>",
        },
    })


@app.route("/medicamentos", methods=["GET"])
def listar_medicamentos():
    try:
        medications = list_medications_db()
        return jsonify(medications), 200
    except RuntimeError as e:
        return jsonify({"erro": str(e)}), 500


@app.route("/medicamentos", methods=["POST"])
def adicionar_medicamento():
    data = request.get_json(silent=True) or {}

    name = str(data.get("nome", "")).strip()
    dosage = str(data.get("dosagem", "")).strip()
    time = str(data.get("horario", "")).strip()

    if not name:
        return jsonify({"erro": "O campo 'nome' é obrigatório."}), 400
    if not dosage:
        return jsonify({"erro": "O campo 'dosagem' é obrigatório."}), 400
    if not validate_time_format(time):
        return jsonify({"erro": "Horário inválido. Use o formato HH:MM."}), 400

    try:
        new_id = add_medication_db(name, dosage, time)
        return jsonify({
            "id": new_id,
            "nome": name,
            "dosagem": dosage,
            "horario": time,
            "tomado": False,
        }), 201
    except RuntimeError as e:
        return jsonify({"erro": str(e)}), 500


@app.route("/medicamentos/<int:med_id>/tomar", methods=["PATCH"])
def marcar_tomado(med_id):
    try:
        if mark_as_taken_db(med_id):
            return jsonify({"mensagem": "Medicamento marcado como tomado.", "id": med_id}), 200
        return jsonify({"erro": "Nenhum medicamento encontrado com esse ID."}), 404
    except RuntimeError as e:
        return jsonify({"erro": str(e)}), 500


@app.route("/medicamentos/<int:med_id>", methods=["DELETE"])
def remover_medicamento(med_id):
    try:
        if remove_medication_db(med_id):
            return jsonify({"mensagem": "Medicamento removido.", "id": med_id}), 200
        return jsonify({"erro": "Nenhum medicamento encontrado com esse ID."}), 404
    except RuntimeError as e:
        return jsonify({"erro": str(e)}), 500


if __name__ == "__main__":
    port = int(os.environ.get("PORT", 10000))
    app.run(host="0.0.0.0", port=port)
