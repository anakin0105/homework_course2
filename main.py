from six import print_

from src.generators import filter_by_currency, filter_by_currency_csv_excel
from src.processing import filter_by_state, sort_by_date
from src.search import process_bank_search
from src.utils import read_transactions_json
from src.utils_cvs_excel import get_read_csv, get_read_excel
from src.widget import get_date, mask_account_card
from tests.test_generator import transactions_data


def main() -> None:
    """Функция, позволяющая пользователю производить отбор банковских транзакций,
    соответствующих заданным им критериям"""

    print ("Привет! Добро пожаловать в программу работы с банковскими транзакциями.")
    user_name = input("Укажите как в вам обращаться:")
    flag_json = False
    while True:
        file_format = input(
            f"""{user_name}, выберите необходимый пункт меню:
        1. Получить информацию о транзакциях из JSON-файла
        2. Получить информацию о транзакциях из CSV-файла
        3. Получить информацию о транзакциях из XLSX-файла
        Введите номер пункта, {user_name}:   """
        ).replace(" ", "").replace(".", "")
        if file_format == "1":
            print("Для обработки выбран JSON-файл.")
            transactions = read_transactions_json("data/operations.json")
            flag_json = True
            break
        elif file_format == "2":
            print("Для обработки выбран CSV-файл.")
            transactions = get_read_csv("data/transactions.csv")
            break
        elif file_format == "3":
            print("Для обработки выбран XLSX-файл.")
            transactions = get_read_excel("data/transactions_excel.xlsx")
            break
        else:
            print ("Введите номер пункта цифрой. Пример: => 1")
    while True:
        input_state_of_operations = input(
        f"""{user_name}, введите статус, по которому необходимо выполнить фильтрацию.
        Доступные для фильтровки статусы:
        1 - EXECUTED,
        2 - CANCELED,
        3 - PENDING.
        Введите статус для фильтрации, {user_name}: """
        ).replace(" ", "").replace(".", "").upper()

        if input_state_of_operations == "1" or input_state_of_operations =="EXECUTED":
            input_state_of_operations = "EXECUTED"
            print(f"Операция отфильтрована по статусу {input_state_of_operations}")
            state_of_operations = filter_by_state(transactions, input_state_of_operations)
            break

        elif input_state_of_operations == "2" or input_state_of_operations == "CANCELED":
            input_state_of_operations = "CANCELED"
            print(f"Операция отфильтрована по статусу {input_state_of_operations}")
            state_of_operations = filter_by_state(transactions, input_state_of_operations)
            break
        elif input_state_of_operations == "3" or input_state_of_operations == "PENDING":
            input_state_of_operations = "PENDING"
            print(f"Операция отфильтрована по статусу {input_state_of_operations}")
            state_of_operations = filter_by_state(transactions, input_state_of_operations)
            break
        else:
            print(f'''Статус операции "{input_state_of_operations}" недоступен.
        Введите для фильтрации статусы: EXECUTED, CANCELED, PENDING''')

    while True:
        sorted_by_date_check = input("""Отсортировать операции по дате?
                Введите да/нет:  """
                                     ).strip().replace(" ", "").replace(".", "").lower()
        if sorted_by_date_check == "да":
            while True:
                flow_check = input("""Отсортировать по возрастанию или по убыванию?
                           ведите по возрастанию/ по убыванию: """).strip().replace(".", "").lower()
                if flow_check == "по возрастанию":
                    sorted_transaction = sort_by_date(state_of_operations, False)
                    break
                elif flow_check == "по убыванию":
                    sorted_transaction = sort_by_date(state_of_operations)
                    break
                else:
                    print(f"Введите по возрастанию или по убыванию.")
            break
        elif sorted_by_date_check == "нет":
            sorted_transaction = state_of_operations
            break
        else:
            print(f"Введите да или нет.")
    while True:
        currency_check = input("""Выводить только рублевые транзакции да/нет?
        Введите да/нет: """
        ).strip().replace(" ", "").replace(".", "").lower()
        if currency_check == "да":
            if flag_json:
                currency_search = list(filter_by_currency(sorted_transaction,"RUB"))
                break
            else:
                currency_search = list(filter_by_currency_csv_excel(sorted_transaction,"RUB"))
                break
        elif currency_check == "нет":
            currency_search = sorted_transaction
            break
        else:
            print(f"Введите да или нет.")
    while True:
        search_check = input("""Отфильтровать список транзакций по определенному слову в описании да/нет?
        Введите да/нет: """).strip().replace(" ", "").replace(".", "").lower()
        if search_check == "да":
            target = input("""Введите слово для поиска: """)
            search_word = process_bank_search(currency_search, target)
            break
        elif search_check == "нет":
            search_word = currency_search
            break
        else:
            print("Введите да или нет")

    print("Распечатываю итоговый список транзакций...")
    if not search_word:
        print(f"Не найдено ни одной операции подходящие под ваши условия.")
    else:
        print(f"Всего банковских операций в выборке: {len(search_word)}")
        for transaction in search_word:
            print(f"{get_date(transaction.get("date"))}. {transaction.get('description')}")
            if "from" in transaction:
                print(
                    f"""откуда: {mask_account_card(transaction.get("from"))} -> куда: {mask_account_card(transaction.get("to"))}"""
                )
            else:
                print(f"""{mask_account_card(transaction.get("to"))}""")
            if flag_json:
                print(f"""Сумма: {transaction.get('operationAmount',{}).get('amount', '')} 
Валюта: {transaction.get('operationAmount',{}).get('currency',{}).get('code', '')} \n""")
            else:
                print(f"""Сумма: {transaction.get('amount', '')}  "
                        Валюта: {transaction.get('currency_name', '')}""")

if __name__ == "__main__":
    main()