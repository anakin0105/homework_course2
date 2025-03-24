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

    if name.lower().startswith("счет"):
        masked_number = get_mask_account(number)
    else:
        masked_number = get_mask_card_number(number)
    return f"{name} {masked_number}"


def get_date(date_time: str) -> str:
    """
    Преобразует дату и время в формат ДД.ММ.ГГГГ.

    :param date_time: строка в формате "YYYY-MM-DDTHH:MM:SS".
    :return: строка в формате "ДД.ММ.ГГГГ".
    """
    return f"{date_time[8:10]}.{date_time[5:7]}.{date_time[:4]}"
