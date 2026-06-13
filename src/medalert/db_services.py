"""Camada de acesso ao banco de dados PostgreSQL (Supabase).

Substitui a persistência antiga em arquivo (data.json). Todas as operações
de CRUD usam psycopg2 puro, com abertura/fechamento explícitos de cursor e
conexão no bloco finally.
"""

import os
from typing import List

import psycopg2
from psycopg2.extras import RealDictCursor

try:
    from dotenv import load_dotenv

    load_dotenv()
except ImportError:  # pragma: no cover - python-dotenv é opcional em runtime
    pass


def get_db_connection():
    """Abre uma conexão com o PostgreSQL usando a DATABASE_URL.

    Lê a variável de ambiente DATABASE_URL. Caso não esteja definida (ex: em
    um ambiente de testes sem .env), levanta um erro claro em vez de falhar
    com uma mensagem genérica do driver — esse é o "fallback seguro".
    """
    database_url = os.getenv("DATABASE_URL")

    if not database_url:
        raise RuntimeError(
            "DATABASE_URL não configurada. Crie um arquivo .env na raiz do "
            "projeto com a string de conexão do PostgreSQL (Supabase)."
        )

    return psycopg2.connect(database_url)


def add_medication_db(name: str, dosage: str, time: str) -> int:
    """Insere um medicamento e retorna o ID gerado pelo banco."""
    conn = None
    cursor = None
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute(
            """
            INSERT INTO medicamentos (nome, dosagem, horario)
            VALUES (%s, %s, %s)
            RETURNING id
            """,
            (name, dosage, time),
        )
        new_id = cursor.fetchone()[0]
        conn.commit()
        return new_id
    except psycopg2.Error as e:
        if conn is not None:
            conn.rollback()
        raise RuntimeError(f"Erro ao adicionar medicamento no banco: {e}") from e
    finally:
        if cursor is not None:
            cursor.close()
        if conn is not None:
            conn.close()


def list_medications_db() -> List[dict]:
    """Retorna todos os medicamentos ordenados por ID como lista de dicts."""
    conn = None
    cursor = None
    try:
        conn = get_db_connection()
        cursor = conn.cursor(cursor_factory=RealDictCursor)
        cursor.execute(
            """
            SELECT id, nome, dosagem, horario, tomado, criado_em
            FROM medicamentos
            ORDER BY id
            """
        )
        rows = cursor.fetchall()
        return [dict(row) for row in rows]
    except psycopg2.Error as e:
        raise RuntimeError(f"Erro ao listar medicamentos do banco: {e}") from e
    finally:
        if cursor is not None:
            cursor.close()
        if conn is not None:
            conn.close()


def mark_as_taken_db(med_id: int) -> bool:
    """Marca o medicamento como tomado. Retorna True se algum registro foi atualizado."""
    conn = None
    cursor = None
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute(
            "UPDATE medicamentos SET tomado = TRUE WHERE id = %s",
            (med_id,),
        )
        updated = cursor.rowcount
        conn.commit()
        return updated > 0
    except psycopg2.Error as e:
        if conn is not None:
            conn.rollback()
        raise RuntimeError(f"Erro ao marcar medicamento como tomado: {e}") from e
    finally:
        if cursor is not None:
            cursor.close()
        if conn is not None:
            conn.close()


def remove_medication_db(med_id: int) -> bool:
    """Remove o medicamento pelo ID. Retorna True se algum registro foi removido."""
    conn = None
    cursor = None
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute(
            "DELETE FROM medicamentos WHERE id = %s",
            (med_id,),
        )
        deleted = cursor.rowcount
        conn.commit()
        return deleted > 0
    except psycopg2.Error as e:
        if conn is not None:
            conn.rollback()
        raise RuntimeError(f"Erro ao remover medicamento: {e}") from e
    finally:
        if cursor is not None:
            cursor.close()
        if conn is not None:
            conn.close()
