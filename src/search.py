import re
from collections import Counter


def process_bank_search(data: list[dict], search: str) -> list[dict]:
    """Фильтрует операции, где в описании есть строка поиска (регистронезависимо)."""
    pattern = re.compile(re.escape(search), re.IGNORECASE)
    return [item for item in data if pattern.search(item.get("description", ""))]


def process_bank_operations(data: list[dict], categories: list) -> dict:
    """Считает количество операций по категориям."""
    if not categories:
        return {}
    result = {}
    for operation in data:
        description = operation.get("description", "")
        if description in categories:
            if description in result:
                result[description] += 1
            else:
                result[description] = 1
    return result


def process_bank_operations_count(data: list[dict], count_dict: dict) -> dict:
    """Функция принимает список транзакций и словарь для подсчета и возвращает словарь."""
    descriptions = [transaction.get("description") for transaction in data]
    count_description = Counter(descriptions)
    for key, value in count_description.items():
        if key in count_dict:
            count_dict[key] = value
    return count_dict


# if __name__ == '__main__':
#     from src.utils import read_transactions_json
#     data = read_transactions_json("../data/operations.json")
#     # search_1 = process_bank_search(data, "перевод")
#     # print(search_1)
#     list_1 = ["Нет данных"]
#     count_1 = process_bank_operations(data,list_1)
#     print(count_1)
#     dict_1 = {"нет данных": 0}
#     count_2 = process_bank_operations_count(data, dict_1)
#     print(count_2)
