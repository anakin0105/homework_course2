def filter_by_state(data: list[dict], state: str = 'EXECUTED') -> list[dict]:
    """
    Фильтрует список словарей, оставляя только элементы с указанным значением ключа "state".

    :param data: Список словарей.
    :param state: Значение ключа "state" для фильтрации (по умолчанию 'EXECUTED').
    :return: Список словарей, содержащих только те, у которых "state" соответствует `state`.
    """
    # Используем list comprehension для фильтрации
    return [item for item in data if item.get('state') == state]


def sort_by_date(data: list[dict], descending: bool = True) -> list[dict]:
    """
    Сортирует список словарей по ключу "date".

    :param data: Список словарей, содержащих ключ "date".
    :param descending: Порядок сортировки (по умолчанию убывающий, True).
    :return: Новый список, отсортированный по ключу "date".
    """
    # Используем sorted() с ключом сортировки по ключу "date"
    return sorted(data, key=lambda item: item['date'], reverse=descending)