from src.masks import get_mask_account
from src.masks import get_mask_card_number


# Тесты для функции get_mask_card_number
def test_mask_card_number_valid() -> None:
    """Тест: Корректное маскирование номера карты."""
    assert get_mask_card_number("1234567812345678") == "1234 56** **** 5678"
    assert get_mask_card_number("8765432187654321") == "8765 43** **** 4321"


def test_mask_card_number_invalid_length() -> None:
    """Тест: Возврат ошибки при некорректной длине номера карты."""
    assert get_mask_card_number("123") == "Проверьте правильность введенного номера карты!"
    assert get_mask_card_number("12345678") == "Проверьте правильность введенного номера карты!"
    assert get_mask_card_number("123456781234567890") == "Проверьте правильность введенного номера карты!"


def test_mask_card_number_non_digit() -> None:
    """Тест: Возврат ошибки при наличии недопустимых символов в номере карты."""
    assert get_mask_card_number("1234abcd5678efgh") == "Проверьте правильность введенного номера карты!"
    assert get_mask_card_number("1234 5678 9012 3456") == "Проверьте правильность введенного номера карты!"


# Тесты для функции get_mask_account
def test_mask_account_valid() -> None:
    """Тест: Корректное маскирование номера счета."""
    assert get_mask_account("12345678901234567890") == "**7890"
    assert get_mask_account("00000000000000011234") == "**1234"


def test_mask_account_invalid_length() -> None:
    """Тест: Возврат ошибки при номере счета меньше 20 символов."""
    assert get_mask_account("12345678") == "Проверьте правильность введенного номера счета!"
    assert get_mask_account("123456789012345") == "Проверьте правильность введенного номера счета!"


def test_mask_account_non_digit() -> None:
    """Тест: Возврат ошибки при наличии символов в номере счета."""
    assert get_mask_account("12345678abcdefgh1234") == "Проверьте правильность введенного номера счета!"
    assert get_mask_account("accountnumber!") == "Проверьте правильность введенного номера счета!"
