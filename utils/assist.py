def validate_nums_requests(message: str) -> list | bool:
    try:
        nums = set(map(int, message.strip().split(',')))
    except ValueError:
        return False
    return list(nums)


def validate_my_ratio(message: str) -> float | bool:
    message = message.replace(',', '.')
    try:
        ratio = float(message.strip())
    except ValueError:
        return False
    if ratio > 5 or ratio < 1:
        return False
    return ratio


def validate_text(message: str):
    message = message.strip()
    if len(message) > 150:
        return False
    return message


def validate_count_day(message: str):
    message = message.replace(',', '.')
    try:
        count_day = int(float(message.strip()))
    except ValueError:
        return False
    if count_day < 1 or count_day > 1000:
        return False
    return count_day


def list_requests_to_text(requests: list) -> str:
    text = 'Задачи:\n\n'
    for i, request in enumerate(requests, start=1):
        text += f'{i}.\n{request}\n'
    return text
