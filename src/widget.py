from typing import Union

from src.masks import get_mask_account, get_mask_card_number


def mask_account_card(data: str) -> Union[str]:
    """
    Маскирует номер карты или счета.
    """
    parts = data.split()
    if len(parts) < 2:
        return "Некорректный формат данных!"

    name = " ".join(parts[:-1])
    number = parts[-1]

    if len(number) == 20:
        masked_number = get_mask_account(number)
    else:
        masked_number = get_mask_card_number(number)
    return f"{name} {masked_number}"


def get_date(date_time: str) -> str:
    """
    Преобразует дату и время в формат ДД.ММ.ГГГГ.

    :param date_time: строка в формате "YYYY-MM-DDTHH:MM:SS".
    :return: строка в формате "ДД.ММ.ГГГГ" или сообщение об ошибке.
    """
    # Проверяем длину строки и наличие необходимых разделителей
    if not isinstance(date_time, str) or len(date_time) < 10:
        return "Дата указана неверно!"
    if len(date_time) >= 10 and (date_time[4] != "-" or date_time[7] != "-"):
        return "Дата указана неверно!"
    if "T" not in date_time:
        return "Дата указана неверно!"

    try:
        # Если удалось успешно извлечь части даты, возвращаем результат
        return f"{date_time[8:10]}.{date_time[5:7]}.{date_time[:4]}"
    except Exception:
        # Любое исключение интерпретируем как некорректный формат
        return "Дата указана неверно!"