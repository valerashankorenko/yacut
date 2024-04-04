import re


def validate_url(url):
    """Функция для валидации URL-адреса."""
    pattern = r'^[a-zA-Z0-9_]+$'
    if url == '' or re.match(pattern, url):
        return True
    return False