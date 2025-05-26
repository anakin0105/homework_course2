from typing import Any
from typing import Dict
from typing import List
from typing import Optional
from typing import Union

import pytest

from src.generators import card_number_generator
from src.generators import filter_by_currency
from src.generators import transaction_descriptions


# Тест 1: Фильтрация транзакций с валютой "USD"
def test_filter_by_currency_usd() -> None:
    transactions = [
        {"id": 1, "operationAmount": {"currency": {"code": "USD"}}},
        {"id": 2, "operationAmount": {"currency": {"code": "EUR"}}},
        {"id": 3, "operationAmount": {"currency": {"code": "USD"}}},
    ]
    usd_transactions = list(filter_by_currency(transactions, "USD"))
    assert len(usd_transactions) == 2
    assert usd_transactions[0]["id"] == 1
    assert usd_transactions[1]["id"] == 3


# Тест 2: Фильтрация, где нет транзакций с валютой "USD"
def test_filter_by_currency_empty_result() -> None:
    transactions = [
        {"id": 1, "operationAmount": {"currency": {"code": "EUR"}}},
        {"id": 2, "operationAmount": {"currency": {"code": "GBP"}}},
    ]
    usd_transactions = list(filter_by_currency(transactions, "USD"))
    assert len(usd_transactions) == 0


# Тест 3: Обработка пустого списка
def test_filter_by_currency_empty_list() -> None:
    transactions: list[dict[str, str]] = []
    usd_transactions = list(filter_by_currency(transactions, "USD"))
    assert len(usd_transactions) == 0


# Тест 4: Транзакции без поля "currency"
def test_filter_by_currency_missing_currency() -> None:
    transactions: list[dict[str, Any]] = [{"id": 1}, {"id": 2, "operationAmount": {"currency": {"code": "USD"}}}]
    usd_transactions = list(filter_by_currency(transactions, "USD"))
    assert len(usd_transactions) == 1
    assert usd_transactions[0]["id"] == 2


def transaction_descriptions1(transactions: List[Dict[str, Any]]) -> List[Optional[str]]:
    """Возвращает список описаний транзакций."""
    return [transaction.get("description") for transaction in transactions]


def transaction_descriptions2(transactions: List[Dict[str, Any]]) -> List[Optional[str]]:
    """Возвращает список описаний транзакций."""
    return [transaction.get("description") for transaction in transactions]


def test_transaction_descriptions() -> None:
    """Тестирует функцию transaction_descriptions с корректными данными."""
    # Тестовые данные
    transactions: List[Dict[str, Optional[str]]] = [
        {"id": "1", "description": "Оплата товаров"},  # id преобразован в строку
        {"id": "2", "description": "Перевод средств"},
        {"id": "3", "description": "Покупка билетов"},
    ]
    # Проверка результатов
    descriptions = list(transaction_descriptions(transactions))
    assert descriptions == ["Оплата товаров", "Перевод средств", "Покупка билетов"]


def test_transaction_descriptions_missing_field() -> None:
    """Тестирует функцию transaction_descriptions с отсутствующими ключами."""
    # Данные с отсутствующими описаниями, где "id" сохранён как число
    transactions: List[Dict[str, Union[int, Optional[str]]]] = [
        {"id": 1, "description": "Оплата товаров"},
        {"id": 2},  # Нет поля "description"
        {"id": 3, "description": "Покупка билетов"},
    ]

    # Проверка списка
    descriptions = list(transaction_descriptions(transactions))
    assert descriptions == ["Оплата товаров", "Покупка билетов"]


def test_transaction_descriptions_empty_list() -> None:
    """Тестируем функцию transaction_descriptions на пустом списке."""
    # Пустой список
    transactions: List[Dict[str, Optional[str]]] = []  # Аннотируем список транзакций
    descriptions = list(transaction_descriptions(transactions))
    assert descriptions == []


