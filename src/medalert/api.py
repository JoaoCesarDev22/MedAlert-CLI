import requests


OPENFDA_URL = "https://api.fda.gov/drug/label.json"


def fetch_drug_info(drug_name: str) -> dict:
    if not drug_name.strip():
        raise ValueError("Nome do medicamento não pode ser vazio.")

    params = {
        "search": f'openfda.generic_name:"{drug_name}"',
        "limit": 1,
    }

    response = requests.get(OPENFDA_URL, params=params, timeout=10)
    response.raise_for_status()

    data = response.json()

    if "results" not in data or len(data["results"]) == 0:
        raise ValueError("Nenhuma informação encontrada na OpenFDA para este medicamento.")

    return data["results"][0]


def format_drug_info(drug_data: dict) -> str:
    openfda = drug_data.get("openfda", {})

    brand_name = openfda.get("brand_name", ["Não informado"])
    generic_name = openfda.get("generic_name", ["Não informado"])
    manufacturer = openfda.get("manufacturer_name", ["Não informado"])

    return (
        "\n=== Informação do Medicamento (OpenFDA) ===\n"
        f"Nome genérico: {generic_name[0]}\n"
        f"Nome comercial: {brand_name[0]}\n"
        f"Fabricante: {manufacturer[0]}\n"
    )
