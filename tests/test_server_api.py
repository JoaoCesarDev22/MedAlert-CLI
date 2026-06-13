"""Testes das rotas da API Flask (server.py).

As funções de banco (db_services) são mockadas no namespace de `medalert.server`,
portanto estes testes são determinísticos e NÃO dependem do Supabase / rede.
"""

from unittest.mock import patch

import pytest

from medalert.server import app


@pytest.fixture
def client():
    app.config["TESTING"] = True
    return app.test_client()


# --- Rota de status ---

def test_home_status_ok(client):
    resp = client.get("/")
    assert resp.status_code == 200
    body = resp.get_json()
    assert body["status"] == "online"
    assert "endpoints" in body


# --- READ: GET /medicamentos ---

def test_listar_medicamentos_ok(client):
    fake = [
        {"id": 1, "nome": "Dipirona", "dosagem": "500mg", "horario": "08:00", "tomado": False},
    ]
    with patch("medalert.server.list_medications_db", return_value=fake) as mock_list:
        resp = client.get("/medicamentos")

    assert resp.status_code == 200
    assert resp.get_json() == fake
    mock_list.assert_called_once()


def test_listar_medicamentos_erro_banco_retorna_500(client):
    with patch("medalert.server.list_medications_db", side_effect=RuntimeError("falha no banco")):
        resp = client.get("/medicamentos")

    assert resp.status_code == 500
    assert "erro" in resp.get_json()


# --- CREATE: POST /medicamentos ---

def test_adicionar_medicamento_ok(client):
    with patch("medalert.server.add_medication_db", return_value=42) as mock_add:
        resp = client.post(
            "/medicamentos",
            json={"nome": "Ibuprofeno", "dosagem": "200mg", "horario": "12:30"},
        )

    assert resp.status_code == 201
    body = resp.get_json()
    assert body["id"] == 42
    assert body["nome"] == "Ibuprofeno"
    assert body["tomado"] is False
    mock_add.assert_called_once_with("Ibuprofeno", "200mg", "12:30")


def test_adicionar_sem_nome_retorna_400(client):
    with patch("medalert.server.add_medication_db") as mock_add:
        resp = client.post("/medicamentos", json={"dosagem": "200mg", "horario": "12:30"})

    assert resp.status_code == 400
    assert "erro" in resp.get_json()
    mock_add.assert_not_called()


def test_adicionar_sem_dosagem_retorna_400(client):
    with patch("medalert.server.add_medication_db") as mock_add:
        resp = client.post("/medicamentos", json={"nome": "Ibuprofeno", "horario": "12:30"})

    assert resp.status_code == 400
    mock_add.assert_not_called()


def test_adicionar_horario_invalido_retorna_400(client):
    with patch("medalert.server.add_medication_db") as mock_add:
        resp = client.post(
            "/medicamentos",
            json={"nome": "Ibuprofeno", "dosagem": "200mg", "horario": "99:99"},
        )

    assert resp.status_code == 400
    mock_add.assert_not_called()


# --- UPDATE: PATCH /medicamentos/<id>/tomar ---

def test_marcar_tomado_ok(client):
    with patch("medalert.server.mark_as_taken_db", return_value=True) as mock_mark:
        resp = client.patch("/medicamentos/7/tomar")

    assert resp.status_code == 200
    assert resp.get_json()["id"] == 7
    mock_mark.assert_called_once_with(7)


def test_marcar_tomado_id_inexistente_retorna_404(client):
    with patch("medalert.server.mark_as_taken_db", return_value=False):
        resp = client.patch("/medicamentos/999/tomar")

    assert resp.status_code == 404
    assert "erro" in resp.get_json()


# --- DELETE: DELETE /medicamentos/<id> ---

def test_remover_medicamento_ok(client):
    with patch("medalert.server.remove_medication_db", return_value=True) as mock_rm:
        resp = client.delete("/medicamentos/7")

    assert resp.status_code == 200
    assert resp.get_json()["id"] == 7
    mock_rm.assert_called_once_with(7)


def test_remover_id_inexistente_retorna_404(client):
    with patch("medalert.server.remove_medication_db", return_value=False):
        resp = client.delete("/medicamentos/999")

    assert resp.status_code == 404
    assert "erro" in resp.get_json()


def test_remover_erro_banco_retorna_500(client):
    with patch("medalert.server.remove_medication_db", side_effect=RuntimeError("db down")):
        resp = client.delete("/medicamentos/1")

    assert resp.status_code == 500
    assert "erro" in resp.get_json()
