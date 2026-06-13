from typing import List
from medalert.models import Medication


def validate_time_format(time: str) -> bool:
    """Valida se o horário está no formato HH:MM"""
    try:
        parts = time.split(":")
        if len(parts) != 2:
            return False

        hour, minute = int(parts[0]), int(parts[1])

        return 0 <= hour <= 23 and 0 <= minute <= 59
    except ValueError:
        return False


def add_medication(
    medications: List[Medication],
    name: str,
    dosage: str,
    time: str,
) -> List[Medication]:
    """Adiciona um novo medicamento na lista"""

    if not name.strip():
        raise ValueError("Nome do medicamento não pode ser vazio.")

    if not dosage.strip():
        raise ValueError("Dosagem não pode ser vazia.")

    if not validate_time_format(time):
        raise ValueError("Horário inválido. Use o formato HH:MM.")

    medications.append(Medication(name=name, dosage=dosage, time=time))
    return medications


def mark_as_taken(medications: List[Medication], index: int) -> List[Medication]:
    """Marca um medicamento como tomado"""

    if index < 0 or index >= len(medications):
        raise IndexError("Índice inválido.")

    medications[index].taken = True
    return medications