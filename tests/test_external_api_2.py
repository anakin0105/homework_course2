import os
from unittest.mock import patch, Mock  # Используется для подмены API вызова и переменной окружения
from src.external_api import convert_to_rub  # Замените `your_module` на реальный путь к вашему модулю
@patch("os.getenv", return_value="mock_api_key")  # Подменяем вызов os.getenv, чтобы всегда возвращать "mock_api_key"
@patch("requests.get")  # Подменяем запрос requests.get через mock
def test_convert_to_rub_success(mock_get, mock_getenv):
    """
    Тест успешной конвертации валюты (USD -> RUB) через mock API.
    """
    # Подготовим mock-ответ от API
    mock_response_data = {
        "success": True,
        "query": {"from": "USD", "to": "RUB", "amount": 9824.07},
        "info": {"rate": 62.78},
        "result": 616804.61,
    }
    # Настраиваем mock, чтобы возвращать подготовленный ответ
    mock_get.return_value = Mock(status_code=200, json=lambda: mock_response_data)
    # Подготавливаем тестовые данные транзакции
    transaction = {
        "date": "2023-01-01",
        "operationAmount": {
            "amount": "9824.07",  # Сумма для конвертации
            "currency": {"code": "USD"}  # Исходная валюта (доллары США)
        },
    }
    # Вызываем тестируемую функцию
    result = convert_to_rub(transaction)
    # Проверяем результат конвертации
    assert result == 616804.61, "Результат конверсии не соответствует ожидаемому значению."
    # Проверяем вызов mock-объекта requests.get с нужными параметрами
    mock_get.assert_called_once_with(
        "https://api.apilayer.com/exchangerates_data/convert?to=RUB&from=USD&amount=9824.07",
        headers={"apikey": "mock_api_key"},  # Ожидаемый mock-ключ
        timeout=10
    )