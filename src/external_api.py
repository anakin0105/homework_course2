import os  # Импортирую модуль os для работы с файловой системой и переменными окружения
import requests  # Импортирую библиотеку requests для работы с HTTP-запросами (например, для API)
from dotenv import load_dotenv  # Импортирую load_dotenv из библиотеки python - dotenv для загрузки переменных файла .env load_dotenv

load_dotenv() #Загружаю переменные окружения из файла .env (например, мой API - ключ)
API_KEY = os.getenv("API_KEY") # Получаю значение переменной APIKAY из .env и сохраняю в переменную API_KAY
if not API_KEY:
    raise ValueError("API_KEY не найден в .env")

def convert_to_rub(transaction: dict) -> float: #Определяю функцию covert, которая принимает аргумент transaction (словарь с данными транзакций)
    """Функция конвертации в рубли"""
    currency = transaction["operationAmount"]["currency"]["code"] #Извлекаю код валюты (например, "USD", "EUR", "RUB") из словаря transaction
    amount = float(transaction["operationAmount"]["amount"]) #Извлекаю сумму транзакций (например, "100.00") из словаря transaction
    if currency == "RUB": #Проверяю, является ли валюта рублями, если нет (например, "USD", "EUR"), нужно конвертировать
        return amount
    else:
        headers = {"apikey": API_KEY}
        respons = requests.get(
            f"https://api.apilayer.com/exchangerates_data/convert?to=RUB&from={currency}&amount={amount}",
            headers = headers
        ) # Делаю GET - запрос к API для конвертации суммы в RUB
        data = respons.json() # Преобразую ответ API (в формат API (в формате JSON) в Рython-словарь
        return float(data["result"]) #Извлекаю результат конвертации из словаря (ключ "result") и возвращаю его как float


