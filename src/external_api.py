import os  # Импортирую модуль os для работы с файловой системой и переменными окружения

import requests  # Импортирую библиотеку requests для работы с HTTP-запросами (например, для API)
from dotenv import \
    load_dotenv  # Импортирую load_dotenv из библиотеки python - dotenv для загрузки переменных файла .env load_dotenv

load_dotenv()  # Загружаю переменные окружения из файла .env (например, мой API - ключ)
API_KEY = os.getenv("API_KEY")  # Получаю значение переменной APIKAY из .env и сохраняю в переменную API_KAY
if not API_KEY:
    raise ValueError("API_KEY не найден в .env")


def convert_to_rub(transaction: dict,) -> float:  # Определяю функцию covert, которая принимает аргумент transaction (словарь с данными транзакций)
    """Функция конвертации в рубли"""
    if not isinstance(transaction, dict):
        raise TypeError("Параметр 'transaction' должен быть словарем.")
    if "operationAmount" not in transaction or not isinstance(transaction["operationAmount"], dict):
        raise KeyError("Ключ 'operationAmount' или его структура отсутствует в transaction.")
    if "currency" not in transaction["operationAmount"] or "amount" not in transaction["operationAmount"]:
        raise KeyError("Ключи 'currency' и 'amount' должны присутствовать в 'operationAmount'.")
    currency = transaction["operationAmount"]["currency"]["code"]  # Извлекаю код валюты (например, "USD", "EUR", "RUB") из словаря transaction
    amount = float(transaction["operationAmount"]["amount"])  # Извлекаю сумму транзакций (например, "100.00") из словаря transaction
    try:
        amount = float(amount)
        if amount < 0:
            raise ValueError("Сумма транзакции 'amount' должна быть положительным числом.")
    except ValueError:
        raise ValueError("Сумма транзакции 'amount' должна быть числом.")
        # Проверка валюты
    valid_currencies = ["USD", "EUR", "RUB"]
    if currency not in valid_currencies:
        raise ValueError(f"Некорректный код валюты '{currency}'. Допустимые значения: {valid_currencies}")

    if currency == "RUB":  # Проверяю, является ли валюта рублями, если нет (например, "USD", "EUR"), нужно конвертировать
        return amount
    try:
        headers = {"apikey": API_KEY}
        respons = requests.get(
            f"https://api.apilayer.com/exchangerates_data/convert?to=RUB&from={currency}&amount={amount}",
            headers=headers,
            timeout=10
        )  # Делаю GET - запрос к API для конвертации суммы в RUB
        data = respons.json()  # Преобразую ответ API (в формат API (в формате JSON) в Рython-словарь
        respons.raise_for_status()
        data = respons.json()
        if "result" not in data:
            raise ValueError("Ответ API не содержит ключ 'result'.")
        return round(float(data["result"]), 2)
    except requests.exceptions.Timeout:
        raise TimeoutError("Превышено время ожидания ответа от API.")