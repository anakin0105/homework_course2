import pytest
from src.generators import filter_by_currency


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
