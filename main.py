from typing import List, Dict, Any, Optional

from src.generators import card_number_generator
from src.generators import filter_by_currency
from src.processing import filter_by_state
from src.processing import sort_by_date
from src.widget import get_date
from src.widget import mask_account_card
from src.external_api import convert_to_rub
if __name__ == "__main__":
    print(mask_account_card("Maestro 1596837868705199"))
    print(mask_account_card("Счет 64686473678894779589"))
    print(mask_account_card("MasterCard 7158300734726758"))
    print(mask_account_card("Счет 35383033474447895560"))
    print(mask_account_card("Visa Classic 6831982476737658"))
    print(mask_account_card("Visa Platinum 8990922113665229"))
    print(mask_account_card("Visa Gold 5999414228426353"))
    print(mask_account_card("Счет 7p3654108430135874305"))
    # Вызов get_date.
    print(get_date("2024-03-11T02:26:18.671407"))
    print(get_date("2025-12-31T23:59:59.000000"))

    # Исходные данные.
    data = [
        {"id": 41428829, "state": "EXECUTED", "date": "2019-07-03T18:35:29.512364"},
        {"id": 939719570, "state": "EXECUTED", "date": "2018-06-30T02:08:58.425572"},
        {"id": 594226727, "state": "CANCELED", "date": "2018-09-12T21:27:25.241689"},
        {"id": 615064591, "state": "CANCELED", "date": "2018-10-14T08:21:33.419441"},
    ]

    # Вызов filter_by_state для EXECUTED.
    print(filter_by_state(data, "EXECUTED"))

    # Вызов filter_by_state для CANCELED.
    print(filter_by_state(data, "CANCELED"))

    # Вызов sort_by_date на отфильтрованных данных (EXECUTED) в порядке убывания.
    print(sort_by_date(filter_by_state(data, "EXECUTED"), True))

    # Вызов sort_by_date на отфильтрованных данных (CANCELED) по возрастанию.
    print(sort_by_date(filter_by_state(data, "CANCELED"), False))

    # Вызов filter_by_currency для USD
    transactions = [
        {
            "id": 939719570,
            "state": "EXECUTED",
            "date": "2018-06-30T02:08:58.425572",
            "operationAmount": {"amount": "9824.07", "currency": {"name": "USD", "code": "USD"}},
            "description": "Перевод организации",
            "from": "Счет 75106830613657916952",
            "to": "Счет 11776614605963066702",
        },
        {
            "id": 142264268,
            "state": "EXECUTED",
            "date": "2019-04-04T23:20:05.206878",
            "operationAmount": {"amount": "79114.93", "currency": {"name": "USD", "code": "USD"}},
            "description": "Перевод со счета на счет",
            "from": "Счет 19708645243227258542",
            "to": "Счет 75651667383060284188",
        },
        {
            "id": 123456789,
            "state": "PENDING",
            "date": "2020-01-01T00:00:00",
            "operationAmount": {"amount": "1200.00", "currency": {"name": "EUR", "code": "EUR"}},
            "description": "Покупка",
            "from": "Счет 12345678912345678912",
            "to": "Счет 98765432198765432198",
        },
    ]

    # Используем генератор для получения первых двух транзакций в USD:
    print("Транзакции в валюте USD:")
    usd_transactions = filter_by_currency(transactions, "USD")
    for _ in range(2):  # Получить две первые транзакции
        print(next(usd_transactions))

    # Вызов transaction_descriptions с исправленной типизацией.
    def transaction_descriptions(txns: List[Dict[str, Any]]) -> List[Optional[str]]:
        """Возвращает список описаний транзакций."""
        return [txn.get("description") for txn in txns]

    # Генерация номеров карт.
    print("Генерация номеров карт:")
    card_gen = card_number_generator(1, 10)  # Сгенерируем первые 10 номеров
    for card in card_gen:
        print(card)

    print(convert_to_rub({
    "id": 41428829,
    "state": "EXECUTED",
    "date": "2019-07-03T18:35:29.512364",
    "operationAmount": {
      "amount": "8221.37",
      "currency": {
        "name": "USD",
        "code": "USD"
      }
    },
    "description": "Перевод организации",
    "from": "MasterCard 7158300734726758",
    "to": "Счет 35383033474447895560"
  }))




