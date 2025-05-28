import pytest

from src.decorators import log
from src.masks import get_mask_card_number


def test_valid_card():
    assert get_mask_card_number("1234567890123456") == "1234 56** **** 3456"


def test_invalid_card_short():
    assert get_mask_card_number("12345678") == "Проверьте правильность введенного номера карты!"


def test_invalid_card_letters():
    assert get_mask_card_number("1234ABCD5678EFGH") == "Проверьте правильность введенного номера карты!"


# Пример функции с декоратором log
@log()  # Логирование в консоль
def add(a, b):
    return a + b


def test_log_successful_execution(capsys):
    """Тест успешного выполнения функции с логированием в консоль."""

    # Вызываем функцию, чтобы триггерить декоратор log
    result = add(3, 5)

    # Проверяем результат выполнения функции
    assert result == 8

    # С помощью capsys перехватываем вывод в консоль
    captured = capsys.readouterr()

    # Проверяем, что в консоли есть корректное логирование
    assert "Calling function 'add' with args: (3, 5), kwargs: {}" in captured.out
    assert "Function 'add' executed successfully with result: 8" in captured.out


@log()  # Логирование в консоль
def divide(a, b):
    return a / b


def test_log_on_error(capsys):
    """Тест логирования при выбросе исключения."""

    # Проверяем, что функция выбрасывает ZeroDivisionError
    with pytest.raises(ZeroDivisionError):
        divide(5, 0)

    # С помощью capsys перехватываем вывод в консоль
    captured = capsys.readouterr()

    # Проверяем, что информация об ошибке залогирована
    assert "Function 'divide' failed with error: division by zero." in captured.out
    assert "Inputs: (5, 0)" in captured.out


@log(filename="test_log.txt")  # Логирование в файл test_log.txt
def multiply(a, b):
    return a * b


def test_log_to_file(tmp_path):
    """Тест логирования данных в файл."""

    # Создаём временный файл для логирования
    log_file = tmp_path / "log.txt"

    # Переназначим декоратор для использования временного файла
    @log(filename=str(log_file))
    def test_function(x, y):
        return x * y

    # Вызываем декорированную функцию
    test_function(4, 5)

    # Проверяем, что временный файл был создан и содержит логи
    assert log_file.exists()

    # Читаем содержимое файла
    with open(log_file, "r") as file:
        log_content = file.read()

    # Проверяем, что лог содержит информацию о вызове и результат
    assert "Calling function 'test_function' with args: (4, 5), kwargs: {}" in log_content
    assert "Function 'test_function' executed successfully with result: 20" in log_content
