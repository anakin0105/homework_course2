
def main() -> None:
    """Функция, позволяющая пользователю производить отбор банковских транзакций,
    соответствующих заданным им критериям"""

    print ("Привет! Добро пожаловать в программу работы с банковскими транзакциями.")
    user_name = input("Укажите как в вам обращаться:")


    file_format = input(
        f"""{user_name}, выберите необходимый пункт меню:
    1. Получить информацию о транзакциях из JSON-файла
    2. Получить информацию о транзакциях из CSV-файла
    3. Получить информацию о транзакциях из XLSX-файла
    Введите номер пункта, {user_name}:   """
    ).strip().replace(" ", "").replace(".", "")
    if file_format == "1":
        print("Для обработки выбран JSON-файл.")

    elif file_format == "2":
        print("Для обработки выбран CSV-файл.")

    elif file_format == "3":
        print("Для обработки выбран XLSX-файл.")

    else:
        print ("Введите номер пункта цифрой. Пример: => 1")

    input_state_of_operations = input(
    f"""{user_name}, введите статус, по которому необходимо выполнить фильтрацию.
    Доступные для фильтровки статусы:
    1 - EXECUTED,
    2 - CANCELED,
    3 - PENDING.
    Введите статус для фильтрации, {user_name}: """
    ).strip().replace(" ", "").replace(".", "").strip().upper()

    if input_state_of_operations == "1" or input_state_of_operations =="EXECUTED":
        print(f"{input_state_of_operations} статус а")

    elif input_state_of_operations == "2" or input_state_of_operations == "CANCELED":
        print(f"{input_state_of_operations} статус б")

    elif input_state_of_operations == "3" or input_state_of_operations == "PENDING":
        print(f"{input_state_of_operations} статус в")
    else:
        print(f'''Статус операции "{input_state_of_operations}" недоступен.
    Введите для фильтрации статусы: EXECUTED, CANCELED, PENDING''')

    sorted_by_date_check = input("""Отсортировать операции по дате?
    Введите да/нет:  """
    ).strip().replace(" ", "").replace(".", "").lower()
    print(sorted_by_date_check)

    flow_check = input("""Отсортировать по возрастанию или по убыванию?
    ведите по возрастанию/ по убыванию: """).strip().replace(".", "").lower()
    print(flow_check)

    currency_check = input("""Выводить только рублевые транзакции да/нет?
    Введите да/нет: """
    ).strip().replace(" ", "").replace(".", "").lower()
    print(currency_check)

    search_check = input("""Отфильтровать список транзакций по определенному слову в описании да/нет?
    Введите да/нет: """).strip().replace(" ", "").replace(".", "").lower()
    if search_check == "да":
        target = input("""Введите слово для поиска: """).strip().replace(" ", "").replace(".", "").lower()
    else:
        print("Спасибо")
    print("Распечатываю итоговый список транзакций...")
    print(f"Всего банковских операций в выборке: ")

if __name__ == "__main__":
    main()