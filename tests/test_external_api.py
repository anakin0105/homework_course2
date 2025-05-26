from typing import Any
import pytest
from unittest.mock import patch, Mock
from src.external_api import API_KEY, convert_to_rub


# Тест для RUB (без обращения к API)
def test_convert_to_rub_rub_no_api():
    transaction = {
        "date": "2018-06-30T02:08:58.425572",
        "operationAmount": {
            "amount": "5000.56",
            "currency": {"name": "RUB", "code": "RUB"}
        }
    }
    result = convert_to_rub(transaction)
    assert result == 5000.56  # Округлено до 2 знаков

# Тест на некорректную валюту
def test_convert_to_rub_invalid_currency():
    transaction = {
        "operationAmount": {
            "amount": "100",
            "currency": {"name": "GBP", "code": "GBP"}
        }
    }
    with pytest.raises(ValueError, match="Некорректный код валюты 'GBP'. Допустимые значения: \\['USD', 'EUR', 'RUB'\\]"):
        convert_to_rub(transaction)