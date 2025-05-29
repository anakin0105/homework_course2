import json
import os
from typing import Any
from typing import Dict
from typing import List
import logging
import os

log_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "logs")
log_file = os.path.join(log_dir, "utils.log")
masks_logger = logging.getLogger("ulils_logger")
masks_logger.setLevel(logging.DEBUG)
file_handler = logging.FileHandler(log_file, mode="w", encoding="utf-8")
file_formatter = logging.Formatter("%(asctime)s %(filename)s %(levelname)s: %(message)s")
file_handler.setFormatter(file_formatter)
masks_logger.addHandler(file_handler)

masks_logger.info("Скрипт запущен")
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
    except (FileNotFoundError, json.JSONDecodeError, TypeError, KeyError, ValueError) as e:
        masks_logger.error(f"Функция get_mask_account завершила работу c ошибкой {e}! ")
        return []


file_path = r"C:\Users\Admin\PycharmProjects\pythonProjectBank1\data\operations.json"
file_path_1 = r"C:\Users\Admin\PycharmProjects\pythonProjectBank1\data\dateerror"
print(read_transactions_json(file_path))
print(read_transactions_json([]))
print(read_transactions_json([23413]))
print(read_transactions_json(file_path_1))