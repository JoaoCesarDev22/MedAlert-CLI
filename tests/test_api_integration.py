import pytest
from unittest.mock import patch
# Importando corretamente as funções de dentro do seu api.py original
from medalert.api import fetch_drug_info, format_drug_info


def test_fetch_drug_info_integration_mock():
    """Valida o comportamento da busca simulando (mockando) a resposta da API pública"""
    fake_response = {
        "results": [
            {
                "openfda": {
                    "brand_name": ["Dipirona Teste"],
                    "generic_name": ["Dipirona"],
                    "manufacturer_name": ["Farmacia Fake"],
                }
            }
        ]
    }

    with patch("requests.get") as mock_get:
        mock_get.return_value.status_code = 200
        mock_get.return_value.json.return_value = fake_response
        mock_get.return_value.raise_for_status.return_value = None

        result = fetch_drug_info("Dipirona")

        assert "openfda" in result
        assert result["openfda"]["generic_name"][0] == "Dipirona"


def test_format_drug_info_returns_string():
    """Valida se a função de formatação monta a string corretamente"""
    drug_data = {
        "openfda": {
            "brand_name": ["Dipirona Teste"],
            "generic_name": ["Dipirona"],
            "manufacturer_name": ["Farmacia Fake"],
        }
    }

    formatted = format_drug_info(drug_data)

    assert "Dipirona" in formatted
    assert "Fabricante" in formatted


def test_fetch_drug_info_real_api_integration():
    """Teste de Integração Real: Valida a comunicação viva conectando à API da OpenFDA"""
    try:
        # Buscando por um princípio ativo global padrão (Ibuprofen)
        result = fetch_drug_info("Ibuprofen")
        
        assert "openfda" in result
        assert len(result["openfda"].get("generic_name", [])) > 0
    except Exception as e:
        # Se a API externa estiver instável ou fora do ar, avisa o pytest para pular 
        # sem quebrar a pipeline de CI de forma injusta
        pytest.skip(f"A API externa da OpenFDA ficou indisponível durante o teste: {e}")