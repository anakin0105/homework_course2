import pytest

from src.search import process_bank_operations
from src.search import process_bank_operations_count
from src.search import process_bank_search


@pytest.fixture
def search_data():
    return [
        {"description": "Оплата в магазине", "amount": 100},
        {"description": "Поступление зарплаты", "amount": 1000},
        {"description": "Перевод другу", "amount": 300},
        {"description": "Оплата ЖКХ", "amount": 250},
        {"description": ""},
        {},
    ]


def test_exact_match(search_data):
    result = process_bank_search(search_data, "магазине")
    assert len(result) == 1
    assert result[0]["description"] == "Оплата в магазине"


def test_case_insensitive(search_data):
    result = process_bank_search(search_data, "МАГАзин")
    assert len(result) == 1
    assert result[0]["description"] == "Оплата в магазине"


def test_no_match(search_data):
    result = process_bank_search(search_data, "рестораны")
    assert result == []


def test_partial_match(search_data):
    result = process_bank_search(search_data, "лата")
    assert len(result) == 2
    assert {r["description"] for r in result} == {"Оплата в магазине", "Оплата ЖКХ"}


def test_empty_description(search_data):
    result = process_bank_search(search_data, "оплата")
    # Ожидаем, что будут найдены только те, что с "Оплата..." (2 штуки)
    assert len(result) == 2


def test_empty_search(search_data):
    result = process_bank_search(search_data, "")
    # Возвращает все записи с заполненным description (включая пустые строки + возвращает список словарей так что 6)
    assert len(result) == 6  # строки с ключом description


def test_non_exist_description(search_data):
    data = [{"amount": 200}]
    result = process_bank_search(data, "anything")
    assert result == []


@pytest.fixture
def operations_data():
    return [
        {"description": "Перевод"},
        {"description": "Оплата"},
        {"description": "Перевод"},
        {"description": "Зарплата"},
        {"description": "Оплата"},
        {"description": "Перевод"},
        {"other_key": "Нет описания"},
    ]


def test_usual_case(operations_data):
    categories = ["Перевод", "Оплата", "Зарплата"]
    result = process_bank_operations(operations_data, categories)
    assert result == {"Перевод": 3, "Оплата": 2, "Зарплата": 1}


def test_no_categories(operations_data):
    result = process_bank_operations(operations_data, [])
    assert result == {}


def test_category_not_in_data(operations_data):
    categories = ["Налоги", "Аренда"]
    result = process_bank_operations(operations_data, categories)
    assert result == {}


def test_some_missing_descriptions():
    data = [{"description": "Перевод"}, {}, {"description": ""}, {"description": "Оплата"}]
    categories = ["Перевод", "Оплата"]
    result = process_bank_operations(data, categories)
    assert result == {"Перевод": 1, "Оплата": 1}


def test_duplicate_descriptions(operations_data):
    # Проверим, что счетчик работает корректно для дублирующихся категорий
    categories = ["Перевод", "Перевод", "Оплата"]
    result = process_bank_operations(operations_data, categories)
    assert result == {"Перевод": 3, "Оплата": 2}


def test_empty_data():
    result = process_bank_operations([], ["Перевод"])
    assert result == {}


def test_empty_description_value():
    data = [{"description": ""}, {"description": ""}]
    categories = [""]
    result = process_bank_operations(data, categories)
    assert result == {"": 2}


def test_operation_count_basic(operations_data):
    count_dict = {"Перевод": 0, "Оплата": 0, "Зарплата": 0}
    result = process_bank_operations_count(operations_data, count_dict.copy())
    assert result == {"Перевод": 3, "Оплата": 2, "Зарплата": 1}


def test_count_dict_with_extra_keys(operations_data):
    count_dict = {"Перевод": 0, "Аренда": 99, "Оплата": 0}
    result = process_bank_operations_count(operations_data, count_dict.copy())
    assert result == {"Перевод": 3, "Аренда": 99, "Оплата": 2}  # 'Аренда' не встречается, значение не меняется


def test_empty_data_count(operations_data):
    count_dict = {"Перевод": 5}
    result = process_bank_operations_count([], count_dict.copy())
    assert result == {"Перевод": 5}


def test_empty_count_dict(operations_data):
    count_dict = {}
    result = process_bank_operations_count(operations_data, count_dict.copy())
    assert result == {}


def test_description_absent_in_data(operations_data):
    count_dict = {"Налоги": 10, "Аренда": 20}
    result = process_bank_operations_count(operations_data, count_dict.copy())
    assert result == {"Налоги": 10, "Аренда": 20}


def test_missing_description_key():
    data = [{"unknown_key": "test"}, {"description": "Тест"}]
    count_dict = {"Тест": 0}
    result = process_bank_operations_count(data, count_dict.copy())
    assert result == {"Тест": 1}


def test_none_description_in_data():
    data = [{"description": None}, {"description": None}, {"description": "Перевод"}]
    count_dict = {"Перевод": 0, None: 0}
    result = process_bank_operations_count(data, count_dict.copy())
    assert result == {"Перевод": 1, None: 2}
