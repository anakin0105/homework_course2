import pytest
from src.generators import filter_by_currency, transaction_descriptions


# Тест 1: Фильтрация транзакций с валютой "USD"
def test_filter_by_currency_usd():
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
def test_filter_by_currency_empty_result():
    transactions = [
        {"id": 1, "operationAmount": {"currency": {"code": "EUR"}}},
        {"id": 2, "operationAmount": {"currency": {"code": "GBP"}}},
    ]
    usd_transactions = list(filter_by_currency(transactions, "USD"))
    assert len(usd_transactions) == 0


# Тест 3: Обработка пустого списка
def test_filter_by_currency_empty_list():
    transactions = []
    usd_transactions = list(filter_by_currency(transactions, "USD"))
    assert len(usd_transactions) == 0


# Тест 4: Транзакции без поля "currency"
def test_filter_by_currency_missing_currency():
    transactions = [{"id": 1}, {"id": 2, "operationAmount": {"currency": {"code": "USD"}}}]
    usd_transactions = list(filter_by_currency(transactions, "USD"))
    assert len(usd_transactions) == 1
    assert usd_transactions[0]["id"] == 2


def test_transaction_descriptions():
    # Тестовые данные
    transactions = [
        {"id": 1, "description": "Оплата товаров"},
        {"id": 2, "description": "Перевод средств"},
        {"id": 3, "description": "Покупка билетов"},
    ]
    # Проверка результатов
    descriptions = list(transaction_descriptions(transactions))
    assert descriptions == ["Оплата товаров", "Перевод средств", "Покупка билетов"]


def test_transaction_descriptions_missing_field():
    # Данные с отсутствующими описаниями
    transactions = [
        {"id": 1, "description": "Оплата товаров"},
        {"id": 2},  # Нет поля "description"
        {"id": 3, "description": "Покупка билетов"},
    ]
    # Проверка списка
    descriptions = list(transaction_descriptions(transactions))
    assert descriptions == ["Оплата товаров", "Покупка билетов"]


def test_transaction_descriptions_empty_list():
    # Пустой список
    transactions = []
    descriptions = list(transaction_descriptions(transactions))
    assert descriptions == []