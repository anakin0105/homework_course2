def filter_by_currency(transactions, currency):
    for transaction in transactions:
        operation_currency = transaction.get("operationAmount", {}).get("currency", {}).get("code")
        if operation_currency == currency:
            yield transaction
        # Возможно, этой строке нужно покрытие
        elif operation_currency is None:
            print("Пропущенная операция: нет валюты")


def transaction_descriptions(transactions):
    """
    Генератор, который возвращает описание транзакций по очереди.

    :param transactions: список транзакций (словарей).
    :yield: строка с описанием каждой транзакции.
    """
    for transaction in transactions:
        description = transaction.get("description")
        if description:
            yield description


def card_number_generator(start=1, end=10**16 - 1):
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
