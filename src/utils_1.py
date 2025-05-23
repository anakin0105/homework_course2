import json
import os
from typing import List, Dict, Any



def read_transactions_json(file_json) -> List[Dict[Any, Any]]:
    """Читает JSON-файл и возвращает список словарей с данными о транзакциях."""
    try:
        with open(file_json, 'r') as f:
            data = json.load(f)
            if not isinstance(data, list):
                return []
            return data
    except (FileNotFoundError, json.JSONDecodeError, TypeError):
        return []

# Проверка функции с print
file_path = "operations.json"  # Укажи правильный путь, если нужно
transactions = read_transactions_json(file_path)
print(f"Данные из файла {file_path}: {transactions}")