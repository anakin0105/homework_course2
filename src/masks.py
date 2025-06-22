import logging
import os
from typing import Union


log_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "logs")
log_file = os.path.join(log_dir, "masks.log")
masks_logger = logging.getLogger("masks_logger")
masks_logger.setLevel(logging.DEBUG)
file_handler = logging.FileHandler(log_file, mode="w", encoding="utf-8")
file_formatter = logging.Formatter("%(asctime)s %(filename)s %(levelname)s: %(message)s")
file_handler.setFormatter(file_formatter)
masks_logger.addHandler(file_handler)


# @log()
def get_mask_card_number(card_number: Union[str]) -> Union[str]:
    """Функция принимает на вход номер карты в виде числа и
    возвращает маску номера по правилу XXXX XX** **** XXXX"""
    masks_logger.info("Запущена функция get_mask_card_number! ")
    if card_number.isdigit() and len(card_number) == 16:
        masked_number = card_number[0:4] + " " + card_number[4:6] + "** **** " + card_number[-4:]
        masks_logger.info("Функция get_mask_card_number завершила работу! ")
        return masked_number
    else:
        masks_logger.warning("Входные данные не могут быть обработаны корректно!")
        masks_logger.info("Функция get_mask_card_number завершила работу! ")
        return "Проверьте правильность введенного номера карты!"


# @log()
def get_mask_account(account_number: Union[str]) -> Union[str]:
    masks_logger.info("Запущена функция get_mask_account!")
    try:
        if account_number.isdigit() and len(account_number) == 20:
            masked_number = "**" + account_number[-4:]
            masks_logger.info("Функция get_mask_account завершила работу! ")
            return masked_number
        else:
            masks_logger.warning("Входные данные не могут быть обработаны корректно!")
            masks_logger.info("Функция get_mask_account завершила работу! ")
            return "Проверьте правильность введенного номера счета!"
    except (TypeError, SyntaxError, AttributeError) as e:
        error_message = f"Функция get_mask_account завершила работу с ошибкой: {e}"
        masks_logger.error(error_message)  # Логируем ошибку
        print(error_message)  # Выводим ошибку через print
        return "Введены некорректные данные!"


#
# get_mask_card_number("123")
# get_mask_account("abc")
# print(get_mask_account("12751596837868705199"))
# print(get_mask_account("1596837868705199"))
# print(get_mask_account([]))
