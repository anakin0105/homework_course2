import datetime
from typing import Any, Optional


def log(filename: Optional[str] = None) -> Any:
    """Декоратор, который автоматически регистрирует детали
    выполнения функций, такие как: время вызова, имя функции,
    передаваемые аргументы, результат выполнения и информацию об ошибках"""

    def decorator_1(func: Any) -> Any:
        def wrapper(*args: Any, **kwargs: Any) -> Any:
            # Формируем информацию о запуске функции
            mark = ""
            start_time = datetime.datetime.now()
            log_entry = [
                f"{func.__name__} started with arguments: {args}, {kwargs}",
            ]

            try:
                # Вызываем функцию и получаем результат
                result = func(*args, **kwargs)

                if result:
                    mark = "OK"

                # Формируем информацию об успешном выполнении
                end_time = datetime.datetime.now()
                log_entry.extend(
                    [
                        f"Execution time: {end_time - start_time}",
                        f"{func.__name__} ended -> {mark}",
                        f"Results: {result}",
                    ]
                )

                # Объединяем все строки лога
                full_log = "\n".join(log_entry) + "\n"

                # Записываем лог в файл или выводим в консоль
                if filename:
                    with open(filename, "a") as file:
                        file.write(full_log)
                else:
                    print(full_log)

                return result

            except Exception as e:
                # Формируем информацию об ошибке
                error_time = datetime.datetime.now()
                log_entry.extend(
                    [
                        f"{func.__name__} raised an error",
                        f"Error type: {type(e).__name__}",
                        f"Error message: {str(e)}",
                        f"Execution time before error: {error_time - start_time}",
                    ]
                )

                # Объединяем все строки лога
                full_log = "\n".join(log_entry) + "\n"

                # Записываем лог в файл или выводим в консоль
                if filename:
                    with open(filename, "a") as file:
                        file.write(full_log)
                else:
                    print(full_log)

        return wrapper

    return decorator_1
