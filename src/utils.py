import json
import os
from typing import Any
from typing import Dict
from typing import List


def read_transactions_json(file_json) -> List[Dict[Any, Any]]:
    """Читает JSON-файл и возвращает список словарей с данными о транзакция.
    Параметры:
    - file_path (str): Путь до JSON-файла.
    Возвращает:
    - List[Dict[Any, Any]: Список словарей с данными о транзакциях.
    Если файл отсутствует, пустой или содержит некорректные данные, возвращает пустой список."""

    try:
        with open(file_json, "r", encoding="utf-8", errors="ignore") as f:

            data = json.load(f)

            if not isinstance(data, list):
                return []

            return data
    except (FileNotFoundError, json.JSONDecodeError, TypeError, KeyError, ValueError):
        return []


file_path = r"C:\Users\Admin\PycharmProjects\pythonProjectBank1\data\operations.json"
print(read_transactions_json(file_path))
