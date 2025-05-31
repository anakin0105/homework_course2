import json
from unittest.mock import mock_open
from unittest.mock import patch

from src.utils import read_transactions_json  # Импортируем тестируемую функцию


def test_read_correct_file():
    """Чтение корректного JSON-файла с вложенными данными."""
    # Тестовые данные в правильном формате
    mock_data = json.dumps(
        [
            {
                "id": 1,
                "state": "EXECUTED",
                "date": "2019-04-12T17:27:27.896421",
                "operationAmount": {"amount": "100.00", "currency": {"name": "USD", "code": "USD"}},
            },
            {
                "id": 2,
                "state": "PENDING",
                "date": "2020-01-01T10:00:00.000000",
                "operationAmount": {"amount": "200.00", "currency": {"name": "EUR", "code": "EUR"}},
            },
        ]
    )
    # Используем mock_open для эмуляции открытия файла с этими данными
    with patch("builtins.open", mock_open(read_data=mock_data)):
        result = read_transactions_json("fake_file.json")
        # Проверяем, что список содержит 2 транзакции
        assert len(result) == 2
        # Проверяем, что первая транзакция корректно прочитана
        assert result[0]["id"] == 1
        assert result[0]["operationAmount"]["amount"] == "100.00"
        assert result[0]["operationAmount"]["currency"]["code"] == "USD"
        # Проверяем, что вторая транзакция корректно прочитана
        assert result[1]["id"] == 2
        assert result[1]["operationAmount"]["amount"] == "200.00"
        assert result[1]["operationAmount"]["currency"]["code"] == "EUR"


def test_read_empty_file():
    """Чтение пустого файла."""
    with patch("builtins.open", mock_open(read_data="")):
        result = read_transactions_json("fake_file.json")
        assert result == []


def test_read_invalid_json():
    """Чтение файла с некорректным JSON."""
    with patch("builtins.open", mock_open(read_data="{invalid json}")):
        result = read_transactions_json("fake_file.json")
        assert result == []


def test_file_not_found():
    """Случай отсутствия файла."""
    with patch("builtins.open", side_effect=FileNotFoundError):
        result = read_transactions_json("missing_file.json")
        assert result == []


def test_incorrect_format():
    """Файл содержит объект вместо списка."""
    mock_data = json.dumps(
        {
            "id": 1,
            "state": "EXECUTED",
            "date": "2019-04-12T17:27:27.896421",
            "operationAmount": {"amount": "100.00", "currency": {"name": "USD", "code": "USD"}},
        },
    )
    with patch("builtins.open", mock_open(read_data=mock_data)):
        result = read_transactions_json("fake_file.json")
        assert result == []
