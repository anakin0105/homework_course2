from typing import Dict
from typing import Generator
from typing import List
from typing import Optional
from typing import Union


def filter_by_currency(transactions: List[Dict], currency: str) -> Generator[Dict, None, None]:
    for transaction in transactions:
        operation_currency = transaction.get("operationAmount", {}).get("currency", {}).get("code")
        if operation_currency == currency:
            yield transaction
        # Возможно, этой строке нужно покрытие
        elif operation_currency is None:
            print("Пропущенная операция: нет валюты")


def filter_by_currency_csv_excel(transactions: List[Dict], currency: str) -> Generator[Dict, None, None]:
    for transaction in transactions:
        operation_currency = transaction.get("currency_code")
        if operation_currency == currency:
            yield transaction
        # Возможно, этой строке нужно покрытие
        elif operation_currency is None:
            print("Пропущенная операция: нет валюты")


def transaction_descriptions(transactions: List[Dict[str, Union[int, Optional[str]]]]) -> List[Optional[str]]:
    """
    Генератор, который возвращает описание транзакций по очереди.

    :param transactions: Списки транзакций (словарей).
    :yield: строка с описанием каждой транзакции.
    """
    for transaction in transactions:
        description = transaction.get("description")
        if description:
            yield description


def card_number_generator(start: int = 1, end: int = 10**16 - 1) -> Generator[str, None, None]:
    """
    Генерирует последовательные номера карт от `start` до `end`.

    :param start: Начальный номер (по умолчанию 0000 0000 0000 0001).
    :param end: Конечный номер (по умолчанию 9999 9999 9999 9999).
    :yield: Номер карты в формате строки с разделителями.
    """
    for number in range(start, end + 1):
        # Форматируем номер карты с пробелами каждые 4 цифры
        yield f"{number:016d}"[:4] + " " + f"{number:016d}"[4:8] + " " + f"{number:016d}"[
            8:12
        ] + " " + f"{number:016d}"[12:]
