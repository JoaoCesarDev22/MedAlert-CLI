from unittest.mock import patch
from medalert.api import fetch_drug_info, format_drug_info


def test_fetch_drug_info_integration_mock():
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
