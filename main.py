from src.widget import mask_account_card, get_date
from src.processing import filter_by_state, sort_by_date

if __name__ == "__main__":
    print(mask_account_card("Maestro 1596837868705199"))
    print(mask_account_card("Счет 64686473678894779589"))
    print(mask_account_card("MasterCard 7158300734726758"))
    print(mask_account_card("Счет 35383033474447895560"))
    print(mask_account_card("Visa Classic 6831982476737658"))
    print(mask_account_card("Visa Platinum 8990922113665229"))
    print(mask_account_card("Visa Gold 5999414228426353"))
    print(mask_account_card("Счет 7p3654108430135874305"))
    # Вызов get_date.
    print(get_date("2024-03-11T02:26:18.671407"))
    print(get_date("2025-12-31T23:59:59.000000"))

    # Исходные данные.
    data = [
        {"id": 41428829, "state": "EXECUTED", "date": "2019-07-03T18:35:29.512364"},
        {"id": 939719570, "state": "EXECUTED", "date": "2018-06-30T02:08:58.425572"},
        {"id": 594226727, "state": "CANCELED", "date": "2018-09-12T21:27:25.241689"},
        {"id": 615064591, "state": "CANCELED", "date": "2018-10-14T08:21:33.419441"},
    ]

    # Вызов filter_by_state для EXECUTED.
    print(filter_by_state(data, "EXECUTED"))

    # Вызов filter_by_state для CANCELED.
    print(filter_by_state(data, "CANCELED"))

    # Вызов sort_by_date на отфильтрованных данных (EXECUTED) в порядке убывания.
    print(sort_by_date(filter_by_state(data, "EXECUTED"), True))

    # Вызов sort_by_date на отфильтрованных данных (CANCELED) по возрастанию.
    print(sort_by_date(filter_by_state(data, "CANCELED"), False))
