"""Testes da camada de banco (db_services.py).

O psycopg2 é mockado: nenhum teste abre conexão real com o Supabase. Validam-se
o uso de queries parametrizadas, commit/rollback e fechamento de cursor/conexão.
"""

from unittest.mock import MagicMock, patch

import psycopg2
import pytest

from medalert import db_services


def _fake_conn_cursor():
    """Cria um par (conn, cursor) mockado com suporte a context/close."""
    cursor = MagicMock()
    conn = MagicMock()
    conn.cursor.return_value = cursor
    return conn, cursor


# --- get_db_connection ---

def test_get_db_connection_sem_url_levanta_erro(monkeypatch):
    monkeypatch.delenv("DATABASE_URL", raising=False)
    with pytest.raises(RuntimeError, match="DATABASE_URL"):
        db_services.get_db_connection()


# --- add_medication_db ---

def test_add_medication_db_insere_e_retorna_id(monkeypatch):
    monkeypatch.setenv("DATABASE_URL", "postgresql://fake")
    conn, cursor = _fake_conn_cursor()
    cursor.fetchone.return_value = [123]

    with patch.object(db_services.psycopg2, "connect", return_value=conn):
        new_id = db_services.add_medication_db("Dipirona", "500mg", "08:00")

    assert new_id == 123
    # query parametrizada (nunca interpolada) + valores passados separadamente
    sql, params = cursor.execute.call_args[0]
    assert "%s" in sql
    assert params == ("Dipirona", "500mg", "08:00")
    conn.commit.assert_called_once()
    cursor.close.assert_called_once()
    conn.close.assert_called_once()


def test_add_medication_db_erro_faz_rollback(monkeypatch):
    monkeypatch.setenv("DATABASE_URL", "postgresql://fake")
    conn, cursor = _fake_conn_cursor()
    cursor.execute.side_effect = psycopg2.Error("boom")

    with patch.object(db_services.psycopg2, "connect", return_value=conn):
        with pytest.raises(RuntimeError):
            db_services.add_medication_db("X", "Y", "08:00")

    conn.rollback.assert_called_once()
    conn.commit.assert_not_called()
    conn.close.assert_called_once()


# --- mark_as_taken_db ---

def test_mark_as_taken_db_true_quando_atualiza(monkeypatch):
    monkeypatch.setenv("DATABASE_URL", "postgresql://fake")
    conn, cursor = _fake_conn_cursor()
    cursor.rowcount = 1

    with patch.object(db_services.psycopg2, "connect", return_value=conn):
        assert db_services.mark_as_taken_db(5) is True

    sql, params = cursor.execute.call_args[0]
    assert "%s" in sql and params == (5,)
    conn.commit.assert_called_once()


def test_mark_as_taken_db_false_quando_id_inexistente(monkeypatch):
    monkeypatch.setenv("DATABASE_URL", "postgresql://fake")
    conn, cursor = _fake_conn_cursor()
    cursor.rowcount = 0

    with patch.object(db_services.psycopg2, "connect", return_value=conn):
        assert db_services.mark_as_taken_db(999) is False


# --- remove_medication_db ---

def test_remove_medication_db_true_quando_remove(monkeypatch):
    monkeypatch.setenv("DATABASE_URL", "postgresql://fake")
    conn, cursor = _fake_conn_cursor()
    cursor.rowcount = 1

    with patch.object(db_services.psycopg2, "connect", return_value=conn):
        assert db_services.remove_medication_db(5) is True

    conn.commit.assert_called_once()
    cursor.close.assert_called_once()
    conn.close.assert_called_once()


def test_remove_medication_db_false_quando_id_inexistente(monkeypatch):
    monkeypatch.setenv("DATABASE_URL", "postgresql://fake")
    conn, cursor = _fake_conn_cursor()
    cursor.rowcount = 0

    with patch.object(db_services.psycopg2, "connect", return_value=conn):
        assert db_services.remove_medication_db(999) is False
