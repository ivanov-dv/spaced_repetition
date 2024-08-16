def validate_nums_requests(message: str) -> list | bool:
    try:
        nums = set(map(int, message.strip().split(',')))
    except ValueError:
        return False
    return list(nums)


def list_requests_to_text(requests: list) -> str:
    text = 'Задачи:\n\n'
    for i, request in enumerate(requests, start=1):
        text += f'{i}.\n{request}\n'
    return text
