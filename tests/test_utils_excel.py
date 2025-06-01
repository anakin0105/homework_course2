import os
from unittest.mock import mock_open
from unittest.mock import patch

import pandas as pd
import pytest

from src.utils_cvs_excel import get_read_csv
from src.utils_cvs_excel import get_read_excel


# Фикстура для make_csv_transaction
@pytest.fixture
def make_read_csv():
    return {
        "id": "650703",
        "state": "EXECUTED",
        "date": "2023-09-05T11:30:32Z",
        "amount": "100.50",
        "currency_name": "Dollar",
        "currency_code": "USD",
        "from": "Alice",
        "to": "Bob",
        "description": "Payment",
    }


def test_get_read_csv_norm(make_read_csv):
    """Тест функции .csv - нормальный случай"""
    # Полный формат данных согласно указанной структуре
    csv_content = (
        "id;state;date;amount;currency_name;currency_code;from;to;description\n"
        "650703;EXECUTED;2023-09-05T11:30:32Z;100.50;Dollar;USD;Alice;Bob;Payment"
    )
    # Мок для файла
    with patch("builtins.open", mock_open(read_data=csv_content)):
        result = get_read_csv()

    # Проверяем, что результат соответствует фикстуре
    assert result == [make_read_csv]


def test_get_read_csv_invert_format(capsys: pytest.CaptureFixture[str]) -> None:
    """Тест функции .csv - данные не являются словарем"""
    csv_content = """test"""
    expect_result = "Данные имеют неверный формат!"
    with patch("builtins.open", mock_open(read_data=csv_content)):
        get_read_csv()
        print_result = capsys.readouterr()
    assert print_result.out.strip() == expect_result


def test_get_read_csv_not_found(capsys: pytest.CaptureFixture[str]) -> None:
    """Тест функции .csv - файл или папка не найдены"""
    get_read_csv("../date/transactions.csv")
    print_result = capsys.readouterr()
    expect_result = "Ошибка! Файл не найден!"
    assert print_result.out.strip() == expect_result


def test_get_read_csv_different_format(capsys: pytest.CaptureFixture[str]) -> None:
    """Тест функции .csv - файл с форматом, отличным от .csv"""
    file_dir = os.path.dirname(os.path.abspath(__file__))
    file_path = os.path.join(file_dir, "..", "data", "example.json")
    get_read_csv(file_path)
    print_result = capsys.readouterr()
    expect_result = "Данные имеют неверный формат!"
    assert print_result.out.strip() == expect_result


def test_get_read_excel_norm() -> None:
    """Тест функции .xlsx - нормальный случай"""
    data_frame = pd.DataFrame({"name": ["Ann", "Bob"], "age": [25, 31], "city": ["NY", "LA"]})
    with patch("pandas.read_excel", return_value=data_frame):
        result = get_read_excel()
    assert result[0] == {"name": "Ann", "age": 25, "city": "NY"}


def test_get_transactions_excel_not_found(capsys: pytest.CaptureFixture[str]) -> None:
    """Тест функции .xlsx - файл не найден"""
    file_path = "../date/transactions_excel.xlsx"  # Явно задаём file_path

    # Имитация отсутствия файла
    with patch("os.path.isfile", return_value=False):
        result = get_read_excel(file_path)
        print_result = capsys.readouterr()
        expect_result = f"Ошибка! Файл {file_path} не найден."
        assert print_result.out.strip() == expect_result
        assert result is None  # Проверяем, что возвращается None


def test_get_transactions_excel_unknown_error(capsys: pytest.CaptureFixture[str]) -> None:
    """Тест функции .xlsx - неизвестная ошибка при чтении файла"""
    file_path = "../date/transactions_excel.xlsx"

    # Имитация неизвестной ошибки (например, ValueError) в pd.read_excel
    with patch("pandas.read_excel", side_effect=ValueError("Invalid file format")):
        with patch("os.path.isfile", return_value=True):  # Файл существует
            result = get_read_excel(file_path)
            print_result = capsys.readouterr()
            expect_result = "Неизвестная ошибка: Invalid file format"
            assert print_result.out.strip() == expect_result
            assert result is None  # Проверяем, что возвращается None
