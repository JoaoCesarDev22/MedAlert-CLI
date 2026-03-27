from typing import List
from medalert.models import Medication


def validate_time_format(time_str: str) -> bool:
    if len(time_str) != 5:
        return False

    if time_str[2] != ":":
        return False

    hour_part = time_str[:2]
    minute_part = time_str[3:]

    if not hour_part.isdigit() or not minute_part.isdigit():
        return False

    hour = int(hour_part)
    minute = int(minute_part)

    if hour < 0 or hour > 23:
        return False

    if minute < 0 or minute > 59:
        return False

    return True


def add_medication(
    medications: List[Medication],
    name: str,
    dosage: str,
    time: str,
) -> List[Medication]:
    if not name.strip():
        raise ValueError("Nome do medicamento não pode ser vazio.")

    if not dosage.strip():
        raise ValueError("Dosagem não pode ser vazia.")

    if not validate_time_format(time):
        raise ValueError("Horário inválido. Use o formato HH:MM.")

    medications.append(Medication(name=name, dosage=dosage, time=time))
    return medications


def list_medications(medications: List[Medication]) -> List[str]:
    result = []
    for idx, med in enumerate(medications, start=1):
        status = "Tomado" if med.taken else "Pendente"
        result.append(f"{idx}. {med.name} | {med.dosage} | {med.time} | {status}")
    return result


def mark_as_taken(medications: List[Medication], index: int) -> None:
    if index < 1 or index > len(medications):
        raise ValueError("Índice inválido.")

    medications[index - 1].taken = True


def remove_medication(medications: List[Medication], index: int) -> None:
    if index < 1 or index > len(medications):
        raise ValueError("Índice inválido.")

    medications.pop(index - 1)