import random
import string


def get_unique_short_id(len=6):
    """Функция для формирования коротких идентификаторов переменной длинны."""
    return ''.join(random.choices(string.ascii_letters + string.digits, k=len))