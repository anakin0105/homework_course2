import csv
import logging
import os
from typing import Any

import pandas as pd

log_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "logs")
log_file = os.path.join(log_dir, "utils_excel.log")
utils_excel_logger = logging.getLogger("ulils_excel.logger")
utils_excel_logger.setLevel(logging.DEBUG)
file_handler = logging.FileHandler(log_file, mode="w", encoding="utf-8")
file_formatter = logging.Formatter("%(asctime)s %(filename)s %(levelname)s: %(message)s")
file_handler.setFormatter(file_formatter)
utils_excel_logger.addHandler(file_handler)


def get_read_csv(file_path: str | None = None) -> Any:
    """Функция считывает транзакции из файла .csv и возвращает список словарей"""
    utils_excel_logger.info("Функция get_read_csv запущена.")
    if not file_path:
        file_dir = os.path.dirname(os.path.abspath(__file__))
        file_path = os.path.join(file_dir, "..", "data", "transactions.csv")

    # Проверяем расширение файла
    if not file_path.lower().endswith(".csv"):
        print("Данные имеют неверный формат!")
        utils_excel_logger.error(f"Файл {file_path} не является .csv")
        utils_excel_logger.info("Функция get_read_csv завершила работу.")
        return []

    expected_headers = ["id", "state", "date", "amount", "currency_name", "currency_code", "from", "to", "description"]
    try:
        data_csv = []
        with open(file_path, "r", encoding="UTF-8") as file_csv:
            reader = csv.DictReader(file_csv, delimiter=";")
            # Проверяем заголовки
            if sorted(reader.fieldnames) != sorted(expected_headers):
                print("Данные имеют неверный формат!")
                utils_excel_logger.error(f"Неверные заголовки: {reader.fieldnames}")
                return []
            for row in reader:
                # Проверяем, что все обязательные поля заполнены
                if all(row.get(key) for key in expected_headers):
                    data_csv.append(row)
                else:
                    utils_excel_logger.warning(f"Пропущены данные в строке: {row}")
            return data_csv
    except FileNotFoundError:
        print("Ошибка! Файл не найден!")
        utils_excel_logger.error(f"Файл {file_path} не найден!")
        return []
    except (csv.Error, ValueError, TypeError) as e:
        print("Данные имеют неверный формат!")
        utils_excel_logger.error(f"Ошибка обработки файла {file_path}: {e}.")
        return []
    finally:
        utils_excel_logger.info("Функция get_read_csv завершила работу.")


def get_read_excel(file_path: str | None = None) -> Any:
    """
    Функция считывает транзакции из файла .xlsx и возвращает список словарей.
    """
    utils_excel_logger.info("Функция get_read_xlsx запущена.")
    if not file_path:
        file_dir = os.path.dirname(os.path.abspath(__file__))
        file_path = os.path.join(file_dir, "..", "data", "transactions_excel.xlsx")
    # Проверка существования файла
    if not os.path.isfile(file_path):
        print(f"Ошибка! Файл {file_path} не найден.")
        utils_excel_logger.info(f"Ошибка! Файл {file_path} не найден.")
        return None
    # Проверка расширения файла
    if not file_path.endswith(".xlsx"):
        print(f"Ошибка! Файл {file_path} не является Excel-файлом.")
        utils_excel_logger.info(f"Ошибка! Файл {file_path} не является Excel-файлом.")
        return None
    try:
        # Чтение Excel-файла
        data_frame = pd.read_excel(file_path)
        data_xlsx = data_frame.to_dict(orient="records")
        print(f"Считывание Excel-файла успешно: {len(data_xlsx)} записей загружено.")
        utils_excel_logger.info(f"Считывание Excel-файла успешно: {len(data_xlsx)} записей загружено.")
        return data_xlsx
    except FileNotFoundError:
        print(f"Ошибка! Файл {file_path} не найден.")
        utils_excel_logger.info(f"Ошибка! Файл {file_path} не найден.")
    except Exception as e:
        print(f"Неизвестная ошибка: {e}")
        utils_excel_logger.info(f"Неизвестная ошибка: {e}")
        return None
    finally:
        utils_excel_logger.info("Функция get_read_xlsx завершила работу.")


# # Проверяем функцию чтения CSV
# csv_result = get_read_csv()
# print("\nПроверка работы get_read_csv:")
# if csv_result:
#     print(f"Считаны данные из CSV (первые 3 записи): {csv_result[:3]}")  # Вывести первые 3 записи
# else:
#     print("Данные из CSV не считаны или пусты!")
#
#
# # Проверяем функцию чтения CSV
# xlsx_result = get_read_excel()
# print("\nПроверка работы get_read_excel:")
# if xlsx_result:
#     print(f"Считаны данные из Excel (первые 3 записи): {xlsx_result[:3]}")  # Вывести первые 3 записи
# else:
#     print("Данные из Excel не считаны или пусты!")
