import csv
import os
from typing import Any

import pandas as pd


def get_read_csv(file_path: str | None = None) -> Any:
    """Функция считывает транзакции из файла .csv и возвращает список словарей"""
    if not file_path:
        file_dir = os.path.dirname(os.path.abspath(__file__))
        file_path = os.path.join(file_dir, "..", "data", "transactions.csv")

    try:
        data_csv = []
        with open(file_path, "r", encoding="UTF-8") as file_csv:
            reader = csv.DictReader(file_csv, delimiter=";")
            for row in reader:
                data_csv.append(row)
            if len(data_csv) != 0:
                return data_csv
            else:
                print("Данные имеют неверный формат!")

    except FileNotFoundError:
        print("Ошибка! Файл не найден!")
    except TypeError as e:
        print("Данные имеют неверный формат!")


def get_read_xlsx(file_path: str | None = None) -> Any:
    """
    Функция считывает транзакции из файла .xlsx и возвращает список словарей.
    """
    if not file_path:
        file_dir = os.path.dirname(os.path.abspath(__file__))
        file_path = os.path.join(file_dir, "..", "data", "transactions_excel.xlsx")

    print(f"Попытка чтения Excel-файла: {file_path}")
    # Проверка существования файла
    if not os.path.isfile(file_path):
        print(f"Ошибка! Файл {file_path} не найден.")
        return None
    # Проверка расширения файла
    if not file_path.endswith(".xlsx"):
        print(f"Ошибка! Файл {file_path} не является Excel-файлом.")
        return None
    try:
        # Чтение Excel-файла
        data_frame = pd.read_excel(file_path)
        data_xlsx = data_frame.to_dict(orient="records")
        print(f"Считывание Excel-файла успешно: {len(data_xlsx)} записей загружено.")
        return data_xlsx
    except FileNotFoundError:
        print(f"Ошибка! Файл {file_path} не найден.")
    except ValueError as e:
        print(f"Ошибка чтения Excel: {e}")
    except Exception as e:
        print(f"Неизвестная ошибка: {e}")
    return None

# Проверяем функцию чтения CSV
xlsx_result = get_read_xlsx()
print("\nПроверка работы get_read_excel:")
if xlsx_result:
    print(f"Считаны данные из Excel (первые 3 записи): {xlsx_result[:3]}")  # Вывести первые 3 записи
else:
    print("Данные из Excel не считаны или пусты!")


