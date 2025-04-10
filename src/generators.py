def filter_by_currency(transactions, currency):
    for transaction in transactions:
        operation_currency = transaction.get("operationAmount", {}).get("currency", {}).get("code")
        if operation_currency == currency:
            yield transaction
        # Возможно, этой строке нужно покрытие
        elif operation_currency is None:
            print("Пропущенная операция: нет валюты")
