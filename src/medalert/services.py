from typing import List
import requests
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


# --- INTEGRACAO COM API PÚBLICA (OPENFDA) ---

def fetch_drug_info(drug_name: str) -> dict:
    """
    Consome a API pública da OpenFDA para buscar informações sobre um medicamento.
    """
    if not drug_name.strip():
        raise ValueError("O nome do medicamento não pode ser vazio.")

    url = f"https://api.fda.gov/drug/label.json?search=openfda.generic_name:{drug_name}&limit=1"
    
    try:
        response = requests.get(url, timeout=5)
        if response.status_code == 404:
            raise ValueError("Medicamento não encontrado na base da OpenFDA.")
        
        response.raise_for_status()
        data = response.json()
        
        if "results" not in data or len(data["results"]) == 0:
            raise ValueError("Medicamento não encontrado na base da OpenFDA.")
            
        return data["results"][0]
    except requests.RequestException as e:
        raise RuntimeError(f"Erro de comunicação com a OpenFDA: {e}")


def format_drug_info(drug_data: dict) -> str:
    """
    Formata os dados brutos recebidos da OpenFDA para exibição na interface.
    """
    openfda = drug_data.get("openfda", {})
    
    brand_name = openfda.get("brand_name", ["Não informado"])[0]
    generic_name = openfda.get("generic_name", ["Não informado"])[0]
    manufacturer = openfda.get("manufacturer_name", ["Não informado"])[0]
    
    return f"Medicamento: {brand_name} (Genérico: {generic_name}) | Fabricante: {manufacturer}"