import re
from collections import Counter
from typing import Any

import pandas as pd

from src.utils_cvs_excel import get_read_csv, get_read_excel
from src.utils import read_transactions_json
from main import main


def process_transaction(user_name: str, file_format: str, sort_order: str) -> None:
    """Обрабатывает данные транзакций на основе введённых параметров."""
    print(f"{user_name}, обработка транзакций:")
    if file_format == "1":
        print("Формат: JSON")
    elif file_format == "2":
        print("Формат: CSV")
    elif file_format == "3":
        print("Формат: XLSX")

    if sort_order == "по возрастанию":
        print("Сортировка: по возрастанию")
    elif sort_order == "по убыванию":
        print("Сортировка: по убыванию")
    else:
        print("Неверный порядок сортировки")
def make_transactions() -> list | str:
    file_format = input(
        """Выберите необходимый пункт меню:
    1. Получить информацию о транзакциях из JSON-файла
    2. Получить информацию о транзакциях из CSV-файла
    3. Получить информацию о транзакциях из XLSX-файла
    => """
    )
    print(f"{user_name}, обработка транзакций:")
    if file_format == "1":
        print("Для обработки выбран JSON-файл.")
        transaction_list = get_operations()
        transactions = []
        for item in transaction_list:
            transaction = normalize_transaction(item)
            transactions.append(transaction)
        return transactions
    elif file_format == "2":
        print("Для обработки выбран CSV-файл.")
        transactions = get_transactions_csv()
        return transactions
    elif file_format == "3":
        print("Для обработки выбран XLSX-файл.")
        transaction_list = get_transactions_xlsx()
        transactions = []
        for item in transaction_list:
            transaction = normalize_transaction(item)
            transactions.append(transaction)
        return transactions
    else:
        return "Ошибка ввода! Данные не найдены!"

def single_format_transaction(transaction: Any) -> dict:
    """Приводит транзакцию из любого формата к единому формату"""
    single_format = {
        "id": None,
        "state": None,
        "date": None,
        "amount": None,
        "currency_name": None,
        "currency_code": None,
        "from": None,
        "to": None,
        "description": None,
    }

    # Обработка JSON формата
    if "operationAmount" in transaction:
        single_format["id"] = str(transaction.get("id"))
        single_format["state"] = transaction.get("state")
        single_format["date"] = str(transaction.get("date"))

        # Обрабатываем вложенные словари amount, currency
        op_amount = transaction.get("operationAmount", {})
        single_format["amount"] = str(op_amount.get("amount", "0"))
        currency = op_amount.get("currency", {})
        single_format["currency_name"] = currency.get("name")
        single_format["currency_code"] = currency.get("code")

        single_format["from"] = transaction.get("from")
        single_format["to"] = transaction.get("to")
        single_format["description"] = transaction.get("description")

    # Обработка XLSX формата
    else:
        single_format["id"] = str(transaction.get("id")) if transaction.get("id") else ""
        single_format["state"] = transaction.get("state")
        single_format["date"] = transaction.get("date")

        # Для amount: преобразуем в str, независимо от исходного типа
        amount = transaction.get("amount")
        if amount is not None:
            single_format["amount"] = str(amount)
        else:
            single_format["amount"] = "0"

        single_format["currency_name"] = transaction.get("currency_name")
        single_format["currency_code"] = transaction.get("currency_code")
        single_format["from"] = transaction.get("from")
        single_format["to"] = transaction.get("to")
        single_format["description"] = transaction.get("description")

    return single_format

def filter_transactions(transactions: Any = None, target: Any = None) -> list:
    """Функция принимает список словарей с данными о банковских
    операциях и строку поиска и возвращает список словарей,
    у которых в описании есть данная строка"""
    if not transactions or not target:
        transactions, target = make_transactions(), input("Введите слово для поиска: ")

    try:
        filtered_transactions = []
        target_str = re.compile(re.escape(str(target)), flags=re.IGNORECASE)

        for transaction in transactions:
            for value in transaction.values():
                if value and isinstance(value, str) and target_str.search(value):
                    filtered_transactions.append(transaction)
                    break
        return filtered_transactions
    except TypeError("Таргет для поиска имеет неверный формат"):
        return []

def search_operations(operations, search_string) -> dict:
    """ Ищет операции, в описании которых есть заданная строка, используя регулярные выражения.
    Args: operations (list): Список словарей с данными об операциях.
    search_string (str): Строка для поиска в описании операций. Returns:
    list: Список словарей, где в описании есть совпадение с search_string. """
    result = []
    # Экранируем специальные символы в строке поиска, чтобы использовать её как шаблон
    pattern = re.escape(search_string) for operation in operations:
    # Проверяем, есть ли description в словаре и содержит ли оно искомую строку
    if "description" in operation and re.search(pattern, operation["description"], re.IGNORECASE): result.append(operation)
    return result