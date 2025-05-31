import datetime
from functools import wraps
from typing import Any
from typing import Callable
from typing import Optional


def log(filename: Optional[str] = None) -> Callable:
    """
    Декоратор для логирования работы функций.

    :param filename: Имя файла, в который записываются логи. Если None, вывод идёт в консоль.
    :return: Декорированная функция pytest --cov=. --cov-report=html
    """

    def decorator(func: Callable) -> Callable:
        @wraps(func)
        def wrapper(*args: Any, **kwargs: Any) -> Any:
            try:
                # Регистрируем время вызова и аргументы
                start_time = datetime.datetime.now()
                log_message = (
                    f"{start_time} - Calling function '{func.__name__}' with args: {args}, kwargs: {kwargs}\n"
                )

                # Запускаем функцию и логируем успех
                result = func(*args, **kwargs)
                log_message += (
                    f"{start_time} - Function '{func.__name__}' executed successfully with result: {result}\n"
                )

                # Запись логов
                if filename:
                    with open(filename, "a") as file:
                        file.write(log_message)
                else:
                    print(log_message)

                return result
            except Exception as e:
                # Логируем ошибку
                log_message = (
                    f"{datetime.datetime.now()} - Function '{func.__name__}' failed with error: {str(e)}. "
                    f"Inputs: {args}, {kwargs}\n"
                )

                if filename:
                    with open(filename, "a") as file:
                        file.write(log_message)
                else:
                    print(log_message)

                raise

        return wrapper

    return decorator
