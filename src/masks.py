from typing import Union


def get_mask_card_number(card_number: Union[str]) -> Union[str]:
    """Функция принимает на вход номер карты в виде числа и
    возвращает маску номера по правилу XXXX XX** **** XXXX"""
    if card_number.isdigit() and len(card_number) == 16:
        masked_number = card_number[0:4] + " " + card_number[4:6] + "** **** " + card_number[-4:]
        return masked_number
    else:
        return "Проверьте правильность введенного номера карты!"


def get_mask_account(account_number: Union[str]) -> Union[str]:
    if account_number.isdigit() and len(account_number) == 20:
        masked_number = "**" + account_number[-4:]
        return masked_number
    else:
        return "Проверьте правильность введенного номера счета!"
