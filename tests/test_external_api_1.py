import pytest
from unittest.mock import patch, Mock
from src.external_api import convert_to_rub  # Замените my_module на ваше имя модуля
import requests
from requests.exceptions import Timeout, RequestException

# API ключ для mock-запросов
API_KEY = "mock_api_key"  # Подставьте значение из вашего окружения

# Тест 1: Корректная транзакция с успешной конвертацией через API
@patch("requests.get")
def test_convert_to_rub_success(mock_get):
    mock_response_data = {
        "success": True,
        "query": {"from": "USD", "to": "RUB", "amount": 9824.07},
        "info": {"timestamp": 1530403199, "rate": 62.785038},
        "date": "2018-06-30",
        "historical": True,
        "result": 617119.65,
    }
    mock_get.return_value = Mock(status_code=200, json=lambda: mock_response_data)

    transaction = {
        "date": "2018-06-30T02:08:58.425572",
        "operationAmount": {
            "amount": "9824.07",
            "currency": {"name": "USD", "code": "USD"},
        },
    }

    result = convert_to_rub(transaction)
    assert result == 617119.65  # Проверить, что сумма конвертации совпадает с результатом от API
    mock_get.assert_called_once_with(
        f"https://api.apilayer.com/exchangerates_data/convert?to=RUB&from=USD&amount=9824.07",
        headers={"apikey": API_KEY},
        timeout=10,
    )


# Тест 2: Валюта RUB (без вызова API)
@patch("requests.get")
def test_convert_to_rub_rub_currency(mock_get):
    transaction = {
        "date": "2018-06-30T02:08:58.425572",
        "operationAmount": {
            "amount": "9898.87",
            "currency": {"name": "RUB", "code": "RUB"},
        },
    }

    result = convert_to_rub(transaction)
    assert result == 9898.87  # Проверить, что значение возвращается без изменений
    mock_get.assert_not_called()  # Убедиться, что API вызов не происходит


# Тест 3: Отсутствие ключа 'operationAmount'
def test_convert_to_rub_missing_operation_amount():
    transaction = {}
    with pytest.raises(KeyError, match="Ключ 'operationAmount' или его структура отсутствует в transaction."):
        convert_to_rub(transaction)


# Тест 4: Некорректный формат 'amount'
def test_convert_to_rub_invalid_amount():
    transaction = {
        "operationAmount": {
            "amount": "INVALID",
            "currency": {"code": "USD"},
        }
    }
    with pytest.raises(ValueError, match="Сумма транзакции 'amount' должна быть числом."):
        convert_to_rub(transaction)


# Тест 5: Таймаут API
@patch("requests.get", side_effect=Timeout)
def test_convert_to_rub_timeout(mock_get):
    transaction = {
        "date": "2018-06-30T02:08:58.425572",
        "operationAmount": {
            "amount": "9898.87",
            "currency": {"name": "USD", "code": "USD"},
        },
    }

    with pytest.raises(TimeoutError, match="Превышено время ожидания ответа от API."):
        convert_to_rub(transaction)


# Тест 6: Ошибка подключения к API
@patch("requests.get", side_effect=RequestException("Connection error"))
def test_convert_to_rub_connection_error(mock_get):
    transaction = {
        "date": "2018-06-30T02:08:58.425572",
        "operationAmount": {
            "amount": "9898.87",
            "currency": {"name": "USD", "code": "USD"},
        },
    }

    with pytest.raises(ConnectionError, match="Ошибка подключения к API: Connection error"):
        convert_to_rub(transaction)