import re
from typing import List, Dict
def process_bank_search_grok(data: list[dict], search: str) -> list[dict]:
    """Фильтрует операции, где в описании есть строка поиска (регистронезависимо)."""
    pattern = re.compile(re.escape(search), re.IGNORECASE)
    return [item for item in data if pattern.search(item.get('description', ''))]


def process_bank_operations_grok(data: list[dict], categories: list) -> dict:
    """Считает количество операций по категориям."""
    result = {cat: 0 for cat in categories}
    for item in data:
        desc = item.get('description', '')
        for cat in categories:
            if cat.lower() in desc.lower():
                result[cat] += 1
    return result

def process_bank_search_gpt(data: List[Dict], search: str) -> List[Dict]:
    """
    Ищет операции, в описании которых есть подстрока search (регистронезависимо).

    :param data: список словарей с банковскими операциями
    :param search: строка для поиска
    :return: список операций, удовлетворяющих поиску
    """
    result = []
    pattern = re.compile(re.escape(search), re.IGNORECASE)
    for operation in data:
        description = operation.get("description", "")
        if pattern.search(description):
            result.append(operation)
    return result


def process_bank_operations_gpt(data: List[Dict], categories: List[str]) -> Dict[str, int]:
    """
    Считает количество операций в каждой категории.

    :param data: список словарей с банковскими операциями
    :param categories: список категорий для подсчёта
    :return: словарь вида {категория: количество}
    """
    result = {category: 0 for category in categories}
    for operation in data:
        description = operation.get("description", "")
        for category in categories:
            if category in description:
                result[category] += 1
    return result