def test_card_number_generator_standard() -> None:
    """Проверяем стандартный диапазон генерации номеров карт"""
    card_gen = card_number_generator(1, 5)
    cards = list(card_gen)
    assert cards == [
        "0000 0000 0000 0001",
        "0000 0000 0000 0002",
        "0000 0000 0000 0003",
        "0000 0000 0000 0004",
        "0000 0000 0000 0005",
    ]


def test_card_number_generator_large_numbers() -> None:
    """Проверяем генерацию больших номеров"""
    card_gen = card_number_generator(9999999999999995, 9999999999999999)
    cards = list(card_gen)
    assert cards == [
        "9999 9999 9999 9995",
        "9999 9999 9999 9996",
        "9999 9999 9999 9997",
        "9999 9999 9999 9998",
        "9999 9999 9999 9999",
    ]


def test_card_number_generator_empty_range() -> None:
    """Проверяем случай, когда start > end"""
    card_gen = card_number_generator(10, 5)
    cards = list(card_gen)
    assert cards == []  # Генерация должна быть пустой


def test_card_number_generator_single_number() -> None:
    """Проверяем случай, когда start == end"""
    card_gen = card_number_generator(5, 5)
    cards = list(card_gen)
    assert cards == ["0000 0000 0000 0005"]  # Должен быть один номер


def test_card_number_generator_no_start_end() -> None:
    """Проверяем генерацию по умолчанию от 1 до 9999...9999"""
    # Ограничимся первыми 3 номерами, чтобы не грузить генерацию
    card_gen = card_number_generator()
    cards = [next(card_gen) for _ in range(3)]
    assert cards == [
        "0000 0000 0000 0001",
        "0000 0000 0000 0002",
        "0000 0000 0000 0003",
    ]


@pytest.fixture
def transactions_data() -> List[Dict[str, Any]]:
    """Фикстура: список транзакций для тестирования."""
    return [
        {
            "id": 1,
            "operationAmount": {"amount": "100.00", "currency": {"name": "USD", "code": "USD"}},
            "state": "EXECUTED",
        },
        {
            "id": 2,
            "operationAmount": {"amount": "200.00", "currency": {"name": "EUR", "code": "EUR"}},
            "state": "PENDING",
        },
        {
            "id": 3,
            "operationAmount": {"amount": "300.00", "currency": {"name": "USD", "code": "USD"}},
            "state": "CANCELED",
        },
        {
            "id": 4,
            "operationAmount": {"amount": "400.00", "currency": {"name": "GBP", "code": "GBP"}},
            "state": "EXECUTED",
        },
    ]


@pytest.mark.parametrize(
    "currency_code, expected_ids",
    [
        ("USD", [1, 3]),
        ("EUR", [2]),
        ("GBP", [4]),
        ("JPY", []),
    ],
)
def test_filter_by_currency(
    transactions_data: List[Dict[str, Any]], currency_code: str, expected_ids: List[int]
) -> None:
    """Тестируем filter_by_currency с разными валютами."""
    filtered_gen = filter_by_currency(transactions_data, currency_code)
    result_ids = [transaction["id"] for transaction in filtered_gen]
    assert result_ids == expected_ids


@pytest.fixture
def transactions_with_descriptions() -> List[Dict[str, Any]]:
    """Фикстура: список транзакций с описаниями."""
    return [
        {"description": "Перевод организации", "id": 1},
        {"description": "Оплата за услуги", "id": 2},
        {"state": "EXECUTED", "id": 3},  # Без описания
    ]


@pytest.mark.parametrize(
    "start, stop",
    [
        (9999999999999995, 9999999999999999),  # Проверка больших диапазонов
    ],
)
def test_card_number_generator_large_range(start: int, stop: int) -> None:
    """Тестируем генерацию номеров для большого диапазона."""
    card_gen = card_number_generator(start, stop)
    result = list(card_gen)
    assert len(result) == 5  # Должно быть 5 номеров
    assert result[0] == "9999 9999 9999 9995"
    assert result[-1] == "9999 9999 9999 9999"
